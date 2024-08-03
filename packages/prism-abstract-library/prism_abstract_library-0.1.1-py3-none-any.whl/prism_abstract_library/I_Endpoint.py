from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional
from fastapi import APIRouter, Depends, status


class IEndpoint(ABC):
    @abstractmethod
    def __init__(self, router: APIRouter):
        """Endpoint initialization."""
        pass

    @abstractmethod
    def setup_routes(self):
        """Abstract method to set up the routes for the endpoint"""
        pass

    def get(self, path: str, *args, **kwargs):
        """Shared method to handle GET requests"""
        pass

    def post(self, path: str, *args, **kwargs):
        """Shared method to handle POST requests"""
        pass

    def put(self, path: str, *args, **kwargs):
        """Shared method to handle PUT requests."""
        pass

    def delete(self, path: str, *args, **kwargs):
        """Shared method to handle DELETE requests."""
        pass

    @abstractmethod
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Abstract method to get an item."""
        pass

    @abstractmethod
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Abstract method to create an item."""
        pass

    @abstractmethod
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Abstract method to update an item."""
        pass

    @abstractmethod
    def delete_item(self, item_id: int):
        """Abstract method to delete an item."""
        pass
