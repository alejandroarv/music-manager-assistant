# utils/state_sync.py

# Streamlit UI framework
import streamlit as st


def sync_linked_text_field(
    source_value,
    target_key,
    touched_key,
):
    """
    Synchronize a target field with a
    source value until manually overridden.

    Responsibilities:
    - initialize missing state
    - continuously synchronize values
    - preserve manual overrides
    """

    # Initialize missing field state
    if target_key not in st.session_state:

        st.session_state[target_key] = (
            source_value
        )

    # Keep synchronized until manually edited
    if not st.session_state.get(
        touched_key,
        False,
    ):

        st.session_state[target_key] = (
            source_value
        )


def detect_manual_override(
    source_value,
    target_value,
    touched_key,
):
    """
    Detect manual overrides only when
    values truly diverge.

    Prevents false-positive overrides
    caused by reruns or formatting.
    """

    normalized_source = (
        str(source_value).strip()
    )

    normalized_target = (
        str(target_value).strip()
    )

    # Only mark override when values
    # actually differ meaningfully
    if (
        normalized_target
        and normalized_target
        != normalized_source
    ):

        st.session_state[
            touched_key
        ] = True

