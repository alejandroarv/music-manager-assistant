# features/contracts/presentation/sections/deal_structure.py

# Streamlit UI framework
import streamlit as st

from core.constants import (
    DEAL_TYPES,
    DEAL_BASIS_OPTIONS,
)

from core.models.deal_profile import (
    DealProfile,
)

from utils.synced_widgets import (
    render_synced_number_input,
    render_synced_selectbox,
)

def render_deal_structure_section(
    key_prefix,
    container,
):
    """
    Render performance deal configuration.

    Responsibilities:
    - Select deal type
    - Collect deal-specific values

    Returns:
        dict: Normalized deal configuration
    """

    st.markdown(
        "### Deal Structure"
    )

    deal_profiles = (
        container
        .deal_profile_service
        .get_profiles()
    )

    profile_options = [

        "None",

    ] + [

        profile["name"]

        for profile in deal_profiles

    ]

    selected_profile = st.selectbox(

        "Deal Profile",

        options=profile_options,

        key=f"{key_prefix}_deal_profile",

    )

    loaded_profile = None

    if selected_profile != "None":

        selected_record = next(

            (

                profile

                for profile in deal_profiles

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

    deal_type = (
        render_synced_selectbox(

            label="Base Deal",

            source_value=(

                loaded_profile.base_deal_type

                if loaded_profile

                else DEAL_TYPES[0]

            ),

            options=DEAL_TYPES,

            key=(
                f"{key_prefix}"
                f"_deal_type"
            ),

            touched_key=(
                f"{key_prefix}"
                f"_deal_type_touched"
            ),

        )
    )

    flat_guarantee = 0.0

    percentage = 0.0

    deal_basis = "Net"


    if deal_type == "Flat Guarantee":

        flat_guarantee = (
            render_synced_number_input(

                label="Flat Guarantee",

                source_value=(

                    loaded_profile.flat_guarantee

                    if loaded_profile

                    else 0.0

                ),

                key=(
                    f"{key_prefix}"
                    f"_flat_guarantee"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_flat_guarantee_touched"
                ),

                min_value=0.0,

                step=100.0,

            )
        )

    elif deal_type == "Versus Deal":

        st.info(
            "Artist receives whichever is greater: the minimum guarantee or the percentage deal."
        )

        flat_guarantee = (
            render_synced_number_input(

                label="Minimum Guarantee",

                source_value=(

                    loaded_profile.flat_guarantee

                    if loaded_profile

                    else 0.0

                ),

                key=(
                    f"{key_prefix}"
                    f"_flat_guarantee"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_flat_guarantee_touched"
                ),

                min_value=0.0,

                step=100.0,

            )
        )

        percentage = (
            render_synced_number_input(

                label="Artist Percentage",

                source_value=(

                    loaded_profile.percentage

                    if loaded_profile

                    else 85.0

                ),

                key=(
                    f"{key_prefix}"
                    f"_percentage"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_percentage_touched"
                ),

                min_value=0.0,

                max_value=100.0,

                step=1.0,

            )
        )

        deal_basis = (
            render_synced_selectbox(

                label="Percentage Based On",

                source_value=(

                    loaded_profile.deal_basis

                    if loaded_profile

                    else DEAL_BASIS_OPTIONS[0]

                ),

                options=DEAL_BASIS_OPTIONS,

                key=(
                    f"{key_prefix}"
                    f"_deal_basis"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_deal_basis_touched"
                ),

            )
        )

    elif deal_type == "Percentage Deal":

        percentage = (
            render_synced_number_input(

                label="Artist Percentage",

                source_value=(

                    loaded_profile.percentage

                    if loaded_profile

                    else 85.0

                ),

                key=(
                    f"{key_prefix}"
                    f"_percentage"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_percentage_touched"
                ),

                min_value=0.0,

                max_value=100.0,

                step=1.0,

            )
        )

        deal_basis = (
            render_synced_selectbox(

                label="Percentage Based On",

                source_value=(

                    loaded_profile.deal_basis

                    if loaded_profile

                    else DEAL_BASIS_OPTIONS[0]

                ),

                options=DEAL_BASIS_OPTIONS,

                key=(
                    f"{key_prefix}"
                    f"_deal_basis"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_deal_basis_touched"
                ),

            )
        )


    elif deal_type == "Door Deal":

        percentage = (
            render_synced_number_input(

                label="Artist Percentage",

                source_value=(

                    loaded_profile.percentage

                    if loaded_profile

                    else 100.0

                ),

                key=(
                    f"{key_prefix}"
                    f"_percentage"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_percentage_touched"
                ),

                min_value=0.0,

                max_value=100.0,

                step=1.0,

            )
        )

    elif deal_type == "Buyout":

        flat_guarantee = (
            render_synced_number_input(

                label="Buyout Amount",

                source_value=(

                    loaded_profile.flat_guarantee

                    if loaded_profile

                    else 0.0

                ),

                key=(
                    f"{key_prefix}"
                    f"_flat_guarantee"
                ),

                touched_key=(
                    f"{key_prefix}"
                    f"_flat_guarantee_touched"
                ),

                min_value=0.0,

                step=100.0,

            )
        )

    return {

        "deal_type": deal_type,

        "flat_guarantee": flat_guarantee,

        "percentage": percentage,

        "deal_basis": deal_basis,

    }