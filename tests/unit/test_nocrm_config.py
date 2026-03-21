"""Tests for NoCRMConfig module."""
import pytest
from nocrm_wrapper.config.config import NoCRMConfig


class TestNoCRMConfig:
    """Test cases for NoCRMConfig class."""
    
    def test_init_with_required_params(self):
        """Test NoCRMConfig initialization with required parameters."""
        config = NoCRMConfig(api_key="test_key_123", subdomain="testcompany")
        
        assert config.api_key == "test_key_123"
        assert config.subdomain == "testcompany"
        assert config.base_url == "https://testcompany.nocrm.io/api/v2"
        assert config.timeout == 30
    
    def test_init_with_custom_base_url(self):
        """Test NoCRMConfig initialization with custom base URL."""
        config = NoCRMConfig(
            api_key="test_key", 
            subdomain="testcompany",
            base_url="https://custom.api.com"
        )
        
        assert config.base_url == "https://custom.api.com"
    
    def test_init_with_custom_timeout(self):
        """Test NoCRMConfig initialization with custom timeout."""
        config = NoCRMConfig(
            api_key="test_key", 
            subdomain="testcompany",
            timeout=60
        )
        
        assert config.timeout == 60
    
    def test_init_missing_api_key(self):
        """Test NoCRMConfig initialization without API key."""
        with pytest.raises(ValueError, match="API key is required"):
            NoCRMConfig(api_key="", subdomain="testcompany")
    
    def test_init_missing_subdomain(self):
        """Test NoCRMConfig initialization without subdomain."""
        with pytest.raises(ValueError, match="Subdomain is required"):
            NoCRMConfig(api_key="test_key", subdomain="")
    
    def test_init_none_api_key(self):
        """Test NoCRMConfig initialization with None API key."""
        with pytest.raises(ValueError, match="API key is required"):
            NoCRMConfig(api_key=None, subdomain="testcompany")
    
    def test_init_none_subdomain(self):
        """Test NoCRMConfig initialization with None subdomain."""
        with pytest.raises(ValueError, match="Subdomain is required"):
            NoCRMConfig(api_key="test_key", subdomain=None)
    
    def test_init_invalid_base_url_format(self):
        """Test NoCRMConfig initialization with invalid base URL format."""
        with pytest.raises(ValueError, match="Invalid base URL format"):
            NoCRMConfig(
                api_key="test_key", 
                subdomain="testcompany",
                base_url="invalid-url"
            )
    
    def test_auto_build_base_url_with_subdomain(self):
        """Test that base_url is automatically built from subdomain."""
        config = NoCRMConfig(api_key="test_key", subdomain="mycompany")
        
        assert config.base_url == "https://mycompany.nocrm.io/api/v2"
    
    def test_valid_http_base_url(self):
        """Test that HTTP URLs are accepted."""
        config = NoCRMConfig(
            api_key="test_key", 
            subdomain="testcompany",
            base_url="http://local.api.com"
        )
        
        assert config.base_url == "http://local.api.com"
    
    def test_valid_https_base_url(self):
        """Test that HTTPS URLs are accepted."""
        config = NoCRMConfig(
            api_key="test_key", 
            subdomain="testcompany",
            base_url="https://secure.api.com"
        )
        
        assert config.base_url == "https://secure.api.com"
    
    def test_dataclass_equality(self):
        """Test that dataclass equality works correctly."""
        config1 = NoCRMConfig(api_key="test_key", subdomain="testcompany")
        config2 = NoCRMConfig(api_key="test_key", subdomain="testcompany")
        config3 = NoCRMConfig(api_key="different_key", subdomain="testcompany")
        
        assert config1 == config2
        assert config1 != config3
    
    def test_dataclass_repr(self):
        """Test that dataclass repr works correctly."""
        config = NoCRMConfig(api_key="test_key", subdomain="testcompany")
        
        repr_str = repr(config)
        
        assert "NoCRMConfig" in repr_str
        assert "test_key" in repr_str
        assert "testcompany" in repr_str