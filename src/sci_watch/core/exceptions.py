class QuerySyntaxError(Exception):
    """
    Exception raised when queries are syntactically wrong
    """

    def __init__(self, message: str) -> None:
        """
        Parameters
        ----------
        message: str
            Error message
        """
        super().__init__(message)
