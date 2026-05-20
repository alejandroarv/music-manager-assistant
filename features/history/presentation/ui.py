# features/history/presentation/ui.py

from datetime import datetime

import streamlit as st


def render_history(container):
    """
    Render the history management interface.

    Responsibilities:
    - Display persisted records
    - Filter records by type
    - Render content previews dynamically
    - Provide download functionality
    - Handle deletion confirmation workflows

    This module is strictly part of the
    presentation layer and should not contain
    business or persistence logic.
    """

    st.header("History")

    # Retrieve history application service
    service = container.history_service

    # ---------------------
    # Filtering Controls
    # ---------------------

    # Record type filter selector
    filter_type = st.selectbox(
        "Filter by type",
        service.get_record_types()
    )

    # Retrieve filtered records
    records = service.get_all_records(
        filter_type
    )

    if not records:

        st.info("No records yet.")
        return

    # Display record count summary
    total_records = len(
        service.get_all_records()
    )

    st.caption(
        f"{len(records)} shown "
        f"({total_records} total)"
    )

    # ----------------------
    # Record Rendering
    # ----------------------

    for record in records:

        record_type = record.get(
            "type",
            "unknown"
        )

        timestamp = record.get(
            "timestamp",
            ""
        )

        content = record.get(
            "content",
            ""
        )

        # Human-readable section title
        st.markdown(
            f'### '
            f'{record_type.replace("_", " ").title()}'
        )

        # Display persistence timestamp
        st.caption(timestamp)

        # -------------------------
        # Expandable Record Content
        # -------------------------

        with st.expander("View Content"):

            # Specialized rendering for
            # structured tour schedules
            if (
                record_type == "tour"
                and isinstance(content, dict)
            ):

                st.markdown(
                    "#### Tour Preview"
                )

                # Render formatted tour timeline
                for item in content.get(
                    "schedule",
                    []
                ):

                    # Normalize dates from either
                    # datetime objects or ISO strings
                    date_obj = (
                        item["date"]

                        if isinstance(
                            item["date"],
                            datetime
                        )

                        else datetime.fromisoformat(
                            item["date"]
                        )
                    )

                    date_str = (
                        date_obj.strftime(
                            "%b %d"
                        )
                    )

                    # Render event type
                    if item["type"] == "concert":

                        st.write(
                            f'{date_str} - '
                            f'{item["city"]} Concert'
                        )

                    else:

                        st.write(
                            f"{date_str} - Rest"
                        )

                # Section divider
                st.markdown("---")

                # Display raw structured content
                st.markdown("#### Raw Data")

                st.json(content)

            else:

                # Default rendering for
                # contracts, bookings, and
                # generic persisted records
                if isinstance(content, dict):

                    st.json(content)

                else:

                    st.text(content)

            # ------------------------
            # Download Functionality
            # ------------------------

            # Generate filename-safe timestamps
            safe_timestamp = (
                timestamp.replace(":", "-")
            )

            # Delegate export formatting
            # to the application service
            download_content = (
                service.build_download_content(
                    record,
                    container.tour_service
                    .format_tour_for_export,
                )
            )

            st.download_button(
                f"Download {record_type}",

                download_content,

                file_name=(
                    f"{record_type}_"
                    f"{safe_timestamp}.txt"
                ),
            )

            # -------------------------
            # Record Deletion Workflow
            # -------------------------

            record_id = record.get("id")

            # Session state key used for
            # deletion confirmation flow
            confirm_key = (
                f"confirm_delete_{record_id}"
            )

            # Initialize confirmation state
            if (
                confirm_key
                not in st.session_state
            ):

                st.session_state[
                    confirm_key
                ] = False

            # First interaction requests confirmation
            if not st.session_state[confirm_key]:

                if st.button(
                    "Delete",
                    key=f"delete_{record_id}"
                ):

                    st.session_state[
                        confirm_key
                    ] = True

            else:

                st.warning(
                    "Are you sure you want "
                    "to delete this record?"
                )

                col1, col2 = st.columns(2)

                # Confirm deletion
                with col1:

                    if st.button(
                        "Yes, delete",

                        key=(
                            f"confirm_yes_"
                            f"{record_id}"
                        )
                    ):

                        service.delete_record(
                            record_id
                        )

                        st.session_state[
                            confirm_key
                        ] = False

                        # Refresh UI after deletion
                        st.rerun()

                # Cancel deletion flow
                with col2:

                    if st.button(
                        "Cancel",

                        key=(
                            f"confirm_cancel_"
                            f"{record_id}"
                        )
                    ):

                        st.session_state[
                            confirm_key
                        ] = False

        # Visual separator between records
        st.markdown("---")