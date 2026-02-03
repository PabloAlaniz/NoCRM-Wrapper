from .config.config import NoCRMConfig
from .services.lead_service import LeadService
from .repositories.lead_repository import LeadRepository

class NoCRMClient:
    """
    Cliente principal para interactuar con la API de NoCRM.
    
    Este cliente proporciona acceso a todos los servicios de NoCRM a través de
    una interfaz unificada. Implementa una arquitectura N-tier con clara separación
    de responsabilidades entre repositorios (acceso a datos) y servicios (lógica de negocio).
    
    Attributes:
        config (NoCRMConfig): Configuración de conexión a la API de NoCRM
        repository (LeadRepository): Repositorio de acceso a datos de leads
        leads (LeadService): Servicio de lógica de negocio para leads
    
    Example:
        >>> client = NoCRMClient(api_key="tu_api_key", subdomain="tu_subdominio")
        >>> lead = await client.leads.get_lead(123)
        >>> new_lead = Lead(title="Nueva Oportunidad", status="new")
        >>> created = await client.leads.create_lead(new_lead)
    """
    
    def __init__(self, api_key: str, subdomain: str):
        """
        Inicializa el cliente de NoCRM con las credenciales proporcionadas.
        
        Args:
            api_key: API key de NoCRM (obtener desde configuración de cuenta)
            subdomain: Subdominio de tu cuenta de NoCRM (ej: "mi-empresa" para mi-empresa.nocrm.io)
        """
        self.config = NoCRMConfig(api_key=api_key, subdomain=subdomain)
        self.repository = LeadRepository(self.config)
        self.leads = LeadService(self.repository)