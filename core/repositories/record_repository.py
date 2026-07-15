# core/repositories/record_repository.py

import logging
import uuid
from datetime import datetime, UTC

from core.models.record import Record


# Module-level logger for repository operations
logger = logging.getLogger(__name__)


class RecordRepository:
    """
    Concrete repository implementation for record persistence.

    Acts as the intermediary between the service layer
    and the underlying storage system.

    Responsibilities:
    - Persist records
    - Generate system-managed fields
    - Retrieve and filter records
    - Handle deletion operations
    - Coordinate storage interactions
    """

    def __init__(self, storage):
        """
        Initialize the repository with a storage backend.

        Args:
            storage: Low-level persistence implementation.
        """
        self.storage = storage

    def save(self, record: Record):
        """
        Persist a record and attach system-generated metadata.

        Responsibilities:
        - Generate unique identifiers
        - Attach timestamps
        - Convert records into serializable structures
        - Persist data through the storage layer

        Args:
            record: Record instance to persist.

        Returns:
            dict: The persisted record including generated metadata.
        """

        # Load existing persisted records
        data = self.storage.load_all()

        # Support both dataclass models and standard objects
        record_dict = (
            record.to_dict()
            if hasattr(record, "to_dict")
            else record.__dict__.copy()
        )

        # Attach system-generated metadata
        record_dict["id"] = str(uuid.uuid4())
        record_dict["timestamp"] = datetime.now(
            UTC
        ).isoformat()

        # Append the new record to the dataset
        data.append(record_dict)

        # Persist updated dataset
        self.storage.save_all(data)

        # Log persistence operation
        logger.info(
            "Saved record: %s (%s)",
            record_dict.get("type", "unknown"),
            record_dict["id"],
        )

        return record_dict

    def update(
        self,
        record: Record,
    ):
        """
        Update an existing persisted record.

        Args:
            record:
                Updated record instance.
        """

        data = self.storage.load_all()

        record_dict = (
            record.to_dict()
            if hasattr(record, "to_dict")
            else record.__dict__.copy()
        )

        for index, existing in enumerate(data):

            if existing["id"] == record.id:

                record_dict["timestamp"] = (
                    existing["timestamp"]
                )

                data[index] = record_dict

                self.storage.save_all(
                    data
                )

                logger.info(
                    "Updated record: %s",
                    record.id,
                )

                return record_dict

        raise ValueError(
            "Record not found."
        )
    
    def get_all(self):
        """
        Retrieve all persisted records.

        Returns:
            list: All stored records.
        """
        return self.storage.load_all()

    def get_by_type(self, record_type: str):
        """
        Retrieve records filtered by type.

        Args:
            record_type: Record category to filter by.

        Returns:
            list: Matching records.
        """
        return [
            record
            for record in self.storage.load_all()
            if record.get("type", "").lower()
            == record_type.lower()
        ]

    def delete(self, record_id: str):
        """
        Delete a persisted record by its identifier.

        Args:
            record_id: Unique record identifier.
        """

        data = self.storage.load_all()

        # Remove records matching the target ID
        updated_data = [
            record
            for record in data
            if record.get("id") != record_id
        ]

        # Persist updated dataset
        self.storage.save_all(updated_data)

        # Log deletion operation
        logger.info(
            "Deleted record: %s",
            record_id,
        )
