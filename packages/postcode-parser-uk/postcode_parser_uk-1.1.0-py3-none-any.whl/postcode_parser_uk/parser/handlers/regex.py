import re
from typing import Union

from .handler import ParsingHandler
from ...result import Result
from ...postcode import UKPostCode, SpecialUKPostCode
from ...errors import PostCodeFormatError


class RegexParsingHandler(ParsingHandler):
    """
    A class for parsing UK postcodes using regular expressions.

    Methods:
        parse(postcode: str) -> Result[Union[UKPostCode, SpecialUKPostCode]]:
        Parse a UK postcode using regular expressions.
    """

    def __init__(self) -> None:
        self._bs7666_patterns = [
            r"^(?P<area>[A-Z]{1,2})(?P<district>[0-9R][0-9A-Z]?) ?(?P<sector>[0-9])(?P<unit>[ABDEFGHJLNPQRSTUWXYZ]{2})$",
            r"^BFPO ?(?P<bfpo>[0-9]{1,4})$",
            r"^(?P<area>[AC-FHKNPRTV-Y]\d{2}|D6W)? ?(?P<unit>[0-9AC-FHKNPRTV-Y]{4})$",
        ]
        self._edge_case_patterns = {
            "british_overseas_territories": r"^(?P<special>(ASCN ?1ZZ|BBND ?1ZZ|BIQQ ?1ZZ|FIQQ ?1ZZ|GX11 ?1AA|PCRN ?1ZZ|SIQQ ?1ZZ|STHL ?1ZZ|TDCU ?1ZZ|TKCA ?1ZZ))$",  # noqa: E501
            "anguilla": r"^(?P<special>AI-2640)$",
            "cayman_islands": r"^(?P<special>KY[0-9]-[0-9]{4})$",
            "montserrat": r"^(?P<special>MSR-[0-9]{4})$",
            "british_virgin_islands": r"^(?P<special>VG-[0-9]{4})$",
            "bermuda": r"^(?P<special>[A-Z]{2} ?[0-9]{2}|[A-Z]{2} ?[A-Z]{2})$",
            "bfpo": r"^(?P<special>BFPO ?[0-9]{1,4})$",
            "bf": r"^(?P<special>BF1 ?[0-9]{1,4})$",
            "non_geographic": r"^(?P<special>(GIR ?0AA|XM4 ?5HQ|BX[0-9]{1,2} ?[0-9A-Z]{2}))$",
            "bulk_mail": r"^(?P<special>(BS98|BT58|EC50|IM99|JE4|M60|N1P|NE99|SA99|SW9|WV98) ?[0-9A-Z]{2})$",
        }

    def _parse(
        self, postcode: str
    ) -> Result[Union[UKPostCode, SpecialUKPostCode, None]]:
        """Parse a UK postcode using regular expressions."""

        for key, pattern in self._edge_case_patterns.items():
            if re.match(pattern, postcode):
                return self._handle_edge_case(postcode, key)

        for pattern in self._bs7666_patterns:
            if match := re.match(pattern, postcode):
                return self._handle_standard_case(match)

        return Result.failure(error=PostCodeFormatError(value=postcode))

    def _handle_standard_case(self, match: re.Match) -> Result[UKPostCode]:
        """Handle a standard case postcode."""
        return Result.success(
            value=UKPostCode(
                area=match.group("area"),
                district=match.group("district"),
                sector=match.group("sector"),
                unit=match.group("unit"),
            ),
        )

    def _handle_edge_case(
        self, postcode: str, special_case: str
    ) -> Result[SpecialUKPostCode]:
        """Handle a special case postcode."""
        return Result.success(
            value=SpecialUKPostCode(special_case=special_case, postcode=postcode)
        )
