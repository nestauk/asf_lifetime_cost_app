"""
This script sets up a Streamlit app.

To run this app localy:
streamlit run lifetime_costs_app.py
"""

## Package imports
import streamlit as st  # For building the web app
from PIL import Image  # For loading images
import altair as alt  # For creating interactive charts with Altair
from streamlit_option_menu import option_menu  # For creating a sidebar menu
import os

# Local imports
from config.fonts_setup import nestafont, NESTA_COLOURS
from config.css_style import set_css_style
from pages.about_dashboard_page import about_dashboard_page
from pages.results_page import results_page
from pages.about_data_page import about_data_page

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")
set_css_style()

# Get the current directory to load images and other resources
current_dir = os.getcwd()


def set_up_sidebar():
    """
    This function sets up the sidebar with a menu for navigating the app.
    """
    side_bar_options = option_menu(
        menu_title="Lifetime costs app",
        menu_icon="piggy-bank",  # Icon for the sidebar menu
        options=[
            "About the app",
            "Results",
            "About the data",
        ],  # The options to be displayed in the sidebar
        icons=[
            "house",
            "bar-chart",
            "info-circle",
        ],  # These are the icons to be displayed next to the options. You can select from: https://icons.getbootstrap.com/
        default_index=0,  # Defaults to the "About this app" page
        orientation="vertical",
        styles={
            "container": {
                "padding": "5!important",
                "background-color": NESTA_COLOURS[12],
            },
            "icon": {"color": NESTA_COLOURS[10], "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": NESTA_COLOURS[0]},
        },
    )
    return side_bar_options


def lifetime_costs_app():
    """
    This function will setup a Streamlit app .
    """

    favicon = Image.open(f"{current_dir}/images/nesta_favicon.png")
    nesta_logo = Image.open(f"{current_dir}/images/nesta_logo.png")
    # Configure your browser tab by adding a title, changing the layout, and adding an icon to appear on your browser tab
    st.set_page_config(
        page_title="Lifetime costs explorer",
        layout="wide",
        page_icon=favicon,
    )

    # Setting the CSS style for the app
    set_css_style()

    with st.sidebar:
        side_bar_options = set_up_sidebar()

    if side_bar_options == "About the explorer":
        st.image(nesta_logo, width=200)
        about_dashboard_page()
    elif side_bar_options == "Explore the results":
        results_page()
    else:
        about_data_page()


with st.spinner("Loading lifetime costs app..."):
    lifetime_costs_app()
