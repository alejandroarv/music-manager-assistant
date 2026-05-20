# features/history/presentation/ui.py

from datetime import datetime
import streamlit as st


def render_history(container):
    """
    # History UI (Presentation Layer)
    
    # Responsibilities: 
    # - Display stored records
    # - Filter records by type
    # - Render content dynamically based on type
    # - Provide download functionality
    # - Handle record deletion with confimation
    
    # IMPORTANT:
    # No business logic here - only presentation + interaction
    """
    st.header("History")

    # Extract service
    service = container.history_service

    # ---------------------
    # Filtering
    # ---------------------

    # Dropdown of available record types (e.g., booking, tour, contract)
    filter_type = st.selectbox("Filter by type", service.get_record_types())
 
    # Retrieve filtered records
    records = service.get_all_records(filter_type)

    if not records:
        st.info("No records yet.")
        return

    # Show count info
    total_records = len(service.get_all_records())
    st.caption(f"{len(records)} shown ({total_records} total)")

    # ----------------------
    # Render Records
    # ----------------------

    for record in records:
        record_type = record.get("type", "unknown")
        timestamp = record.get("timestamp", "")
        content = record.get("content", "")

        # Section title (formatted nicely)
        st.markdown(f'### {record_type.replace("_", " ").title()}')

        # Timestamp display
        st.caption(timestamp)

        # -------------------------
        # Expandable Content View
        #--------------------------

        with st.expander("View Content"):

            # Special rendering for tour data
            if record_type == "tour" and isinstance(content, dict):
                st.markdown("#### Tour Preview")

                # Loop through tour schedule
                for item in content.get("schedule", []):

                    # Normalize date (handles both datetime and string)
                    date_obj = (
                        item["date"]
                        if isinstance(item["date"], datetime)
                        else datetime.fromisoformat(item["date"])
                    )

                    date_str = date_obj.strftime("%b %d")

                    # Display event type
                    if item["type"] == "concert":
                        st.write(f'{date_str} - {item["city"]} Concert')
                    else:
                        st.write(f"{date_str} - Rest")

                # Divider
                st.markdown("---")

                # Show raw JSON
                st.markdown("#### Raw Data")
                st.json(content)

            else:
                # Default rendering (contracts, bookings, etc.)
                if isinstance(content, dict):
                    st.json(content)
                else:
                    st.text(content)

            # ------------------------
            # Download functionality
            # ------------------------

            # Make timestamp safe for filename
            safe_timestamp = timestamp.replace(":", "-")

            # Delegate formatting to service
            download_content = service.build_download_content(
                record,
                container.tour_service.format_tour_for_export,
            )

            st.download_button(
                f"Download {record_type}",
                download_content,
                file_name=f"{record_type}_{safe_timestamp}.txt",
            )

            # -------------------------
            # Delete with confirmation
            # -------------------------

            record_id = record.get("id")

            # Unique key per record
            confirm_key = f"confirm_delete_{record_id}"

            # Initialize confirmation state
            if confirm_key not in st.session_state:
                st.session_state[confirm_key] = False

            # First click -> ask confirmation
            if not st.session_state[confirm_key]:
                if st.button("Delete", key=f"delete_{record_id}"):
                    st.session_state[confirm_key] = True
            else:
                st.warning("Are you sure you want to delete this record?")
            
                col1, col2 = st.columns(2)

                # Confirm deletion
                with col1:
                    if st.button("Yes, delete", key=f"confirm_yes_{record_id}"):
                        service.delete_record(record_id)
                        st.session_state[confirm_key] = False
                        st.rerun()

                # Cancel deletion
                with col2:
                    if st.button("Cancel", key=f"confirm_cancel_{record_id}"):
                        st.session_state[confirm_key] = False

        st.markdown("---")
