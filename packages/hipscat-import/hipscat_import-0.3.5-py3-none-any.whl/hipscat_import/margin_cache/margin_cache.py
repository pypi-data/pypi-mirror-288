from hipscat.catalog import PartitionInfo
from hipscat.io import file_io, parquet_metadata, paths, write_metadata

import hipscat_import.margin_cache.margin_cache_map_reduce as mcmr
from hipscat_import.margin_cache.margin_cache_resume_plan import MarginCachePlan

# pylint: disable=too-many-locals,too-many-arguments


def generate_margin_cache(args, client):
    """Generate a margin cache for a given input catalog.
    The input catalog must be in hipscat format.

    Args:
        args (MarginCacheArguments): A valid `MarginCacheArguments` object.
        client (dask.distributed.Client): A dask distributed client object.
    """
    resume_plan = MarginCachePlan(args)
    original_catalog_metadata = paths.get_common_metadata_pointer(args.input_catalog_path)

    if not resume_plan.is_mapping_done():
        futures = []
        for mapping_key, pix in resume_plan.get_remaining_map_keys():
            partition_file = paths.pixel_catalog_file(args.input_catalog_path, pix.order, pix.pixel)
            futures.append(
                client.submit(
                    mcmr.map_pixel_shards,
                    partition_file=partition_file,
                    mapping_key=mapping_key,
                    input_storage_options=args.input_storage_options,
                    original_catalog_metadata=original_catalog_metadata,
                    margin_pair_file=resume_plan.margin_pair_file,
                    margin_threshold=args.margin_threshold,
                    output_path=args.tmp_path,
                    margin_order=args.margin_order,
                    ra_column=args.catalog.catalog_info.ra_column,
                    dec_column=args.catalog.catalog_info.dec_column,
                    fine_filtering=args.fine_filtering,
                )
            )
        resume_plan.wait_for_mapping(futures)

    if not resume_plan.is_reducing_done():
        futures = []
        for reducing_key, pix in resume_plan.get_remaining_reduce_keys():
            futures.append(
                client.submit(
                    mcmr.reduce_margin_shards,
                    intermediate_directory=args.tmp_path,
                    reducing_key=reducing_key,
                    output_path=args.catalog_path,
                    output_storage_options=args.output_storage_options,
                    partition_order=pix.order,
                    partition_pixel=pix.pixel,
                    original_catalog_metadata=original_catalog_metadata,
                    delete_intermediate_parquet_files=args.delete_intermediate_parquet_files,
                    input_storage_options=args.input_storage_options,
                )
            )
        resume_plan.wait_for_reducing(futures)

    with resume_plan.print_progress(total=4, stage_name="Finishing") as step_progress:
        total_rows = parquet_metadata.write_parquet_metadata(
            args.catalog_path, storage_options=args.output_storage_options
        )
        step_progress.update(1)
        metadata_path = paths.get_parquet_metadata_pointer(args.catalog_path)
        partition_info = PartitionInfo.read_from_file(
            metadata_path, storage_options=args.output_storage_options
        )
        partition_info_file = paths.get_partition_info_pointer(args.catalog_path)
        partition_info.write_to_file(partition_info_file, storage_options=args.output_storage_options)

        step_progress.update(1)
        margin_catalog_info = args.to_catalog_info(int(total_rows))
        write_metadata.write_provenance_info(
            catalog_base_dir=args.catalog_path,
            dataset_info=margin_catalog_info,
            tool_args=args.provenance_info(),
            storage_options=args.output_storage_options,
        )
        write_metadata.write_catalog_info(
            catalog_base_dir=args.catalog_path,
            dataset_info=margin_catalog_info,
            storage_options=args.output_storage_options,
        )
        step_progress.update(1)
        file_io.remove_directory(
            args.tmp_path, ignore_errors=True, storage_options=args.output_storage_options
        )
        step_progress.update(1)
