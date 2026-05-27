# features/contracts/presentation/sections/merchandising.py

# Streamlit UI framework
import streamlit as st


def render_merchandising_section(
    key_prefix,
):
    """
    Render merchandising-related
    contract configuration fields.

    Responsibilities:
    - render merchandising controls
    - collect merchandising terms
    - normalize merchandising payload

    Returns:
        dict: Normalized merchandising values
    """

    # ==================================================
    # Merchandising Section
    # ==================================================

    st.markdown("### Merchandising")

    merch_col1, merch_col2 = st.columns(2)

    # ==================================================
    # Hard Merchandising
    # ==================================================

    with merch_col1:

        hard_merchandising = st.selectbox(
            "Hard Merchandising",

            options=[
                "Allowed",
                "Restricted",
                "Not Allowed",
            ],

            key=f"{key_prefix}_hard_merchandising",
        )

    # ==================================================
    # Soft Merchandising
    # ==================================================

    with merch_col2:

        soft_merchandising = st.selectbox(
            "Soft Merchandising",

            options=[
                "Allowed",
                "Restricted",
                "Not Allowed",
            ],

            key=f"{key_prefix}_soft_merchandising",
        )

    # ==================================================
    # Merchandising Terms
    # ==================================================

    merchandising_terms = st.text_area(
        "Merchandising Terms",
        key=f"{key_prefix}_merchandising_terms",
    )

    additional_addenda = st.text_area(
        "Additional Addenda",
        key=f"{key_prefix}_additional_addenda",
    )

    # Return normalized section payload
    return {
        "hard_merchandising": (
            hard_merchandising
        ),

        "soft_merchandising": (
            soft_merchandising
        ),

        "merchandising_terms": (
            merchandising_terms
        ),

        "additional_addenda": (
            additional_addenda
        ),
    }