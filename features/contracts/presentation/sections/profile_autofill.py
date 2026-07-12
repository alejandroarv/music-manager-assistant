# features/contracts/presentation/sections/profile_autofill.py

# Streamlit UI framework
import streamlit as st

# Strongly-typed profile model
from core.models.artist_profile import (
    ArtistProfile,
)

from core.models.company_profile import (
    CompanyProfile,
)

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

    # Build display labels while keeping
    # the original profile records
    profile_options = {

        (
            f"{profile['content'].get('artist_name', '')}"
            f" — "
            f"{profile['content'].get('profile_name', 'Default')}"
        ): {

            "record": profile,

            "model": ArtistProfile.from_dict(
                profile["content"]
            ),

        }

        for profile in profiles

    }

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

            *profile_options.keys(),

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

        # Retrieve the selected profile
        # directly from the dropdown map
        selected_profile_data = (
            profile_options.get(
                selected_profile
            )
        )

        profile = (

            selected_profile_data["model"]

            if selected_profile_data

            else None

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

            capacities = defaults.get(
                "capacities",
                [],
            )

            for show_index in range(12):

                st.session_state[
                    (
                        f"{key_prefix}_capacity_default_"
                        f"{show_index}"
                    )
                ] = (
                    capacities[show_index]
                    if show_index < len(capacities)
                    else defaults.get(
                        "capacity",
                        "",
                    )
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
            ]

            sync_target_keys = [
                f"{key_prefix}_signatory",
            ]

            for show_index in range(12):

                sync_target_keys.extend(
                    [
                        (
                            f"{key_prefix}_show_city_"
                            f"{show_index}"
                        ),

                        (
                            f"{key_prefix}_show_venue_"
                            f"{show_index}"
                        ),

                        (
                            f"{key_prefix}_show_date_"
                            f"{show_index}"
                        ),

                        (
                            f"{key_prefix}_show_length_"
                            f"{show_index}"
                        ),

                        (
                            f"{key_prefix}_capacity_"
                            f"{show_index}"
                        ),

                        (
                            f"{key_prefix}_show_notes_"
                            f"{show_index}"
                        ),
                    ]
                )

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

def render_company_autofill(
    key_prefix,
    container,
):
    """
    Render company profile autofill controls
    and synchronize selected company data
    into Streamlit session state.
    """

    companies = (

        container
        .company_profile_service
        .get_all_profiles()

    )

    company_options = {

        company["name"]: {

            "record": company,

            "model": CompanyProfile.from_dict(

                company["content"]

            ),

        }

        for company in companies

    }

    last_company_key = (
        f"{key_prefix}_last_company"
    )

    selected_company = st.selectbox(

        "Company",

        options=[

            "None",

            *company_options.keys(),

        ],

        key=f"{key_prefix}_company_selector",

    )

    # Only autofill when the selected
    # company actually changes
    if (

        selected_company != "None"

        and

        st.session_state.get(
            last_company_key
        ) != selected_company

    ):

        selected_company_data = (

            company_options.get(
                selected_company
            )

        )

        profile = (

            selected_company_data["model"]

            if selected_company_data

            else None

        )

        if profile:

            defaults = (

                container
                .company_profile_service
                .build_form_defaults(
                    profile
                )

            )

            st.session_state[
                f"{key_prefix}_company_name"
            ] = defaults.get(
                "company_name",
                "",
            )

            st.session_state[
                f"{key_prefix}_company_address"
            ] = defaults.get(
                "company_address",
                "",
            )
            
            st.session_state[
                last_company_key
            ] = selected_company

            st.rerun()