# features/profiles/presentation/merchandising.py

# Streamlit UI framework
import streamlit as st


def render_merchandising_section(
    loaded_profile,
):
    """
    Render merchandising-related
    profile defaults.

    Returns:
        dict
    """

    st.markdown(
        "### Merchandising"
    )

    concessionaire_fee = st.text_input(
        "Concessionaire Fee",

        value=(
            loaded_profile.concessionaire_fee
            if loaded_profile
            else ""
        ),
    )

    seller = st.text_input(
        "Seller",

        value=(
            loaded_profile.seller
            if loaded_profile
            else ""
        ),
    )

    hard_merchandising = st.text_input(
        "Hard Merchandising",

        value=(
            loaded_profile.hard_merchandising
            if loaded_profile
            else ""
        ),
    )

    soft_merchandising = st.text_input(
        "Soft Merchandising",

        value=(
            loaded_profile.soft_merchandising
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

    merchandising_terms = st.text_area(
        "Merchandising Terms",

        value=(
            loaded_profile.merchandising_terms
            if loaded_profile
            else ""
        ),
    )

    return {

        "concessionaire_fee": (
            concessionaire_fee
        ),

        "seller": (
            seller
        ),

        "hard_merchandising": (
            hard_merchandising
        ),

        "soft_merchandising": (
            soft_merchandising
        ),

        "complimentary_tickets": (
            complimentary_tickets
        ),

        "merchandising_terms": (
            merchandising_terms
        ),
    }