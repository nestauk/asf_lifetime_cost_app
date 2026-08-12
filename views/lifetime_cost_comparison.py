"""Lifetime cost comparison page: sidebar inputs + main content results tabs."""

import os

import streamlit as st
from PIL import Image

from components.layout import render_page_title, render_section_heading
from page_sections.assumptions_summary import render_assumptions_summary
from page_sections.comparison_outputs import (
    render_eac_breakdown_section,
    render_eac_by_year_section,
    render_price_ratio_table,
)
from page_sections.sidebar import render_sidebar
from results.compute import build_annual_breakdown_df, build_comparison_df

# Get the current directory to load images and other resources
current_dir = os.getcwd()
nesta_asf_logo = Image.open(f"{current_dir}/images/nesta_asf_stacked_logo.png")


# ---------------------------------------------------------------------------
#  Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    user_inputs = render_sidebar()


# ---------------------------------------------------------------------------
#  Main content
# ---------------------------------------------------------------------------

render_page_title(
    title="Lifetime cost: air-to-water heat pump vs gas boiler",
    subtitle="Change any assumption on the left and the outputs below will update together.",
)

comparison_df = build_comparison_df(user_inputs)
annual_breakdown_df = build_annual_breakdown_df(user_inputs)

# --- Output #1 ---#
render_eac_by_year_section(comparison_df)

# --- Output #2 ---#
render_eac_breakdown_section(comparison_df, annual_breakdown_df)
# TODO add total annualised lifetime cost somewhere
# TODO make the bars closer together to be able to compare

# --- Price ratio table --- #
render_price_ratio_table(user_inputs)

# ---Assumptions table ---#
render_section_heading(" ")
render_assumptions_summary(user_inputs)
