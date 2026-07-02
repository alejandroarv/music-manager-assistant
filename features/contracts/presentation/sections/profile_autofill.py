# features/contracts/presentation/sections/profile_autofill.py

# Streamlit UI framework
import streamlit as st


def render_profile_autofill(
    key_prefix,
    container,
):
    """
    Render artist profile autofill controls
    and synchronize selected profile data
    into Streamlit session state.

    Responsibilities:
    - render profile selector
    - load selected profile
    - map profile defaults
    - populate session-state values
    - protect manual user edits

    Returns:
        str: Selected profile name
    """


    # Retrieve Saved Profiles
    profiles = (
        container.profile_service
        .get_all_profiles()
    )

    # Build dropdown options
    profile_names = [
        profile["name"]
        for profile in profiles
    ]

    # Session-state key used to prevent
    # repeated autofill overwrites
    last_profile_key = (
        f"{key_prefix}_last_profile"
    )


    # Profile Selector
    selected_profile = st.selectbox(
        "Artist Profile",

        options=[
            "None",
            *profile_names,
        ],

        key=f"{key_prefix}_profile_selector",
    )


    # Autofill Synchronization

    # Only autofill when the selected
    # profile actually changes
    if (
        selected_profile != "None"
        and
        st.session_state.get(
            last_profile_key
        ) != selected_profile
    ):

        # Load selected artist profile
        profile = (
            container.profile_service
            .get_profile_by_artist(
                selected_profile
            )
        )

        if profile:

            # Convert profile into reusable
            # form default values
            defaults = (
                container.profile_service
                .build_form_defaults(
                    profile
                )
            )

            # Core Identity Fields
            st.session_state[
                f"{key_prefix}_company_name"
            ] = defaults.get(
                "company_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_artist"
            ] = defaults.get(
                "artist_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_purchaser_name"
            ] = defaults.get(
                "purchaser_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_purchaser_address"
            ] = defaults.get(
                "purchaser_address",
                "",
            )

            st.session_state[
                f"{key_prefix}_signatory"
            ] = defaults.get(
                "signatory",
                "",
            )

            st.session_state[
                f"{key_prefix}_company_address"
            ] = defaults.get(
                "company_address",
                "",
            )


            # Terms & Logistics
            st.session_state[
                f"{key_prefix}_air_transportation"
            ] = defaults.get(
                "air_transportation",
                "",
            )

            st.session_state[
                f"{key_prefix}_hotel_accommodations"
            ] = defaults.get(
                "hotel_accommodations",
                "",
            )

            st.session_state[
                f"{key_prefix}_ground_transportation"
            ] = defaults.get(
                "ground_transportation",
                "",
            )

            st.session_state[
                f"{key_prefix}_meals_incidentals"
            ] = defaults.get(
                "meals_incidentals",
                "",
            )

            st.session_state[
                f"{key_prefix}_air_freight"
            ] = defaults.get(
                "air_freight",
                "",
            )
            
            st.session_state[
                f"{key_prefix}_special_provisions"
            ] = defaults.get(
                "special_provisions",
                "",
            )

            st.session_state[
                f"{key_prefix}_production"
            ] = defaults.get(
                "production",
                "",
            )

            st.session_state[
                f"{key_prefix}_catering"
            ] = defaults.get(
                "catering",
                "",
                
            )
            st.session_state[
                f"{key_prefix}_concessionaire_fee"
            ] = defaults.get(
                "concessionaire_fee",
                "",
            )

            st.session_state[
                f"{key_prefix}_seller"
            ] = defaults.get(
                "seller",
                "",
            )

            st.session_state[
                f"{key_prefix}_hard_merchandising"
            ] = defaults.get(
                "hard_merchandising",
                "",
            )

            st.session_state[
                f"{key_prefix}_soft_merchandising"
            ] = defaults.get(
                "soft_merchandising",
                "",
            )

            st.session_state[
                f"{key_prefix}_merchandising_terms"
            ] = defaults.get(
                "merchandising_terms",
                "",
            )

            st.session_state[
                f"{key_prefix}_complimentary_tickets"
            ] = defaults.get(
                "complimentary_tickets",
                "",
            )

            # Core show defaults
            st.session_state[
                f"{key_prefix}_venue"
            ] = defaults.get(
                "venue",
                "",
            )

            st.session_state[
                f"{key_prefix}_city"
            ] = defaults.get(
                "city",
                "",
            )

            st.session_state[
                f"{key_prefix}_capacity"
            ] = defaults.get(
                "capacity",
                "",
            )

            st.session_state[
                f"{key_prefix}_notes"
            ] = defaults.get(
                "notes",
                "",
            )

            # Restore default show length
            show_length = defaults.get(
                "show_length",
                "90 Minutes",
            )

            # Split formatted value into
            # numeric + unit session fields
            parts = show_length.split()

            if len(parts) >= 2:

                try:

                    st.session_state[
                        f"{key_prefix}_show_length_value"
                    ] = int(parts[0])

                except ValueError:

                    st.session_state[
                        f"{key_prefix}_show_length_value"
                    ] = 90

                unit = parts[1]

                # Normalize plural form
                if not unit.endswith("s"):

                    unit += "s"

                st.session_state[
                    f"{key_prefix}_show_length_unit"
                ] = unit

            # Reset synchronized show fields
            # so profile autofill propagates
            # into dependent show sections
            sync_reset_keys = [
                f"{key_prefix}_signatory_touched",

                f"{key_prefix}_show_city_0_touched",
                f"{key_prefix}_show_venue_0_touched",
                f"{key_prefix}_show_date_0_touched",
                f"{key_prefix}_show_length_0_touched",
                f"{key_prefix}_capacity_0_touched",
                f"{key_prefix}_show_notes_0_touched",
            ]

            for reset_key in sync_reset_keys:

                st.session_state[
                    reset_key
                ] = False

            # Prevent Company Name sync
            # from overwriting profile values.
            st.session_state[
                f"{key_prefix}_profile_loaded"
            ] = True
            
            # Save selected profile state
            st.session_state[
                last_profile_key
            ] = selected_profile

            # Force rerun so populated
            # values appear immediately
            st.rerun()

    return selected_profile