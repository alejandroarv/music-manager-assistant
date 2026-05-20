import streamlit as st

from features.contracts.presentation.form_fields import (
    render_performance_contract_fields,
)


def render_contracts(contract_type, container):
    st.header("Contract Generator")

    if contract_type == "Performance":
        render_performance(container)
    elif contract_type == "NDA":
        render_nda(container)


def render_performance(container):
    service = container.contract_service
    contract_key = "performance_contract"

    form_data = render_performance_contract_fields("perf")

    if st.button("Generate Performance Contract"):
        result = service.create_performance_contract(form_data)

        if result.success:
            st.session_state[contract_key] = result.data
            st.success("Generated")
        else:
            st.error(f"Warning: {result.error}")

    if contract_key in st.session_state:
        st.info("Preview not available for .docx files. Please download to view.")
        st.download_button(
            "Download Contract",
            st.session_state[contract_key],
            file_name=service.generate_filename(
                form_data["artist"],
                "performance_contract",
                extension="docx",
            ),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )


def render_nda(container):
    disclosing = st.text_input("Disclosing Party", key="nda_disclosing")
    receiving = st.text_input("Receiving Party")
    purpose = st.text_area("Purpose")
    duration = int(st.number_input("Duration (months)", min_value=1, step=1))

    service = container.contract_service
    contract_key = "nda_contract"

    if st.button("Generate NDA"):
        result = service.create_nda_contract(
            {
                "disclosing_party": disclosing,
                "receiving_party": receiving,
                "purpose": purpose,
                "duration": duration,
            }
        )

        if result.success:
            st.session_state[contract_key] = result.data
            st.success("Generated")
        else:
            st.error(f"Warning: {result.error}")

    if contract_key in st.session_state:
        st.download_button(
            "Download NDA",
            st.session_state[contract_key],
            file_name=service.generate_filename(disclosing, "nda"),
        )
