# utils/contract_helpers.py

from datetime import date, datetime


def safe_value(value, default="TBD"):
    if value is None:
        return default

    if isinstance(value, str) and not value.strip():
        return default

    if isinstance(value, (list, dict)) and not value:
        return default

    return str(value)


def parse_date_value(value):
    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    text = str(value).strip()
    if not text:
        return None

    for parser in (datetime.fromisoformat, date.fromisoformat):
        try:
            parsed = parser(text)
            if isinstance(parsed, datetime):
                return parsed
            return datetime.combine(parsed, datetime.min.time())
        except ValueError:
            continue

    return None


def format_contract_date(value):
    parsed = parse_date_value(value)
    if parsed is None:
        return str(value).strip()

    return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"


def default_ticket_rows():
    return [
        {"label": "Platinum", "total": 400, "comps_kills": 0, "price": 57.38, "line_total": 22952.00},
        {"label": "Gold", "total": 400, "comps_kills": 0, "price": 49.18, "line_total": 19672.00},
        {"label": "VIP", "total": 100, "comps_kills": 0, "price": 40.98, "line_total": 4098.00},
        {"label": "Platea Oeste", "total": 600, "comps_kills": 0, "price": 36.89, "line_total": 22134.00},
        {"label": "Platea Este", "total": 1000, "comps_kills": 0, "price": 32.79, "line_total": 32790.00},
        {"label": "Popular", "total": 1500, "comps_kills": 0, "price": 28.69, "line_total": 43035.00},
    ]