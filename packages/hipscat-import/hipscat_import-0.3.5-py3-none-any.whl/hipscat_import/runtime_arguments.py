"""Data class to hold common runtime arguments for dataset creation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from importlib.metadata import version
from typing import Any, Dict, Union

from hipscat.io import FilePointer, file_io

# pylint: disable=too-many-instance-attributes


@dataclass
class RuntimeArguments:
    """Data class for holding runtime arguments"""

    ## Output
    output_path: str = ""
    """base path where new catalog should be output"""
    output_artifact_name: str = ""
    """short, convenient name for the catalog"""
    output_storage_options: Union[Dict[Any, Any], None] = None
    """optional dictionary of abstract filesystem credentials for the OUTPUT."""

    ## Execution
    tmp_dir: str = ""
    """path for storing intermediate files"""
    resume: bool = True
    """If True, we try to read any existing intermediate files and continue to run
    the pipeline where we left off. If False, we start the import from scratch,
    overwriting any content of the output directory."""
    progress_bar: bool = True
    """if true, a progress bar will be displayed for user
    feedback of map reduce progress"""
    simple_progress_bar: bool = False
    """if displaying a progress bar, use a text-only simple progress
    bar instead of widget. this can be useful in some environments when running
    in a notebook where ipywidgets cannot be used (see `progress_bar` argument)"""
    dask_tmp: str = ""
    """directory for dask worker space. this should be local to
    the execution of the pipeline, for speed of reads and writes"""
    dask_n_workers: int = 1
    """number of workers for the dask client"""
    dask_threads_per_worker: int = 1
    """number of threads per dask worker"""
    resume_tmp: str = ""
    """directory for intermediate resume files, when needed. see RTD for more info."""

    completion_email_address: str = ""
    """if provided, send an email to the indicated email address once the 
    import pipeline has complete."""

    catalog_path: FilePointer | None = None
    """constructed output path for the catalog that will be something like
    <output_path>/<output_artifact_name>"""
    tmp_path: FilePointer | None = None
    """constructed temp path - defaults to tmp_dir, then dask_tmp, but will create
    a new temp directory under catalog_path if no other options are provided"""

    def __post_init__(self):
        self._check_arguments()

    def _check_arguments(self):
        if not self.output_path:
            raise ValueError("output_path is required")
        if not self.output_artifact_name:
            raise ValueError("output_artifact_name is required")
        if re.search(r"[^A-Za-z0-9\._\-\\]", self.output_artifact_name):
            raise ValueError("output_artifact_name contains invalid characters")

        if self.dask_n_workers <= 0:
            raise ValueError("dask_n_workers should be greather than 0")
        if self.dask_threads_per_worker <= 0:
            raise ValueError("dask_threads_per_worker should be greater than 0")

        self.catalog_path = file_io.append_paths_to_pointer(self.output_path, self.output_artifact_name)
        if not self.resume:
            file_io.remove_directory(
                self.catalog_path, ignore_errors=True, storage_options=self.output_storage_options
            )
        file_io.make_directory(self.catalog_path, exist_ok=True, storage_options=self.output_storage_options)

        if self.tmp_dir:
            if not file_io.does_file_or_directory_exist(self.tmp_dir):
                raise FileNotFoundError(f"tmp_dir ({self.tmp_dir}) not found on local storage")
            self.tmp_path = file_io.append_paths_to_pointer(
                self.tmp_dir, self.output_artifact_name, "intermediate"
            )
        elif self.dask_tmp:
            if not file_io.does_file_or_directory_exist(self.dask_tmp):
                raise FileNotFoundError(f"dask_tmp ({self.dask_tmp}) not found on local storage")
            self.tmp_path = file_io.append_paths_to_pointer(
                self.dask_tmp, self.output_artifact_name, "intermediate"
            )
        else:
            self.tmp_path = file_io.append_paths_to_pointer(self.catalog_path, "intermediate")
        file_io.make_directory(self.tmp_path, exist_ok=True, storage_options=self.output_storage_options)
        if self.resume_tmp:
            self.resume_tmp = file_io.append_paths_to_pointer(self.resume_tmp, self.output_artifact_name)
        else:
            self.resume_tmp = self.tmp_path

    def provenance_info(self) -> dict:
        """Fill all known information in a dictionary for provenance tracking.

        Returns:
            dictionary with all argument_name -> argument_value as key -> value pairs.
        """
        runtime_args = {
            "catalog_name": self.output_artifact_name,
            "output_path": self.output_path,
            "output_artifact_name": self.output_artifact_name,
            "tmp_dir": self.tmp_dir,
            "dask_tmp": self.dask_tmp,
            "dask_n_workers": self.dask_n_workers,
            "dask_threads_per_worker": self.dask_threads_per_worker,
            "catalog_path": self.catalog_path,
            "tmp_path": self.tmp_path,
        }

        runtime_args.update(self.additional_runtime_provenance_info())
        provenance_info = {
            "tool_name": "hipscat_import",
            "version": version("hipscat-import"),
            "runtime_args": runtime_args,
        }

        return provenance_info

    def additional_runtime_provenance_info(self):
        """Any additional runtime args to be included in provenance info from subclasses"""
        return {}


def find_input_paths(
    input_path="", file_matcher="", input_file_list=None, storage_options: Union[Dict[Any, Any], None] = None
):
    """Helper method to find input paths, given either a prefix and format, or an
    explicit list of paths.

    Args:
        input_path (str): prefix to search for
        file_matcher (str): matcher to use when searching for files
        input_file_list (List[str]): list of input paths
    Returns:
        matching files, if input_path is provided, otherwise, input_file_list
    Raises:
        FileNotFoundError: if no files are found at the input_path and the provided list is empty.
    """
    input_paths = []
    if input_path:
        if input_file_list:
            raise ValueError("exactly one of input_path or input_file_list is required")

        if not file_io.does_file_or_directory_exist(input_path, storage_options=storage_options):
            raise FileNotFoundError("input_path not found on local storage")
        input_paths = file_io.find_files_matching_path(
            input_path, file_matcher, include_protocol=True, storage_options=storage_options
        )
    elif not input_file_list is None:
        # It's common for users to accidentally pass in an empty list. Give them a friendly error.
        if len(input_file_list) == 0:
            raise ValueError("input_file_list is empty")
        input_paths = input_file_list
    else:
        raise ValueError("exactly one of input_path or input_file_list is required")
    if len(input_paths) == 0:
        raise FileNotFoundError("No input files found")
    return input_paths
