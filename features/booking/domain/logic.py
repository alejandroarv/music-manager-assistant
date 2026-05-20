# features/booking/domain/logic.py

from core.models.booking import BookingData
from core.normalizers.booking import normalize_booking

from utils.helpers import make_json_safe


def build_booking_payload(
    data: BookingData
) -> dict:
    """
    Build a normalized booking payload suitable
    for persistence and export operations.

    Responsibilities:
    - Normalize booking input data
    - Convert values into JSON-safe structures
    - Produce a consistent persistence payload
    """

    normalized = normalize_booking(data)

    return {
        "artist": normalized["artist"],
        "client": normalized["client"],
        "venue": normalized["venue"],
        "city": normalized["city"],

        # Serialize date values for persistence
        "date": normalized["date"].isoformat(),

        "fee": normalized["fee"],

        # Preserve backward compatibility with
        # older booking note structures
        "notes": normalized["additional_acts"],

        "number_of_shows": normalized[
            "number_of_shows"
        ],

        "shows": make_json_safe(
            normalized["shows"]
        ),

        # Purchaser and company information
        "purchaser_name": normalized[
            "purchaser_name"
        ],

        "purchaser_address": normalized[
            "purchaser_address"
        ],

        "signatory": normalized[
            "signatory"
        ],

        "company_name": normalized[
            "company_name"
        ],

        "company_address": normalized[
            "company_address"
        ],

        "signature_date": make_json_safe(
            normalized["signature_date"]
        ),

        # Show configuration
        "show_length": normalized[
            "show_length"
        ],

        "capacity": normalized[
            "capacity"
        ],

        # Logistics information
        "air_transportation": normalized[
            "air_transportation"
        ],

        "hotel_accommodations": normalized[
            "hotel_accommodations"
        ],

        "air_freight": normalized[
            "air_freight"
        ],

        "ground_transportation": normalized[
            "ground_transportation"
        ],

        "meals_incidentals": normalized[
            "meals_incidentals"
        ],

        # Contract and merchandising terms
        "special_provisions": normalized[
            "special_provisions"
        ],

        "concessionaire_fee": normalized[
            "concessionaire_fee"
        ],

        "seller": normalized["seller"],

        "hard_merchandising": normalized[
            "hard_merchandising"
        ],

        "soft_merchandising": normalized[
            "soft_merchandising"
        ],

        "complimentary_tickets": normalized[
            "complimentary_tickets"
        ],

        "production_catering": normalized[
            "production_catering"
        ],

        "additional_addenda": normalized[
            "additional_addenda"
        ],

        "merchandising_terms": normalized[
            "merchandising_terms"
        ],

        # Buyer information
        "buyer_name": normalized[
            "buyer_name"
        ],

        "buyer_company_name": normalized[
            "buyer_company_name"
        ],
    }


def build_booking_export_line(
    booking: dict
) -> str:
    """
    Build a human-readable export line
    for a booking entry.
    """

    return (
        f'{booking["artist"]} - '
        f'{booking["city"]} - '
        f'{booking["date"]}'
    )
