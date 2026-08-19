"""Entry point for the Lifetime Costs App."""

import os

import altair as alt  # For creating interactive charts with Altair
import streamlit as st  # For building the web app
from PIL import Image  # For loading images

from components.layout import render_beta_banner, render_top_bar
from config.auth import check_password
from config.css_style import set_css_style
from config.fonts_setup import nestafont

# Password
if not check_password():
    st.stop()

# Setting up themes and fonts
alt.theme.register("nestafont", enable=True)(lambda: alt.theme.ThemeConfig(nestafont()))
set_css_style()

# Get the current directory to load images and other resources
current_dir = os.getcwd()

# configure browser-tab-level settings for the entire app
favicon = Image.open(f"{current_dir}/images/nesta_favicon.png")
st.set_page_config(
    page_title="ASF Lifetime Cost Model", layout="wide", page_icon=favicon
)

# top banners
render_top_bar()
render_beta_banner()

# create Page objects
comparison_page = st.Page(
    "views/lifetime_cost_comparison.py",
    title="Lifetime cost comparison",
    icon="🏠",
    default=True,
)
solve_subsidy_page = st.Page(
    "views/solve_subsidy.py",
    title="Solve for subsidy",
    icon="🎯",
)
solve_electricity_price_page = st.Page(
    "views/solve_price_ratio.py",
    title="Solve for electricity-gas price ratio",
    icon="⚡",
)
methodology_page = st.Page(
    "views/methodology.py",
    title="Guide & methodology",
    icon="📄",
)


# build the app page-routing system
pg = st.navigation(
    {
        "Pages": [
            comparison_page,
            solve_subsidy_page,
            solve_electricity_price_page,
            methodology_page,
        ]
    },
    position="sidebar",
)

# execute code inside the page file currently selected
pg.run()
