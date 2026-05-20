# core/models/booking.py

from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class BookingData:
    """
    Structured booking input model

    Represents validated booking data collected from the UI layer
    before it is processed by application services or persisted

    Responsibilities:
    - Enforce a consistent data structure
    - Normalize incoming values
    - Perform basic validation at creation time
    """
    artist: str
    client: str
    city: str
    venue: str
    date: datetime.date
    fee: float

    # Optional booking details
    notes: str | None = None
    additional_acts: str | None = None

    # Multi-show support
    number_of_shows: int = 1
    shows: list[dict] | None = None

    # Contract and purchaser information
    purchaser_name: str | None = None
    purchaser_address: str | None = None
    signatory: str | None = None

    # Company information
    company_name: str | None = None
    company_address: str | None = None

    signature_date: Optional[datetime.date] = None

    # Performance details
    show_length: str = ""
    capacity: str = ""

    # Logistics and transportation
    air_transportation: str | None = None
    hotel_accommodations: str | None = None
    air_freight: str | None = None
    ground_transportation: str | None = None
    meals_incidentals: str | None = None

    # Additional agreement terms
    special_provisions: str | None = None
    concessionaire_fee: str | None = None
    seller: str | None = None
    hard_merchandising: str | None = None
    soft_merchandising: str | None = None
    complimentary_tickets: str | None = None
    production_catering: str | None = None
    additional_addenda: str | None = None
    merchandising_terms: str | None = None

    # Buyer information
    buyer_name: str | None = None
    buyer_company_name: str | None = None

    def __post_init__(self):
        """
        Normalize and validate booking data after initialization
        """

        # Normalize numeric and collection values
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


        # Business rule validation
        if self.fee < 0:
            raise ValueError("Fee cannot be negative")

        if self.number_of_shows < 1:
            raise ValueError("Number of shows must be at least 1")