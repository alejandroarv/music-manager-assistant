import streamlit as st

from features.booking.presentation.presenter import map_booking_to_view
from features.contracts.presentation.form_fields import (
    render_performance_contract_fields,
)


def render_create_booking_form(booking_service):
    st.subheader("Create New Booking")

    with st.form("create_booking"):
        form_data = render_performance_contract_fields("booking")
        submitted = st.form_submit_button("Create Booking")

    if submitted:
        result = booking_service.create_booking(form_data)

        if not result.success:
            st.error(f"Warning: {result.error}")
            return

        booking = result.data
        st.success(f'Booking created for {booking["artist"]}')


def render_booking_list(booking_service):
    bookings = booking_service.list_bookings()

    st.subheader("All Bookings")

    if not bookings:
        st.info("No bookings yet. Create your first booking above.")
        return

    for booking in bookings:
        render_booking_row(map_booking_to_view(booking), booking_service)


def render_booking_row(view, booking_service):
    st.markdown(f'### {view["title"]}')

    col1, col2, col3 = st.columns(3)

    with col1:
        contract_key = f"contract_{view['id']}"

        if st.button("Generate Contract", key=f"gen_{view['id']}"):
            result = booking_service.generate_contract(view["id"])

            if result.success:
                st.session_state[contract_key] = result.data
            else:
                st.error(result.error)

        if contract_key in st.session_state:
            st.download_button(
                label="Download Contract",
                data=st.session_state[contract_key],
                file_name=f"contract_{view['id']}.docx",
                key=f"download_{view['id']}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

    with col2:
        export_data = booking_service.export_single_booking(view["raw"])
        st.download_button(
            label="Download Booking",
            data=export_data,
            file_name=f"booking_{view['id']}.txt",
            key=f'booking_{view["id"]}',
        )

    with col3:
        st.caption(view["date_label"])
        st.caption(view["fee_label"])
        st.caption(view["shows_label"])

    with st.expander("View Booking Details"):
        st.json(view["raw"])

    st.divider()


def render_export_all(booking_service):
    bookings = booking_service.list_bookings()

    st.subheader("Export All Bookings")

    if bookings:
        export_text = booking_service.export_bookings_text(bookings)
        st.download_button(
            label="Download All Bookings",
            data=export_text,
            file_name="all_bookings.txt",
        )


def render_booking(booking_service):
    st.header("Booking Manager")

    render_create_booking_form(booking_service)
    render_booking_list(booking_service)
    render_export_all(booking_service)
