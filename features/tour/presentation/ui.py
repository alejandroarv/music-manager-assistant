# features/tour/presentation/ui.py

from datetime import datetime
import streamlit as st
from core.models.tour import TourData


def format_date(date_value):
    """
    # Normalize and format date for display

    # Handles:
    # - datetime objects
    # - ISO string dates

    # Returns:
    # e. g. "Apr 12"
    """

    if isinstance(date_value, datetime):
        return date_value.strftime("%b %d")

    return datetime.fromisoformat(date_value).strftime("%b %d")


def render_tour(container):
    """
    # Tour UI (Presentation Layer)

    # Responsibilities:
    # - Collect user input
    # - Validate basic input
    # - Call service to generate tour
    # - Display results
    # - Provide download option

    # No buwsiness logic here - only orchestration
    """
    st.header("Tour Planner")

    # Get service from container
    service = container.tour_service

    # -------------------------------
    # Input fields
    # -------------------------------

    artist = st.text_input("Artist Name")
    cities_input = st.text_area("Cities (comma separated)")
    start_date = st.date_input("Tour Start Date")

    concerts_before_rest = st.number_input("Concerts before rest", 1, 10, 3)
    rest_days = st.number_input("Rest days", 0, 5, 1)

    # -------------------------------
    # Generate Tour Action
    # -------------------------------

    if st.button("Generate Tour Plan"):

        # Basic UI validation
        if not artist.strip():
            st.error("Artist name is required.")
        elif not cities_input.strip():
            st.error("Enter at least one city.")
        else:
            # Parse input string -> list
            cities = service.parse_cities(cities_input)

            if not cities:
                st.error("Invalid cities.")
            else:
                # Build validated model
                data = TourData(
                    artist,
                    cities,
                    start_date,
                    concerts_before_rest,
                    rest_days,
                )

                try:
                    # Generate tour via service
                    result = service.generate_tour(data)

                    st.success("Tour generated!")
                    st.markdown("---")

                    # --------------------------
                    # Display schedule
                    # --------------------------

                    for item in result["schedule"]:
                        date_str = format_date(item["date"])

                        if item["type"] == "concert":
                            st.success(f'{date_str} - {item["city"]} Concert')
                        else:
                            st.info(f"{date_str} - Rest Day")

                    # --------------------------
                    # Download functionality
                    # --------------------------

                    download_text = service.format_tour_for_export(result)
                    file_name = service.generate_filename(result["name"], "tour")

                    st.download_button(
                        "Download Tour Plan",
                        download_text,
                        file_name=file_name,
                    )

                except ValueError as error:
                    # Handle validation errors from service
                    st.error(str(error))
