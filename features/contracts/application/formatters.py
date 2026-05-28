# features/contracts/application/formatters.py

def format_purchaser_term(
    purchaser_name,
    term_name,
    value,
):
    """
    Format purchaser-provided contract terms
    using standardized legal wording.

    Responsibilities:
    - standardize purchaser obligations
    - normalize legal phrasing
    - avoid rendering empty sections

    Args:
        term_name:
            Human-readable contract term label.

        value:
            User-provided contract term value.

    Returns:
        str:
            Formatted legal contract clause.
    """

    # Normalize incoming value
    normalized_value = (
        str(value).strip()
    )

    # Avoid rendering empty clauses
    if not normalized_value:

        return ""

    normalized_purchaser = (
        str(purchaser_name).strip()
        or "PURCHASER"
    )

    return (
        f"{normalized_purchaser} "
        "shall provide and pay for "
        f"{term_name}: "
        f"{normalized_value}"
    )