# features/history/application/service.py

import json

from core.repositories.record_repository import (
    RecordRepository,
)


class HistoryService:
    """
    Application service responsible for
    history and record retrieval workflows.

    Responsibilities:
    - Retrieve persisted records
    - Filter and sort records
    - Provide record type metadata
    - Prepare downloadable content
    - Coordinate record deletion operations

    This service acts as a read-oriented
    utility layer over the repository system.
    """

    def __init__(
        self,
        repository: RecordRepository
    ):
        """
        Initialize the history service with
        a repository dependency.
        """

        self.repo = repository

    def get_all_records(
        self,
        record_type: str = "All"
    ):
        """
        Retrieve persisted records with
        optional type filtering.

        Responsibilities:
        - Retrieve all records
        - Filter by record type
        - Sort records by timestamp

        Args:
            record_type:
                Optional record type filter.

        Returns:
            list: Filtered and sorted records.
        """

        # Retrieve all persisted records
        records = self.repo.get_all()

        # Filter records when a specific
        # record type is selected
        filtered = [
            record
            for record in records
            if (
                record_type == "All"
                or record.get("type")
                == record_type
            )
        ]

        # Sort newest records first
        filtered.sort(
            key=lambda item: item.get(
                "timestamp",
                ""
            ),
            reverse=True,
        )

        return filtered

    def get_record_types(self) -> list[str]:
        """
        Retrieve all unique persisted
        record types.

        Returns:
            list[str]:
                Available record type options.
        """

        # Extract unique record categories
        types = sorted(
            {
                record.get(
                    "type",
                    "unknown"
                )
                for record in self.repo.get_all()
            }
        )

        # Include generic UI filter option
        return ["All", *types]

    def build_download_content(
        self,
        record: dict,
        tour_exporter
    ) -> str:
        """
        Build downloadable content for
        persisted records.

        Handles multiple content formats:
        - Tour exports
        - Structured JSON content
        - Plain string content

        Args:
            record:
                Persisted record structure.

            tour_exporter:
                Formatter function for
                exporting tour data.

        Returns:
            str: Download-ready content.
        """

        record_type = record.get("type")

        content = record.get(
            "content",
            ""
        )

        # Tour exports require custom
        # formatting logic
        if (
            record_type == "tour"
            and isinstance(content, dict)
        ):

            return tour_exporter(content)

        # Serialize structured data
        # into formatted JSON
        if isinstance(content, dict):

            return json.dumps(
                content,
                indent=2
            )

        # Fallback for plain text
        # contract or export content
        return str(content)

    def delete_record(
        self,
        record_id: str
    ):
        """
        Delete a persisted record by ID.

        Delegates deletion operations
        to the repository layer.
        """

        self.repo.delete(record_id)