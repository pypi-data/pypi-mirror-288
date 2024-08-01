#!/usr/bin/env python
from __future__ import annotations

import logging

# import contextlib
import multiprocessing as mp
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Mapping, NamedTuple, Sequence

from opera_utils import group_by_burst, group_by_date  # , get_dates
from tqdm.auto import tqdm

from dolphin import __version__, io, timeseries, utils
from dolphin._log import log_runtime, setup_logging
from dolphin.atmosphere import estimate_ionospheric_delay, estimate_tropospheric_delay
from dolphin.workflows import CallFunc

from . import stitching_bursts, unwrapping, wrapped_phase
from ._utils import _create_burst_cfg, _remove_dir_if_empty
from .config import DisplacementWorkflow  # , TimeseriesOptions

logger = logging.getLogger(__name__)


class OutputPaths(NamedTuple):
    """Named tuple of `DisplacementWorkflow` outputs."""

    comp_slc_dict: dict[str, list[Path]]
    stitched_ifg_paths: list[Path]
    stitched_cor_paths: list[Path]
    stitched_temp_coh_file: Path
    stitched_ps_file: Path
    stitched_amp_dispersion_file: Path
    stitched_shp_count_file: Path
    unwrapped_paths: list[Path] | None
    conncomp_paths: list[Path] | None
    timeseries_paths: list[Path] | None
    tropospheric_corrections: list[Path] | None
    ionospheric_corrections: list[Path] | None


@log_runtime
def run(
    cfg: DisplacementWorkflow,
    debug: bool = False,
) -> OutputPaths:
    """Run the displacement workflow on a stack of SLCs.

    Parameters
    ----------
    cfg : DisplacementWorkflow
        [`DisplacementWorkflow`][dolphin.workflows.config.DisplacementWorkflow] object
        for controlling the workflow.
    debug : bool, optional
        Enable debug logging, by default False.

    """
    if cfg.log_file is None:
        cfg.log_file = cfg.work_directory / "dolphin.log"
    # Set the logging level for all `dolphin.` modules
    setup_logging(debug=debug, filename=cfg.log_file)
    # TODO: need to pass the cfg filename for the logger
    logger.debug(cfg.model_dump())

    if not cfg.worker_settings.gpu_enabled:
        utils.disable_gpu()
    utils.set_num_threads(cfg.worker_settings.threads_per_worker)

    try:
        grouped_slc_files = group_by_burst(cfg.cslc_file_list)
    except ValueError as e:
        # Make sure it's not some other ValueError
        if "Could not parse burst id" not in str(e):
            raise
        # Otherwise, we have SLC files which are not OPERA burst files
        grouped_slc_files = {"": cfg.cslc_file_list}

    if cfg.amplitude_dispersion_files:
        grouped_amp_dispersion_files = group_by_burst(cfg.amplitude_dispersion_files)
    else:
        grouped_amp_dispersion_files = defaultdict(list)
    if cfg.amplitude_mean_files:
        grouped_amp_mean_files = group_by_burst(cfg.amplitude_mean_files)
    else:
        grouped_amp_mean_files = defaultdict(list)

    grouped_iono_files: Mapping[tuple[datetime], Sequence[str | PathLike[str]]] = {}
    if len(cfg.correction_options.ionosphere_files) > 0:
        for fmt in cfg.correction_options._iono_date_fmt:
            group_iono = group_by_date(
                cfg.correction_options.ionosphere_files,
                file_date_fmt=fmt,
            )
            if len(next(iter(group_iono))) == 0:
                continue
            grouped_iono_files = {**grouped_iono_files, **group_iono}

    # ######################################
    # 1. Burst-wise Wrapped phase estimation
    # ######################################
    if len(grouped_slc_files) > 1:
        logger.info(f"Found SLC files from {len(grouped_slc_files)} bursts")
        wrapped_phase_cfgs = [
            (
                burst,  # Include the burst for logging purposes
                _create_burst_cfg(
                    cfg,
                    burst,
                    grouped_slc_files,
                    grouped_amp_mean_files,
                    grouped_amp_dispersion_files,
                ),
            )
            for burst in grouped_slc_files
        ]
        for _, burst_cfg in wrapped_phase_cfgs:
            burst_cfg.create_dir_tree()
        # Remove the mid-level directories which will be empty due to re-grouping
        _remove_dir_if_empty(cfg.phase_linking._directory)
        _remove_dir_if_empty(cfg.ps_options._directory)

    else:
        # grab the only key (either a burst, or "") and use that
        cfg.create_dir_tree()
        b = next(iter(grouped_slc_files.keys()))
        wrapped_phase_cfgs = [(b, cfg)]

    ifg_file_list: list[Path] = []
    temp_coh_file_list: list[Path] = []
    ps_file_list: list[Path] = []
    amp_dispersion_file_list: list[Path] = []
    shp_count_file_list: list[Path] = []
    # The comp_slc tracking object is a dict, since we'll need to organize
    # multiple comp slcs by burst (they'll have the same filename)
    comp_slc_dict: dict[str, list[Path]] = {}
    # Now for each burst, run the wrapped phase estimation
    # Try running several bursts in parallel...
    Executor = (
        ProcessPoolExecutor
        if cfg.worker_settings.n_parallel_bursts > 1
        else utils.DummyProcessPoolExecutor
    )
    mw = cfg.worker_settings.n_parallel_bursts
    ctx = mp.get_context("spawn")
    tqdm.set_lock(ctx.RLock())
    with Executor(
        max_workers=mw,
        mp_context=ctx,
        initializer=tqdm.set_lock,
        initargs=(tqdm.get_lock(),),
    ) as exc:
        fut_to_burst = {
            exc.submit(
                wrapped_phase.run,
                burst_cfg,
                debug=debug,
                tqdm_kwargs={
                    "position": i,
                },
            ): burst
            for i, (burst, burst_cfg) in enumerate(wrapped_phase_cfgs)
        }
        for fut in fut_to_burst:
            burst = fut_to_burst[fut]

            cur_ifg_list, comp_slcs, temp_coh, ps_file, amp_disp_file, shp_count = (
                fut.result()
            )
            ifg_file_list.extend(cur_ifg_list)
            comp_slc_dict[burst] = comp_slcs
            temp_coh_file_list.append(temp_coh)
            ps_file_list.append(ps_file)
            amp_dispersion_file_list.append(amp_disp_file)
            shp_count_file_list.append(shp_count)

    # ###################################
    # 2. Stitch burst-wise interferograms
    # ###################################

    # TODO: figure out how best to pick the corr size
    # Is there one best size? dependent on `half_window` or resolution?
    # For now, just pick a reasonable size
    corr_window_size = (11, 11)
    (
        stitched_ifg_paths,
        stitched_cor_paths,
        stitched_temp_coh_file,
        stitched_ps_file,
        stitched_amp_dispersion_file,
        stitched_shp_count_file,
    ) = stitching_bursts.run(
        ifg_file_list=ifg_file_list,
        temp_coh_file_list=temp_coh_file_list,
        ps_file_list=ps_file_list,
        amp_dispersion_list=amp_dispersion_file_list,
        shp_count_file_list=shp_count_file_list,
        stitched_ifg_dir=cfg.interferogram_network._directory,
        output_options=cfg.output_options,
        file_date_fmt=cfg.input_options.cslc_date_fmt,
        corr_window_size=corr_window_size,
    )

    # ###################################
    # 3. Unwrap stitched interferograms
    # ###################################
    if not cfg.unwrap_options.run_unwrap:
        logger.info("Skipping unwrap step")
        _print_summary(cfg)
        return OutputPaths(
            comp_slc_dict=comp_slc_dict,
            stitched_ifg_paths=stitched_ifg_paths,
            stitched_cor_paths=stitched_cor_paths,
            stitched_temp_coh_file=stitched_temp_coh_file,
            stitched_ps_file=stitched_ps_file,
            stitched_amp_dispersion_file=stitched_amp_dispersion_file,
            stitched_shp_count_file=stitched_shp_count_file,
            unwrapped_paths=None,
            conncomp_paths=None,
            timeseries_paths=None,
            tropospheric_corrections=None,
            ionospheric_corrections=None,
        )

    row_looks, col_looks = cfg.phase_linking.half_window.to_looks()
    nlooks = row_looks * col_looks
    unwrapped_paths, conncomp_paths = unwrapping.run(
        ifg_file_list=stitched_ifg_paths,
        cor_file_list=stitched_cor_paths,
        temporal_coherence_file=stitched_temp_coh_file,
        nlooks=nlooks,
        unwrap_options=cfg.unwrap_options,
        mask_file=cfg.mask_file,
    )

    # ##############################################
    # 4. If a network was unwrapped, invert it
    # ##############################################

    ts_opts = cfg.timeseries_options
    # Skip if we only have 1 unwrapped, or if we didn't ask for inversion/velocity
    if len(unwrapped_paths) > 1 and (ts_opts.run_inversion or ts_opts.run_velocity):
        # the output of run_timeseries is not currently used so pre-commit removes it
        # let's add back if we need it
        timeseries_paths = timeseries.run(
            unwrapped_paths=unwrapped_paths,
            conncomp_paths=conncomp_paths,
            corr_paths=stitched_cor_paths,
            condition_file=stitched_temp_coh_file,
            condition=CallFunc.MAX,
            output_dir=ts_opts._directory,
            run_velocity=ts_opts.run_velocity,
            velocity_file=ts_opts._velocity_file,
            correlation_threshold=ts_opts.correlation_threshold,
            # TODO: do i care to configure block shape, or num threads from somewhere?
            # num_threads=cfg.worker_settings....?
        )

    else:
        timeseries_paths = None

    # ##############################################
    # 5. Estimate corrections for each interferogram
    # ##############################################
    tropo_paths: list[Path] | None = None
    iono_paths: list[Path] | None = None
    if len(cfg.correction_options.geometry_files) > 0:
        stitched_ifg_dir = cfg.interferogram_network._directory
        ifg_filenames = sorted(Path(stitched_ifg_dir).glob("*.int.tif"))
        out_dir = cfg.work_directory / cfg.correction_options._atm_directory
        out_dir.mkdir(exist_ok=True)
        grouped_slc_files = group_by_date(cfg.cslc_file_list)

        # Prepare frame geometry files
        geometry_dir = out_dir / "geometry"
        geometry_dir.mkdir(exist_ok=True)
        crs = io.get_raster_crs(ifg_filenames[0])
        epsg = crs.to_epsg()
        out_bounds = io.get_raster_bounds(ifg_filenames[0])
        frame_geometry_files = utils.prepare_geometry(
            geometry_dir=geometry_dir,
            geo_files=cfg.correction_options.geometry_files,
            matching_file=ifg_filenames[0],
            dem_file=cfg.correction_options.dem_file,
            epsg=epsg,
            out_bounds=out_bounds,
            strides=cfg.output_options.strides,
        )

        # Troposphere
        if "height" not in frame_geometry_files:
            logger.warning(
                "DEM file is not given, skip estimating tropospheric corrections..."
            )
        else:
            if cfg.correction_options.troposphere_files is not None:
                tropo_paths = estimate_tropospheric_delay(
                    ifg_file_list=ifg_filenames,
                    troposphere_files=cfg.correction_options.troposphere_files,
                    file_date_fmt=cfg.correction_options.tropo_date_fmt,
                    slc_files=grouped_slc_files,
                    geom_files=frame_geometry_files,
                    output_dir=out_dir,
                    tropo_model=cfg.correction_options.tropo_model,
                    tropo_delay_type=cfg.correction_options.tropo_delay_type,
                    epsg=epsg,
                    bounds=out_bounds,
                )
            else:
                logger.info("No weather model, skip tropospheric correction ...")

        # Ionosphere
        if grouped_iono_files:
            iono_paths = estimate_ionospheric_delay(
                ifg_file_list=ifg_filenames,
                slc_files=grouped_slc_files,
                tec_files=grouped_iono_files,
                geom_files=frame_geometry_files,
                output_dir=out_dir,
                epsg=epsg,
                bounds=out_bounds,
            )
        else:
            logger.info("No TEC files, skip ionospheric correction ...")

    # Print the maximum memory usage for each worker
    _print_summary(cfg)
    return OutputPaths(
        comp_slc_dict=comp_slc_dict,
        stitched_ifg_paths=stitched_ifg_paths,
        stitched_cor_paths=stitched_cor_paths,
        stitched_temp_coh_file=stitched_temp_coh_file,
        stitched_ps_file=stitched_ps_file,
        stitched_amp_dispersion_file=stitched_amp_dispersion_file,
        stitched_shp_count_file=stitched_shp_count_file,
        unwrapped_paths=unwrapped_paths,
        # TODO: Let's keep the unwrapped_paths since all the outputs are
        # corresponding to those and if we have a network unwrapping, the
        # inversion would create different single-reference network and we need
        # to update other products like conncomp
        # unwrapped_paths=inverted_phase_paths,
        conncomp_paths=conncomp_paths,
        timeseries_paths=timeseries_paths,
        tropospheric_corrections=tropo_paths,
        ionospheric_corrections=iono_paths,
    )


def _print_summary(cfg):
    """Print the maximum memory usage and version info."""
    max_mem = utils.get_max_memory_usage(units="GB")
    logger.info(f"Maximum memory usage: {max_mem:.2f} GB")
    logger.info(f"Config file dolphin version: {cfg._dolphin_version}")
    logger.info(f"Current running dolphin version: {__version__}")
