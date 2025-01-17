# src/services/lead_service.py
from typing import List, Optional, Dict
from datetime import datetime
from ..models.lead import Lead
from ..repositories.lead_repository import LeadRepository
from ..exceptions.nocrm_exceptions import NoCRMValidationError
from .base_service import BaseService


class LeadService(BaseService[Lead]):
    def __init__(self, repository: LeadRepository):
        super().__init__(repository)
        self.repository: LeadRepository = repository

    async def create_lead(self, lead: Lead) -> Lead:
        """
        Crea un nuevo lead con validaciones de negocio
        """
        self._validate_lead(lead)
        return await self.repository.create(lead)

    async def update_lead(self, id: int, lead: Lead) -> Lead:
        """
        Actualiza un lead existente con validaciones
        """
        self._validate_lead(lead)
        existing_lead = await self.repository.get(id)
        if not existing_lead:
            raise NoCRMValidationError(f"Lead with id {id} not found")
        return await self.repository.update(id, lead)

    async def process_lead(self, id: int, user_id: int, step_name: str) -> Lead:
        """
        Procesa un lead: asigna y cambia estado en una sola operación
        """
        # Primero asignamos el lead
        assigned_lead = await self.repository.assign_lead(id, user_id)

        # Luego cambiamos su estado
        updated_lead = await self.repository.change_status(id, step_name)

        return updated_lead

    async def get_lead_pipeline_status(self, id: int) -> Dict:
        """
        Obtiene información completa del estado del lead en el pipeline
        """
        lead = await self.repository.get(id)
        if not lead:
            raise NoCRMValidationError(f"Lead with id {id} not found")

        pipelines = await self.repository.list_pipelines()
        steps = await self.repository.list_steps()

        current_step = next((step for step in steps if step['name'] == lead.status), None)
        current_pipeline = next((p for p in pipelines if p['id'] == current_step['pipeline_id']),
                                None) if current_step else None

        return {
            'lead': lead,
            'current_step': current_step,
            'current_pipeline': current_pipeline,
            'available_steps': steps
        }

    async def search_leads(self,
                           status: Optional[str] = None,
                           min_amount: Optional[float] = None,
                           max_amount: Optional[float] = None,
                           date_from: Optional[datetime] = None,
                           date_to: Optional[datetime] = None) -> List[Lead]:
        """
        Búsqueda avanzada de leads con múltiples criterios
        """
        # Construir filtros
        filters = {}
        if status:
            filters['status'] = status
        if min_amount is not None:
            filters['min_amount'] = min_amount
        if max_amount is not None:
            filters['max_amount'] = max_amount
        if date_from:
            filters['date_from'] = date_from.isoformat()
        if date_to:
            filters['date_to'] = date_to.isoformat()

        return await self.repository.list(**filters)

    def _validate_lead(self, lead: Lead) -> None:
        """
        Validaciones de negocio para leads
        """
        if not lead.title or len(lead.title.strip()) < 3:
            raise NoCRMValidationError("Lead title is required and must be at least 3 characters")

        if lead.amount is not None and lead.amount < 0:
            raise NoCRMValidationError("Lead amount cannot be negative")

        if lead.probability is not None and not 0 <= lead.probability <= 100:
            raise NoCRMValidationError("Lead probability must be between 0 and 100")

        if lead.expected_closing_date and lead.expected_closing_date < datetime.now():
            raise NoCRMValidationError("Expected closing date cannot be in the past")