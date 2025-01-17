from typing import List, Optional, Dict
from ..models import Lead
from ..config import NoCRMConfig
from ..exceptions import NoCRMAPIError
from .base_repository import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    """Repositorio para operaciones CRUD de Leads en NoCRM"""

    def __init__(self, config: NoCRMConfig):
        super().__init__(config)
        self.endpoint = "leads"

    async def create(self, lead: Lead) -> Lead:
        """
        Crea un nuevo lead en NoCRM

        Args:
            lead: Instancia de Lead a crear

        Returns:
            Lead: Lead creado con ID y timestamps

        Raises:
            NoCRMAPIError: Si hay un error en la creación
        """
        data = lead.to_dict()
        response = await self._make_request("POST", self.endpoint, data=data)
        return Lead.from_dict(response)

    async def get(self, id: int) -> Optional[Lead]:
        """
        Obtiene un lead por su ID

        Args:
            id: ID del lead a obtener

        Returns:
            Optional[Lead]: Lead encontrado o None si no existe

        Raises:
            NoCRMAPIError: Si hay un error en la petición
        """
        try:
            response = await self._make_request("GET", f"{self.endpoint}/{id}")
            return Lead.from_dict(response)
        except NoCRMAPIError as e:
            if e.status_code == 404:
                return None
            raise

    async def update(self, id: int, lead: Lead) -> Lead:
        """
        Actualiza un lead existente

        Args:
            id: ID del lead a actualizar
            lead: Lead con los datos actualizados

        Returns:
            Lead: Lead actualizado

        Raises:
            NoCRMAPIError: Si hay un error en la actualización
        """
        data = lead.to_dict()
        # Removemos campos que no se pueden actualizar directamente
        fields_to_remove = ['status', 'step', 'client_folder']
        for field in fields_to_remove:
            data.pop(field, None)

        response = await self._make_request("PUT", f"{self.endpoint}/{id}", data=data)
        return Lead.from_dict(response)

    async def delete(self, id: int) -> bool:
        """
        Elimina un lead

        Args:
            id: ID del lead a eliminar

        Returns:
            bool: True si se eliminó correctamente

        Raises:
            NoCRMAPIError: Si hay un error en la eliminación
        """
        try:
            await self._make_request("DELETE", f"{self.endpoint}/{id}")
            return True
        except NoCRMAPIError as e:
            if e.status_code == 404:
                return False
            raise

    async def list(self, **filters) -> List[Lead]:
        """
        Lista todos los leads con filtros opcionales

        Args:
            **filters: Filtros para la búsqueda (status, page, per_page, etc.)

        Returns:
            List[Lead]: Lista de leads que coinciden con los filtros

        Raises:
            NoCRMAPIError: Si hay un error en la petición
        """
        response = await self._make_request("GET", self.endpoint, params=filters)
        return [Lead.from_dict(lead_data) for lead_data in response]

    async def list_pipelines(self) -> List[dict]:
        """
        Obtiene la lista de pipelines disponibles

        Returns:
            List[dict]: Lista de pipelines
        """
        response = await self._make_request("GET", "pipelines")
        return response

    async def list_steps(self) -> List[dict]:
        """
        Obtiene la lista de estados disponibles

        Returns:
            List[dict]: Lista de estados (steps) disponibles
        """
        response = await self._make_request("GET", "steps")
        return response

    async def assign_lead(self, id: int, user_id: int) -> Lead:
        """
        Asigna un lead a un usuario

        Args:
            id: ID del lead
            user_id: ID del usuario al que se asignará el lead

        Returns:
            Lead: Lead actualizado
        """
        response = await self._make_request(
            "POST",
            f"leads/{id}/assign",
            data={"user_id": user_id}
        )
        return Lead.from_dict(response)

    async def change_status(self, id: int, step_id_or_name: str) -> Lead:
        """
        Cambia el estado de un lead

        Args:
            id: ID del lead
            step_id_or_name: ID o nombre del nuevo estado (step)

        Returns:
            Lead: Lead actualizado
        """
        response = await self._make_request(
            "PUT",
            f"leads/{id}",
            data={"step": step_id_or_name}
        )
        return Lead.from_dict(response)