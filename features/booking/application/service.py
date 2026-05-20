# features/booking/application/service.py

from core.models.booking import BookingData
from core.models.record import Record
from core.repositories.record_repository import RecordRepository
from core.result import Result
from core.models.contracts import PerformanceContractData
from datetime import datetime, timezone
from core.constants import BOOKING

# Domain logic (pure functions, no side effects)
from features.booking.domain.logic import (
    build_booking_export_line,
    build_booking_payload,
)

from utils.helpers import format_filename


class BookingService:
    def __init__(self, repository: RecordRepository, contract_service):
        self.repo = repository
        self.contract_service = contract_service

    def create_booking(self, data: dict) -> Result:

        try:
            # Convert dict -> BookingData (validation happens here)
            booking_data = BookingData(**data)
        except ValueError as e:
            return Result.fail(str(e))
        
        try:
            booking = build_booking_payload(booking_data)

            if not isinstance(booking, dict):
                return Result.fail("Booking payload must be a dictionary")
            
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
            return Result.fail(f"Failed to save booking: {str(e)}")
        
        booking["id"] = saved_record["id"]
        booking["timestamp"] = saved_record["timestamp"]

        return Result.ok(booking)

    def get_safe_fee(self, booking):
        try:
            return float(booking.get("fee", 0))
        except (TypeError, ValueError):
            return 0.0
    

    def list_bookings(self) -> list[dict]:

        bookings = self.repo.get_by_type(BOOKING)
        def parse_timestamp(ts):
            try:
                parsed = datetime.fromisoformat(ts)
                if parsed.tzinfo is None:
                    return parsed.replace(tzinfo=timezone.utc)
                return parsed.astimezone(timezone.utc)
            except Exception:
                return datetime.min.replace(tzinfo=timezone.utc)

        bookings.sort(
            key=lambda item: parse_timestamp(item.get("timestamp", "")),
                reverse=True
        )

        normalized = []

        for record in bookings:
            booking = self._normalize_booking(record)
            if booking:
                normalized.append(booking)
        
        return normalized

    def generate_contract(self, booking_id: str) -> Result:
        result = self.get_booking_by_id(booking_id)

        if not result.success:
            return result

        booking = result.data

        try:
            contract_data = PerformanceContractData(
                artist=booking.get("artist", ""),
                client=booking.get("client", ""),
                purchaser_name=booking.get("purchaser_name"),
                purchaser_address=booking.get("purchaser_address"),
                signatory=booking.get("signatory"),
                company_name=booking.get("company_name"),
                company_address=booking.get("company_address"),
                venue=booking.get("venue", ""),
                date=booking.get("date", ""),
                signature_date=booking.get("signature_date"),
                city=booking.get("city", ""),
                fee=booking.get("fee", 0),
                number_of_shows=booking.get("number_of_shows", 1),
                notes=booking.get("notes", ""),
                show_length=booking.get("show_length", ""),
                capacity=booking.get("capacity", ""),
                air_transportation=booking.get("air_transportation", ""),
                hotel_accommodations=booking.get("hotel_accommodations", ""),
                air_freight=booking.get("air_freight", ""),
                ground_transportation=booking.get("ground_transportation", ""),
                meals_incidentals=booking.get("meals_incidentals", ""),
                special_provisions=booking.get("special_provisions", ""),
                concessionaire_fee=booking.get("concessionaire_fee", "0%"),
                seller=booking.get("seller", ""),
                hard_merchandising=booking.get("hard_merchandising", ""),
                soft_merchandising=booking.get("soft_merchandising", ""),
                complimentary_tickets=booking.get("complimentary_tickets", ""),
                production_catering=booking.get("production_catering", ""),
                additional_addenda=booking.get("additional_addenda", ""),
                merchandising_terms=booking.get("merchandising_terms", ""),
                buyer_name=booking.get("buyer_name"),
                buyer_company_name=booking.get("buyer_company_name"),
                shows=booking.get("shows", []),
            )

            contract_result = self.contract_service.preview_performance_contract(contract_data)

            if not contract_result.success:
                return Result.fail(contract_result.error)

            return Result.ok(contract_result.data)

        except Exception as e:
            return Result.fail(str(e))

    def export_single_booking(self, booking: dict) -> str:
        return build_booking_export_line(booking)

    def export_bookings_text(self, bookings: list[dict]) -> str:
        return "\n".join(build_booking_export_line(booking) for booking in bookings)

    def generate_export_filename(self, artist: str, suffix: str) -> str:
        extension = "docx" if suffix == "contract" else "txt"
        return f"{format_filename(artist)}_{suffix}.{extension}"
    
    def get_booking_by_id(self, booking_id: str) -> dict | None:
        try:
            bookings = self.repo.get_by_type("booking")

            for record in bookings:
                if record.get("id") == booking_id:
                    booking = self._normalize_booking(record)
                
                    if not booking:
                        return Result.fail("Invalid booking data")
                    
                    return Result.ok(booking)
                
            return Result.fail("Booking not found")
            
        except Exception:
            return Result.fail("Failed to retrieve booking")

    def _normalize_booking(self, record: dict) -> dict | None:
        raw = record.get("content", {})
        metadata = record.get("metadata", {})

        if isinstance(raw, dict):
            source = raw
        elif isinstance(metadata, dict):
            # Support older booking records that stored the readable sentence in
            # `content` and the structured fields in `metadata`.
            source = metadata
        else:
            return None

        try:
            normalized = {
                "id": record.get("id"),
                "timestamp": record.get("timestamp"),

                "artist": source.get("artist", "").strip(),
                "client": source.get("client", "").strip(),
                "venue": source.get("venue", "").strip(),
                "city": source.get("city", "").strip(),
                "date": str(source.get("date", "")),
                "fee": float(source.get("fee", 0)),
                "notes": source.get("notes", ""),
                "number_of_shows": int(source.get("number_of_shows", 1) or 1),
                "shows": list(source.get("shows", []) or []),
                "purchaser_name": source.get("purchaser_name", "").strip(),
                "purchaser_address": source.get("purchaser_address", "").strip(),
                "signatory": source.get("signatory", "").strip(),
                "company_name": source.get("company_name", "").strip(),
                "company_address": source.get("company_address", "").strip(),
                "signature_date": str(source.get("signature_date", "")),
                "show_length": source.get("show_length", ""),
                "capacity": str(source.get("capacity", "")),
                "air_transportation": source.get("air_transportation", ""),
                "hotel_accommodations": source.get("hotel_accommodations", ""),
                "air_freight": source.get("air_freight", ""),
                "ground_transportation": source.get("ground_transportation", ""),
                "meals_incidentals": source.get("meals_incidentals", ""),
                "special_provisions": source.get("special_provisions", ""),
                "concessionaire_fee": source.get("concessionaire_fee", "0%"),
                "seller": source.get("seller", ""),
                "hard_merchandising": source.get("hard_merchandising", ""),
                "soft_merchandising": source.get("soft_merchandising", ""),
                "complimentary_tickets": str(source.get("complimentary_tickets", "")),
                "production_catering": source.get("production_catering", ""),
                "additional_addenda": source.get("additional_addenda", ""),
                "merchandising_terms": source.get("merchandising_terms", ""),
                "buyer_name": source.get("buyer_name", "").strip(),
                "buyer_company_name": source.get("buyer_company_name", "").strip(),
            }

            # Required fields check
            if not normalized["artist"] or not normalized["city"]:
                return None

            return normalized

        except Exception:
            return None
