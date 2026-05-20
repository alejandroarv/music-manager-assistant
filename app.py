# app.py

import logging
import streamlit as st

# Dependency container (wires up services, repositories, etc.)
from core.container import Container

# Import feature UI entry points
# Each feature exposes a "presentation" layer function
from features.booking.presentation import render_booking
from features.contracts.presentation import render_contracts
from features.history.presentation import render_history
from features.tour.presentation import render_tour


# Configure global logging for the entire app
# It helps track events like template loading, saving records, errors, etc.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Initialize the dependency container once
# This creates and connects:
# - Repositories (data layer e.g., ContractRepository, BookingRepository)
# - Services (business logic layer e.g., ContractService, BookingService)
container = Container()

# Configure Streamlit page serttings 
# Has to be called before UI rendering
st.set_page_config(
    page_title="Music Manager Assistant", 
    page_icon=":material/music_note:"
    )

# Main app title at the top of the page
st.title("Music Manager Assistant")

# Sidebar navigation menu
# Controls which feature's UI is rendered in the main area
menu = ["Booking", "Tour Planner", "Contracts", "History"]
choice = st.sidebar.selectbox("Select Feature", menu)

# Route user to the selected feature
# This is essentially the router or controller layer
if choice == "Contracts":
    # Additional optioin for contracts feature
    # Lets the user choose a contract type
    contract_type = st.sidebar.selectbox(
        "Contract Type",
        ["Performance", "NDA"],
        key="contract_type",
    )

    # Pass both the selected type and the container
    #The UI will extract the needed services from the container based on the contract type
    render_contracts(contract_type, container)
elif choice == "Tour Planner":
    # Render the tour planning feature
    render_tour(container)
elif choice == "History":
    # Render the history/audit feature
    render_history(container)
elif choice == "Booking":
    # Render the booking feature's core functionality
    render_booking(container.booking_service)
