# core/result.py

class Result:
    """
    Standardized operation result wrapper.

    Encapsulates the outcome of service and application
    operations in a consistent structure.

    Attributes:
        success: Indicates whether the operation succeeded.
        data: Optional returned data for successful operations.
        error: Optional error message for failed operations.
    """

    def __init__(
        self,
        success: bool,
        data=None,
        error: str = None
    ):
        self.success = success
        self.data = data
        self.error = error

    @staticmethod
    def ok(data=None):
        """
        Create a successful result instance.
        """
        return Result(True, data=data)

    @staticmethod
    def fail(error: str):
        """
        Create a failed result instance.
        """
        return Result(False, error=error)