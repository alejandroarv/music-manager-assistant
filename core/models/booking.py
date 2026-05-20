# core/models/booking.py

from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class BookingData:
    """
    # Data model for creating booking

    # It represents structured input coming from the UI
    # It ensures:
    # - Consistent data shape
    # - Validation at creation time
    """
    artist: str
    client: str
    city: str
    venue: str
    date: datetime.date
    fee: float
    notes: str | None = None
    additional_acts: str | None = None
    number_of_shows: int = 1
    shows: list[dict] | None = None
    purchaser_name: str | None = None
    purchaser_address: str | None = None
    signatory: str | None = None
    company_name: str | None = None
    company_address: str | None = None
    signature_date: Optional[datetime.date] = None
    show_length: str = ""
    capacity: str = ""
    air_transportation: str | None = None
    hotel_accommodations: str | None = None
    air_freight: str | None = None
    ground_transportation: str | None = None
    meals_incidentals: str | None = None
    special_provisions: str | None = None
    concessionaire_fee: str | None = None
    seller: str | None = None
    hard_merchandising: str | None = None
    soft_merchandising: str | None = None
    complimentary_tickets: str | None = None
    production_catering: str | None = None
    additional_addenda: str | None = None
    merchandising_terms: str | None = None
    buyer_name: str | None = None
    buyer_company_name: str | None = None

    def __post_init__(self):
        # Type enforcement
        self.fee = float(self.fee)
        self.number_of_shows = int(self.number_of_shows)
        self.shows = list(self.shows or [])

        # Required field validation
        if not self.artist:
            raise ValueError("Artist is required")

        if not self.client:
            raise ValueError("Client is required")

        if not self.city:
            raise ValueError("City is required")

        if not self.venue:
            raise ValueError("Venue is required")

        if self.fee < 0:
            raise ValueError("Fee cannot be negative")

        if self.number_of_shows < 1:
            raise ValueError("Number of shows must be at least 1")