import os
from abc import abstractmethod
from typing import Optional

import requests
from dotenv import load_dotenv

from .handler import ParsingHandler
from .regex import RegexParsingHandler
from ...result import Result
from ...postcode import UKPostCode
from ...errors import (
    UnexpectedResponseStructureError,
    PostcodeNotFoundError,
    APIKeyNotFoundError,
    InvalidApiKeyError,
)
from ...logging import get_logger


logger = get_logger()


class ThirdPartyAPIParsingHandler(ParsingHandler):
    """
    Base class for postcode parsers using an API.

    Args:
        endpoint (str): The API endpoint URL.
        timeout (int): The timeout for the API request.

    Methods:
        parse(postcode: str) -> Result[Union[UKPostCode, SpecialUKPostCode]]:
        Handle the parsing of the provided postcode and return a Result object.
    """

    def __init__(self, endpoint: str, timeout: int = 5) -> None:
        self._endpoint = endpoint
        self._timeout = timeout

    def _parse(self, postcode: str) -> Result[Optional[UKPostCode]]:
        """Handle the postcode."""
        try:
            request = self._create_request(postcode)
            response = self._send_request(request)
            parsed_postcode = self._parse_response(response.json())
            return RegexParsingHandler()._parse(parsed_postcode)
        except Exception as e:
            return Result.failure(error=e)

    def _send_request(self, request: dict) -> requests.Response:
        """Send the API request."""
        response = requests.get(
            request["url"],
            params=request.get("params", {}),
            headers=request.get("headers", {}),
            timeout=self._timeout,
        )
        if response.status_code == 401:
            raise InvalidApiKeyError()
        if response.status_code == 404:
            raise PostcodeNotFoundError()
        response.raise_for_status()
        return response

    @abstractmethod
    def _create_request(self, postcode: str) -> dict:
        """Create the request for the API."""

    @abstractmethod
    def _parse_response(self, data: dict) -> str:
        """Extract postcode from the API response."""


class OSDataHubNamesAPIParsingHandler(ThirdPartyAPIParsingHandler):
    """
    A handler for interacting with the OS Data Hub Names API.
    Uses the endpoint https://api.os.uk/search/names/v1/find.

    Args:
        timeout (int): The timeout for the API request.
        api_key (str): The API key for the OS Data Hub API

    Methods:
        parse(postcode: str) -> Result[Union[UKPostCode, SpecialUKPostCode]]:
        Handle the parsing of the provided postcode and return a Result object.
    """

    def __init__(self, timeout: int = 5, api_key: str = None):
        self._api_key = api_key
        logger.warning(
            (
                "OSDataHubNamesAPIParsingHandler -> OS Data Hub API key was not provided in the constructor. "
                "Will try to load from the environment variable OSDATAHUB_API_KEY."
            )
        )
        super().__init__("https://api.os.uk/search/names/v1/find", timeout)

    @property
    def api_key(self) -> str:
        """Lazy load the API key if not already provided."""
        if self._api_key is None:
            self._api_key = self._load_key_from_env()
        return self._api_key

    def _create_request(self, postcode: str) -> dict:
        """Create the request for the OS Data Hub API."""
        return {
            "url": self._endpoint,
            "params": {
                "key": self.api_key,
                "query": postcode,
            },
        }

    def _send_request(self, request: dict) -> requests.Response:
        """Send the API request."""
        try:
            return super()._send_request(request)
        except InvalidApiKeyError:
            raise InvalidApiKeyError(
                message="Access to the OS Data Hub Names API is forbidden. Please check your API key."
            )

    def _parse_response(self, data: dict) -> str:
        """Extract the postcode from the API response."""
        try:
            results = data["results"]
            return results[0]["GAZETTEER_ENTRY"]["NAME1"]
        except KeyError:
            raise PostcodeNotFoundError(
                message=("No matching results found from OS Data Hub Names API.")
            )

    def _load_key_from_env(self) -> str:
        """Load the API key from the environment or raise an error if not found."""
        load_dotenv()
        key = os.getenv("OSDATAHUB_API_KEY")
        if not key:
            raise APIKeyNotFoundError(
                message=(
                    "OS Data Hub API key not found. "
                    "Please provide one through the constructor or set "
                    "the OSDATAHUB_API_KEY environment variable."
                )
            )
        return key


class PostcodesIOAPIParsingHandler(ThirdPartyAPIParsingHandler):
    """
    A handler for interacting with the Postcodes.io API.
    Uses the endpoint https://api.postcodes.io/postcodes.

    Args:
        timeout (int): The timeout for the API request.

    Methods:
        parse(postcode: str) -> Result[Union[UKPostCode, SpecialUKPostCode]]:
        Handle the parsing of the provided postcode and return a Result object.

    """

    def __init__(self, timeout: int = 5):
        super().__init__("https://api.postcodes.io/postcodes", timeout)

    def _create_request(self, postcode: str) -> dict:
        """Create the request for the Postcodes.io API."""
        return {"url": f"{self._endpoint}/{postcode}"}

    def _parse_response(self, data: dict) -> str:
        """Extract the postcode from the API response."""
        try:
            result = data["result"]
            if not result:
                raise PostcodeNotFoundError(message="No matching results found")
            return result["postcode"]
        except KeyError as e:
            raise UnexpectedResponseStructureError(
                message=f"Invalid response structure: {e}"
            )
