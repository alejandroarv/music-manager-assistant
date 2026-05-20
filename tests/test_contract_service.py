from datetime import date


def test_create_single_performance_contract(
    contract_service,
    repo,
    performance_payload
):
    """
    Verify successful generation and
    persistence of a single-show
    performance contract.
    """

    result = (
        contract_service
        .create_performance_contract(
            performance_payload
        )
    )

    # Validate successful contract generation
    assert result.success

    # Generated DOCX contracts are returned as bytes
    assert isinstance(
        result.data,
        bytes,
    )

    # Verify persistence layer state
    records = repo.get_by_type(
        "performance_contract"
    )

    assert len(records) == 1

    # Single-show workflows should use
    # the single-show template
    assert (
        records[0]["content"]["template"]
        == "performance_single"
    )


def test_create_multi_performance_contract(
    contract_service,
    repo,
    performance_payload
):
    """
    Verify successful generation of a
    multi-show performance contract.
    """

    payload = {
        **performance_payload,

        "number_of_shows": 3,

        "shows": [
            {
                "city": "Miami",

                "venue": "Arena 1",

                "date": date(2026, 5, 1),

                "time": "8:00 PM",
            },

            {
                "city": "Orlando",

                "venue": "Arena 2",

                "date": date(2026, 5, 2),

                "time": "9:00 PM",
            },

            {
                "city": "Tampa",

                "venue": "Arena 3",

                "date": date(2026, 5, 3),

                "time": "7:30 PM",
            },
        ],
    }

    result = (
        contract_service
        .create_performance_contract(
            payload
        )
    )

    # Validate successful generation
    assert result.success

    records = repo.get_by_type(
        "performance_contract"
    )

    # Multi-show workflows should use
    # the multi-show template
    assert (
        records[0]["content"]["template"]
        == "performance_multi"
    )

    # Verify persisted show structures
    assert (
        len(records[0]["content"]["shows"])
        == 3
    )


def test_create_nda_contract(
    contract_service,
    repo
):
    """
    Verify successful NDA generation
    and persistence.
    """

    result = (
        contract_service.create_nda_contract(
            {
                "disclosing_party": (
                    "Company A"
                ),

                "receiving_party": (
                    "Company B"
                ),

                "purpose": (
                    "Testing NDA "
                    "generation flow"
                ),

                "duration": 6,
            }
        )
    )

    # Validate successful generation
    assert result.success

    # NDA output should contain
    # expected template content
    assert (
        "NON-DISCLOSURE AGREEMENT"
        in result.data
    )

    # Verify NDA persistence
    assert (
        len(
            repo.get_by_type(
                "nda_contract"
            )
        )
        == 1
    )