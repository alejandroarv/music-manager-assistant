# features/profiles/presentation/identity.py

# Streamlit UI framework
import streamlit as st


def render_identity_section(

    loaded_profile,

    container,

    default_artist_name="",

    default_profile_name="Default",

):
    """
    Render artist identity fields.

    Returns:
        dict
    """

    st.subheader(
        "Profile Details"
    )

    companies = (

        container
        .company_profile_service
        .get_all_profiles()

    )

    company_names = [

        company["name"]

        for company in companies

    ]

    artist_name = st.text_input(

        "Artist Name",

        value=(

            loaded_profile.artist_name

            if loaded_profile

            else default_artist_name

        ),

    )

    profile_name = st.text_input(

        "Profile Name",

        value=(

            loaded_profile.profile_name

            if loaded_profile

            else default_profile_name

        ),

    )

    default_company = st.selectbox(

        "Default Company",

        options=[

            "None",

            *company_names,

        ],

        index=(

            ["None", *company_names].index(

                loaded_profile.default_company

                if (

                    loaded_profile

                    and

                    loaded_profile.default_company

                    in company_names

                )

                else "None"

            )

        ),

    )

    return {

        "artist_name": artist_name,

        "profile_name": profile_name,

        "default_company": (
            default_company
        ),
    }