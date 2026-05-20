# core/normalizers/contract.py
from utils.contract_helpers import (
    safe_value,
    format_contract_date,
    default_ticket_rows,
)


def normalize_show(show, data):
    ticket_rows = show.get("ticket_rows") or default_ticket_rows()
    total_tickets = sum(int(row.get("total", 0) or 0) for row in ticket_rows)
    total_comps = sum(int(row.get("comps_kills", 0) or 0) for row in ticket_rows)
    gross_potential = show.get(
        "gross_potential",
        sum(float(row.get("line_total", 0) or 0) for row in ticket_rows),
    )
    expenses = show.get("expenses") or {}

    return {
        "raw_date": show.get("date", data["date"]),
        "date": format_contract_date(show.get("date", data["date"])),

        "venue": safe_value(show.get("venue") or data["venue"]),
        "venue_address": safe_value(
            show.get("venue_address") or show.get("venue") or data["venue"]
        ),

        "time": safe_value(show.get("time")),

        "additional_acts": safe_value(
            show.get("additional_acts") or data["additional_acts"],
            default="None"
        ),

        "capacity": safe_value(show.get("capacity") or data["capacity"]),
        "show_length": safe_value(show.get("show_length") or data["show_length"]),

        "city": show.get("city", data["city"]),

        "ticket_rows": ticket_rows,
        "ticket_total": show.get("ticket_total", total_tickets),
        "ticket_comps_kills": show.get("ticket_comps_kills", total_comps),

        "gross_potential": gross_potential,
        "net_potential": show.get("net_potential", gross_potential),

        "expenses": {
            "fixed_expenses": expenses.get("fixed_expenses", 0),
            "variable_expenses": expenses.get("variable_expenses", 0),
            "break_even": expenses.get("break_even", 0),
            "net_potential": expenses.get(
                "net_potential",
                show.get("net_potential", gross_potential),
            ),
            "total_est_expenses": expenses.get("total_est_expenses", 0),
            "amount_to_split": expenses.get("amount_to_split", 0),
            "walkout_potential": expenses.get("walkout_potential", 0),
        },
    }

def normalize_performance_contract(data):
    def fallback(value, default):
        return safe_value(value) or default

    return {
        "artist": safe_value(data.artist),
        "client": safe_value(data.client),

        "purchaser_name": fallback(data.purchaser_name, data.client),
        "purchaser_address": safe_value(data.purchaser_address),

        "signatory": fallback(data.signatory, data.purchaser_name or data.client),

        "company_name": fallback(data.company_name, data.client),
        "company_address": safe_value(data.company_address),

        "venue": safe_value(data.venue),
        "city": safe_value(data.city),

        # ✅ FIXED HERE
        "date": data.date,
        "signature_date": data.signature_date or data.date,

        "fee": data.fee,
        "number_of_shows": data.number_of_shows,

        "additional_acts": fallback(data.additional_acts, "None"),

        "show_length": safe_value(data.show_length),
        "capacity": safe_value(data.capacity),

        "air_transportation": fallback(data.air_transportation, "Provided"),
        "hotel_accommodations": fallback(data.hotel_accommodations, "Provided"),
        "air_freight": fallback(data.air_freight, "Included"),
        "ground_transportation": fallback(data.ground_transportation, "Provided"),
        "meals_incidentals": fallback(data.meals_incidentals, "Provided"),

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

        "buyer_name": fallback(data.buyer_name, data.signatory or data.client),
        "buyer_company_name": fallback(
            data.buyer_company_name, data.company_name or data.client
        ),

        "shows": data.shows or [],
    }