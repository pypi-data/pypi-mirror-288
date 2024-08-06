"""Import a set of non-hipscat files using dask for parallelization

Methods in this file set up a dask pipeline using futures. 
The actual logic of the map reduce is in the `map_reduce.py` file.
"""

import os
import pickle

import hipscat.io.write_metadata as io
from hipscat.catalog import PartitionInfo
from hipscat.io import paths
from hipscat.io.parquet_metadata import write_parquet_metadata

import hipscat_import.catalog.map_reduce as mr
from hipscat_import.catalog.arguments import ImportArguments


def run(args, client):
    """Run catalog creation pipeline."""
    if not args:
        raise ValueError("args is required and should be type ImportArguments")
    if not isinstance(args, ImportArguments):
        raise ValueError("args must be type ImportArguments")

    pickled_reader_file = os.path.join(args.resume_plan.tmp_path, "reader.pickle")
    with open(pickled_reader_file, "wb") as pickle_file:
        pickle.dump(args.file_reader, pickle_file)

    if not args.resume_plan.is_mapping_done():
        futures = []
        for key, file_path in args.resume_plan.map_files:
            futures.append(
                client.submit(
                    mr.map_to_pixels,
                    input_file=file_path,
                    resume_path=args.resume_plan.tmp_path,
                    pickled_reader_file=pickled_reader_file,
                    mapping_key=key,
                    highest_order=args.mapping_healpix_order,
                    ra_column=args.ra_column,
                    dec_column=args.dec_column,
                    use_hipscat_index=args.use_hipscat_index,
                )
            )
        args.resume_plan.wait_for_mapping(futures)

    with args.resume_plan.print_progress(total=2, stage_name="Binning") as step_progress:
        raw_histogram = args.resume_plan.read_histogram(args.mapping_healpix_order)
        total_rows = int(raw_histogram.sum())
        if args.expected_total_rows > 0 and args.expected_total_rows != total_rows:
            raise ValueError(
                f"Number of rows ({total_rows}) does not match expectation ({args.expected_total_rows})"
            )

        step_progress.update(1)
        alignment_file = args.resume_plan.get_alignment_file(
            raw_histogram,
            args.constant_healpix_order,
            args.highest_healpix_order,
            args.lowest_healpix_order,
            args.pixel_threshold,
            args.drop_empty_siblings,
            total_rows,
        )

        step_progress.update(1)

    if not args.debug_stats_only:
        if not args.resume_plan.is_splitting_done():
            futures = []
            for key, file_path in args.resume_plan.split_keys:
                futures.append(
                    client.submit(
                        mr.split_pixels,
                        input_file=file_path,
                        pickled_reader_file=pickled_reader_file,
                        highest_order=args.mapping_healpix_order,
                        ra_column=args.ra_column,
                        dec_column=args.dec_column,
                        splitting_key=key,
                        cache_shard_path=args.tmp_path,
                        resume_path=args.resume_plan.tmp_path,
                        alignment_file=alignment_file,
                        use_hipscat_index=args.use_hipscat_index,
                    )
                )

            args.resume_plan.wait_for_splitting(futures)

        if not args.resume_plan.is_reducing_done():
            futures = []
            for (
                destination_pixel,
                source_pixel_count,
                destination_pixel_key,
            ) in args.resume_plan.get_reduce_items():
                futures.append(
                    client.submit(
                        mr.reduce_pixel_shards,
                        cache_shard_path=args.tmp_path,
                        resume_path=args.resume_plan.tmp_path,
                        reducing_key=destination_pixel_key,
                        destination_pixel_order=destination_pixel.order,
                        destination_pixel_number=destination_pixel.pixel,
                        destination_pixel_size=source_pixel_count,
                        output_path=args.catalog_path,
                        ra_column=args.ra_column,
                        dec_column=args.dec_column,
                        sort_columns=args.sort_columns,
                        add_hipscat_index=args.add_hipscat_index,
                        use_schema_file=args.use_schema_file,
                        use_hipscat_index=args.use_hipscat_index,
                        delete_input_files=args.delete_intermediate_parquet_files,
                        storage_options=args.output_storage_options,
                    )
                )

            args.resume_plan.wait_for_reducing(futures)

    # All done - write out the metadata
    with args.resume_plan.print_progress(total=5, stage_name="Finishing") as step_progress:
        catalog_info = args.to_catalog_info(total_rows)
        io.write_provenance_info(
            catalog_base_dir=args.catalog_path,
            dataset_info=catalog_info,
            tool_args=args.provenance_info(),
            storage_options=args.output_storage_options,
        )
        step_progress.update(1)

        io.write_catalog_info(
            catalog_base_dir=args.catalog_path,
            dataset_info=catalog_info,
            storage_options=args.output_storage_options,
        )
        step_progress.update(1)
        partition_info = PartitionInfo.from_healpix(args.resume_plan.get_destination_pixels())
        partition_info_file = paths.get_partition_info_pointer(args.catalog_path)
        partition_info.write_to_file(partition_info_file, storage_options=args.output_storage_options)
        if not args.debug_stats_only:
            parquet_rows = write_parquet_metadata(
                args.catalog_path, storage_options=args.output_storage_options
            )
            if total_rows > 0 and parquet_rows != total_rows:
                raise ValueError(
                    f"Number of rows in parquet ({parquet_rows}) does not match expectation ({total_rows})"
                )

        else:
            partition_info.write_to_metadata_files(
                args.catalog_path, storage_options=args.output_storage_options
            )
        step_progress.update(1)
        io.write_fits_map(args.catalog_path, raw_histogram, storage_options=args.output_storage_options)
        step_progress.update(1)
        args.resume_plan.clean_resume_files()
        step_progress.update(1)
