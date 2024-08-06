from typing import Optional, Union, List, Dict
from .handlers.handler import ParsingHandler
from .handlers.regex import RegexParsingHandler
from .handlers.third_party_api import (
    OSDataHubNamesAPIParsingHandler,
    PostcodesIOAPIParsingHandler,
)

from .handlers.onspd_csv_file import ONSPDCSVFileParsingHandler
from .handlers.types import ParingHandlerType
from ..postcode import UKPostCode, SpecialUKPostCode
from ..result import Result


class UkPostcodeParser:
    """
    A class for parsing UK postcodes.

    Args:
        osdatahub_api_key (Optional[str]): API key for the OS Data Hub Names API.
        onspd_zip_file_path (Optional[str]): Path to the zipped ONSPD CSV file.

    Methods:
        parse(postcode: str, handler_type: str = ParingHandlerType.REGEX.value)
        -> Result[Union[UKPostCode, SpecialUKPostCode, None]]:
        Parse a single postcode using the specified handler.

        parse_batch(postcodes: List[str], handler_type: str = ParingHandlerType.REGEX.value)
        -> List[Result[Union[UKPostCode, SpecialUKPostCode, None]]]:
        Parse a batch of postcodes using the specified handler.
    """

    def __init__(
        self,
        osdatahub_api_key: Optional[str] = None,
        onspd_zip_file_path: Optional[str] = None,
    ):
        self._handlers: Dict[str, ParsingHandler] = {
            ParingHandlerType.REGEX.value: RegexParsingHandler(),
            ParingHandlerType.OSDATAHUB_API.value: OSDataHubNamesAPIParsingHandler(
                api_key=osdatahub_api_key
            ),
            ParingHandlerType.POSTCODESIO_API.value: PostcodesIOAPIParsingHandler(),
            ParingHandlerType.ONSPD_EXCEL_FILE.value: ONSPDCSVFileParsingHandler(
                path=onspd_zip_file_path
            ),
        }

    def parse(
        self, postcode: str, handler_type: str = ParingHandlerType.REGEX.value
    ) -> Result[Union[UKPostCode, SpecialUKPostCode, None]]:
        """
        Parse a single postcode using the specified handler.

        Args:
            postcode (str): Postcode to be parsed.
            handler_type (str): The type of handler to use for parsing. Default is 'regex'.
            Other options are 'osdatahub_api', 'postcodesio_api', 'onspd_excel_file'.

        Returns:
            Result[Union[UKPostCode, SpecialUKPostCode, None]]: The result of the parsing operation.
        """
        handler = self._get_handler(handler_type)
        return handler.parse(postcode)

    def parse_batch(
        self, postcodes: List[str], handler_type: str = ParingHandlerType.REGEX.value
    ) -> List[Result[Union[UKPostCode, SpecialUKPostCode, None]]]:
        """
        Parse a batch of postcodes using the specified handler.

        Args:
            postcodes (List[str]): A List of postcodes to be parsed.
            handler_type (str): The type of handler to use for parsing. Default is 'regex'.
            Other options are 'osdatahub_api', 'postcodesio_api', 'onspd_excel_file'.

        Returns:
            List[Result[Union[UKPostCode, SpecialUKPostCode, None]]]: A List of results for each parsed postcode.
        """
        return [self.parse(postcode, handler_type) for postcode in postcodes]

    def _get_handler(self, handler_type: str) -> ParsingHandler:
        """Get the handler for the specified type."""
        return self._handlers.get(
            handler_type, self._handlers[ParingHandlerType.REGEX.value]
        )
