# core/container.py

# Low-level infrastructure (data storage))
from core.infrastructure.storage import Storage

# Repository layer (abstracts data access)
from core.repositories.record_repository import RecordRepository

# Application/service layer (business logic)
from features.tour.application.service import TourService
from features.history.application.service import HistoryService
from features.booking.application.service import BookingService
from features.contracts.application.service import ContractService

# Configuration (e.g., file paths, settings)
from core.config import settings


class Container:
    """
    # Dependency injection container for the entire app
    # - It centralizes the creation of all core components
    # - Wires dependencies between layers
    # - Provides a single place to access services
    # This prevents
    # - Recreating objects multiple times
    # - Tight coupling between layers
    # - Messy imports across the app
    """
    def __init__(self):

        # Infrastrucrture layer
        # - handles raw data storage (e.g., JSON file, database)
        self.storage = Storage(settings.STORAGE_FILE)

        # Repository layer
        # - abstracts data storage and retrieval
        # - Services should never talk directly to storage
        self.record_repository = RecordRepository(self.storage)

        # Application layer services
        # - Each service receives the same repository
        # - This ensures consistent data access accross features

        # Core features
        self.tour_service = TourService(self.record_repository)
        self.history_service = HistoryService(self.record_repository)
        self.contract_service = ContractService(self.record_repository)

        # Booking feature services
        self.booking_service = BookingService(
            self.record_repository,
            self.contract_service
        )
