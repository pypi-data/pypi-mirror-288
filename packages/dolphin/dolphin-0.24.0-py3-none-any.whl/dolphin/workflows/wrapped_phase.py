from __future__ import annotations

import datetime
import logging
import time
from pathlib import Path
from typing import Optional, Sequence, cast

import numpy as np
from opera_utils import get_dates, make_nodata_mask

from dolphin import interferogram, ps, stack
from dolphin._log import log_runtime, setup_logging
from dolphin.io import VRTStack

from . import InterferogramNetwork, sequential
from .config import DisplacementWorkflow

logger = logging.getLogger(__name__)


@log_runtime
def run(
    cfg: DisplacementWorkflow, debug: bool = False, tqdm_kwargs=None
) -> tuple[list[Path], list[Path], Path, Path, Path, Path]:
    """Run the displacement workflow on a stack of SLCs.

    Parameters
    ----------
    cfg : DisplacementWorkflow
        [`DisplacementWorkflow`][dolphin.workflows.config.DisplacementWorkflow] object
        for controlling the workflow.
    debug : bool, optional
        Enable debug logging, by default False.
    tqdm_kwargs : dict, optional
        dict of arguments to pass to `tqdm` (e.g. `position=n` for n parallel bars)
        See https://tqdm.github.io/docs/tqdm/#tqdm-objects for all options.

    Returns
    -------
    ifg_file_list : list[Path]
        list of Paths to virtual interferograms created.
    comp_slc_file_list : list[Path]
        Paths to the compressed SLC files created from each ministack.
    temp_coh_file : Path
        Path to temporal coherence file created.
        In the case of a single phase linking step, this is from one phase linking step.
        In the case of sequential phase linking, this is the average of all ministacks.
    ps_looked_file : Path
        The multilooked boolean persistent scatterer file.
    amp_disp_looked_file : Path
        The multilooked amplitude dispersion file.
    shp_count_file : Path
        Path to the created SHP counts file.

    """
    t0 = time.perf_counter()
    setup_logging(debug=debug, filename=cfg.log_file)
    if tqdm_kwargs is None:
        tqdm_kwargs = {}
    work_dir = cfg.work_directory
    logger.info("Running wrapped phase estimation in %s", work_dir)

    input_file_list = cfg.cslc_file_list

    # #############################################
    # Make a VRT pointing to the input SLC files
    # #############################################
    subdataset = cfg.input_options.subdataset
    vrt_stack = VRTStack(
        input_file_list,
        subdataset=subdataset,
        outfile=cfg.work_directory / "slc_stack.vrt",
    )

    # ###############
    # PS selection
    # ###############
    ps_output = cfg.ps_options._output_file
    ps_output.parent.mkdir(parents=True, exist_ok=True)
    if ps_output.exists():
        logger.info(f"Skipping making existing PS file {ps_output}")
    else:
        logger.info(f"Creating persistent scatterer file {ps_output}")
        try:
            existing_amp: Optional[Path] = cfg.amplitude_mean_files[0]
            existing_disp: Optional[Path] = cfg.amplitude_dispersion_files[0]
        except IndexError:
            existing_amp = existing_disp = None

        kwargs = tqdm_kwargs | {"desc": f"PS ({ps_output.parent})"}
        ps.create_ps(
            reader=vrt_stack,
            like_filename=vrt_stack.outfile,
            output_file=ps_output,
            output_amp_mean_file=cfg.ps_options._amp_mean_file,
            output_amp_dispersion_file=cfg.ps_options._amp_dispersion_file,
            amp_dispersion_threshold=cfg.ps_options.amp_dispersion_threshold,
            existing_amp_dispersion_file=existing_disp,
            existing_amp_mean_file=existing_amp,
            block_shape=cfg.worker_settings.block_shape,
            **kwargs,
        )

    # Save a looked version of the PS mask too
    strides = cfg.output_options.strides
    ps_looked_file, amp_disp_looked_file = ps.multilook_ps_files(
        strides=strides,
        ps_mask_file=cfg.ps_options._output_file,
        amp_dispersion_file=cfg.ps_options._amp_dispersion_file,
    )

    # #########################
    # phase linking/EVD step
    # #########################
    pl_path = cfg.phase_linking._directory
    pl_path.mkdir(parents=True, exist_ok=True)

    # Mark any files beginning with "compressed" as compressed
    is_compressed = ["compressed" in str(f).lower() for f in input_file_list]
    input_dates = _get_input_dates(
        input_file_list, is_compressed, cfg.input_options.cslc_date_fmt
    )
    reference_date, reference_idx = _get_reference_date_idx(
        input_file_list, is_compressed, input_dates
    )

    ministack_planner = stack.MiniStackPlanner(
        file_list=input_file_list,
        dates=input_dates,
        is_compressed=is_compressed,
        output_folder=pl_path,
        max_num_compressed=cfg.phase_linking.max_num_compressed,
        reference_date=reference_date,
        reference_idx=reference_idx,
    )

    # Make the nodata mask from the polygons, if we're using OPERA CSLCs
    non_compressed_slcs = [
        f for f, is_comp in zip(input_file_list, is_compressed) if not is_comp
    ]
    try:
        nodata_mask_file = cfg.work_directory / "nodata_mask.tif"
        make_nodata_mask(
            non_compressed_slcs, out_file=nodata_mask_file, buffer_pixels=200
        )
    except Exception as e:
        logger.warning(f"Could not make nodata mask: {e}")
        nodata_mask_file = None

    phase_linked_slcs = sorted(pl_path.glob("2*.tif"))
    if len(phase_linked_slcs) > 0:
        logger.info(f"Skipping EVD step, {len(phase_linked_slcs)} files already exist")
        comp_slc_list = sorted(pl_path.glob("compressed*tif"))
        temp_coh_file = next(pl_path.glob("temporal_coherence*tif"))
        shp_count_file = next(pl_path.glob("shp_count*tif"))
    else:
        logger.info(f"Running sequential EMI step in {pl_path}")
        kwargs = tqdm_kwargs | {"desc": f"Phase linking ({pl_path})"}

        # TODO: Need a good way to store the nslc attribute in the PS file...
        # If we pre-compute it from some big stack, we need to use that for SHP
        # finding, not use the size of `slc_vrt_file`
        shp_nslc = None
        (phase_linked_slcs, comp_slc_list, temp_coh_file, shp_count_file) = (
            sequential.run_wrapped_phase_sequential(
                slc_vrt_file=vrt_stack.outfile,
                ministack_planner=ministack_planner,
                ministack_size=cfg.phase_linking.ministack_size,
                half_window=cfg.phase_linking.half_window.model_dump(),
                strides=strides,
                use_evd=cfg.phase_linking.use_evd,
                beta=cfg.phase_linking.beta,
                mask_file=nodata_mask_file,
                ps_mask_file=ps_output,
                amp_mean_file=cfg.ps_options._amp_mean_file,
                amp_dispersion_file=cfg.ps_options._amp_dispersion_file,
                shp_method=cfg.phase_linking.shp_method,
                shp_alpha=cfg.phase_linking.shp_alpha,
                shp_nslc=shp_nslc,
                block_shape=cfg.worker_settings.block_shape,
                baseline_lag=cfg.phase_linking.baseline_lag,
                **kwargs,
            )
        )
    # Dump the used options for JSON parsing
    logger.info(
        "wrapped_phase complete",
        extra={
            "elapsed": time.perf_counter() - t0,
            "phase_linking_options": cfg.phase_linking.model_dump(mode="json"),
        },
    )

    # ###################################################
    # Form interferograms from estimated wrapped phase
    # ###################################################

    ifg_network = cfg.interferogram_network
    existing_ifgs = list(ifg_network._directory.glob("*.int.vrt"))
    if len(existing_ifgs) > 0:
        logger.info(f"Skipping interferogram step, {len(existing_ifgs)} exists")
        return (
            existing_ifgs,
            comp_slc_list,
            temp_coh_file,
            ps_looked_file,
            amp_disp_looked_file,
            shp_count_file,
        )

    logger.info(f"Creating virtual interferograms from {len(phase_linked_slcs)} files")
    ifg_file_list = create_ifgs(
        ifg_network, phase_linked_slcs, any(is_compressed), reference_date
    )
    return (
        ifg_file_list,
        comp_slc_list,
        temp_coh_file,
        ps_looked_file,
        amp_disp_looked_file,
        shp_count_file,
    )


def create_ifgs(
    interferogram_network: InterferogramNetwork,
    phase_linked_slcs: Sequence[Path],
    contained_compressed_slcs: bool,
    reference_date: datetime.datetime,
    dry_run: bool = False,
) -> list[Path]:
    """Create the list of interferograms for the `phase_linked_slcs`.

    Parameters
    ----------
    interferogram_network : InterferogramNetwork
        Parameters to determine which ifgs to form.
    phase_linked_slcs : Sequence[Path]
        Paths to phase linked SLCs.
    contained_compressed_slcs : bool
        Flag indicating that the inputs to phase linking contained compressed SLCs.
        Needed because the network must be handled differently if we started with
        compressed SLCs.
    reference_date : datetime.datetime
        Date/datetime of the "base phase" for the `phase_linked_slcs`
    dry_run : bool
        Flag indicating that the ifgs should not be written to disk.
        Default = False (ifgs will be created).

    Returns
    -------
    list[Path]
        List of output VRTInterferograms

    Raises
    ------
    ValueError
        If invalid parameters are passed which lead to 0 interferograms being formed
    NotImplementedError
        Currently raised for max-temporal-baseline networks when
        `contained_compressed_slcs` is True

    """
    ifg_dir = interferogram_network._directory
    if not dry_run:
        ifg_dir.mkdir(parents=True, exist_ok=True)
    ifg_file_list: list[Path] = []
    if not contained_compressed_slcs:
        # When no compressed SLCs were passed in to the config, we can directly pass
        # options to `Network` and get the ifg list
        network = interferogram.Network(
            slc_list=phase_linked_slcs,
            reference_idx=interferogram_network.reference_idx,
            max_bandwidth=interferogram_network.max_bandwidth,
            max_temporal_baseline=interferogram_network.max_temporal_baseline,
            indexes=interferogram_network.indexes,
            outdir=ifg_dir,
            write=not dry_run,
            verify_slcs=not dry_run,
        )
        if len(network.ifg_list) == 0:
            msg = "No interferograms were created"
            raise ValueError(msg)
        ifg_file_list = [ifg.path for ifg in network.ifg_list]  # type: ignore[misc]
        assert all(p is not None for p in ifg_file_list)

        return ifg_file_list

    # When we started with compressed SLCs, we need to do some extra work to get the
    # interferograms we want.
    # The total SLC phases we have to work with are
    # 1. reference date (might be before any dates in the filenames)
    # 2. the secondary of all phase-linked SLCs (which are the names of the files)

    # To get the ifgs from the reference date to secondary(conj), this involves doing
    # a `.conj()` on the phase-linked SLCs (which are currently `day1.conj() * day2`)
    single_ref_ifgs = [
        interferogram.convert_pl_to_ifg(
            f, reference_date=reference_date, output_dir=ifg_dir, dry_run=dry_run
        )
        for f in phase_linked_slcs
    ]

    # If we're only wanting single-reference day-(reference) to day-k interferograms,
    # these are all we need
    # XX Fix this hack for later
    if interferogram_network.indexes and interferogram_network.indexes == [(0, -1)]:
        ifg_file_list.append(single_ref_ifgs[-1])
        # # This isn't really what we want here, the logic is different than Network:
        # ifgs = [
        #     (single_ref_ifgs[ref_idx], single_ref_ifgs[sec_idx])
        #     for ref_idx, sec_idx in interferogram_network.indexes
        # ]
        # ifg_file_list.extend(ifgs)

    if interferogram_network.reference_idx == 0:
        ifg_file_list.extend(single_ref_ifgs)

    # For other networks, we have to combine other ones formed from the `Network`
    # Say we had inputs like:
    #  compressed_1_2_3 , slc_4, slc_5, slc_6
    # the compressed one is referenced to "1"
    # There will be 3 PL outputs for days 4, 5, 6, referenced to day "1":
    # (1, 4), (1, 5), (1, 6)
    # If we requested max-bw-2 interferograms, we want
    # (1, 4), (1, 5), (4, 5), (4, 6), (5, 6)
    # (the same as though we had normal SLCs (1, 4, 5, 6) )
    if interferogram_network.max_bandwidth is not None:
        max_b = interferogram_network.max_bandwidth
        # Max bandwidth is easier: take the first `max_b` from `phase_linked_slcs`
        # (which are the (ref_date, ...) interferograms),...
        ifgs_ref_date = single_ref_ifgs[:max_b]
        # ...then combine it with the results from the `Network`
        # Manually specify the dates, which come from the names of `phase_linked_slcs`
        secondary_dates = [get_dates(f)[0] for f in phase_linked_slcs]
        network_rest = interferogram.Network(
            slc_list=phase_linked_slcs,
            max_bandwidth=max_b,
            outdir=ifg_dir,
            dates=secondary_dates,
            write=not dry_run,
            verify_slcs=not dry_run,
        )
        # Using `cast` to assert that the paths are not None
        ifgs_others = cast(list[Path], [ifg.path for ifg in network_rest.ifg_list])

        ifg_file_list.extend(ifgs_ref_date + ifgs_others)

    if interferogram_network.max_temporal_baseline is not None:
        # Other types: TODO
        msg = (
            "max-temporal-baseline networks not yet supported when "
            " starting with compressed SLCs"
        )
        raise NotImplementedError(msg)

    # Dedupe, in case different options made the same ifg
    requested_ifgs = set(ifg_file_list)
    # remove ones we aren't using (in the case of a single index)
    written_ifgs = set(ifg_dir.glob("*.int*"))
    for p in written_ifgs - requested_ifgs:
        p.unlink()
    return ifg_file_list


def _get_reference_date_idx(
    input_file_list: Sequence[Path],
    is_compressed: Sequence[bool],
    input_dates: Sequence[Sequence[datetime.datetime]],
) -> tuple[datetime.datetime, int]:
    is_compressed = ["compressed" in str(f).lower() for f in input_file_list]
    if not is_compressed[0]:
        return input_dates[0][0], 0

    # Otherwise use the last Compressed SLC as reference
    reference_idx = np.where(is_compressed)[0][-1]
    reference_date = input_dates[reference_idx][0]

    return reference_date, reference_idx


def _get_input_dates(
    input_file_list: Sequence[Path], is_compressed: Sequence[bool], date_fmt: str
) -> list[list[datetime.datetime]]:
    input_dates = [get_dates(f, fmt=date_fmt) for f in input_file_list]
    # For any that aren't compressed, take the first date.
    # this is because the official product name of OPERA/Sentinel1 has both
    # "acquisition_date" ... "generation_date" in the filename
    # TODO: this is a bit hacky, perhaps we can make this some input option
    # so that the user can specify how to get dates from their files (or even
    # directly pass in dates?)
    return [
        dates[:1] if not is_comp else dates
        for dates, is_comp in zip(input_dates, is_compressed)
    ]
