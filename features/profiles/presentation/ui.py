# features/profiles/presentation/ui.py

# Streamlit UI framework
import streamlit as st

# Strongly-typed profile model
from core.models.artist_profile import (
    ArtistProfile,
)


def render_profiles(container):
    """
    Render the Artist Profiles interface.
    """

    # Page Header
    st.title("Artist Profiles")


    # Retrieve Existing Profiles
    profiles = (
        container.profile_service
        .get_all_profiles()
    )

    # Build profile selection list
    profile_names = [
        profile["name"]
        for profile in profiles
    ]

    # Profile Selection
    st.subheader("Load Existing Profile")

    selected_profile = st.selectbox(
        "Select Profile",
        options=[
            "New Profile",
            *profile_names,
        ],
    )

    # Default form values
    loaded_profile = None

    # Load selected profile
    if selected_profile != "New Profile":

        loaded_profile = (
            container.profile_service
            .get_profile_by_artist(
                selected_profile
            )
        )


    # Profile Form
    st.divider()

    st.subheader("Profile Details")

    # Prefill fields when profile exists
    artist_name = st.text_input(
        "Artist Name",
        value=(
            loaded_profile.artist_name
            if loaded_profile
            else ""
        ),
    )

    company_name = st.text_input(
        "Company Name",
        value=(
            loaded_profile.company_name
            if loaded_profile
            else ""
        ),
    )

    # Core Contract Identity Fields
    company_address = st.text_area(
        "Company Address",

        value=(
            loaded_profile.company_address
            if loaded_profile
            else ""
        ),
    )

    # Show length field
    show_length = st.text_input(
        "Default Show Length",

        value=(
            loaded_profile.show_length
            if loaded_profile
            else "90 Minutes"
        ),
    )

    # Travel & Hospitality Defaults
    st.markdown(
        "### Travel & Hospitality"
    )

    air_transportation = st.text_input(
        "Air Transportation",

        value=(
            loaded_profile.air_transportation
            if loaded_profile
            else ""
        ),
    )

    hotel_accommodations = st.text_input(
        "Hotel Accommodations",

        value=(
            loaded_profile.hotel_accommodations
            if loaded_profile
            else ""
        ),
    )

    ground_transportation = st.text_input(
        "Ground Transportation",

        value=(
            loaded_profile.ground_transportation
            if loaded_profile
            else ""
        ),
    )

    air_freight = st.selectbox(
        "Air Freight & Excess Baggage",

        options=[
            "Included",
            "Half Covered",
            "Not Included",
            "Custom",
        ],

        index=(
            [
                "Included",
                "Half Covered",
                "Not Included",
                "Custom",
            ].index(
                loaded_profile.air_freight
            )
            if (
                loaded_profile
                and loaded_profile.air_freight
                in [
                    "Included",
                    "Half Covered",
                    "Not Included",
                    "Custom",
                ]
            )
            else 2
        ),
    )

    # Reusable Contract Clauses
    st.markdown(
        "### Contract Clauses"
    )

    production = st.text_area(
        "Production",

        value=(
            loaded_profile.production
            if loaded_profile
            else ""
        ),
    )

    catering = st.text_area(
        "Catering",

        value=(
            loaded_profile.catering
            if loaded_profile
            else ""
        ),
    )
    merchandising_terms = st.text_area(
        "Merchandising Terms",

        value=(
            loaded_profile.merchandising_terms
            if loaded_profile
            else ""
        ),
    )

    special_provisions = st.text_area(
        "Special Provisions",

        value=(
            loaded_profile.special_provisions
            if loaded_profile
            else ""
        ),
    )

    complimentary_tickets = st.selectbox(
        "Complimentary Tickets",

        options=[
            "None",
            "10 Tickets",
            "20 Tickets",
            "50 Tickets",
            "Custom",
        ],

        index=(
            [
                "None",
                "10 Tickets",
                "20 Tickets",
                "50 Tickets",
                "Custom",
            ].index(
                loaded_profile.complimentary_tickets
            )
            if (
                loaded_profile
                and loaded_profile.complimentary_tickets
                in [
                    "None",
                    "10 Tickets",
                    "20 Tickets",
                    "50 Tickets",
                    "Custom",
                ]
            )
            else 0
        ),
    )

    # Save / Update Logic
    if st.button("Save Profile"):

        # Basic validation
        if not artist_name.strip():

            st.error(
                "Artist name is required."
            )

        else:

            # Build updated profile model
            profile = ArtistProfile(

                artist_name=artist_name,

                company_name=company_name,

                company_address=company_address,

                show_length=show_length,

                air_transportation=air_transportation,

                hotel_accommodations=hotel_accommodations,

                ground_transportation=ground_transportation,

                air_freight=air_freight,

                production=production,

                catering=catering,
                
                merchandising_terms=merchandising_terms,

                special_provisions=special_provisions,

                complimentary_tickets=(
                    complimentary_tickets
                ),
            )

            # Update Existing Profile
            if loaded_profile:

                # Find original record ID
                original_record = next(
                    (
                        record
                        for record in profiles
                        if record["name"]
                        ==
                        selected_profile
                    ),
                    None,
                )

                if original_record:

                    container.profile_service.update_profile(
                        original_record["id"],
                        profile,
                    )

                    st.success(
                        "Profile updated."
                    )

            # Create New Profile
            else:

                container.profile_service.create_profile(
                    profile
                )

                st.success(
                    "Profile saved."
                )

            # Refresh UI immediately
            st.rerun()


    # Existing Profiles
    st.divider()

    st.subheader("Existing Profiles")

    if not profiles:

        st.info(
            "No artist profiles found."
        )

        return

    # Display saved profiles
    for record in profiles:

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"🎤 {record['name']}"
            )

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{record['id']}"
            ):

                container.profile_service.delete_profile(
                    record["id"]
                )

                st.success(
                    "Profile deleted."
                )

                st.rerun()