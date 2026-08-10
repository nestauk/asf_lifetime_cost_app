"""Solving subsidy for lifetime cost parity: sidebar inputs + main content results tabs."""

import os

import streamlit as st
from PIL import Image

from components.callouts import render_page_context_callout
from components.layout import render_page_title, render_section_heading
from page_sections.assumptions_summary import render_assumptions_summary
from page_sections.sidebar import render_sidebar
from page_sections.subsidy_solver_outputs import render_required_subsidy_chart_section
from results.compute import build_required_subsidy_df

# Get the current directory to load images and other resources
current_dir = os.getcwd()
nesta_asf_logo = Image.open(f"{current_dir}/images/nesta_asf_stacked_logo.png")


# ---------------------------------------------------------------------------
#  Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    user_inputs = render_sidebar(solve_for_subsidy=True)
    # subsidy_scenario = None
    # subsidy_overrides: dict[int, float] = {}

# ---------------------------------------------------------------------------
#  Main content
# ---------------------------------------------------------------------------

render_page_title(
    title="What subsidy would reach lifetime cost parity?",
    subtitle="For every installation year, this page solves for the subsidy that makes the heat pump's equivalent annual cost match the gas boiler's.",
)
render_page_context_callout(
    "Subsidy is the one thing you don't set here - it's the answer, not an input. Everything else "
    "(property, energy prices, heat pump and gas boiler assumptions) comes from the sidebar, exactly "
    "as it does on the comparison page."
)

required_subsidy_df = build_required_subsidy_df(user_inputs)

# --- Output #1 ---#
render_required_subsidy_chart_section(required_subsidy_df)

# ---Assumptions table ---#
render_section_heading(" ")
render_assumptions_summary(user_inputs)
