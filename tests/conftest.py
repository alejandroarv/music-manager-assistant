from datetime import date
from pathlib import Path
import uuid

import pytest

from core.infrastructure.storage import Storage
from core.repositories.record_repository import RecordRepository
from features.booking.application.service import BookingService
from features.contracts.application.service import ContractService
from features.history.application.service import HistoryService
from features.tour.application.service import TourService


@pytest.fixture
def repo():
    base_dir = Path(__file__).resolve().parent.parent / "data"
    file_path = base_dir / f"test_{uuid.uuid4().hex}.json"
    try:
        storage = Storage(str(file_path))
        yield RecordRepository(storage)
    finally:
        file_path.unlink(missing_ok=True)


@pytest.fixture
def contract_service(repo):
    return ContractService(repo)


@pytest.fixture
def booking_service(repo, contract_service):
    return BookingService(repo, contract_service)


@pytest.fixture
def tour_service(repo):
    return TourService(repo)


@pytest.fixture
def history_service(repo):
    return HistoryService(repo)


@pytest.fixture
def performance_payload():
    return {
        "artist": "Test Artist",
        "client": "Test Client",
        "venue": "Test Arena",
        "date": date(2026, 5, 1),
        "city": "Miami",
        "fee": 10000,
        "number_of_shows": 1,
    }
