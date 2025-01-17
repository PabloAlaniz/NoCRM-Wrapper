class NoCRMException(Exception):
    """Base exception for NoCRM API wrapper"""
    pass

class NoCRMAuthenticationError(NoCRMException):
    """Raised when authentication fails"""
    pass

class NoCRMValidationError(NoCRMException):
    """Raised when input validation fails"""
    pass

class NoCRMAPIError(NoCRMException):
    """Raised when the API returns an error"""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code