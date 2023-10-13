"""Customize exceptions for API calling."""


class ParsingError(BaseException):
    """Error occur when parsing."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Error occur when parsing: {message}")


class APICallingError(BaseException):
    """Error occur when calling API."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Error occur when calling API: {message}")
