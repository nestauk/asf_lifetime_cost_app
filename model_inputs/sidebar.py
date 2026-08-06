"""Renders sidebar widgets, returns a fully populated AppInputs object.

Shared across all pages — each page calls render_sidebar() with a `mode`
argument selecting which section (if any) should be replaced with a
"solved for" note instead of its normal editable widgets.
"""

import streamlit as st

from components.callouts import render_callout, render_divider
from components.sidebar_builder import (
    render_locked_value,
    render_sidebar_section_header,
)


def render_fixed_inputs() -> None:
    render_sidebar_section_header(
        "Fixed inputs", "Set for you. You can't change these."
    )
    # ---Inflation and discounting--- #
    col1, col2 = st.columns(2)
    with col1:
        render_locked_value("Base year", "2026")
    with col2:
        render_locked_value("Inflation rate", "2.0%")
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-bottom:12px;">HM Treasury Green Book guidance</div>',
        unsafe_allow_html=True,
    )
    render_locked_value(
        "Future discount rate", "3.5%", "HM Treasury Green Book guidance"
    )
    # ---Installation years range--- #
    render_locked_value("Installation year range", "2026 - 2035")
    # ---Reminder callout--- #
    render_callout(
        "Every result is a <strong>present value in 2026 real £</strong>. Costs are inflation-adjusted and discounted to what they are worth today."
    )


def render_user_inputs_heading() -> None:
    render_sidebar_section_header(
        "Your inputs",
        "Set today's value and, where it matters, how each assumption changes in future years.",
    )
    render_divider()


# SETS ASHP_HEAT_DEMAND_UPLIFT
def render_household_section() -> float:
    """Render the Property characteristics section: locked heat demand display + editable uplift slider.

    Returns the heat demand uplift value (0.0-0.2) chosen by the user.
    """
    st.markdown(
        '<div style="font-size:16px; font-weight:700; color:#0F294A; margin-bottom:6px;">'
        "Household characteristics</div>",
        unsafe_allow_html=True,
    )

    render_locked_value(
        label="Heat demand met by the heat pump",
        value="Space heat: 13,686 kWh/yr<br/>Hot water: 3,152 kWh/yr",
        caption=(
            "Median heat demand for a 3-4 bed house fitting an 8-10 kW air-to-water heat pump."
        ),
    )

    st.markdown(
        '<div style="font-size:14px; font-weight:700; color:#0F294A; margin-bottom:2px;">'
        "Extra heat demand with a heat pump</div>",
        unsafe_allow_html=True,
    )
    heat_demand_uplift_pct = st.slider(
        label="Extra heat demand with a heat pump",
        min_value=0,
        max_value=20,
        value=0,
        format="%d%%",
        label_visibility="collapsed",
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "Heat pumps run at lower flow temperatures for longer, which can raise total heat demand "
        "compared with a gas boiler in the same home. Set this to 0 to assume no difference between "
        "the two systems.</div>",
        unsafe_allow_html=True,
    )
    render_divider()

    return heat_demand_uplift_pct / 100


def render_sidebar() -> dict:
    with st.sidebar:
        render_fixed_inputs()
        render_user_inputs_heading()
        heat_demand_uplift = render_household_section()

    return {"ASHP_HEAT_DEMAND_UPLIFT": heat_demand_uplift}
