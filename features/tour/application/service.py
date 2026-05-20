# features/tour/application/service.py

from core.models.tour import TourData
from core.models.record import Record
from features.tour.domain.logic import build_tour
from core.repositories.record_repository import RecordRepository
from datetime import datetime


class TourService:
    """
    # Convert a tour result into a readable text format

    # Used by:
    # - HistoryService (download)
    # - Export functionality

    # Handles:
    # - date normalization
    # - formatting schedule
    """

    def __init__(self, repository: RecordRepository):
        self.repo = repository

    def format_tour_for_export(self, result: dict) -> str:
        lines = [f"Tour Plan for {result['name']}", ""]

        for i, item in enumerate(result["schedule"], start=1):

            # Normalize date (supports datetime or string)
            date_obj = (
                item["date"]
                if isinstance(item["date"], datetime)
                else datetime.fromisoformat(item["date"])
            )

            date_str = date_obj.strftime("%Y-%m-%d")

            # Format based on event type
            if item["type"] == "concert":
                lines.append(f"{i}. {date_str} - {item['city']} Concert")
            else:
                lines.append(f"{date_str} - Rest Day")

        return "\n".join(lines)

    def parse_cities(self, cities_input: str):
        """
        # Convert comma-separated string into lists of cities

        # Example:
        # "NY, LA, Paris" -> ["NY", "LA", "Paris"]
        """

        return [c.strip() for c in cities_input.split(",") if c.strip()]
    
    def generate_filename(self, name: str, suffix: str):
        """
        # Generate safe filename for exports
        """

        from utils.helpers import format_filename

        safe_name = format_filename(name)
        return f"{safe_name}_{suffix}.txt"
    
    
    def generate_tour(self, data: TourData) -> dict:
        """
        # Generate and persist a tour schedule

        # Steps:
        # 1. Clean input
        # 2. Validate business rules
        # 3. Generate schedule via domain logic
        # 4. Normalize dates for storage
        # 5. Save as record
        # 6. Return result
        """

        # -----------------------
        # Input cleaning
        # -----------------------

        cleaned_cities = [c.strip() for c in data.cities if c.strip()]
        data.cities = cleaned_cities

        # -----------------------
        # Validation rules
        # -----------------------

        if len(data.cities) == 0:
            raise ValueError("At least one city is required")
        
        if data.concerts_before_rest < 1:
            raise ValueError("Must have at least 1 concert before rest")

        if data.concerts_before_rest > len(data.cities):
            raise ValueError("Concerts before rest exceeds total cities")
        
        if data.rest_days < 0:
            raise ValueError("Rest days cannot be negative")
        
        # -----------------------------
        # Generate tour (domain logic)
        # -----------------------------

        tour = build_tour(data)

        # Convert dates into ISO format (JSON-safe)
        for item in tour["schedule"]:
            item["date"] = item["date"].isoformat()

        # ----------------------
        # Persist tour
        # ----------------------
        
        record = Record(
            type="tour",
            name=data.artist,
            content=tour,
            metadata={
                "artist": data.artist,
                "cities": data.cities,
                "start_date": str(data.start_date)
            }
        )
        self.repo.save(record)

        return tour


