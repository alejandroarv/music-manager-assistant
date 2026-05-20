# core/normalizers/booking.py

from utils.contract_helpers import safe_value


def normalize_booking(data):
    def fallback(value, default):
        return safe_value(value) or default

    return {
        "artist": safe_value(data.artist),
        "client": safe_value(data.client),
        "city": safe_value(data.city),
        "venue": safe_value(data.venue),

        "date": data.date,
        "signature_date": data.signature_date or data.date,

        "fee": float(data.fee),
        "number_of_shows": int(data.number_of_shows),

        "notes": safe_value(data.notes, default=""),
        "additional_acts": fallback(data.additional_acts, data.notes or "None"),

        "show_length": safe_value(data.show_length),
        "capacity": safe_value(data.capacity),

        # travel + logistics
        "air_transportation": fallback(data.air_transportation, "Provided"),
        "hotel_accommodations": fallback(data.hotel_accommodations, "Provided"),
        "air_freight": fallback(data.air_freight, "Included"),
        "ground_transportation": fallback(data.ground_transportation, "Provided"),
        "meals_incidentals": fallback(data.meals_incidentals, "Provided"),

        # business terms
        "special_provisions": fallback(data.special_provisions, "None"),
        "concessionaire_fee": fallback(data.concessionaire_fee, "0%"),
        "seller": fallback(data.seller, "TBD"),

        "hard_merchandising": fallback(data.hard_merchandising, "Allowed"),
        "soft_merchandising": fallback(data.soft_merchandising, "Allowed"),

        "complimentary_tickets": fallback(data.complimentary_tickets, "20"),
        "production_catering": fallback(
            data.production_catering,
            "Standard production provided",
        ),

        "additional_addenda": fallback(data.additional_addenda, "None"),
        "merchandising_terms": fallback(
            data.merchandising_terms,
            "Standard merchandising terms apply",
        ),

        # buyer / purchaser
        "purchaser_name": fallback(data.purchaser_name, data.client),
        "purchaser_address": safe_value(data.purchaser_address),
        "signatory": fallback(data.signatory, data.purchaser_name or data.client),

        "company_name": fallback(data.company_name, data.client),
        "company_address": safe_value(data.company_address),

        "buyer_name": fallback(data.buyer_name, data.signatory or data.client),
        "buyer_company_name": fallback(
            data.buyer_company_name, data.company_name or data.client
        ),

        # shows
        "shows": data.shows or [],
    }