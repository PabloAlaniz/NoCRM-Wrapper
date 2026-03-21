"""Tests for NoCRMClient module."""
import pytest
from unittest.mock import Mock, patch
from nocrm_wrapper.nocrm_client import NoCRMClient
from nocrm_wrapper.config.config import NoCRMConfig
from nocrm_wrapper.services.lead_service import LeadService
from nocrm_wrapper.repositories.lead_repository import LeadRepository


class TestNoCRMClient:
    """Test cases for NoCRMClient class."""
    
    def test_init_with_valid_credentials(self):
        """Test NoCRMClient initialization with valid credentials."""
        client = NoCRMClient(api_key="test_key_123", subdomain="testcompany")
        
        # Test that config is created correctly
        assert isinstance(client.config, NoCRMConfig)
        assert client.config.api_key == "test_key_123"
        assert client.config.subdomain == "testcompany"
        assert client.config.base_url == "https://testcompany.nocrm.io/api/v2"
        
        # Test that repository is created
        assert isinstance(client.repository, LeadRepository)
        assert client.repository.config == client.config
        
        # Test that leads service is created
        assert isinstance(client.leads, LeadService)
        assert client.leads.repository == client.repository
    
    def test_init_with_empty_api_key(self):
        """Test NoCRMClient initialization with empty API key."""
        with pytest.raises(ValueError, match="API key is required"):
            NoCRMClient(api_key="", subdomain="testcompany")
    
    def test_init_with_empty_subdomain(self):
        """Test NoCRMClient initialization with empty subdomain."""
        with pytest.raises(ValueError, match="Subdomain is required"):
            NoCRMClient(api_key="test_key", subdomain="")
    
    def test_init_with_none_api_key(self):
        """Test NoCRMClient initialization with None API key."""
        with pytest.raises(ValueError, match="API key is required"):
            NoCRMClient(api_key=None, subdomain="testcompany")
    
    def test_init_with_none_subdomain(self):
        """Test NoCRMClient initialization with None subdomain."""
        with pytest.raises(ValueError, match="Subdomain is required"):
            NoCRMClient(api_key="test_key", subdomain=None)
    
    @patch('nocrm_wrapper.nocrm_client.NoCRMConfig')
    @patch('nocrm_wrapper.nocrm_client.LeadRepository')
    @patch('nocrm_wrapper.nocrm_client.LeadService')
    def test_init_creates_components_in_order(self, mock_lead_service, mock_lead_repo, mock_config):
        """Test that components are created in the correct order."""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        
        mock_repo_instance = Mock()
        mock_lead_repo.return_value = mock_repo_instance
        
        mock_service_instance = Mock()
        mock_lead_service.return_value = mock_service_instance
        
        client = NoCRMClient(api_key="test_key", subdomain="testcompany")
        
        # Verify creation order and parameters
        mock_config.assert_called_once_with(api_key="test_key", subdomain="testcompany")
        mock_lead_repo.assert_called_once_with(mock_config_instance)
        mock_lead_service.assert_called_once_with(mock_repo_instance)
        
        # Verify assignments
        assert client.config == mock_config_instance
        assert client.repository == mock_repo_instance
        assert client.leads == mock_service_instance
    
    def test_client_attributes_are_accessible(self):
        """Test that all client attributes are accessible."""
        client = NoCRMClient(api_key="test_key", subdomain="testcompany")
        
        # Test that all expected attributes exist
        assert hasattr(client, 'config')
        assert hasattr(client, 'repository')
        assert hasattr(client, 'leads')
        
        # Test that attributes are not None
        assert client.config is not None
        assert client.repository is not None
        assert client.leads is not None
    
    def test_multiple_client_instances_are_independent(self):
        """Test that multiple client instances are independent."""
        client1 = NoCRMClient(api_key="key1", subdomain="company1")
        client2 = NoCRMClient(api_key="key2", subdomain="company2")
        
        # Test that configs are different
        assert client1.config != client2.config
        assert client1.config.api_key != client2.config.api_key
        assert client1.config.subdomain != client2.config.subdomain
        
        # Test that repositories are different instances
        assert client1.repository != client2.repository
        assert client1.leads != client2.leads
    
    def test_config_attributes_are_correctly_passed(self):
        """Test that config attributes are correctly passed to components."""
        api_key = "special_test_key_456"
        subdomain = "my_test_company"
        
        client = NoCRMClient(api_key=api_key, subdomain=subdomain)
        
        # Test config has correct values
        assert client.config.api_key == api_key
        assert client.config.subdomain == subdomain
        
        # Test repository has the same config
        assert client.repository.config == client.config
        assert client.repository.config.api_key == api_key
        assert client.repository.config.subdomain == subdomain