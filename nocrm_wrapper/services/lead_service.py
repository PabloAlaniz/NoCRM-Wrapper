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
        Crea un nuevo lead con validaciones de negocio.
        
        Valida que el lead cumpla con las reglas de negocio antes de crearlo:
        - Título mínimo 3 caracteres
        - Monto no negativo
        - Probabilidad entre 0-100%
        - Fecha de cierre no en el pasado
        
        Args:
            lead: Instancia de Lead a crear
        
        Returns:
            Lead: Lead creado con ID y timestamps asignados por el servidor
        
        Raises:
            NoCRMValidationError: Si el lead no pasa las validaciones de negocio
            NoCRMAPIError: Si hay un error en la comunicación con la API
        
        Example:
            >>> new_lead = Lead(title="Nueva Oportunidad", status="new", amount=10000.0)
            >>> created = await service.create_lead(new_lead)
            >>> print(created.id)  # ID asignado por NoCRM
        """
        self._validate_lead(lead)
        return await self.repository.create(lead)

    async def update_lead(self, id: int, lead: Lead) -> Lead:
        """
        Actualiza un lead existente con validaciones de negocio.
        
        Args:
            id: ID del lead a actualizar
            lead: Instancia de Lead con los datos actualizados
        
        Returns:
            Lead: Lead actualizado
        
        Raises:
            NoCRMValidationError: Si el lead no existe o no pasa validaciones
            NoCRMAPIError: Si hay un error en la comunicación con la API
        """
        self._validate_lead(lead)
        existing_lead = await self.repository.get(id)
        if not existing_lead:
            raise NoCRMValidationError(f"Lead with id {id} not found")
        return await self.repository.update(id, lead)

    async def process_lead(self, id: int, user_id: int, step_name: str) -> Lead:
        """
        Procesa un lead: asigna a un usuario y cambia su estado en una operación compuesta.
        
        Esta operación de alto nivel combina dos acciones:
        1. Asignar el lead a un usuario específico
        2. Mover el lead a un nuevo paso del pipeline
        
        Args:
            id: ID del lead a procesar
            user_id: ID del usuario al que se asignará el lead
            step_name: Nombre del paso (estado) al que mover el lead
        
        Returns:
            Lead: Lead actualizado con nueva asignación y estado
        
        Raises:
            NoCRMAPIError: Si hay un error en cualquiera de las dos operaciones
        
        Example:
            >>> processed = await service.process_lead(
            ...     id=123,
            ...     user_id=456,
            ...     step_name="Contactado"
            ... )
        """
        # Primero asignamos el lead
        assigned_lead = await self.repository.assign_lead(id, user_id)

        # Luego cambiamos su estado
        updated_lead = await self.repository.change_status(id, step_name)

        return updated_lead

    async def get_lead_pipeline_status(self, id: int) -> Dict:
        """
        Obtiene información completa del estado del lead en el pipeline.
        
        Recupera no solo el lead, sino también información contextual del pipeline:
        el paso actual, el pipeline al que pertenece, y todos los pasos disponibles.
        
        Args:
            id: ID del lead
        
        Returns:
            Dict con las siguientes claves:
                - lead: Instancia del Lead
                - current_step: Diccionario con información del paso actual
                - current_pipeline: Diccionario con información del pipeline actual
                - available_steps: Lista de todos los pasos disponibles
        
        Raises:
            NoCRMValidationError: Si el lead no existe
            NoCRMAPIError: Si hay un error en la comunicación con la API
        
        Example:
            >>> status = await service.get_lead_pipeline_status(123)
            >>> print(f"Pipeline: {status['current_pipeline']['name']}")
            >>> print(f"Paso: {status['current_step']['name']}")
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
        Búsqueda avanzada de leads con múltiples criterios opcionales.
        
        Permite combinar varios filtros para encontrar leads específicos.
        Todos los parámetros son opcionales y se pueden combinar libremente.
        
        Args:
            status: Filtrar por estado específico
            min_amount: Monto mínimo (inclusive)
            max_amount: Monto máximo (inclusive)
            date_from: Fecha de inicio para filtrar por creación
            date_to: Fecha de fin para filtrar por creación
        
        Returns:
            List[Lead]: Lista de leads que cumplen con todos los criterios
        
        Raises:
            NoCRMAPIError: Si hay un error en la comunicación con la API
        
        Example:
            >>> # Leads nuevos con monto entre 5k y 20k del último mes
            >>> leads = await service.search_leads(
            ...     status="new",
            ...     min_amount=5000,
            ...     max_amount=20000,
            ...     date_from=datetime.now() - timedelta(days=30)
            ... )
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
        Validaciones de negocio para leads.
        
        Aplica reglas de negocio:
        - Título requerido (mínimo 3 caracteres)
        - Monto no negativo
        - Probabilidad entre 0-100%
        - Fecha de cierre no puede estar en el pasado
        
        Args:
            lead: Lead a validar
        
        Raises:
            NoCRMValidationError: Si alguna validación falla
        """
        if not lead.title or len(lead.title.strip()) < 3:
            raise NoCRMValidationError("Lead title is required and must be at least 3 characters")

        if lead.amount is not None and lead.amount < 0:
            raise NoCRMValidationError("Lead amount cannot be negative")

        if lead.probability is not None and not 0 <= lead.probability <= 100:
            raise NoCRMValidationError("Lead probability must be between 0 and 100")

        if lead.expected_closing_date and lead.expected_closing_date < datetime.now():
            raise NoCRMValidationError("Expected closing date cannot be in the past")

    async def list(self):
        """
        Lista todos los leads disponibles.
        Returns:
            List[Lead]: Lista de leads encontrados
        """
        return await self.repository.list()