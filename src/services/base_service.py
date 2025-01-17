# src/services/base_service.py
from typing import Generic, TypeVar, List, Optional
from ..repositories.base_repository import BaseRepository

T = TypeVar('T')

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository
