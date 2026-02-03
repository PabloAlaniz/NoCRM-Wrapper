# src/services/base_service.py
from typing import Generic, TypeVar, List, Optional
from ..repositories.base_repository import BaseRepository

T = TypeVar('T')

class BaseService(Generic[T]):
    """
    Clase base para todos los servicios de lógica de negocio.
    
    Esta clase abstracta proporciona la estructura común para servicios que
    implementan lógica de negocio sobre repositorios de datos. Utiliza genéricos
    para mantener type safety mientras permite reutilización de código.
    
    Type Parameters:
        T: Tipo del modelo de dominio que maneja este servicio
    
    Attributes:
        repository: Repositorio de acceso a datos para el modelo T
    
    Example:
        >>> class LeadService(BaseService[Lead]):
        ...     def __init__(self, repository: LeadRepository):
        ...         super().__init__(repository)
        ...         # Lógica específica de leads
    """
    
    def __init__(self, repository: BaseRepository[T]):
        """
        Inicializa el servicio con un repositorio.
        
        Args:
            repository: Repositorio de acceso a datos del tipo T
        """
        self.repository = repository
