# core/repositories/record_repository.py

import logging
import uuid
from datetime import datetime, UTC
from core.models.record import Record

# Logger specific to this module
logger = logging.getLogger(__name__)

class RecordRepository:
    """
    # Concrete implementation of the Repository

    # Responsibilities
    # - Interact with the storage layer
    # - Add system-level fields (id, timestamp)
    # - Provide query methods (get_all, get_by_type)
    # - Manage persistence operations (save, delete)

    # This is the bridge between:
    # - Service Layer <-> Storage Layer
    """
    def __init__(self, storage):
        # Inject storage dependency (JSON file handler)
        self.storage = storage

    def save(self, record: Record):
        """
        # Save a record to storage

        # Steps
        # 1. Load existing data
        # 2. Convert record to dict (if needed)
        # 3. Add system fields (id, timestamp)
        # 4. Append to data list
        # 5. Persist back to storage
        """
        # Load all existing records
        data = self.storage.load_all()

        # Convert record object to dictionary
        # Supports both dataclass (to_dict) and fallback (__dict__)
        record_dict = (
            record.to_dict()
            if hasattr(record, "to_dict")
            else record.__dict__.copy()
        )

        # Generate unique ID for the record
        record_dict["id"] = str(uuid.uuid4())

        # Add timestamp (UTC ISO format)
        record_dict["timestamp"] = datetime.now(UTC).isoformat()

        # Add new record to dataset
        data.append(record_dict)

        # Persist updated dataset
        self.storage.save_all(data)

        # Log operation
        logger.info(
            f"Saved record: {record_dict.get('type', 'unknown')} ({record_dict['id']})"
        )

        # Return saved record (Including id and timestamp)
        return record_dict

    def get_all(self):
        """
        # Retrieve all records from storage
        """
        return self.storage.load_all()

    def get_by_type(self, record_type: str):
        """
        # Filter records by type

        # Example:
        # - "booking"
        # - "contract"

        # Returns only matching records
        """
        return [
            record for record in self.storage.load_all()
            if record.get("type", "").lower() == record_type.lower()
        ]
    
    def delete(self, record_id: str):
        """
        # Delete a record by ID

        # Steps
        # 1. Load all records
        # 2. Filter out maching ID
        # 3. Save updated dataset
        """

        data = self.storage.load_all()

        # Remove record with matching ID
        updated_data = [r for r in data if r.get("id") != record_id]

        # Save updated dataset
        self.storage.save_all(updated_data)

        # Log deletion
        logger.info(f"Deleted record: {record_id}")
