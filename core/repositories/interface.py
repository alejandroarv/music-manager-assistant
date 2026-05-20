# core/repositories/interface.py

from typing import Protocol, List
from core.models.record import Record

class Repository(Protocol):
    """
    # Repository Interface (using Python Protocol)

    # Purpose
    # - define a contract for repository behaviour
    # - ensure all repository implementations provide the same methods
    # - decouple services from concrete implementations

    # This allows
    # - swapping storage implementations (JSON -> DB -> API)
    # - easier testing (mock repositories)
    """
    def save(self, record: Record) -> str:
        """
        # Save a record to storage
`                           
        # Args
        # - record (Record): The record to persist'

        # Returns
        # - str: The ID of the saved record
        """
        ...

    def get_all(self) -> List[dict]:
        """
        # Retrieve all records from storage

        # Returns
        # - List[dict]: Raw stored records
        """
        ...

    def delete(self, record_id:str) -> None:
        """
        # Delete a record by its ID

        # Args
        # - record_id (str): Unique identifier of the record
        """
        ...
        

    
