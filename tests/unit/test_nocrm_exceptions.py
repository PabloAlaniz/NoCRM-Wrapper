"""Tests for NoCRM exceptions module."""
import pytest
from nocrm_wrapper.exceptions.nocrm_exceptions import (
    NoCRMException,
    NoCRMAuthenticationError,
    NoCRMValidationError,
    NoCRMAPIError
)


class TestNoCRMExceptions:
    """Test cases for NoCRM exception classes."""
    
    def test_nocrm_exception_base(self):
        """Test NoCRMException base exception."""
        message = "Base error occurred"
        exception = NoCRMException(message)
        
        assert str(exception) == message
        assert isinstance(exception, Exception)
    
    def test_nocrm_authentication_error(self):
        """Test NoCRMAuthenticationError exception."""
        message = "Authentication failed"
        exception = NoCRMAuthenticationError(message)
        
        assert str(exception) == message
        assert isinstance(exception, NoCRMException)
        assert isinstance(exception, Exception)
    
    def test_nocrm_validation_error(self):
        """Test NoCRMValidationError exception."""
        message = "Validation failed"
        exception = NoCRMValidationError(message)
        
        assert str(exception) == message
        assert isinstance(exception, NoCRMException)
        assert isinstance(exception, Exception)
    
    def test_nocrm_api_error_with_message_only(self):
        """Test NoCRMAPIError with message only."""
        message = "API error occurred"
        exception = NoCRMAPIError(message)
        
        assert str(exception) == message
        assert exception.status_code is None
        assert isinstance(exception, NoCRMException)
        assert isinstance(exception, Exception)
    
    def test_nocrm_api_error_with_status_code(self):
        """Test NoCRMAPIError with message and status code."""
        message = "API error occurred"
        status_code = 500
        exception = NoCRMAPIError(message, status_code)
        
        assert str(exception) == message
        assert exception.status_code == status_code
        assert isinstance(exception, NoCRMException)
        assert isinstance(exception, Exception)
    
    def test_nocrm_api_error_zero_status_code(self):
        """Test NoCRMAPIError with zero status code."""
        message = "API error"
        status_code = 0
        exception = NoCRMAPIError(message, status_code)
        
        assert str(exception) == message
        assert exception.status_code == 0
    
    def test_nocrm_api_error_negative_status_code(self):
        """Test NoCRMAPIError with negative status code."""
        message = "API error"
        status_code = -1
        exception = NoCRMAPIError(message, status_code)
        
        assert str(exception) == message
        assert exception.status_code == -1
    
    def test_inheritance_chain(self):
        """Test that all exceptions inherit correctly."""
        auth_error = NoCRMAuthenticationError("auth error")
        validation_error = NoCRMValidationError("validation error")
        api_error = NoCRMAPIError("api error", 400)
        
        # Test inheritance chain
        assert issubclass(NoCRMAuthenticationError, NoCRMException)
        assert issubclass(NoCRMValidationError, NoCRMException)
        assert issubclass(NoCRMAPIError, NoCRMException)
        assert issubclass(NoCRMException, Exception)
        
        # Test isinstance
        assert isinstance(auth_error, NoCRMException)
        assert isinstance(validation_error, NoCRMException)
        assert isinstance(api_error, NoCRMException)
    
    def test_exception_raising_and_catching(self):
        """Test that exceptions can be raised and caught correctly."""
        # Test raising and catching specific exceptions
        with pytest.raises(NoCRMAuthenticationError):
            raise NoCRMAuthenticationError("Auth failed")
        
        with pytest.raises(NoCRMValidationError):
            raise NoCRMValidationError("Validation failed")
        
        with pytest.raises(NoCRMAPIError):
            raise NoCRMAPIError("API failed", 500)
        
        # Test catching as base exception
        with pytest.raises(NoCRMException):
            raise NoCRMAuthenticationError("This should be caught as NoCRMException")
    
    def test_exception_attributes_preservation(self):
        """Test that exception attributes are preserved when caught."""
        try:
            raise NoCRMAPIError("Test error", 404)
        except NoCRMAPIError as e:
            assert str(e) == "Test error"
            assert e.status_code == 404
        
        try:
            raise NoCRMAPIError("Test error without status")
        except NoCRMAPIError as e:
            assert str(e) == "Test error without status"
            assert e.status_code is None