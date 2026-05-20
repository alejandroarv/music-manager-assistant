from datetime import date

from core.models.tour import TourData


def test_generate_tour_and_export(
    tour_service,
    repo
):
    """
    Verify successful tour generation,
    export formatting, and persistence.
    """

    result = tour_service.generate_tour(
        TourData(
            artist="Tour Artist",

            cities=[
                "Bogota",
                "Medellin",
                "Cali",
            ],

            start_date=date(2026, 5, 1),

            concerts_before_rest=2,

            rest_days=1,
        )
    )

    # Validate generated tour metadata
    assert (
        result["name"]
        == "Tour Artist"
    )

    # Expected schedule:
    # 3 concerts + 1 rest day
    assert (
        len(result["schedule"])
        == 4
    )

    # Validate export formatting
    exported = (
        tour_service
        .format_tour_for_export(result)
    )

    assert (
        "Tour Plan for Tour Artist"
        in exported
    )

    assert (
        "Bogota Concert"
        in exported
    )

    assert (
        "Rest Day"
        in exported
    )

    # Verify persistence layer state
    assert (
        len(repo.get_by_type("tour"))
        == 1
    )


def test_history_service_filters_and_downloads(
    history_service,
    booking_service,
    contract_service
):
    """
    Verify history retrieval, filtering,
    and download-content generation workflows.
    """

    # Create persisted booking record
    booking_service.create_booking(
        {
            "artist": "History Artist",

            "client": "Client",

            "venue": "Arena",

            "city": "Bogota",

            "date": date(2026, 5, 1),

            "fee": 2000,
        }
    )

    # Create persisted NDA contract
    contract_service.create_nda_contract(
        {
            "disclosing_party": (
                "History Artist"
            ),

            "receiving_party": (
                "Partner"
            ),

            "purpose": (
                "Testing history service "
                "download path"
            ),

            "duration": 3,
        }
    )

    # Retrieve filtered booking history
    booking_records = (
        history_service.get_all_records(
            "booking"
        )
    )

    # Retrieve available record categories
    all_types = (
        history_service.get_record_types()
    )

    # Validate filtered history retrieval
    assert len(booking_records) == 1

    # Validate available history types
    assert "booking" in all_types

    assert "nda_contract" in all_types

    # Build downloadable export content
    booking_download = (
        history_service
        .build_download_content(
            booking_records[0],

            lambda content: str(content),
        )
    )

    # Download content should contain
    # persisted booking information
    assert (
        "History Artist"
        in booking_download
    )