from .config.config import NoCRMConfig
from .services.lead_service import LeadService
from .repositories.lead_repository import LeadRepository

class NoCRMClient:
    def __init__(self, api_key: str, subdomain: str):
        self.config = NoCRMConfig(api_key=api_key, subdomain=subdomain)
        self.repository = LeadRepository(self.config)
        self.leads = LeadService(self.repository)