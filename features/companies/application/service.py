# features/companies/application/service.py

# Record type constant used for company profile persistence
from core.constants import COMPANY_PROFILE

# Strongly-typed company profile model
from core.models.company_profile import (
    CompanyProfile,
)

# Generic persistence record model
from core.models.record import Record


class CompanyProfileService:
    """
    Application service responsible for
    company profile operations.

    Responsibilities:
    - create company profiles
    - retrieve company profiles
    - update company profiles
    - delete company profiles
    """

    def __init__(
        self,
        record_repository,
    ):

        self.record_repository = (
            record_repository
        )

    def create_profile(
        self,
        profile: CompanyProfile,
    ):
        """
        Persist a company profile.
        """

        record = Record(

            type=COMPANY_PROFILE,

            name=profile.company_name,

            content=profile.to_dict(),

            metadata={
                "company": profile.company_name,
            },
        )

        self.record_repository.save(
            record
        )

        return record

    def get_all_profiles(
        self,
    ):
        """
        Retrieve all saved company profiles.
        """

        records = (
            self.record_repository
            .get_by_type(
                COMPANY_PROFILE
            )
        )

        profiles = []

        for record in records:

            profiles.append({

                "id": record.get("id"),

                "name": record.get("name"),

                "content": record.get(
                    "content",
                    {},
                ),

                "metadata": record.get(
                    "metadata",
                    {},
                ),

                "timestamp": record.get(
                    "timestamp"
                ),
            })

        return profiles

    def get_profile_by_company(
        self,
        company_name,
    ):
        """
        Retrieve a company profile
        by company name.
        """

        profiles = (
            self.record_repository
            .get_by_type(
                COMPANY_PROFILE
            )
        )

        for record in profiles:

            if (

                record.get(
                    "name",
                    ""
                ).strip().lower()

                ==

                company_name.strip().lower()

            ):

                return CompanyProfile.from_dict(
                    record.get(
                        "content",
                        {},
                    )
                )

        return None

    def delete_profile(
        self,
        record_id,
    ):
        """
        Delete a company profile.
        """

        self.record_repository.delete(
            record_id
        )

    def update_profile(
        self,
        record_id,
        updated_profile,
    ):
        """
        Update an existing company profile.
        """

        self.delete_profile(
            record_id
        )

        return self.create_profile(
            updated_profile
        )
    
    def build_form_defaults(
        self,
        profile: CompanyProfile,
    ):
        """
        Convert a company profile into
        reusable contract form defaults.

        This keeps autofill mapping logic
        centralized inside the service layer.
        """

        return {

            "company_name": (
                profile.company_name
            ),

            "company_address": (
                profile.company_address
            ),

        }
