"""
Results page
"""

## Package imports
import streamlit as st
import altair as alt

# Local imports
from config.fonts_setup import nestafont, NESTA_COLOURS

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")

def results_page():
    """
    This function sets up the 'Results page' of the app.
    """

    st.markdown("# Results")
