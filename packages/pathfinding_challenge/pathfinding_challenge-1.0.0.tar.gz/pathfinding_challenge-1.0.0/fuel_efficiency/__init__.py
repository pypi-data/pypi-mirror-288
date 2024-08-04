class InvalidComparisonError(TypeError):
    """Exception raised for invalid comparisons between objects."""

    def __init__(self, message: str):
        super().__init__(message)


class MissingAttrError(TypeError):
    """Exception raised when missing attributes."""

    def __init__(self, message: str):
        super().__init__(message)
