"""
Metadata Builder for Beijing Air Quality Project
Produces clean YAML metadata files for raw, combined, cleaned, engineered
and ML datasets.

Author: Robert Steven Elliott
"""

import os
import datetime
from pathlib import Path
import yaml


class MetadataBuilder:
    """
    A builder class for generating metadata YAML files with step tracking.
    """

    def __init__(self, dataset_path, dataset_name, description):
        self.dataset_path = Path(dataset_path)
        self.dataset_name = dataset_name
        self.description = description
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Core structure
        self.metadata = {
            "dataset_name": dataset_name,
            "path": str(dataset_path),
            "description": description,
            "created_on": self.timestamp,
            "created_by": "Robert Steven Elliott",
        }

        # Step tracking
        self.metadata["steps"] = []

    def add_step(self, step_description: str):
        """
        Append a step documenting a transformation, cleaning action,
        or processing stage.

        Args:
            step_description (str): Description of the step to add.
        """
        self.metadata["steps"].append(step_description)

    def add_columns(self, columns):
        """
        Add a list of column names to the metadata.

        Args:
            columns (list or iterable): List or iterable of column names.
        """
        self.metadata["columns"] = list(columns)

    def add_creation_script(self, script_path):
        """
        Add the path to the script used to create the dataset.

        Args:
            script_path (str or Path): Path to the creation script.
        """
        self.metadata["creation_script"] = script_path

    def add_source_info(self):
        """
        Add source information for the dataset.
        """
        self.metadata["source"] = {
            "title": "Beijing Multi-Site Air Quality",
            "author": "Song Chen",
            "year": 2017,
            "doi": "https://doi.org/10.24432/C5RK5G",
            "uci_repository": "https://archive.ics.uci.edu/dataset/501",
            "kaggle_mirror": "https://www.kaggle.com/datasets/sid321axn/\
                                beijing-multisite-airquality-data-set"
        }

    def add_licence(self):
        """
        Add licence information for the dataset.
        """
        self.metadata["licence"] = {
            "name": "Creative Commons Attribution 4.0 International \
                (CC BY 4.0)",
            "url": "https://creativecommons.org/licenses/by/4.0/",
            "attribution_required": True,
            "attribution_statement": (
                "Derived from “Beijing Multi-Site Air Quality” (Song Chen, \
                    2017). "
                "UCI Machine Learning Repository. \
                    DOI: https://doi.org/10.24432/C5RK5G"
            )
        }

    def add_intended_use(self, uses):
        """Add intended use information for the dataset.

        Args:
            uses (str or list): Intended use or list of uses for the dataset.
        """
        self.metadata["intended_use"] = uses

    def add_file_list(self, files):
        """
        Add a list of files included in the dataset.

        Args:
            files (list or iterable): List or iterable of file names.
        """
        self.metadata["files"] = sorted(files)

    def add_record_stats(self, file):
        """
        Add file size and record count if applicable.

        Args:
            file (str or Path): Path to the file to analyze.
        """
        if Path(file).exists() and Path(file).is_file():
            size_mb = os.path.getsize(file) / (1024 * 1024)
            self.metadata["file_size"] = f"{size_mb:.2f} MB"
        else:
            self.metadata["file_size"] = "Unknown"

    def add_record_count_from_df(self, df):
        """
        Set the record_count field using df.shape[0].
        Use this when the dataframe is already loaded in the notebook.

        Args:
            df (pandas.DataFrame): DataFrame to get the record count from.
        """
        self.metadata["record_count"] = int(df.shape[0])

    def write(self, output_path=None):
        """
        Write metadata YAML file to disk.
        If output_path is not provided, use <dataset>.yml.

        Args:
            output_path (str or Path, optional): Path to write the YAML file
            to.
        """

        if output_path is None:
            output_path = self.dataset_path.with_suffix(".yml")

        output_path = Path(output_path)

        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(self.metadata, f, sort_keys=False, allow_unicode=True)

        print(f"📄 Metadata written to: {output_path}")
