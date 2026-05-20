# features/booking/presentation/presenter.py
def map_booking_to_view(data: dict) -> dict:
    """
    Convert raw booking data into UI-friendly format.
    Only handles formatting — no business logic or heavy data.
    """

    return {
        "id": data["id"],

        # Display fields
        "title": f'{data["artist"]} - {data["city"]}',
        "date_label": f'Date: {data["date"]}',
        "fee_label": f'Fee: ${data["fee"]:.2f}',
        "shows_label": f'Shows: {data.get("number_of_shows", 1)}',

        # Raw fallback (for debugging / expand view)
        "raw": data,
    }
