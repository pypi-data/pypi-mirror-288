import logging
import os

from typing import List

from .. import constants
from ..record import Record
from ..file_utils import calculate_md5, get_file_creation_date
from .dbutil import (
    create_database,
    create_provenance_table,
    create_table,
    insert_provenance_table,
    insert_record_into_table,
)


class Manager:
    """Class loading the SLURM Completed Jobs records into a SQLite3 database instance."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.database_file = kwargs.get("database_file", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.table_name = kwargs.get("table_name", constants.DEFAULT_TABLE_NAME)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.filtered_column_names = None
        self.ignore_column_lookup = {}
        self._load_ignore_columns_lookup()

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _load_ignore_columns_lookup(self) -> None:
        ignore_columns_list = self.config.get("ignore_columns", {})
        ctr = 0
        for column in ignore_columns_list:
            ctr += 1
            self.ignore_column_lookup[column] = True

        if ctr > 0:
            logging.info(f"Loaded '{ctr}' column names into the ignore column lookup")

    def load_records(self, records: List[Record]) -> None:
        """Load the SLURM Completed Jobs log records into a SQLite3 database
        instance."""
        create_database(self.database_file)
        create_provenance_table()
        self._insert_provenance()
        # TODO: add support to check whether the table already exists
        self._create_jobs_table()
        self._load_records_into_jobs_table(records)

    def _create_jobs_table(self) -> None:
        """Create the jobs table in the SQLite database."""

        column_names = self._get_filtered_column_names()

        create_table(
            self.table_name,
            column_names,
            self.config
        )

    def _get_filtered_column_names(self) -> List[str]:
        column_names = []
        if "table_schema" not in self.config:
            raise Exception(f"'table_schema' not defined in the configuration file '{self.config_file}'")
        if "jobs" not in self.config["table_schema"]:
            raise Exception(f"'jobs' not defined in the 'table_schema' section of the configuration file '{self.config_file}'")

        column_names = self.config["table_schema"]["jobs"]

        filtered_column_names = []

        for column_name in column_names:
            if column_name in self.ignore_column_lookup:
                logging.info(f"Excluding column '{column_name}'")
                continue
            filtered_column_names.append(column_name)

        self.filtered_column_names = filtered_column_names

        return filtered_column_names

    def _load_records_into_jobs_table(self, records: List[Record]) -> None:
        """Load the records into the jobs table in the SQLite database.

        Args:
            records (List[Record]): The list of records to load into the database.
        """
        for record in records:
            record_dict = record.model_dump()
            final_record_list = []
            final_column_names = []
            for key, value in record_dict.items():
                if key in self.filtered_column_names:
                    final_column_names.append(key)
                    final_record_list.append(value)
            insert_record_into_table(self.table_name, final_column_names, final_record_list)

    def _get_normalized_name(self, column_name: str) -> str:
        """Derive a normalized column name for the column.

        This will replace all punctuation, symbols and spaces with underscores

        Args:
            column_name (str): the original column name

        Returns:
            str: the normalized column name
        """
        column_name = (
            column_name.replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace("(", "_")
            .replace(")", "_")
            .replace("*", "_")
            .replace("&", "_")
            .replace("@", "_")
            .replace("#", "")
            .replace("!", "_")
            .replace("?", "_")
            .replace(".", "_")
            .replace("+", "_")
            .replace("-", "_")
            .replace("~", "_")
            .replace("[", "_")
            .replace("]", "_")
            .replace("{", "_")
            .replace("}", "_")
            .replace("|", "_")
            .replace(",", "_")
            .replace(";", "_")
            .replace("'", "_")
            .replace('"', "_")
        )

        # If column_name contains two or more consecutive underscores, replace with a single underscore
        while "__" in column_name:
            column_name = column_name.replace("__", "_")

        # If column_name starts with a number, prepend with an underscore
        if column_name[0].isdigit():
            column_name = f"_{column_name}"

        return column_name

    def _insert_provenance(self) -> None:
        bytesize = os.path.getsize(self.infile)
        checksum = calculate_md5(self.infile)
        date_created = get_file_creation_date(self.infile)

        insert_provenance_table(
            bytesize,
            checksum,
            date_created,
            os.path.abspath(self.infile)
        )
