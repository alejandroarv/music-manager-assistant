# features/companies/presentation/ui.py

# Streamlit UI framework
import streamlit as st

# Strongly-typed company profile model
from core.models.company_profile import (
    CompanyProfile,
)

from features.companies.presentation.sections.identity import (
    render_identity_section,
)

def render_company_profiles(
    container,
):
    """
    Render the Company Profiles interface.
    """

    st.title(
        "Companies"
    )

    companies = (

        container
        .company_profile_service
        .get_all_profiles()

    )

    # Build company selection list
    company_names = [

        company["name"]

        for company in companies

    ]

    st.subheader(
        "Load Existing Company"
    )

    selected_company = st.selectbox(

        "Select Company",

        options=[

            "New Company",

            *company_names,

        ],

    )

    loaded_profile = None

    if (

        selected_company

        !=

        "New Company"

    ):

        loaded_profile = (

            container
            .company_profile_service
            .get_profile_by_company(

                selected_company

            )

        )
    st.divider()

    identity = (

        render_identity_section(
            loaded_profile
        )

    )

    company_name = (

        identity[
            "company_name"
        ]

    )

    company_address = (

        identity[
            "company_address"
        ]

    )

    company_notes = (

        identity[
            "company_notes"
        ]

    )

    # Save / Update Logic
    if st.button(
        "Save Company"
    ):

        if not company_name.strip():

            st.error(
                "Company name is required."
            )

        else:

            profile = CompanyProfile(

                company_name=company_name,

                company_address=(
                    company_address
                ),

                company_notes=(
                    company_notes
                ),

            )

            if loaded_profile:

                original_record = next(

                    (

                        record

                        for record

                        in companies

                        if (

                            record["name"]

                            ==

                            selected_company

                        )

                    ),

                    None,

                )

                if original_record:

                    (
                        container
                        .company_profile_service
                        .update_profile(

                            original_record["id"],

                            profile,

                        )

                    )

                    st.success(
                        "Company updated."
                    )

            else:

                (
                    container
                    .company_profile_service
                    .create_profile(
                        profile
                    )
                )

                st.success(
                    "Company saved."
                )

            st.rerun()

    st.divider()

    st.subheader(
        "Existing Companies"
    )

    if not companies:

        st.info(
            "No company profiles found."
        )

        return

    for record in companies:

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.write(
                f"🏢 {record['name']}"
            )

        with col2:

            if st.button(

                "Delete",

                key=(
                    f"delete_"
                    f"{record['id']}"
                ),

            ):

                (
                    container
                    .company_profile_service
                    .delete_profile(
                        record["id"]
                    )
                )

                st.success(
                    "Company deleted."
                )

                st.rerun()