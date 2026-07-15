# features/deal_profiles/presentation/sections/deal_terms.py

import streamlit as st

def render_deal_terms_section(
    loaded_profile,
):
    """
    Render deal terms.
    """

    st.subheader(
        "Deal Terms"
    )

    flat_guarantee = st.number_input(

        "Flat Guarantee",

        min_value=0.0,

        step=100.0,

        value=(

            loaded_profile.flat_guarantee

            if loaded_profile

            else 0.0

        ),

    )

    percentage = st.number_input(

        "Artist Percentage",

        min_value=0.0,

        max_value=100.0,

        step=1.0,

        value=(

            loaded_profile.percentage

            if loaded_profile

            else 0.0

        ),

    )

    deal_basis = st.selectbox(

        "Deal Basis",

        options=[

            "Net",

            "Gross",

        ],

        index=(

            0

            if (

                not loaded_profile

                or

                loaded_profile.deal_basis

                == "Net"

            )

            else 1

        ),

    )

    minimum_guarantee = st.number_input(

        "Minimum Guarantee",

        min_value=0.0,

        step=100.0,

        value=(

            loaded_profile.minimum_guarantee

            if loaded_profile

            else 0.0

        ),

    )

    return {

        "flat_guarantee": (
            flat_guarantee
        ),

        "percentage": (
            percentage
        ),

        "deal_basis": (
            deal_basis
        ),

        "minimum_guarantee": (
            minimum_guarantee
        ),

    }