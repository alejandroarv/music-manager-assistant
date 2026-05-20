# features/booking/application/service.py

from datetime import datetime, timezone

from core.constants import BOOKING
from core.models.booking import BookingData
from core.models.contracts import PerformanceContractData
from core.models.record import Record
from core.repositories.record_repository import RecordRepository
from core.result import Result

# Domain-level business logic
from features.booking.domain.logic import (
    build_booking_export_line,
    build_booking_payload,
)

from utils.helpers import format_filename


class BookingService:
    """
    Application service responsible for booking workflows.

    Responsibilities:
    - Validate and create bookings
    - Coordinate persistence operations
    - Normalize stored booking data
    - Generate booking exports
    - Coordinate contract generation workflows

    This service acts as the orchestration layer between:
    - Domain logic
    - Persistence
    - Contract services
    """

    def __init__(
        self,
        repository: RecordRepository,
        contract_service
    ):
        self.repo = repository
        self.contract_service = contract_service

    def create_booking(self, data: dict) -> Result:
        """
        Create and persist a new booking.

        Responsibilities:
        - Validate incoming booking data
        - Build normalized booking payloads
        - Persist booking records
        - Return standardized operation results
        """

        try:
            # Validation occurs during model construction
            booking_data = BookingData(**data)

        except ValueError as e:
            return Result.fail(str(e))

        try:
            # Build domain booking payload
            booking = build_booking_payload(
                booking_data
            )

            if not isinstance(booking, dict):
                return Result.fail(
                    "Booking payload must be a dictionary"
                )

            # Persist booking record
            saved_record = self.repo.save(
                Record(
                    type=BOOKING,
                    name=booking_data.artist,
                    content=booking,
                    metadata={
                        "artist": booking_data.artist,
                        "client": booking_data.client,
                        "city": booking_data.city,
                        "venue": booking_data.venue,
                        "date": booking["date"],
                    }
                )
            )

        except Exception as e:
            return Result.fail(
                f"Failed to save booking: {str(e)}"
            )

        # Attach persistence metadata
        booking["id"] = saved_record["id"]
        booking["timestamp"] = saved_record["timestamp"]

        return Result.ok(booking)

    def get_safe_fee(self, booking):
        """
        Safely normalize booking fee values.
        """

        try:
            return float(booking.get("fee", 0))

        except (TypeError, ValueError):
            return 0.0

    def list_bookings(self) -> list[dict]:
        """
        Retrieve and normalize all bookings.

        Returns:
            list[dict]: Normalized booking records sorted
            by most recent timestamp.
        """

        bookings = self.repo.get_by_type(
            BOOKING
        )

        def parse_timestamp(ts):
            """
            Safely parse timestamps for sorting.
            """

            try:
                parsed = datetime.fromisoformat(ts)

                if parsed.tzinfo is None:
                    return parsed.replace(
                        tzinfo=timezone.utc
                    )

                return parsed.astimezone(
                    timezone.utc
                )

            except Exception:
                return datetime.min.replace(
                    tzinfo=timezone.utc
                )

        # Sort newest bookings first
        bookings.sort(
            key=lambda item: parse_timestamp(
                item.get("timestamp", "")
            ),
            reverse=True
        )

        normalized = []

        for record in bookings:
            booking = self._normalize_booking(
                record
            )

            if booking:
                normalized.append(booking)

        return normalized

    def generate_contract(
        self,
        booking_id: str
    ) -> Result:
        """
        Generate a performance contract from
        an existing booking record.
        """

        result = self.get_booking_by_id(
            booking_id
        )

        if not result.success:
            return result

        booking = result.data

        try:
            # Transform booking data into
            # contract-specific input structure
            contract_data = PerformanceContractData(
                ...
            )

            contract_result = (
                self.contract_service
                .preview_performance_contract(
                    contract_data
                )
            )

            if not contract_result.success:
                return Result.fail(
                    contract_result.error
                )

            return Result.ok(
                contract_result.data
            )

        except Exception as e:
            return Result.fail(str(e))

    def export_single_booking(
        self,
        booking: dict
    ) -> str:
        """
        Export a single booking as text.
        """
        return build_booking_export_line(
            booking
        )

    def export_bookings_text(
        self,
        bookings: list[dict]
    ) -> str:
        """
        Export multiple bookings as formatted text.
        """
        return "\n".join(
            build_booking_export_line(booking)
            for booking in bookings
        )

    def generate_export_filename(
        self,
        artist: str,
        suffix: str
    ) -> str:
        """
        Generate a standardized export filename.
        """

        extension = (
            "docx"
            if suffix == "contract"
            else "txt"
        )

        return (
            f"{format_filename(artist)}"
            f"_{suffix}.{extension}"
        )

    def get_booking_by_id(
        self,
        booking_id: str
    ) -> dict | None:
        """
        Retrieve and normalize a booking
        by its identifier.
        """

        try:
            bookings = self.repo.get_by_type(
                BOOKING
            )

            for record in bookings:
                if record.get("id") == booking_id:

                    booking = self._normalize_booking(
                        record
                    )

                    if not booking:
                        return Result.fail(
                            "Invalid booking data"
                        )

                    return Result.ok(booking)

            return Result.fail(
                "Booking not found"
            )

        except Exception:
            return Result.fail(
                "Failed to retrieve booking"
            )

    def _normalize_booking(
        self,
        record: dict
    ) -> dict | None:
        """
        Normalize persisted booking records into a
        consistent application structure.

        Supports both:
        - Current structured booking records
        - Legacy booking persistence formats
        """

        raw = record.get("content", {})
        metadata = record.get("metadata", {})

        if isinstance(raw, dict):
            source = raw

        elif isinstance(metadata, dict):
            # Support older booking formats where
            # structured data was stored in metadata
            source = metadata

        else:
            return None

        try:
            normalized = {
                ...
            }

            # Validate minimum required fields
            if (
                not normalized["artist"]
                or not normalized["city"]
            ):
                return None

            return normalized

        except Exception:
            return None