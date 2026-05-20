# features/tour/presentation/ui.py

from datetime import datetime

import streamlit as st

from core.models.tour import TourData


def format_date(date_value):
    """
    Normalize and format dates for UI display.

    Supports:
    - datetime objects
    - ISO-formatted string dates

    Returns:
        Example:
            "Apr 12"
    """

    if isinstance(date_value, datetime):

        return date_value.strftime(
            "%b %d"
        )

    return (
        datetime.fromisoformat(
            date_value
        ).strftime("%b %d")
    )


def render_tour(container):
    """
    Render the tour planning interface.

    Responsibilities:
    - Collect user input
    - Perform basic UI validation
    - Coordinate tour generation workflows
    - Display generated schedules
    - Provide export functionality

    This module belongs strictly to the
    presentation layer and should not contain
    business or persistence logic.
    """

    st.header("Tour Planner")

    # Retrieve application service
    service = container.tour_service

    # -------------------------------
    # Input Fields
    # -------------------------------

    artist = st.text_input(
        "Artist Name"
    )

    cities_input = st.text_area(
        "Cities (comma separated)"
    )

    start_date = st.date_input(
        "Tour Start Date"
    )

    # Tour scheduling configuration
    concerts_before_rest = (
        st.number_input(
            "Concerts before rest",
            1,
            10,
            3,
        )
    )

    rest_days = st.number_input(
        "Rest days",
        0,
        5,
        1,
    )

    # -------------------------------
    # Tour Generation Workflow
    # -------------------------------

    if st.button("Generate Tour Plan"):

        # Basic presentation-layer validation
        if not artist.strip():

            st.error(
                "Artist name is required."
            )

        elif not cities_input.strip():

            st.error(
                "Enter at least one city."
            )

        else:

            # Parse comma-separated input
            # into normalized city values
            cities = service.parse_cities(
                cities_input
            )

            if not cities:

                st.error("Invalid cities.")

            else:

                # Build validated tour input model
                data = TourData(
                    artist,
                    cities,
                    start_date,
                    concerts_before_rest,
                    rest_days,
                )

                try:

                    # Delegate schedule generation
                    # to the application service
                    result = service.generate_tour(
                        data
                    )

                    st.success(
                        "Tour generated!"
                    )

                    st.markdown("---")

                    # --------------------------
                    # Schedule Rendering
                    # --------------------------

                    for item in result["schedule"]:

                        date_str = format_date(
                            item["date"]
                        )

                        # Render event type
                        if (
                            item["type"]
                            == "concert"
                        ):

                            st.success(
                                f"{date_str} - "
                                f"{item['city']} "
                                "Concert"
                            )

                        else:

                            st.info(
                                f"{date_str} - "
                                "Rest Day"
                            )

                    # --------------------------
                    # Export Functionality
                    # --------------------------

                    # Build downloadable export
                    # representation of the tour
                    download_text = (
                        service
                        .format_tour_for_export(
                            result
                        )
                    )

                    file_name = (
                        service.generate_filename(
                            result["name"],
                            "tour",
                        )
                    )

                    st.download_button(
                        "Download Tour Plan",

                        download_text,

                        file_name=file_name,
                    )

                except ValueError as error:

                    # Handle validation errors
                    # propagated from the
                    # application layer
                    st.error(str(error))