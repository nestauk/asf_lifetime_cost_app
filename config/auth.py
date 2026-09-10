"""Simple password gate for the app, shared internally."""

import streamlit as st


def check_password() -> bool:
    """Check whether the user has entered the correct password.

    Displays a password input widget and checks whether the input
    matches the `PASSWORD` value stored in Streamlit secrets.

    Returns:
        bool: True if the correct password has already been/now entered.
            False, otherwise.
    """

    # Check whether password has already been validated
    if st.session_state.get("password_correct", False):
        return True

    # Render input widget
    password = st.text_input("Password", type="password")
    # Check entered password
    if password:
        if password == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()  # immediately rerun to reveal app content
        else:
            st.error("Incorrect password")

    return False
