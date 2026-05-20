from datetime import date


def test_create_booking_success(
    booking_service
):
    """
    Verify successful booking creation
    with multi-show configuration.
    """

    result = booking_service.create_booking(
        {
            "artist": "Artist",

            "client": "Client",

            "venue": "Arena",

            "city": "Bogota",

            "date": date(2026, 1, 1),

            "fee": 1000,

            "notes": "Test",

            "number_of_shows": 2,

            "shows": [
                {
                    "date": date(2026, 1, 1),

                    "time": "8:00 PM",

                    "venue": "Arena",
                },

                {
                    "date": date(2026, 1, 2),

                    "time": "9:00 PM",

                    "venue": "Arena 2",
                },
            ],
        }
    )

    # Validate successful creation
    assert result.success

    # Validate normalized booking data
    assert result.data["artist"] == "Artist"

    assert (
        result.data["number_of_shows"]
        == 2
    )

    assert (
        len(result.data["shows"])
        == 2
    )


def test_create_booking_invalid(
    booking_service
):
    """
    Verify validation failure for
    invalid booking input.
    """

    result = booking_service.create_booking(
        {
            "artist": "",

            "client": "Client",

            "venue": "Arena",

            "city": "Bogota",

            "date": date(2026, 1, 1),

            "fee": 1000,

            "notes": "Test",
        }
    )

    # Booking should fail validation
    assert not result.success


def test_list_bookings_returns_normalized(
    repo,
    booking_service
):
    """
    Verify booking listing returns
    normalized booking structures.
    """

    booking_service.create_booking(
        {
            "artist": "Artist",

            "client": "Client",

            "venue": "Arena",

            "city": "Bogota",

            "date": date(2026, 1, 1),

            "fee": 1000,

            "notes": "Test",
        }
    )

    bookings = (
        booking_service.list_bookings()
    )

    # Validate booking retrieval
    assert len(bookings) == 1

    booking = bookings[0]

    # Validate normalized fields
    assert "id" in booking

    assert "artist" in booking

    assert "city" in booking

    assert (
        booking["number_of_shows"]
        == 1
    )


def test_generate_contract_success(
    booking_service
):
    """
    Verify contracts can be generated
    from persisted bookings.
    """

    result = booking_service.create_booking(
        {
            "artist": "Artist",

            "client": "Client",

            "venue": "Arena",

            "city": "Bogota",

            "date": date(2026, 1, 1),

            "fee": 1000,

            "notes": "Test",
        }
    )

    # Generate contract using booking ID
    contract_result = (
        booking_service.generate_contract(
            result.data["id"]
        )
    )

    # Validate successful contract generation
    assert contract_result.success

    # DOCX contracts are returned as bytes
    assert isinstance(
        contract_result.data,
        bytes,
    )


def test_list_bookings_handles_mixed_timestamp_formats(
    repo,
    booking_service
):
    """
    Verify booking retrieval handles
    inconsistent timestamp formats safely.
    """

    # Simulate legacy persisted booking data
    repo.save(
        type(
            "RecordLike",

            (),

            {
                "to_dict": lambda self: {
                    "type": "booking",

                    "name": "Old",

                    "content": {
                        "artist": "Old",

                        "client": "Client",

                        "venue": "Arena",

                        "city": "Bogota",

                        "date": "2026-01-01",

                        "fee": 1000,
                    },

                    "metadata": {},

                    "timestamp": (
                        "2026-01-01T00:00:00"
                    ),
                }
            },
        )()
    )

    # Create current-format booking
    booking_service.create_booking(
        {
            "artist": "New",

            "client": "Client",

            "venue": "Arena",

            "city": "Bogota",

            "date": date(2026, 1, 2),

            "fee": 1000,
        }
    )

    bookings = (
        booking_service.list_bookings()
    )

    # Both legacy and current records
    # should be handled successfully
    assert len(bookings) == 2