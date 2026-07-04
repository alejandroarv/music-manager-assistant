# features/contracts/presentation/sections/venue_profile_autofill.py

# Streamlit UI framework
import streamlit as st


def render_venue_profile_autofill(
    key_prefix,
    container,
    venue_key=None,
    city_key=None,
    venue_address_key=None,
    capacity_key=None,
):
    """
    Render venue profile selector and
    populate venue-related contract fields.

    Returns:
        str: Selected venue profile
    """

     # Default to the primary contract fields
    if venue_key is None:

        venue_key = (
            f"{key_prefix}_venue"
        )

    if city_key is None:

        city_key = (
            f"{key_prefix}_city"
        )

    if venue_address_key is None:

        venue_address_key = (
            f"{key_prefix}_venue_address"
        )

    if capacity_key is None:

        capacity_key = (
            f"{key_prefix}_capacity"
        )

    # Retrieve saved venue profiles
    profiles = (
        container
        .venue_profile_service
        .get_all_profiles()
    )

    # Build dropdown list
    profile_names = [
        profile["name"]
        for profile in profiles
    ]

    last_profile_key = (
        f"{key_prefix}_last_venue_profile"
    )

    selected_profile = st.selectbox(

        "Venue Profile",

        options=[
            "None",
            *profile_names,
        ],

        key=(
            f"{key_prefix}"
            "_venue_profile_selector"
        ),
    )

    if selected_profile == "None":

        st.session_state[
            last_profile_key
        ] = selected_profile

        return None

    profile = (
        container
        .venue_profile_service
        .get_profile_by_venue(
            selected_profile
        )
    )

    # Only autofill when the selected
    # venue profile actually changes
    if (
        profile
        and
        st.session_state.get(
            last_profile_key
        ) != selected_profile
    ):

        # Populate venue identity fields
        # before their widgets render
        st.session_state[
            venue_key
        ] = profile.venue_name

        st.session_state[
            city_key
        ] = profile.city

        st.session_state[
            venue_address_key
        ] = profile.venue_address

        st.session_state[
            capacity_key
        ] = profile.venue_capacity

        # Reset synchronized field flags
        # so venue autofill can propagate
        # into dependent show sections
        sync_target_keys = [
            city_key,
            venue_key,
            venue_address_key,
            capacity_key,
        ]

        sync_reset_keys = []

        for target_key in sync_target_keys:

            sync_reset_keys.append(
                f"{target_key}_touched"
            )

            sync_reset_keys.append(
                f"{target_key}_last_source"
            )

        for reset_key in sync_reset_keys:

            if reset_key.endswith(
                "_last_source"
            ):

                st.session_state.pop(
                    reset_key,
                    None,
                )

            else:

                st.session_state[
                    reset_key
                ] = False

        # Save selected profile state
        st.session_state[
            last_profile_key
        ] = selected_profile

        # Force rerun so populated
        # values appear immediately
        st.rerun()

    return profile
