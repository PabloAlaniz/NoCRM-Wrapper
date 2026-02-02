from dataclasses import dataclass, asdict
from typing import Optional, Dict
from datetime import datetime


@dataclass
class Lead:
    """
    Representa un lead (oportunidad de venta) en NoCRM.
    
    Esta clase encapsula toda la información de un lead, incluyendo datos básicos
    de contacto, estado en el pipeline de ventas, y metadatos de seguimiento.
    
    Attributes:
        title: Título descriptivo del lead (requerido, mínimo 3 caracteres)
        status: Estado actual del lead en el pipeline
        contact_name: Nombre del contacto asociado al lead
        description: Descripción detallada del lead o notas adicionales
        amount: Monto estimado de la oportunidad (debe ser >= 0)
        probability: Probabilidad de cierre (0-100%)
        expected_closing_date: Fecha estimada de cierre
        custom_fields: Campos personalizados adicionales definidos en NoCRM
        id: ID único del lead en NoCRM (asignado por el sistema)
        created_at: Fecha/hora de creación del lead
        updated_at: Fecha/hora de última actualización
    
    Example:
        >>> lead = Lead(
        ...     title="Implementación CRM",
        ...     status="new",
        ...     contact_name="Juan Pérez",
        ...     amount=50000.0,
        ...     probability=75
        ... )
    """
    title: str
    status: str
    contact_name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    probability: Optional[int] = None
    expected_closing_date: Optional[datetime] = None
    custom_fields: Optional[Dict] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Lead':
        """
        Crea una instancia de Lead desde un diccionario (deserialización).
        
        Convierte automáticamente strings de fechas ISO a objetos datetime.
        Filtra campos que no estén definidos en el modelo.
        
        Args:
            data: Diccionario con datos del lead (típicamente de respuesta API)
        
        Returns:
            Lead: Instancia de Lead con los datos deserializados
        
        Example:
            >>> data = {"title": "Nuevo Lead", "status": "new", "amount": 1000.0}
            >>> lead = Lead.from_dict(data)
        """
        # Convertir fechas si existen
        if 'expected_closing_date' in data and data['expected_closing_date']:
            data['expected_closing_date'] = datetime.fromisoformat(data['expected_closing_date'].replace('Z', '+00:00'))
        if 'created_at' in data and data['created_at']:
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))

        # Filtrar campos no definidos en el modelo
        valid_fields = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        return cls(**filtered_data)

    def to_dict(self) -> Dict:
        """
        Convierte la instancia a un diccionario (serialización).
        
        Convierte objetos datetime a formato ISO. Excluye campos None y
        campos de solo lectura (id, created_at, updated_at) para operaciones
        de creación/actualización.
        
        Returns:
            Dict: Diccionario con los datos del lead listo para enviar a la API
        
        Example:
            >>> lead = Lead(title="Test", status="new")
            >>> data = lead.to_dict()
            >>> # data será {'title': 'Test', 'status': 'new'}
        """
        data = asdict(self)

        # Convertir fechas a ISO format
        if self.expected_closing_date:
            data['expected_closing_date'] = self.expected_closing_date.isoformat()
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            data['updated_at'] = self.updated_at.isoformat()

        # Remover campos None y campos internos
        return {k: v for k, v in data.items()
                if v is not None and k not in ['id', 'created_at', 'updated_at']}