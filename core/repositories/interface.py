# core/repositories/interface.py

from typing import Protocol, List

from core.models.record import Record


class Repository(Protocol):
    """
    Repository contract for persistence operations.

    Defines the required behavior for repository
    implementations used throughout the application.

    Responsibilities:
    - Persist records
    - Retrieve stored records
    - Delete records

    Using a protocol-based interface allows:
    - Swappable storage implementations
    - Easier unit testing and mocking
    - Decoupling services from persistence details
    """

    def save(self, record: Record) -> str:
        """
        Persist a record to storage.

        Args:
            record: Record instance to store.

        Returns:
            str: Unique identifier of the saved record.
        """
        ...

    def get_all(self) -> List[dict]:
        """
        Retrieve all stored records.

        Returns:
            List[dict]: Raw persisted record data.
        """
        ...

    def delete(self, record_id: str) -> None:
        """
        Delete a record from storage.

        Args:
            record_id: Unique identifier of the record.
        """
        ...
