from datetime import date


def test_create_single_performance_contract(contract_service, repo, performance_payload):
    result = contract_service.create_performance_contract(performance_payload)

    assert result.success
    assert isinstance(result.data, bytes)

    records = repo.get_by_type("performance_contract")
    assert len(records) == 1
    assert records[0]["content"]["template"] == "performance_single"


def test_create_multi_performance_contract(contract_service, repo, performance_payload):
    payload = {
        **performance_payload,
        "number_of_shows": 3,
        "shows": [
            {"city": "Miami", "venue": "Arena 1", "date": date(2026, 5, 1), "time": "8:00 PM"},
            {"city": "Orlando", "venue": "Arena 2", "date": date(2026, 5, 2), "time": "9:00 PM"},
            {"city": "Tampa", "venue": "Arena 3", "date": date(2026, 5, 3), "time": "7:30 PM"},
        ],
    }

    result = contract_service.create_performance_contract(payload)

    assert result.success
    records = repo.get_by_type("performance_contract")
    assert records[0]["content"]["template"] == "performance_multi"
    assert len(records[0]["content"]["shows"]) == 3


def test_create_nda_contract(contract_service, repo):
    result = contract_service.create_nda_contract(
        {
            "disclosing_party": "Company A",
            "receiving_party": "Company B",
            "purpose": "Testing NDA generation flow",
            "duration": 6,
        }
    )

    assert result.success
    assert "NON-DISCLOSURE AGREEMENT" in result.data
    assert len(repo.get_by_type("nda_contract")) == 1
