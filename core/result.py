# core/result.py

class Result:
    """
    # Represents the outcome of an operation

    # success: whether operation succeeded
    # data: returned data (if success)
    # error: error message (if failure)
    """

    def __init__(self, success: bool, data=None, error: str = None):
        self.success = success
        self.data = data
        self.error = error
    
    @staticmethod
    def ok(data=None):
        return Result(True, data=data)
    
    @staticmethod
    def fail(error: str):
        return Result(False, error=error)