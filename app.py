# app.py

import logging

import streamlit as st


# Dependency injection container responsible
# for wiring repositories, services,
# and infrastructure components
from core.container import Container


# Feature presentation entry points
# Each feature exposes its UI layer here
from features.booking.presentation import (
    render_booking,
)

from features.contracts.presentation import (
    render_contracts,
)

from features.history.presentation import (
    render_history,
)

from features.profiles.presentation.ui import (
    render_profiles,
)

from features.tour.presentation import (
    render_tour,
)

from features.venue_profiles.presentation.ui import (
    render_venue_profiles,
)

from features.companies.presentation.ui import (
    render_company_profiles,
)

from features.deal_profiles.presentation.ui import (
    render_deal_profiles,
)

# Configure global application logging.
# Used for:
# - Persistence events
# - Template loading
# - Runtime diagnostics
# - Error tracing
logging.basicConfig(
    level=logging.INFO,

    format=(
        "%(asctime)s "
        "[%(levelname)s] "
        "%(name)s: "
        "%(message)s"
    ),
)


# Initialize dependency container once.
# This centralizes creation of:
# - Infrastructure components
# - Repositories
# - Application services
container = Container()


# Configure Streamlit page settings.
# Must execute before rendering UI elements.
st.set_page_config(
    page_title="Music Manager Assistant",

    page_icon=":material/music_note:",
)


# Main application title
st.title("Music Manager Assistant")


# -----------------------------------
# Sidebar Navigation
# -----------------------------------

# Primary feature routing menu
menu = [
    "Contracts",
    "Artist Profiles",
    "Venue Profiles",
    "Companies",
    "Deal Profiles",
    "Booking",
    "Tour Planner",
    "History",
    
]

choice = st.sidebar.selectbox(
    "Select Feature",
    menu,
)


# -----------------------------------
# Feature Routing
# -----------------------------------

# Route user interaction to the
# selected presentation layer
if choice == "Contracts":

    # Contract-specific routing selector
    contract_type = st.sidebar.selectbox(
        "Contract Type",

        ["Performance", "NDA"],

        key="contract_type",
    )

    # Render contracts workflow
    render_contracts(
        contract_type,
        container,
    )

elif choice == "Tour Planner":

    # Render tour planning workflow
    render_tour(container)

elif choice == "History":

    # Render persisted record history
    render_history(container)

elif choice == "Booking":

    # Render booking management workflow
    render_booking(
        container.booking_service
    )

elif choice == "Artist Profiles":
    # Render artist profile management workflow
    render_profiles(
        container
        )

elif choice == "Venue Profiles":
    # Render venue profile management workflow
    render_venue_profiles(
        container
        )

elif choice == "Companies":
    # Render company profile management workflow
    render_company_profiles(
        container
        )

elif choice == "Deal Profiles":

    # Render deal profile management workflow
    render_deal_profiles(
        container
    )