from dataclasses import dataclass


@dataclass
class UKPostCode:
    """
    Represents a UK postcode.

    Attributes:
        area (str): The area part of the postcode.
        district (str): The district part of the postcode.
        sector (str): The sector part of the postcode.
        unit (str): The unit part of the postcode.

    Properties:
        postcode (str): The full postcode in the format 'area district sector unit'.
        outward_code (str): The outward code in the format 'area district'.
        inward_code (str): The inward code in the format 'sector unit'.
    """

    area: str
    district: str
    sector: str
    unit: str

    @property
    def postcode(self) -> str:
        """Return the full postcode in the format 'area district sector unit'."""
        return f"{self.area}{self.district} {self.sector}{self.unit}"

    @property
    def outward_code(self) -> str:
        """Return the outward code in the format 'area district'."""
        return f"{self.area}{self.district}"

    @property
    def inward_code(self) -> str:
        """Return the inward code in the format 'sector unit'."""
        return f"{self.sector}{self.unit}"


@dataclass
class SpecialUKPostCode:
    """
    Represents a special UK postcode to handle special cases.

    Attributes:
        special_case (str): A description of the special case.
        postcode (str): The postcode associated with the special case.
    """

    special_case: str
    postcode: str
