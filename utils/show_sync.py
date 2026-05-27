# utils/show_sync.py

# Streamlit UI framework
import streamlit as st

# Shared synchronization helpers
from utils.state_sync import (
    sync_linked_text_field,
)


def initialize_show_sync(
    i,
    source_value,
    target_key,
    touched_key,
    fallback_value="",
):
    """
    Initialize synchronized per-show fields.

    Responsibilities:
    - synchronize show 1 with primary fields
    - initialize additional shows independently
    - preserve manual overrides

    Args:
        i:
            Current show index.

        source_value:
            Primary field value used for synchronization.

        target_key:
            Session-state key of the show field.

        touched_key:
            Session-state override flag.

        fallback_value:
            Default value for non-primary shows.
    """

    # Synchronize first show
    if i == 0:

        sync_linked_text_field(
            source_value=source_value,

            target_key=target_key,

            touched_key=touched_key,
        )

    # Initialize additional shows
    elif target_key not in st.session_state:

        st.session_state[
            target_key
        ] = fallback_value