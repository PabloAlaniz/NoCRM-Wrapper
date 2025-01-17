from dataclasses import dataclass
from typing import Optional


@dataclass
class NoCRMConfig:
    """Configuración para el cliente NoCRM"""
    api_key: str
    subdomain: str
    base_url: Optional[str] = None
    timeout: int = 30

    def __post_init__(self):
        """Validación post inicialización y configuración de la URL base"""
        if not self.api_key:
            raise ValueError("API key is required")

        if not self.subdomain:
            raise ValueError("Subdomain is required")

        # Si no se proporciona una base_url, la construimos con el subdominio
        if not self.base_url:
            self.base_url = f"https://{self.subdomain}.nocrm.io/api/v2"
        elif not self.base_url.startswith(("http://", "https://")):
            raise ValueError("Invalid base URL format")