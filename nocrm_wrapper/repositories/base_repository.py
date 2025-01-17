from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict
import aiohttp
from ..config import NoCRMConfig
from ..exceptions import NoCRMAuthenticationError, NoCRMAPIError

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Repositorio base abstracto para operaciones CRUD"""

    def __init__(self, config: NoCRMConfig):
        self.config = config
        self.base_url = config.base_url
        self.headers = {
            "X-API-KEY": config.api_key,
            "Content-Type": "application/json"
        }

    async def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict] = None,
            params: Optional[Dict] = None
    ) -> Dict:
        """
        Realiza una petición HTTP a la API de NoCRM

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint de la API
            data: Datos para enviar en el body
            params: Parámetros de query string

        Returns:
            Dict con la respuesta de la API

        Raises:
            NoCRMAuthenticationError: Error de autenticación
            NoCRMAPIError: Error de la API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                        method=method,
                        url=url,
                        headers=self.headers,
                        json=data,
                        params=params,
                        timeout=self.config.timeout
                ) as response:
                    response_data = await response.json()

                    if response.status == 401:
                        raise NoCRMAuthenticationError("Invalid API key")

                    if not 200 <= response.status < 300:
                        raise NoCRMAPIError(
                            message=response_data.get('message', 'Unknown error'),
                            status_code=response.status
                        )

                    return response_data

            except aiohttp.ClientError as e:
                raise NoCRMAPIError(f"Connection error: {str(e)}")

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Crea una nueva entidad"""
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        """Obtiene una entidad por su ID"""
        pass

    @abstractmethod
    async def update(self, id: int, entity: T) -> T:
        """Actualiza una entidad existente"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Elimina una entidad"""
        pass

    @abstractmethod
    async def list(self, **filters) -> List[T]:
        """Lista todas las entidades con filtros opcionales"""
        pass