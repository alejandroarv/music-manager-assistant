# core/container.py

# Infrastructure layer
from core.infrastructure.storage import Storage

# Repository layer
from core.repositories.record_repository import RecordRepository

# Application services
from features.tour.application.service import TourService
from features.history.application.service import HistoryService
from features.booking.application.service import BookingService
from features.contracts.application.service import ContractService
from features.profiles.application.service import (
    ProfileService,
)

from features.venue_profiles.application.service import (
    VenueProfileService,
)
# Application configuration
from core.config import settings

from features.companies.application.service import (
    CompanyProfileService,
)
from features.deal_profiles.application.service import (
    DealProfileService,
)

class Container:
    """
    Central dependency injection container for the application.

    Responsibilities:
    - Initialize shared infrastructure components
    - Wire dependencies between application layers
    - Provide centralized access to services
    - Maintain consistent application state

    This container reduces tight coupling by ensuring
    services depend on abstractions and shared instances
    rather than creating dependencies directly.
    """

    def __init__(self):

        # Infrastructure layer
        # Handles low-level persistence operations
        self.storage = Storage(
            settings.STORAGE_FILE
        )

        # Repository layer
        # Provides an abstraction over persistence logic
        self.record_repository = RecordRepository(
            self.storage
        )

        # Application services
        # Shared repository access ensures consistent
        # persistence behavior across all features
        self.tour_service = TourService(
            self.record_repository
        )

        # Historical record viewing and retrieval service
        self.history_service = HistoryService(
            self.record_repository
        )

        # Contract generation and management service
        self.contract_service = ContractService(
            self.record_repository
        )

        # Booking service depends on contract generation
        # in addition to repository access
        self.booking_service = BookingService(
            self.record_repository,
            self.contract_service
        )

        # Artist profile management service
        # handles profile creation, persistence, reusable artist 
        # defaults, and future contract autofill support
        self.profile_service = ProfileService(
            self.record_repository
        )

        self.venue_profile_service = (
            VenueProfileService(
                self.record_repository
            )
        )

        self.company_profile_service = (
            CompanyProfileService(
                self.record_repository,
            )
        )

        self.deal_profile_service = (
            DealProfileService(
                self.record_repository,
            )
        )