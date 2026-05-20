import streamlit as st

from features.contracts.presentation.form_fields import (
    render_performance_contract_fields,
)


def render_contracts(
    contract_type,
    container
):
    """
    Render the contract generation interface
    based on the selected contract type.
    """

    st.header("Contract Generator")

    # Route rendering to the appropriate
    # contract workflow
    if contract_type == "Performance":

        render_performance(container)

    elif contract_type == "NDA":

        render_nda(container)


def render_performance(container):
    """
    Render the performance contract
    generation workflow.
    """

    service = container.contract_service

    # Session state key used to persist
    # generated contract bytes
    contract_key = "performance_contract"

    # Render shared contract form fields
    form_data = render_performance_contract_fields(
        "perf"
    )

    if st.button(
        "Generate Performance Contract"
    ):

        # Delegate contract generation to
        # the application service layer
        result = (
            service.create_performance_contract(
                form_data
            )
        )

        if result.success:

            st.session_state[
                contract_key
            ] = result.data

            st.success("Generated")

        else:

            st.error(
                f"Warning: {result.error}"
            )

    # Display download controls once the
    # contract has been generated
    if contract_key in st.session_state:

        st.info(
            "Preview not available for "
            ".docx files. Please download "
            "to view."
        )

        st.download_button(
            "Download Contract",

            st.session_state[
                contract_key
            ],

            file_name=service.generate_filename(
                form_data["artist"],
                "performance_contract",
                extension="docx",
            ),

            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml."
                "document"
            ),
        )


def render_nda(container):
    """
    Render the NDA contract generation workflow.
    """

    # NDA input fields
    disclosing = st.text_input(
        "Disclosing Party",
        key="nda_disclosing"
    )

    receiving = st.text_input(
        "Receiving Party"
    )

    purpose = st.text_area("Purpose")

    duration = int(
        st.number_input(
            "Duration (months)",
            min_value=1,
            step=1
        )
    )

    service = container.contract_service

    # Session state key used to persist
    # generated NDA content
    contract_key = "nda_contract"

    if st.button("Generate NDA"):

        # Build NDA payload and delegate
        # generation to the service layer
        result = service.create_nda_contract(
            {
                "disclosing_party": (
                    disclosing
                ),

                "receiving_party": (
                    receiving
                ),

                "purpose": purpose,

                "duration": duration,
            }
        )

        if result.success:

            st.session_state[
                contract_key
            ] = result.data

            st.success("Generated")

        else:

            st.error(
                f"Warning: {result.error}"
            )

    # Display NDA download once generated
    if contract_key in st.session_state:

        st.download_button(
            "Download NDA",

            st.session_state[
                contract_key
            ],

            file_name=service.generate_filename(
                disclosing,
                "nda"
            ),
        )