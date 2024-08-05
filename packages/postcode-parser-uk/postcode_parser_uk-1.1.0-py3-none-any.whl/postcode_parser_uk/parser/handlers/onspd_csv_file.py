import os
import re
import zipfile
from datetime import datetime
from typing import List, Optional

import pandas as pd

from .regex import RegexParsingHandler
from .handler import ParsingHandler
from ...result import Result
from ...postcode import UKPostCode
from ...errors import PostcodeNotFoundError
from ...logging import get_logger

logger = get_logger()


class _ONSPDFileName:
    """Class to represent and parse the ONSPD file name format."""

    def __init__(self, prefix: str, month: str, year: str, region: str):
        self.prefix = prefix
        self.month = month
        self.year = year
        self.region = region
        self.name = f"{prefix}_{month}_{year}_{region}"

    @classmethod
    def from_string(cls, name: str) -> "_ONSPDFileName":
        """Creates an ONSPDFileName object from a string."""
        pattern = r"ONSPD_([A-Z]{3})_(\d{4})_(\w+)"
        match = re.match(pattern, name)
        if not match:
            raise ValueError(f"Invalid file name format: {name}")
        month, year, region = match.groups()
        return cls("ONSPD", month, year, region)

    def as_datetime(self) -> datetime:
        """Returns the date as a datetime object."""
        month_str_to_int = {
            "JAN": 1,
            "FEB": 2,
            "MAR": 3,
            "APR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AUG": 8,
            "SEP": 9,
            "OCT": 10,
            "NOV": 11,
            "DEC": 12,
        }
        month = month_str_to_int[self.month.upper()]
        year = int(self.year)
        return datetime(year, month, 1)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def find_latest(files: List[str]) -> Optional["_ONSPDFileName"]:
        """Finds the latest file from a list of file names."""
        ons_files: List[_ONSPDFileName] = []
        for file in files:
            try:
                ons_files.append(_ONSPDFileName.from_string(file))
            except ValueError:
                logger.warning(f"Skipping invalid file name: {file}")
        return max(ons_files, key=lambda f: f.as_datetime(), default=None)


class ONSPDDataZipFileProcessor:
    """Class for handling extraction and parsing of a zip file."""

    @staticmethod
    def process(zip_path: str, extracted_path: str, postcodes_path: str) -> str:
        """Full processing pipeline: extract, parse, and write to CSV."""
        zip_file = os.path.basename(zip_path)
        extract_to = ONSPDDataZipFileProcessor._extract_zip_file(
            zip_path, os.path.join(extracted_path, os.path.splitext(zip_file)[0])
        )
        data_csv_path = ONSPDDataZipFileProcessor._get_data_csv_path(
            extract_to, zip_file
        )
        data = ONSPDDataZipFileProcessor._parse_postcodes(data_csv_path)
        return ONSPDDataZipFileProcessor._write_csv(
            data,
            os.path.join(postcodes_path, f"{os.path.splitext(zip_file)[0]}.csv"),
        )

    @staticmethod
    def _extract_zip_file(zip_path: str, extract_to: str) -> str:
        """Extracts CSV files from a zip file."""
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            logger.info(
                f"ONSPDCsvFileParsingHandler -> Extracted files from {zip_path} to {extract_to}"
            )
            return extract_to
        except Exception as e:
            raise Exception(f"An error occurred during extraction: {e}")

    @staticmethod
    def _get_data_csv_path(extract_to: str, zip_file: str) -> str:
        """Gets the path of the main data CSV file."""
        data_folder = os.path.join(extract_to, "Data")
        for file in os.listdir(data_folder):
            if file.endswith(".csv") and file.startswith(os.path.splitext(zip_file)[0]):
                return os.path.join(data_folder, file)
        raise Exception(
            f"No CSV file found in {data_folder} matching the expected pattern."
        )

    @staticmethod
    def _parse_postcodes(csv_path: str) -> pd.DataFrame:
        """Parses and formats postcodes from the main data CSV."""
        try:
            data = pd.read_csv(csv_path, usecols=["pcd"])
            data["postcode"] = (
                data["pcd"].str.replace(" ", "").apply(lambda x: f"{x[:-3]} {x[-3:]}")
            )
            return data[["postcode"]]
        except Exception as e:
            raise Exception(f"An error occurred while reading {csv_path}: {e}")

    @staticmethod
    def _write_csv(data: pd.DataFrame, out_path: str) -> str:
        """Writes DataFrame to a CSV file."""
        postcodes = data["postcode"].drop_duplicates().sort_values()
        logger.info(
            f"ONSPDCsvFileParsingHandler -> There are {len(postcodes):,} postcodes in the dataset."
        )
        try:
            postcodes.to_csv(out_path, index=False)
            logger.info(
                f"ONSPDCsvFileParsingHandler -> Created {out_path} with postcodes."
            )
            return out_path
        except Exception as e:
            raise Exception(f"An error occurred while writing {out_path}: {e}")


class ONSPDCsvFileParsingHandler(ParsingHandler):
    """
    Class for validating parsing from a CSV file.

    Args:
        path (str): The path to the zip file containing the ONSPD data.

    Methods:
        parse(postcode: str) -> Result[Union[UKPostCode, SpecialUKPostCode]]:
        Handle the parsing of the provided postcode and return a Result object.
    """

    def __init__(self, path: Optional[str] = None):
        logger.warning(
            (
                "ONSPDCsvFileParsingHandler -> Path to a zip file was not provided in the constructor. "
                "Will try to load the latest postcodes data from the filesystem."
            )
        )
        self._data_path = "data"
        self._postcodes_path = os.path.join(self._data_path, "postcodes")

        self._csv_path = None
        self._path = path
        self._postcodes = None

    def _parse(self, postcode: str) -> Result[Optional[UKPostCode]]:
        """Parse the postcode."""
        if self._postcodes is None:
            self._initialize_data_path(self._path)

        if postcode not in self.postcodes.values:
            return Result.failure(
                error=PostcodeNotFoundError(
                    f"Postcode {postcode} not found in ONSPD data"
                )
            )
        return RegexParsingHandler()._parse(postcode)

    @property
    def postcodes(self) -> pd.Series:
        """Lazy load the postcodes from the CSV file."""
        if self._postcodes is None:
            logger.info(
                f"ONSPDCsvFileParsingHandler -> Loading postcodes from {self._csv_path}"
            )
            self._postcodes = self._load_csv(self._csv_path)
            logger.info(
                f"ONSPDCsvFileParsingHandler -> Loaded postcodes from {self._csv_path}"
            )
        return self._postcodes

    def _initialize_data_path(self, path: Optional[str]):
        """Initialize the data path based on the provided path."""
        os.makedirs(self._postcodes_path, exist_ok=True)
        if path:
            if self._check_existing_csv(path):
                self._load_existing_csv(path)
            else:
                try:
                    self._process_zip(path)
                except ValueError as e:
                    logger.error(
                        f"ONSPDCsvFileParsingHandler -> Invalid zip file provided: {e}"
                    )
        else:
            self._load_latest_csv()

    def _check_existing_csv(self, zip_path: str) -> bool:
        """Checks if the CSV file for the given zip file already exists."""
        csv_path = self._get_csv_path(zip_path)
        return os.path.exists(csv_path)

    def _get_csv_path(self, zip_path: str) -> str:
        """Gets the corresponding CSV path for the given zip file."""
        zip_file = os.path.basename(zip_path)
        csv_file = f"{os.path.splitext(zip_file)[0]}.csv"
        return os.path.join(self._postcodes_path, csv_file)

    def _load_existing_csv(self, zip_path: str):
        """Loads the existing CSV file for the given zip file."""
        logger.info(
            f"ONSPDCsvFileParsingHandler -> Loading existing CSV file for {zip_path}"
        )
        self._csv_path = self._get_csv_path(zip_path)

    def _load_latest_csv(self):
        """Loads the latest CSV file in the postcodes directory."""
        try:

            latest_csv = self._find_latest_csv(self._postcodes_path)
            logger.info(
                f"ONSPDCsvFileParsingHandler -> Loading latest CSV file: {latest_csv}"
            )
            self._csv_path = os.path.join(self._postcodes_path, latest_csv)
            logger.info(
                f"ONSPDCsvFileParsingHandler -> Loaded latest CSV file: {latest_csv}"
            )

        except ValueError as e:
            raise ValueError(
                "No valid CSV files found in the postcodes directory. Please provide a valid zip file path."
            ) from e

    def _find_latest_csv(self, path: str) -> str:
        """Finds the latest CSV file in the postcodes directory."""
        logger.info(f"ONSPDCsvFileParsingHandler -> Finding latest CSV file in {path}")
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        file = _ONSPDFileName.find_latest(files)
        if file is None:
            raise ValueError("No valid CSV files found in the postcodes directory.")
        logger.info(f"ONSPDCsvFileParsingHandler -> Found latest CSV file: {file}.csv")
        return f"{file.name}.csv"

    def _load_csv(self, path: str) -> pd.Series:
        """Loads postcodes from a CSV file."""
        try:
            return pd.read_csv(path)["postcode"]
        except Exception as e:
            raise Exception(f"An error occurred while loading {path}: {e}")

    def _process_zip(self, zip_path: str):
        """Processes the zip file and updates the postcodes."""
        logger.info(f"ONSPDCsvFileParsingHandler -> Processing zip file: {zip_path}")
        self._csv_path = ONSPDDataZipFileProcessor.process(
            zip_path=zip_path,
            extracted_path=os.path.join(self._data_path, "extracted"),
            postcodes_path=self._postcodes_path,
        )
        logger.info(f"ONSPDCsvFileParsingHandler -> Processed zip file: {zip_path}")
