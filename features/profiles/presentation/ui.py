# features/profiles/presentation/ui.py

# Streamlit UI framework
import streamlit as st

# Strongly-typed profile model
from core.models.artist_profile import (
    ArtistProfile,
)

from features.profiles.presentation.sections.identity import (
    render_identity_section,
)

from features.profiles.presentation.sections.travel import (
    render_terms_section,
)

from features.profiles.presentation.sections.merchandising import (
    render_merchandising_section,
)

from features.profiles.presentation.sections.production import (
    render_production_section,
)

from features.profiles.presentation.sections.defaults import (
    render_defaults_section,
)

def render_profiles(container):
    """
    Render the Artist Profiles interface.
    """

    # Page Header
    st.title("Artist Profiles")


    # Retrieve Existing Profiles
    profiles = (
        container.profile_service
        .get_all_profiles()
    )

    # Tracks whether the user is creating
    # a brand-new profile
    if (
        "creating_new_profile"
        not in st.session_state
    ):

        st.session_state[
            "creating_new_profile"
        ] = False

    # Build unique artist list
    artist_names = sorted({

        profile["content"].get(
            "artist_name",
            "",
        )

        for profile in profiles

    })

    # Profile Selection
    st.subheader("Load Existing Profile")

    selected_artist = st.selectbox(

        "Artist",

        options=[

            "New Artist",

            *artist_names,

        ],

    )

    # Remember the currently selected artist
    st.session_state[
        "selected_artist_name"
    ] = (
        selected_artist
    )

    # Profiles belonging to the selected artist
    available_profiles = [

        profile

        for profile in profiles

        if (

            profile["content"].get(
                "artist_name",
                "",
            )

            ==

            selected_artist

        )

    ]

    profile_names = [

        profile["content"].get(
            "profile_name",
            "Default",
        )

        for profile in available_profiles

    ]

    selected_profile_name = st.selectbox(

        "Profile",

        options=profile_names

        if selected_artist != "New Profile"

        else [],

    )

    # Create a new profile
    if st.button(

        "➕ New Profile",

    ):

        st.session_state[
            "creating_new_profile"
        ] = True

        st.rerun()

    # Default form values
    loaded_profile = None

    # Currently selected repository record
    selected_record = None

    # Load the selected profile variant
    if (

        selected_artist != "New Artist"

        and

        selected_profile_name

    ):

        selected_record = next(

            (

                profile

                for profile in available_profiles

                if (

                    profile["content"].get(
                        "profile_name",
                        "Default",
                    )

                    ==

                    selected_profile_name

                )

            ),

            None,

        )

        if (

            selected_record

            and

            not st.session_state[
                "creating_new_profile"
            ]

        ):

            loaded_profile = (
                ArtistProfile.from_dict(
                    selected_record[
                        "content"
                    ]
                )
            )


    # Profile Form
    st.divider()


    identity = (
        render_identity_section(

            loaded_profile,

            default_artist_name=(

                selected_artist

                if selected_artist
                !=
                "New Artist"

                else ""

            ),

            default_profile_name=(

                ""

                if st.session_state[
                    "creating_new_profile"
                ]

                else "Default"

            ),

        )
    )

    artist_name = (
        identity[
            "artist_name"
        ]
    )

    profile_name = (
        identity[
            "profile_name"
        ]
    )

    company_name = (
        identity[
            "company_name"
        ]
    )

    company_address = (
        identity[
            "company_address"
        ]
    )

    defaults = (
        render_defaults_section(
            loaded_profile
        )
    )

    show_length = (
        defaults[
            "show_length"
        ]
    )

    travel = (
        render_terms_section(
            loaded_profile
        )
    )

    air_transportation = (
        travel[
            "air_transportation"
        ]
    )

    hotel_accommodations = (
        travel[
            "hotel_accommodations"
        ]
    )

    ground_transportation = (
        travel[
            "ground_transportation"
        ]
    )

    meals_incidentals = (
        travel[
            "meals_incidentals"
        ]
    )

    air_freight = (
        travel[
            "air_freight"
        ]
    )

    production_section = (
        render_production_section(
            loaded_profile
        )
    )

    production = (
        production_section[
            "production"
        ]
    )

    catering = (
        production_section[
            "catering"
        ]
    )

    special_provisions = (
        production_section[
            "special_provisions"
        ]
    )

    merchandising = (
        render_merchandising_section(
            loaded_profile
        )
    )

    merchandising_terms = (
        merchandising[
            "merchandising_terms"
        ]
    )

    concessionaire_fee = (
        merchandising[
            "concessionaire_fee"
        ]
    )

    seller = (
        merchandising[
            "seller"
        ]
    )

    hard_merchandising = (
        merchandising[
            "hard_merchandising"
        ]
    )

    soft_merchandising = (
        merchandising[
            "soft_merchandising"
        ]
    )

    complimentary_tickets = (
        merchandising[
            "complimentary_tickets"
        ]
    )


    # Save / Update Logic
    if st.button("Save Profile"):

        # Basic validation
        if not artist_name.strip():

            st.error(
                "Artist name is required."
            )

        else:

            # Build updated profile model
            profile = ArtistProfile(

                artist_name=artist_name,

                profile_name=profile_name,

                company_name=company_name,

                company_address=company_address,

                show_length=show_length,

                air_transportation=air_transportation,

                hotel_accommodations=hotel_accommodations,

                ground_transportation=(
                    ground_transportation
                ),

                meals_incidentals=(
                    meals_incidentals
                ),

                air_freight=(
                    air_freight
                ),

                production=production,

                catering=catering,
                
                merchandising_terms=(
                    merchandising_terms
                ),

                concessionaire_fee=(
                    concessionaire_fee
                ),

                seller=(
                    seller
                ),

                hard_merchandising=(
                    hard_merchandising
                ),

                soft_merchandising=(
                    soft_merchandising
                ),

                special_provisions=(
                    special_provisions
                ),

                complimentary_tickets=(
                    complimentary_tickets
                ),

            )

            # Update Existing Profile
            if (

                selected_record

                and

                not st.session_state[
                    "creating_new_profile"
                ]

            ):

                container.profile_service.update_profile(

                    selected_record["id"],

                    profile,

                )

                st.success(

                    "Profile updated."

                )

            # Create New Profile
            else:

                container.profile_service.create_profile(
                    profile
                )

                # Return to normal edit mode
                st.session_state[
                    "creating_new_profile"
                ] = False

                st.success(
                    "Profile saved."
                )

            # Refresh UI immediately
            st.rerun()


    # Existing Profiles
    st.divider()

    st.subheader("Existing Profiles")

    if not profiles:

        st.info(
            "No artist profiles found."
        )

        return

    # Display saved profiles
    for record in profiles:

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"🎤 {record['name']}"
            )

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{record['id']}"
            ):

                container.profile_service.delete_profile(
                    record["id"]
                )

                st.success(
                    "Profile deleted."
                )

                st.rerun()