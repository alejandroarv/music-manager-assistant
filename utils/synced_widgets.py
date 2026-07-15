# utils/synced_widgets.py

import streamlit as st

from utils.state_sync import (
    sync_linked_text_field,
    detect_manual_override,
)


def render_synced_number_input(
    *,
    label,
    source_value,
    key,
    touched_key,
    min_value=0.0,
    max_value=None,
    step=1.0,
):
    """
    Render a synchronized numeric input.

    Automatically:
    - syncs with source values
    - preserves manual overrides
    - updates when source changes
    """

    sync_linked_text_field(

        source_value,

        key,

        touched_key,

    )

    kwargs = {

        "label": label,

        "min_value": min_value,

        "step": step,

        "key": key,

    }

    if max_value is not None:

        kwargs["max_value"] = max_value

    value = st.number_input(
        **kwargs
    )

    detect_manual_override(

        source_value,

        value,

        touched_key,

    )

    return value

def render_synced_selectbox(
    *,
    label,
    source_value,
    options,
    key,
    touched_key,
):
    """
    Render a synchronized selectbox.

    Automatically:
    - syncs with source values
    - preserves manual overrides
    - updates when source changes
    """

    sync_linked_text_field(

        source_value,

        key,

        touched_key,

    )

    value = st.selectbox(

        label,

        options=options,

        key=key,

    )

    detect_manual_override(

        source_value,

        value,

        touched_key,

    )

    return value