# features/deal_profiles/presentation/ui.py

# Streamlit UI framework
from features.deal_profiles.presentation.sections.general import (
    render_general_section,
)

from features.deal_profiles.presentation.sections.deal_terms import (
    render_deal_terms_section,
)

from features.deal_profiles.presentation.sections.notes import (
    render_notes_section,
)
import streamlit as st

from core.models.deal_profile import (
    DealProfile,
)


def render_deal_profiles(
    container,
):
    """
    Render the Deal Profiles interface.
    """

    st.title(
        "Deal Profiles"
    )

    profiles = (
        container
        .deal_profile_service
        .get_profiles()
    )

    st.subheader(
        "Load Existing Profile"
    )

    profile_names = [

        "New Deal Profile"

    ] + [

        profile["name"]

        for profile in profiles

    ]

    selected_profile = st.selectbox(

        "Deal Profile",

        options=profile_names,

    )

    loaded_profile = None

    selected_record = None

    if (

        selected_profile

        !=

        "New Deal Profile"

    ):

        selected_record = next(

            (

                profile

                for profile in profiles

                if (

                    profile["name"]

                    ==

                    selected_profile

                )

            ),

            None,

        )

        if selected_record:

            loaded_profile = (

                DealProfile.from_dict(

                    selected_record[
                        "content"
                    ]

                )

            )

    st.divider()

    general = (
        render_general_section(
            loaded_profile,
        )
    )

    deal_terms = (
        render_deal_terms_section(
            loaded_profile,
        )
    )

    notes = (
        render_notes_section(
            loaded_profile,
        )
    )

    if st.button(

        "Save Profile",

    ):

        if not general[
            "profile_name"
        ].strip():

            st.error(
                "Profile Name is required."
            )

            return
        
        profile = DealProfile(

            profile_name=(

                general[
                    "profile_name"
                ]

            ),

            base_deal_type=(

                general[
                    "base_deal_type"
                ]

            ),

            flat_guarantee=(

                deal_terms[
                    "flat_guarantee"
                ]

            ),

            percentage=(

                deal_terms[
                    "percentage"
                ]

            ),

            deal_basis=(

                deal_terms[
                    "deal_basis"
                ]

            ),

            minimum_guarantee=(

                deal_terms[
                    "minimum_guarantee"
                ]

            ),

            notes=(

                notes[
                    "notes"
                ]

            ),

        )

        container.deal_profile_service.save_profile(

            profile,

            record_id=(

                selected_record["id"]

                if selected_record

                else None

            ),

        )

        st.success(
            "Deal Profile saved."
        )

        st.rerun()

        st.divider()

    st.subheader(
        "Existing Profiles"
    )

    if not profiles:

        st.info(
            "No deal profiles found."
        )

        return

    for record in profiles:

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.write(
                f"💼 {record['name']}"
            )

        with col2:

            if st.button(

                "Delete",

                key=(
                    f"delete_"
                    f"{record['id']}"
                ),

            ):

                container.deal_profile_service.delete_profile(

                    record["id"]

                )

                st.success(
                    "Profile deleted."
                )

                st.rerun()