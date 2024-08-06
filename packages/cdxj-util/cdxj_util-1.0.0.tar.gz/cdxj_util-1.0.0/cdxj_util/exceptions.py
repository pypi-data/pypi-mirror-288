class CDXJError(Exception):
    """Base exception for CDXJ utility errors."""

    pass


class CDXJLoadError(CDXJError):
    """Raised when there's an error loading the CDXJ file."""

    pass


class CDXJValidationError(CDXJError):
    """Raised when a CDXJ record fails validation."""

    pass


class CDXJParseError(CDXJError):
    """Raised when there's an error parsing a CDXJ record."""

    pass