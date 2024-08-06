from typing import Union
from abc import ABC, abstractmethod
from ...result import Result
from ...postcode import UKPostCode, SpecialUKPostCode
from ...errors import PostCodeFormatError


class ParsingHandler(ABC):
    """
    Base class for postcode parsing handlers.

    Methods:
        parse(postcode: str) -> Result[Union[UKPostCode, SpecialUKPostCode]]:
        Handle the parsing of the provided postcode and return a Result object.
    """

    @abstractmethod
    def _parse(
        self, postcode: str
    ) -> Result[Union[UKPostCode, SpecialUKPostCode, None]]:
        """
        Handle the parsing of the provided postcode.

        Args:
            postcode (str): The normalized postcode to be parsed.

        Returns:
            Result[Union[UKPostCode, SpecialUKPostCode]]: The result of the parsing operation,
            which may contain a UKPostCode, a SpecialUKPostCode, or an error.
        """

    def parse(
        self, postcode: str
    ) -> Result[Union[UKPostCode, SpecialUKPostCode, None]]:
        """Handle the parsing of the provided postcode."""
        if not isinstance(postcode, str):
            return Result.failure(
                error=PostCodeFormatError(
                    message=f"Postcode must be a string. Received type: {type(postcode).__name__}.",
                    value=postcode,
                )
            )

        normalized = postcode.strip().upper()

        if not 4 <= len(normalized) <= 8:
            return Result.failure(
                error=PostCodeFormatError(
                    message="Postcode length must be between 4 and 8 characters.",
                    value=postcode,
                )
            )

        return self._parse(normalized)
