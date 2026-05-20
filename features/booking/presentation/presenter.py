# features/booking/presentation/presenter.py

def map_booking_to_view(data: dict) -> dict:
    """
    Transform booking data into a UI-friendly view model.

    Responsibilities:
    - Format display-ready values
    - Prepare presentation-specific labels
    - Isolate UI formatting from business logic
    """

    return {
        "id": data["id"],

        # Display-oriented fields
        "title": (
            f'{data["artist"]} - '
            f'{data["city"]}'
        ),

        "date_label": (
            f'Date: {data["date"]}'
        ),

        "fee_label": (
            f'Fee: ${data["fee"]:.2f}'
        ),

        "shows_label": (
            f'Shows: '
            f'{data.get("number_of_shows", 1)}'
        ),

        # Preserve raw data for detail views
        # or debugging scenarios
        "raw": data,
    }