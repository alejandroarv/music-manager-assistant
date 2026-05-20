# features/tour/application/service.py

from datetime import datetime

from core.models.record import Record
from core.models.tour import TourData

from core.repositories.record_repository import (
    RecordRepository,
)

from features.tour.domain.logic import (
    build_tour,
)


class TourService:
    """
    Application service responsible for
    tour generation workflows.

    Responsibilities:
    - Validate and normalize tour input
    - Coordinate tour generation logic
    - Persist generated tours
    - Provide export formatting utilities
    - Generate standardized filenames
    """

    def __init__(
        self,
        repository: RecordRepository
    ):
        """
        Initialize the service with
        a repository dependency.
        """

        self.repo = repository

    def format_tour_for_export(
        self,
        result: dict
    ) -> str:
        """
        Convert a generated tour into a
        human-readable export format.

        Used by:
        - History exports
        - Download functionality
        - Tour previews
        """

        lines = [
            f"Tour Plan for {result['name']}",
            "",
        ]

        for i, item in enumerate(
            result["schedule"],
            start=1
        ):

            # Normalize dates from either
            # datetime objects or ISO strings
            date_obj = (
                item["date"]

                if isinstance(
                    item["date"],
                    datetime
                )

                else datetime.fromisoformat(
                    item["date"]
                )
            )

            date_str = (
                date_obj.strftime("%Y-%m-%d")
            )

            # Render schedule line based
            # on event type
            if item["type"] == "concert":

                lines.append(
                    f"{i}. {date_str} - "
                    f"{item['city']} Concert"
                )

            else:

                lines.append(
                    f"{date_str} - Rest Day"
                )

        return "\n".join(lines)

    def parse_cities(
        self,
        cities_input: str
    ):
        """
        Convert comma-separated city input
        into a normalized city list.

        Example:
            "NY, LA, Paris"
            ->
            ["NY", "LA", "Paris"]
        """

        return [
            c.strip()
            for c in cities_input.split(",")
            if c.strip()
        ]

    def generate_filename(
        self,
        name: str,
        suffix: str
    ):
        """
        Generate safe export filenames.
        """

        from utils.helpers import (
            format_filename,
        )

        safe_name = format_filename(name)

        return (
            f"{safe_name}_{suffix}.txt"
        )

    def generate_tour(
        self,
        data: TourData
    ) -> dict:
        """
        Generate and persist a tour schedule.

        Responsibilities:
        - Clean and validate input
        - Execute domain tour generation
        - Normalize dates for persistence
        - Persist generated tour records
        - Return generated schedule data
        """

        # -----------------------
        # Input Normalization
        # -----------------------

        cleaned_cities = [
            c.strip()
            for c in data.cities
            if c.strip()
        ]

        data.cities = cleaned_cities

        # -----------------------
        # Validation Rules
        # -----------------------

        if len(data.cities) == 0:

            raise ValueError(
                "At least one city is required"
            )

        if data.concerts_before_rest < 1:

            raise ValueError(
                "Must have at least 1 concert "
                "before rest"
            )

        if (
            data.concerts_before_rest
            > len(data.cities)
        ):

            raise ValueError(
                "Concerts before rest exceeds "
                "total cities"
            )

        if data.rest_days < 0:

            raise ValueError(
                "Rest days cannot be negative"
            )

        # -----------------------------
        # Tour Generation
        # -----------------------------

        # Delegate schedule generation
        # to the domain layer
        tour = build_tour(data)

        # Convert datetime objects into
        # JSON-safe ISO string values
        for item in tour["schedule"]:

            item["date"] = (
                item["date"].isoformat()
            )

        # ----------------------
        # Persistence
        # ----------------------

        record = Record(
            type="tour",

            name=data.artist,

            content=tour,

            metadata={
                "artist": data.artist,

                "cities": data.cities,

                "start_date": str(
                    data.start_date
                ),
            },
        )

        self.repo.save(record)

        return tour