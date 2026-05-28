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

    Synchronization automatically resets
    whenever the source value changes.

    Responsibilities:
    - initialize missing state
    - preserve manual edits
    - detect source changes
    - restore synchronization lifecycle
    """

    source_tracker_key = (
        f"{target_key}_last_source"
    )

    normalized_source = (
        str(source_value).strip()
    )

    # Initialize target state
    if target_key not in st.session_state:

        st.session_state[target_key] = (
            source_value
        )

    # Retrieve previously tracked source
    previous_source = str(
        st.session_state.get(
            source_tracker_key,
            ""
        )
    ).strip()

    # Detect source changes
    if previous_source != normalized_source:

        # Reset manual override state
        st.session_state[
            touched_key
        ] = False

        # Update synchronized value
        st.session_state[target_key] = (
            source_value
        )

        # Track latest source value
        st.session_state[
            source_tracker_key
        ] = normalized_source

        return

    # Preserve manual overrides
    if st.session_state.get(
        touched_key,
        False,
    ):

        return

    current_value = str(
        st.session_state.get(
            target_key,
            ""
        )
    ).strip()

    # Detect manual divergence
    if (
        current_value
        and current_value
        != normalized_source
    ):

        st.session_state[
            touched_key
        ] = True

        return

    # Keep synchronized while untouched
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

