# features/venue_profiles/presentation/ui.py

# Streamlit UI framework
import streamlit as st

# Strongly-typed venue model
from core.models.venue_profile import (
    VenueProfile,
)


def render_venue_profiles(
    container,
):
    """
    Render the Venue Profiles interface.
    """

    st.title(
        "Venue Profiles"
    )

    profiles = (
        container
        .venue_profile_service
        .get_all_profiles()
    )

    profile_names = [

        profile["name"]

        for profile in profiles
    ]

    st.subheader(
        "Load Existing Venue"
    )

    selected_profile = st.selectbox(

        "Select Venue",

        options=[
            "New Venue",
            *profile_names,
        ],
    )

    loaded_profile = None

    if selected_profile != "New Venue":

        loaded_profile = (
            container
            .venue_profile_service
            .get_profile_by_venue(
                selected_profile
            )
        )

    st.divider()

    st.subheader(
        "Venue Details"
    )

    venue_name = st.text_input(

        "Venue Name",

        value=(
            loaded_profile.venue_name
            if loaded_profile
            else ""
        ),
    )

    city = st.text_input(

        "City",

        value=(
            loaded_profile.city
            if loaded_profile
            else ""
        ),
    )

    venue_address = st.text_area(

        "Venue Address",

        value=(
            loaded_profile.venue_address
            if loaded_profile
            else ""
        ),
    )

    venue_capacity = st.text_input(

        "Venue Capacity",

        value=(
            loaded_profile.venue_capacity
            if loaded_profile
            else ""
        ),
    )

    venue_notes = st.text_area(

        "Venue Notes",

        value=(
            loaded_profile.venue_notes
            if loaded_profile
            else ""
        ),
    )

    if st.button(
        "Save Venue Profile"
    ):

        if not venue_name.strip():

            st.error(
                "Venue name is required."
            )

        else:

            profile = VenueProfile(

                venue_name=venue_name,

                city=city,

                venue_address=(
                    venue_address
                ),

                venue_capacity=(
                    venue_capacity
                ),

                venue_notes=(
                    venue_notes
                ),
            )

            if loaded_profile:

                original_record = next(

                    (
                        record

                        for record
                        in profiles

                        if record["name"]

                        ==

                        selected_profile
                    ),

                    None,
                )

                if original_record:

                    (
                        container
                        .venue_profile_service
                        .update_profile(
                            original_record["id"],
                            profile,
                        )
                    )

                    st.success(
                        "Venue updated."
                    )

            else:

                (
                    container
                    .venue_profile_service
                    .create_profile(
                        profile
                    )
                )

                st.success(
                    "Venue saved."
                )

            st.rerun()

    st.divider()

    st.subheader(
        "Existing Venues"
    )

    if not profiles:

        st.info(
            "No venue profiles found."
        )

        return

    for record in profiles:

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.write(
                f"🏟️ {record['name']}"
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
                    .venue_profile_service
                    .delete_profile(
                        record["id"]
                    )
                )

                st.success(
                    "Venue deleted."
                )

                st.rerun()