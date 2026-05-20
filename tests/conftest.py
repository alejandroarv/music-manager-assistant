from datetime import date
from pathlib import Path
import uuid

import pytest

from core.infrastructure.storage import Storage

from core.repositories.record_repository import (
    RecordRepository,
)

from features.booking.application.service import (
    BookingService,
)

from features.contracts.application.service import (
    ContractService,
)

from features.history.application.service import (
    HistoryService,
)

from features.tour.application.service import (
    TourService,
)


@pytest.fixture
def repo():
    """
    Create an isolated repository instance
    backed by a temporary JSON storage file.

    Responsibilities:
    - Provide clean test persistence
    - Prevent shared state between tests
    - Automatically clean up test files
    """

    base_dir = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
    )

    # Generate unique temporary storage file
    file_path = (
        base_dir
        / f"test_{uuid.uuid4().hex}.json"
    )

    try:

        storage = Storage(str(file_path))

        yield RecordRepository(storage)

    finally:

        # Remove temporary test storage
        file_path.unlink(missing_ok=True)


@pytest.fixture
def contract_service(repo):
    """
    Provide a contract service instance
    for test scenarios.
    """

    return ContractService(repo)


@pytest.fixture
def booking_service(
    repo,
    contract_service
):
    """
    Provide a booking service instance
    with contract service dependencies.
    """

    return BookingService(
        repo,
        contract_service
    )


@pytest.fixture
def tour_service(repo):
    """
    Provide a tour service instance
    for test scenarios.
    """

    return TourService(repo)


@pytest.fixture
def history_service(repo):
    """
    Provide a history service instance
    for test scenarios.
    """

    return HistoryService(repo)


@pytest.fixture
def performance_payload():
    """
    Standardized performance contract payload
    used across test cases.

    Provides reusable baseline test data
    for booking and contract workflows.
    """

    return {
        "artist": "Test Artist",

        "client": "Test Client",

        "venue": "Test Arena",

        "date": date(2026, 5, 1),

        "city": "Miami",

        "fee": 10000,

        "number_of_shows": 1,
    }