from dataclasses import dataclass, asdict
from typing import Optional, Dict
from datetime import datetime


@dataclass
class Lead:
    """
    Representa un lead en NoCRM
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
        """Crea una instancia de Lead desde un diccionario"""
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
        """Convierte la instancia a un diccionario"""
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