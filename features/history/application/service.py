# features/history/application/service.py

import json

from core.repositories.record_repository import RecordRepository


class HistoryService:
    """
    # Application Service for History feature

    # Responsibilities:
    # - Retrieve stored records
    # - Filter and sort records
    # - Provide record type options
    # - Prepare content for download/export
    # - Handle deletion for records

    # This service acts as a "read and utility layer" over the repository
    """

    def __init__(self, repository: RecordRepository):
        # Inject repository dependency
        self.repo = repository

    def get_all_records(self, record_type: str = "All"):
        """
        # Retrieve all records, optionally filtered by type

        # Args:
        #   Record_type (str): Type for filter by (e. g., "booking", "tour")
        
        # Steps:
        # 1. Fetch all records
        # 2. Filter by type (if not "All")
        # 3. Sort by timestamp (newest first)
        """
        records = self.repo.get_all()

        # Filter records by type
        filtered = [
            record for record in records
            if record_type == "All" or record.get("type") == record_type
        ]

        # Sort newest first
        filtered.sort(key=lambda item: item.get("timestamp", ""), reverse=True)
        return filtered

    def get_record_types(self) -> list[str]:
        """
        # Extract unique record types from storage

        # Returns:
        #   list[str]: ["All", "booking", "tour", "nda_contract", ...]
        """

        # Collect unique types
        types = sorted({
            record.get("type", "unknown") 
            for record in self.repo.get_all()
        })
        
        # Add "All" option for UI
        return ["All", *types]

    def build_download_content(self, record: dict, tour_exporter) -> str:
        """
        # Prepare record content for download

        # Handles different content formats depending on record type

        # Args:
        #   record (dict): Stored record
        #   tour_exporter (function): function to format tour data

        # Logic:
        # - Tour (dict) -> use exporter
        # - Dict -> JSON string
        # - String -> return as-is
        """

        record_type = record.get("type")
        content = record.get("content", "")

        # Special handling for tours
        if record_type == "tour" and isinstance(content, dict):
            return tour_exporter(content)

        # Generic dict -> JSON
        if isinstance(content, dict):
            return json.dumps(content, indent=2)

        # Fallback (string content like contracts)
        return str(content)
    

    def delete_record(self, record_id: str):
        """
        # Delete a record by ID
        # Delegates to repository
        """
        self.repo.delete(record_id)
