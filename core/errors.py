# core/errors.py

class ValidationError(Exception):
    """
    Raised when user-provided input fails validation.
    
    These errors are intended to be safely displayed
    to the user interface.
    """
    pass