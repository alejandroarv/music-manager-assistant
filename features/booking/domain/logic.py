# features/booking/domain/logic.py

from core.models.booking import BookingData
from utils.helpers import make_json_safe
from core.normalizers.booking import normalize_booking

def build_booking_payload(data: BookingData) -> dict:
    normalized = normalize_booking(data)

    return {
        "artist": normalized["artist"],
        "client": normalized["client"],
        "venue": normalized["venue"],
        "city": normalized["city"],
        "date": normalized["date"].isoformat(),
        "fee": normalized["fee"],
        "notes": normalized["additional_acts"],
        "number_of_shows": normalized["number_of_shows"],
        "shows": make_json_safe(normalized["shows"]),
        "purchaser_name": normalized["purchaser_name"],
        "purchaser_address": normalized["purchaser_address"],
        "signatory": normalized["signatory"],
        "company_name": normalized["company_name"],
        "company_address": normalized["company_address"],
        "signature_date": make_json_safe(normalized["signature_date"]),
        "show_length": normalized["show_length"],
        "capacity": normalized["capacity"],
        "air_transportation": normalized["air_transportation"],
        "hotel_accommodations": normalized["hotel_accommodations"],
        "air_freight": normalized["air_freight"],
        "ground_transportation": normalized["ground_transportation"],
        "meals_incidentals": normalized["meals_incidentals"],
        "special_provisions": normalized["special_provisions"],
        "concessionaire_fee": normalized["concessionaire_fee"],
        "seller": normalized["seller"],
        "hard_merchandising": normalized["hard_merchandising"],
        "soft_merchandising": normalized["soft_merchandising"],
        "complimentary_tickets": normalized["complimentary_tickets"],
        "production_catering": normalized["production_catering"],
        "additional_addenda": normalized["additional_addenda"],
        "merchandising_terms": normalized["merchandising_terms"],
        "buyer_name": normalized["buyer_name"],
        "buyer_company_name": normalized["buyer_company_name"],
    }


def build_booking_export_line(booking: dict) -> str:
    return f'{booking["artist"]} - {booking["city"]} - {booking["date"]}'
