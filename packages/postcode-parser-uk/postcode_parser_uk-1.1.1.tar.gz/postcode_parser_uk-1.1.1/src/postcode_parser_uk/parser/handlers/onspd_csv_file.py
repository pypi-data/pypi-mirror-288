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
from ...errors import PostcodeNotFoundError, PostCodeFormatError
from ...logging import get_logger

logger = get_logger()


class ONSPDFileName:
    """Class for handling ONSPD file names."""

    def __init__(self, prefix: str, month: str, year: str):
        self.prefix = prefix
        self.month = month
        self.year = year
        self.name = f"{prefix}_{month}_{year}"

    @classmethod
    def from_string(cls, name: str) -> "ONSPDFileName":
        """Creates an ONSPDFileName object from a string."""
        pattern = r"ONSPD_([A-Z]+)_(\d{4})"
        match = re.match(pattern, name)
        if not match:
            logger.error(
                f"Invalid ONSPD file format: {name}. Expected format: ONSPD_MONTH_YEAR"
            )
            raise ValueError(
                f"Invalid ONSPD file format: {name}. Expected format: ONSPD_MONTH_YEAR"
            )
        month, year = match.groups()
        logger.debug(f"Extracted month: {month}, year: {year} from {name}")
        return cls("ONSPD", month, year)

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
    def find_latest(files: List[str]) -> Optional["ONSPDFileName"]:
        """Finds the latest file from a list of file names."""
        ons_files: List[ONSPDFileName] = []
        for file in files:
            try:
                ons_files.append(ONSPDFileName.from_string(file.split(".")[0]))
            except ValueError:
                logger.warning(f"Skipping invalid file name: {file}")
        return max(ons_files, key=lambda f: f.as_datetime(), default=None)


class ONSPDDataZipFileProcessor:
    """Class for handling extraction and parsing of a zip file."""

    @staticmethod
    def process(zip_path: str, extracted_path: str, postcodes_path: str) -> str:
        """Full processing pipeline: extract, parse, and write to CSV."""
        zip_file = os.path.basename(zip_path)
        extraction_dir = os.path.join(extracted_path, os.path.splitext(zip_file)[0])

        logger.info(f"Extracting files from {zip_path} to {extraction_dir}")
        extract_to = ONSPDDataZipFileProcessor._extract_zip(zip_path, extraction_dir)

        logger.info(f"Finding CSV file in {extract_to}")
        data_csv_path = ONSPDDataZipFileProcessor._find_csv_file(extract_to, zip_file)

        logger.info(f"Parsing postcodes from {data_csv_path}")
        data = ONSPDDataZipFileProcessor._parse_postcodes(data_csv_path)

        output_path = os.path.join(
            postcodes_path, f"{os.path.splitext(zip_file)[0]}.csv"
        )
        logger.info(f"Writing postcodes to {output_path}")
        output_file = ONSPDDataZipFileProcessor._write_csv(data, output_path)

        logger.info(f"Created {output_file} with postcodes.")
        return output_file

    @staticmethod
    def _extract_zip(zip_path: str, extract_to: str) -> str:
        """Extracts files from a zip archive."""
        os.makedirs(extract_to, exist_ok=True)
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            return extract_to
        except zipfile.BadZipFile as e:
            logger.error(f"Failed to extract {zip_path}: {e}")
            raise

    @staticmethod
    def _find_csv_file(extract_to: str, zip_file: str) -> str:
        """Finds the main data CSV file."""
        data_folder = os.path.join(extract_to, "Data")
        csv_files = [
            file
            for file in os.listdir(data_folder)
            if file.endswith(".csv") and file.startswith(os.path.splitext(zip_file)[0])
        ]
        if not csv_files:
            raise FileNotFoundError(f"No matching CSV file found in {data_folder}.")
        return os.path.join(data_folder, csv_files[0])

    @staticmethod
    def _parse_postcodes(csv_path: str) -> pd.DataFrame:
        """Parses and formats postcodes from the main data CSV."""
        try:
            data = pd.read_csv(csv_path, usecols=["pcd"])
            data["postcode"] = data["pcd"].str.replace(" ", "")
            data["formatted_postcode"] = data["postcode"].apply(
                lambda x: f"{x[:-3]} {x[-3:]}"
            )
            return data[["postcode", "formatted_postcode"]]
        except pd.errors.EmptyDataError as e:
            raise Exception(f"Failed to read {csv_path}: {e}")

    @staticmethod
    def _write_csv(data: pd.DataFrame, out_path: str) -> str:
        """Writes DataFrame to a CSV file."""
        try:
            postcodes = data.drop_duplicates().sort_values(by="postcode")
            postcodes.to_csv(out_path, index=False)
            return out_path
        except IOError as e:
            raise Exception(f"Failed to write {out_path}: {e}")


class ONSPDCSVFileParsingHandler(ParsingHandler):
    """
    Class for validating parsing from a CSV file.

    Args:
        path (str): The path to the zip file containing the ONSPD data.

    Methods:
        _parse(postcode: str) -> Result[Optional[UKPostCode]]:
        Handle the parsing of the provided postcode and return a Result object.
    """

    def __init__(self, path: Optional[str] = None):
        source_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(source_dir, "../../../.."))
        self._data_path = os.path.join(root_dir, "postcode-parser-uk-data")
        self._postcodes_path = os.path.join(self._data_path, "postcodes")
        self._csv_path = None
        self._postcodes = None
        self._path = path

    def _parse(self, postcode: str) -> Result[Optional[UKPostCode]]:
        """Parse the postcode."""
        try:
            if self._postcodes is None:
                self._initialize_data()
            return self._validate_and_parse_postcode(postcode)
        except Exception as e:
            return Result.failure(error=e)

    def _initialize_data(self) -> None:
        """Initialize data by loading or processing the CSV file."""
        os.makedirs(self._postcodes_path, exist_ok=True)

        if self._path:
            self._initialize_from_path(self._path)
        else:
            self._initialize_from_latest()

        self._postcodes = self._load_postcodes(self._csv_path)

    def _validate_and_parse_postcode(
        self, postcode: str
    ) -> Result[Optional[UKPostCode]]:
        """Validate and parse the postcode."""
        try:
            normalized_postcode = self._normalize_postcode(postcode)
            original_postcode = self._find_matching_postcode(normalized_postcode)
            return self._perform_parsing(original_postcode)
        except PostcodeNotFoundError as e:
            return Result.failure(error=e)

    def _normalize_postcode(self, postcode: str) -> str:
        """Normalize the postcode by removing the space in the standard position."""
        if len(postcode) >= 5 and postcode[-4] == " ":
            return postcode.replace(" ", "")
        else:
            raise PostCodeFormatError(
                f"Postcode {postcode} is not in the correct format."
            )

    def _find_matching_postcode(self, normalized_postcode: str) -> str:
        """Find the original formatted postcode matching the normalized postcode."""
        matching_postcodes = self._postcodes[
            self._postcodes["postcode"] == normalized_postcode
        ]

        if matching_postcodes.empty:
            raise PostcodeNotFoundError(
                f"Postcode {normalized_postcode} not found in ONSPD data"
            )

        return matching_postcodes["formatted_postcode"].values[0]

    def _perform_parsing(self, postcode: str) -> Result[Optional[UKPostCode]]:
        """Perform the actual parsing of the postcode."""
        return RegexParsingHandler()._parse(postcode)

    def _initialize_from_path(self, path: str) -> None:
        """Initialize data from the provided zip file path."""
        if self._check_existing_csv(path):
            self._csv_path = self._get_csv_path(path)
            logger.info(f"Loading existing CSV file from {self._csv_path} for {path}")
        else:
            self._csv_path = self._process_zip(path)
            logger.info(
                f"Processed zip file: {path}, created CSV file at {self._csv_path}"
            )

    def _initialize_from_latest(self) -> None:
        """Initialize data from the latest available CSV file."""
        logger.warning(
            "Path to a zip file was not provided. Will try to load the latest postcodes data from the filesystem."
        )
        self._csv_path = self._load_latest_csv()
        logger.info(f"Loaded latest CSV file: {self._csv_path}")

    def _check_existing_csv(self, zip_path: str) -> bool:
        """Checks if the CSV file for the given zip file already exists."""
        csv_path = self._get_csv_path(zip_path)
        exists = os.path.exists(csv_path)
        logger.debug(f"Checking if CSV file exists at {csv_path}: {exists}")
        return exists

    def _get_csv_path(self, zip_path: str) -> str:
        """Gets the corresponding CSV path for the given zip file."""
        zip_file = os.path.basename(zip_path)
        csv_file = f"{os.path.splitext(zip_file)[0]}.csv"
        csv_path = os.path.join(self._postcodes_path, csv_file)
        logger.debug(f"Determined CSV path for {zip_path} is {csv_path}")
        return csv_path

    def _load_latest_csv(self) -> str:
        """Loads the latest CSV file in the postcodes directory."""
        try:
            latest_csv = self._find_latest_csv(self._postcodes_path)
            logger.info(
                f"Found latest CSV file in directory {self._postcodes_path}: {latest_csv}"
            )
            return os.path.join(self._postcodes_path, latest_csv)
        except ValueError as e:
            logger.error(
                f"No valid CSV files found in directory {self._postcodes_path}: {e}"
            )
            raise ValueError(
                "No valid CSV files found in the postcodes directory. Please provide a valid zip file path."
            ) from e

    def _find_latest_csv(self, path: str) -> str:
        """Finds the latest CSV file in the postcodes directory."""
        logger.debug(f"Finding latest CSV file in {path}")
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        file = ONSPDFileName.find_latest(files)
        if file is None:
            raise ValueError(
                f"No valid CSV files found in the postcodes directory: {path}"
            )
        logger.info(f"Found latest CSV file: {file}.csv in {path}")
        return f"{file.name}.csv"

    def _load_postcodes(self, path: str) -> pd.DataFrame:
        """Loads postcodes from a CSV file."""
        logger.debug(f"Loading postcodes from {path}")
        try:
            postcodes = pd.read_csv(path)
            logger.info(f"Loaded postcodes from {path}")
            return postcodes
        except Exception as e:
            logger.error(f"An error occurred while loading postcodes from {path}: {e}")
            raise Exception(f"An error occurred while loading {path}: {e}")

    def _process_zip(self, zip_path: str) -> str:
        """Processes the zip file and updates the postcodes."""
        logger.info(f"Processing zip file: {zip_path}")
        return ONSPDDataZipFileProcessor.process(
            zip_path=zip_path,
            extracted_path=os.path.join(self._data_path, "extracted"),
            postcodes_path=self._postcodes_path,
        )
