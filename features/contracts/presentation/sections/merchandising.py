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

        hard_merchandising = st.number_input(

            "Hard Merchandising (%)",

            min_value=0,

            max_value=100,

            value=100,

            step=1,

            key=f"{key_prefix}_hard_merchandising",

        )

        st.caption(

            f"Hard Concessionaire Fee: {100 - hard_merchandising}%"

        )

    # ==================================================
    # Soft Merchandising
    # ==================================================

    with merch_col2:

        soft_merchandising = st.number_input(

            "Soft Merchandising (%)",

            min_value=0,

            max_value=100,

            value=100,

            step=1,

            key=f"{key_prefix}_soft_merchandising",

        )

        st.caption(

            f"Soft Concessionaire Fee: {100 - soft_merchandising}%"

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

        "hard_concessionaire_fee": (
            100 - hard_merchandising
        ),

        "soft_merchandising": (
            soft_merchandising
        ),

        "soft_concessionaire_fee": (
            100 - soft_merchandising
        ),

        "merchandising_terms": (
            merchandising_terms
        ),

        "additional_addenda": (
            additional_addenda
        ),
    }