"""Lifetime cost comparison page: sidebar inputs + main content results tabs."""

import os

import streamlit as st  # For building the web app
from PIL import Image  # For loading images

from components.layout import render_page_title, render_section_heading
from model_inputs.sidebar import render_sidebar

# Get the current directory to load images and other resources
current_dir = os.getcwd()
nesta_asf_logo = Image.open(f"{current_dir}/images/nesta_asf_stacked_logo.png")


# ---Sidebar content---#
with st.sidebar:
    user_inputs = render_sidebar()


# ---Main page content---#

render_page_title(
    title="Lifetime cost: air-to-water heat pump vs gas boiler",
    subtitle="Change any assumption on the left and the three views below update together.",
)

render_section_heading("Output #1")

st.markdown(f"ASHP_HEAT_DEMAND_UPLIFT: {user_inputs.get('ASHP_HEAT_DEMAND_UPLIFT')}")

with st.container(border=True):
    st.markdown(
        '<div style="font-weight:700; color:#0F294A; font-size:15px;">Annualised lifetime cost by installation year</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:12px; color:#666; margin-bottom:12px;">Installation year (2026–2035) against annualised lifetime cost (£), one line per heating system</div>',
        unsafe_allow_html=True,
    )
    # st.altair_chart(CHART GOES HERE, use_container_width=True)

render_section_heading("Output #2")
