# core/normalizers/contract.py
from utils.contract_helpers import (
    safe_value,
    format_contract_date,
    default_ticket_rows,
)


def normalize_show(show, data):
    """
    Normalize an individual show entry for contract generation

    Responsibilities:
    - Apply fallback/default values
    - Normalize financial data
    - Calculate ticket and revenue totals
    - Produce a contract-ready show structure
    """

    # Initialize ticket configuration
    ticket_rows = show.get("ticket_rows") or default_ticket_rows()

    # Aggregate ticket metrics
    total_tickets = sum(int(row.get("total", 0) or 0) for row in ticket_rows)
    total_comps = sum(int(row.get("comps_kills", 0) or 0) for row in ticket_rows)

    # Calculate gross potential if not explicitly provided
    gross_potential = show.get(
        "gross_potential",
        sum(float(row.get("line_total", 0) or 0) for row in ticket_rows),
    )

    ticketing_fee_percent = show.get(
        "ticketing_fee_percent",
        data.get("ticketing_fee_percent", 0),
    )

    ticketing_fee_amount = show.get(
        "ticketing_fee_amount",
        float(gross_potential or 0) * (float(ticketing_fee_percent or 0) / 100),
    )

    expenses = show.get("expenses") or {}

    return {
        # Date information
        "raw_date": show.get("date", data["date"]),
        "date": format_contract_date(show.get("date", data["date"])),

        # Venue information
        "venue": safe_value(show.get("venue") or data["venue"]),
        "venue_address": safe_value(
            show.get("venue_address") or show.get("venue") or data["venue"]
        ),

        # Performance details
        # Accept both the current UI field and the older singular field
        # so schedule rows render consistently in every contract template.
        "schedules": (
            show.get("schedules")
            or show.get("schedule")
            or []
        ),
        "additional_acts": safe_value(
            show.get("additional_acts") or data["additional_acts"],
            default="None"
        ),
        "capacity": safe_value(show.get("capacity") or data["capacity"]),
        "show_length": safe_value(show.get("show_length") or data["show_length"]),
        "city": show.get("city", data["city"]),

        # Ticket and attendance information
        "ticket_rows": ticket_rows,
        "ticket_total": show.get("ticket_total", total_tickets),
        "ticket_comps_kills": show.get("ticket_comps_kills", total_comps),

        # Revenue projections
        "gross_potential": gross_potential,
        "net_potential": show.get("net_potential", gross_potential),
        # Preserve ticketing-fee values calculated by the UI so the DOCX
        # summary table can fill both the percent and dollar amount.
        "ticketing_fee_percent": ticketing_fee_percent,
        "ticketing_fee_amount": ticketing_fee_amount,

        # Expense breakdown
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
    """
    Normalize performance contract data into a standarized
    contract-ready structure

    Responsibilities:
    - Sanitize optiona values
    - Apply business default values
    - Normalize purchaser and buyer information
    - Prepare data for document rendering
    """
    def fallback(value, default):
        """
        Return a sanitized value or a fallback default
        """
        return safe_value(value) or default

    return {
        # Core contract information
        "artist": safe_value(data.artist),
        "client": safe_value(data.client),

        # Purchaser information
        "purchaser_name": fallback(data.purchaser_name, data.client),
        "purchaser_address": safe_value(data.purchaser_address),
        "signatory": fallback(data.signatory, data.purchaser_name or data.client),

        # Company information
        "company_name": fallback(data.company_name, data.client),
        "company_address": safe_value(data.company_address),

        # Venue information
        "venue": safe_value(data.venue),
        "city": safe_value(data.city),

        # Date information
        "date": data.date,
        "signature_date": data.signature_date or data.date,

        # Financial and scheduling information
        "fee": data.fee,
        "number_of_shows": data.number_of_shows,
        "ticketing_fee_percent": data.ticketing_fee_percent,

        # Performer information
        "additional_acts": fallback(data.additional_acts, "None"),

        # Show configuration
        "show_length": safe_value(data.show_length),
        "capacity": safe_value(data.capacity),

        # Travel and logistics
        "air_transportation": fallback(data.air_transportation, "Provided"),
        "hotel_accommodations": fallback(data.hotel_accommodations, "Provided"),
        "air_freight": fallback(data.air_freight, "Included"),
        "ground_transportation": fallback(data.ground_transportation, "Provided"),
        "meals_incidentals": fallback(data.meals_incidentals, "Provided"),

        # Business and merchandising terms
        "special_provisions": fallback(data.special_provisions, "None"),
        "concessionaire_fee": fallback(data.concessionaire_fee, "0%"),
        "seller": fallback(data.seller, "TBD"),
        "hard_merchandising": fallback(data.hard_merchandising, "Allowed"),
        "soft_merchandising": fallback(data.soft_merchandising, "Allowed"),
        "complimentary_tickets": fallback(data.complimentary_tickets, "20"),
        "production": fallback(
            data.production,
            "Standard production provided",
        ),
        "catering": fallback(
            data.catering,
            "Standard catering provided",
        ),
        "additional_addenda": fallback(data.additional_addenda, "None"),
        "merchandising_terms": fallback(
            data.merchandising_terms,
            "Standard merchandising terms apply",
        ),

        # Buyer information
        "buyer_name": fallback(
            data.buyer_name,
            data.signatory or data.client,
        ),

        "buyer_company_name": fallback(
            data.buyer_company_name,
            data.company_name or data.client,
        ),

        "manager_name": fallback(
            data.manager_name,
            "",
        ),

        "manager_company_name": fallback(
            data.manager_company_name,
            data.company_name,
        ),

        # Multi-show configuration
        "shows": data.shows or [],
    }
