from typing import Optional


class PostCodeFormatError(Exception):
    """Error for invalid postcode format."""

    def __init__(
        self,
        message: Optional[str] = "Invalid postcode format.",
        code: Optional[str] = "INVALID_POSTCODE_FORMAT",
        value: Optional[str] = "Unknown value",
    ):
        self.message = message
        self.code = code
        self.value = value
        super().__init__(self.message)


class APIKeyNotFoundError(Exception):
    """Error for missing or invalid API key."""

    def __init__(
        self,
        message: Optional[str] = "API key not found.",
        code: Optional[str] = "API_KEY_ERROR",
    ):
        super().__init__(message, code)


class InvalidApiKeyError(Exception):
    """Error for invalid API key."""

    def __init__(
        self,
        message: Optional[
            str
        ] = "Access to the API is forbidden. Please check your API key.",
        code: Optional[str] = "INVALID_API_KEY",
    ):
        self.message = message
        self.code = code
        super().__init__(self.message)


class UnexpectedResponseStructureError(Exception):
    """Error for failed API response parsing."""

    def __init__(
        self,
        message: Optional[str] = "Failed to parse the response.",
        code: Optional[str] = "PARSE_ERROR",
    ):
        super().__init__(message, code)


class PostcodeNotFoundError(Exception):
    """Error for no results found in API response."""

    def __init__(
        self,
        message: Optional[str] = "No matching results found.",
        code: Optional[str] = "NO_RESULTS_FOUND",
    ):
        super().__init__(message, code)
