from datetime import date

from core.models.tour import TourData


def test_generate_tour_and_export(tour_service, repo):
    result = tour_service.generate_tour(
        TourData(
            artist="Tour Artist",
            cities=["Bogota", "Medellin", "Cali"],
            start_date=date(2026, 5, 1),
            concerts_before_rest=2,
            rest_days=1,
        )
    )

    assert result["name"] == "Tour Artist"
    assert len(result["schedule"]) == 4

    exported = tour_service.format_tour_for_export(result)
    assert "Tour Plan for Tour Artist" in exported
    assert "Bogota Concert" in exported
    assert "Rest Day" in exported
    assert len(repo.get_by_type("tour")) == 1


def test_history_service_filters_and_downloads(history_service, booking_service, contract_service):
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
    contract_service.create_nda_contract(
        {
            "disclosing_party": "History Artist",
            "receiving_party": "Partner",
            "purpose": "Testing history service download path",
            "duration": 3,
        }
    )

    booking_records = history_service.get_all_records("booking")
    all_types = history_service.get_record_types()

    assert len(booking_records) == 1
    assert "booking" in all_types
    assert "nda_contract" in all_types

    booking_download = history_service.build_download_content(
        booking_records[0],
        lambda content: str(content),
    )
    assert "History Artist" in booking_download
