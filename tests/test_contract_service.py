from datetime import date
from io import BytesIO
from zipfile import ZipFile
import re


def docx_text(content):
    """
    Extract searchable text from generated DOCX bytes.
    """

    with ZipFile(BytesIO(content)) as archive:
        xml = archive.read(
            "word/document.xml"
        ).decode("utf-8")

    # DOCX text is XML, so remove tags after converting
    # paragraph breaks into searchable whitespace.
    xml = xml.replace("</w:p>", "\n")

    return re.sub("<[^>]+>", "", xml)


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


def test_single_contract_renders_schedule(
    contract_service,
    performance_payload
):
    """
    Verify single-show schedules fill the single template.
    """

    payload = {
        **performance_payload,
        "shows": [
            {
                "schedules": [
                    {
                        "type": "Opening",
                        "time": "12:00 AM",
                    },
                    {
                        "type": "Closing",
                        "time": "3:00 AM",
                    },
                ],
            }
        ],
    }

    result = (
        contract_service
        .create_performance_contract(payload)
    )

    text = docx_text(result.data)

    assert "Opening = 12:00 AM" in text
    assert "Closing = 3:00 AM" in text


def test_multi_contract_renders_schedule(
    contract_service,
    performance_payload
):
    """
    Verify multi-show schedules fill each show section.
    """

    payload = {
        **performance_payload,
        "number_of_shows": 2,
        "shows": [
            {
                "city": "Miami",
                "venue": "Arena 1",
                "date": date(2026, 5, 1),
                "schedules": [
                    {
                        "type": "Opening",
                        "time": "12:00 AM",
                    },
                ],
            },
            {
                "city": "Orlando",
                "venue": "Arena 2",
                "date": date(2026, 5, 2),
                "schedule": [
                    {
                        "type": "Closing",
                        "time": "3:00 AM",
                    },
                ],
            },
        ],
    }

    result = (
        contract_service
        .create_performance_contract(payload)
    )

    text = docx_text(result.data)

    assert "Opening = 12:00 AM" in text
    assert "Closing = 3:00 AM" in text


def test_contract_renders_ticketing_fee_summary(
    contract_service,
    performance_payload
):
    """
    Verify ticketing fee percent and amount fill the DOCX summary.
    """

    payload = {
        **performance_payload,
        "ticketing_fee_percent": 10,
        "shows": [
            {
                "ticket_rows": [
                    {
                        "label": "General Admission",
                        "total": 100,
                        "comps_kills": 0,
                        "price": 20,
                        "line_total": 2000,
                    },
                ],
                "gross_potential": 2000,
                "net_potential": 1800,
                "ticketing_fee_percent": 10,
                "ticketing_fee_amount": 200,
            }
        ],
    }

    result = (
        contract_service
        .create_performance_contract(payload)
    )

    text = docx_text(result.data)

    assert "Ticketing Fees" in text
    assert "10% ($ 200)" in text
    assert "$ 2,000" in text
    assert "$ 1,800" in text


def test_contract_renders_approved_walkout_section(
    contract_service,
    performance_payload
):
    """
    Verify approved production expenses include walkout data.
    """

    payload = {
        **performance_payload,
        "shows": [
            {
                "expenses": {
                    "walkout_potential": 1500,
                },
            }
        ],
    }

    result = (
        contract_service
        .create_performance_contract(payload)
    )

    text = docx_text(result.data)

    assert "APPROVED PRODUCTION EXPENSES" in text
    assert "Approved Walkout: $ 1,500" in text


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
