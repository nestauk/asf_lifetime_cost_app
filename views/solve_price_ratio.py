"""Solving electricity price for lifetime cost parity: sidebar inputs + main content results tabs."""

import os

import streamlit as st
from PIL import Image

from components.callouts import render_page_context_callout
from components.layout import render_page_title, render_section_heading
from config.defaults import (
    INSTALL_END_YEAR,
    INSTALL_START_YEAR,
)
from page_sections.assumptions_summary import render_assumptions_summary
from page_sections.price_ratio_solver_outputs import (
    render_required_price_ratio_section,
)
from page_sections.sidebar import render_sidebar

INSTALLATION_YEARS = range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)

# Get the current directory to load images and other resources
current_dir = os.getcwd()
nesta_asf_logo = Image.open(f"{current_dir}/images/nesta_asf_stacked_logo.png")


# ---------------------------------------------------------------------------
#  Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    user_inputs = render_sidebar(solve_for_electricity=True)
    # For electricity
    # current_price=None, growth_mode=None, growth_rate=None, overrides={}


# ---------------------------------------------------------------------------
#  Main content
# ---------------------------------------------------------------------------

render_page_title(
    title="What electricity-to-gas price ratio would make a heat pump as cheap as a gas boiler?",
    subtitle="For a heat pump installed in a given year, this shows the electricity-to-gas price "
    "ratio needed each year of its lifetime for the two systems to have the same annualised lifetime cost.",
)
render_page_context_callout(
    "The ratio shown compares the <b>headline electricity price cap rate, before any time-of-use "
    "discount</b>, against the gas price. The discount you set in the sidebar is still applied "
    "on top when working out the heat pump's actual running cost. Gas price and everything else "
    "comes from the sidebar, exactly as on the comparison page.<br><br>"
    "The solver works by finding a single scale factor that makes the heat pump's annualised "
    "lifetime cost match that of the gas boiler's. The underlying electricity price trajectory"
    "assumption is flat, so the solved electricity price comes out as <b>one constant value</b>, "
    "held across the whole system's lifetime. If you've set gas prices to rise or fall over time "
    "in the sidebar, the <b>implied ratio</b> to gas will still change from year to year, even "
    "though the electricity price itself stays fixed."
)

from config.defaults import get_electricity_price_default, get_gas_price_default

current_electricity_price = (
    get_electricity_price_default()
)  # latest Ofgem price cap, p/kWh
current_gas_price = get_gas_price_default()  # latest Ofgem price cap, p/kWh
current_ratio = current_electricity_price / current_gas_price

render_required_price_ratio_section(user_inputs, current_ratio)

# ---Assumptions table ---#
render_section_heading(" ")
render_assumptions_summary(user_inputs)
