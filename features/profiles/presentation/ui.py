# features/profiles/presentation/ui.py

# Streamlit UI framework
import streamlit as st

# Strongly-typed profile model
from core.models.artist_profile import (
    ArtistProfile,
)

from features.profiles.presentation.sections.identity import (
    render_identity_section,
)

from features.profiles.presentation.sections.travel import (
    render_travel_section,
)

from features.profiles.presentation.sections.merchandising import (
    render_merchandising_section,
)

from features.profiles.presentation.sections.production import (
    render_production_section,
)

from features.profiles.presentation.sections.defaults import (
    render_defaults_section,
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


    identity = (
        render_identity_section(
            loaded_profile
        )
    )

    artist_name = (
        identity[
            "artist_name"
        ]
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

    defaults = (
        render_defaults_section(
            loaded_profile
        )
    )

    show_length = (
        defaults[
            "show_length"
        ]
    )

    travel = (
        render_travel_section(
            loaded_profile
        )
    )

    air_transportation = (
        travel[
            "air_transportation"
        ]
    )

    hotel_accommodations = (
        travel[
            "hotel_accommodations"
        ]
    )

    ground_transportation = (
        travel[
            "ground_transportation"
        ]
    )

    meals_incidentals = (
        travel[
            "meals_incidentals"
        ]
    )

    air_freight = (
        travel[
            "air_freight"
        ]
    )

    production_section = (
        render_production_section(
            loaded_profile
        )
    )

    production = (
        production_section[
            "production"
        ]
    )

    catering = (
        production_section[
            "catering"
        ]
    )

    special_provisions = (
        production_section[
            "special_provisions"
        ]
    )

    merchandising = (
        render_merchandising_section(
            loaded_profile
        )
    )

    merchandising_terms = (
        merchandising[
            "merchandising_terms"
        ]
    )

    concessionaire_fee = (
        merchandising[
            "concessionaire_fee"
        ]
    )

    seller = (
        merchandising[
            "seller"
        ]
    )

    hard_merchandising = (
        merchandising[
            "hard_merchandising"
        ]
    )

    soft_merchandising = (
        merchandising[
            "soft_merchandising"
        ]
    )

    complimentary_tickets = (
        merchandising[
            "complimentary_tickets"
        ]
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

                ground_transportation=(
                    ground_transportation
                ),

                meals_incidentals=(
                    meals_incidentals
                ),

                air_freight=(
                    air_freight
                ),

                production=production,

                catering=catering,
                
                merchandising_terms=(
                    merchandising_terms
                ),

                concessionaire_fee=(
                    concessionaire_fee
                ),

                seller=(
                    seller
                ),

                hard_merchandising=(
                    hard_merchandising
                ),

                soft_merchandising=(
                    soft_merchandising
                ),

                special_provisions=(
                    special_provisions
                ),

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