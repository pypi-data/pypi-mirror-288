from enum import Enum


class ParingHandlerType(str, Enum):
    """Types of parsing handlers."""

    REGEX = "regex"
    OSDATAHUB_API = "osdatahub_api"
    POSTCODESIO_API = "postcodesio_api"
    ONSPD_EXCEL_FILE = "onspd_excel_file"
