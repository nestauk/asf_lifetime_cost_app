"""
Scenario selection page.
"""

## Package imports
import streamlit as st
import altair as alt

# Local imports
from config.fonts_setup import nestafont, NESTA_COLOURS

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")

def scenario_selection_page():
    """
    This function sets up the 'Scenario selection' page of the app.
    """

    st.markdown("# Lifetime costs: scenario selection")
