"""Methodology and data documentation page."""

import streamlit as st

from components.callouts import render_callout, render_page_context_callout
from components.layout import render_page_title, render_section_heading
from config.defaults import (
    BASE_YEAR_DEFAULT,
    DISCOUNT_RATE_DEFAULT,
)

render_page_title(
    title="Guide & methodology",
    subtitle="How to use this tool, and how the numbers behind it are calculated.",
)


# ---------------------------------------------------------------------------
# What this tool does
# ---------------------------------------------------------------------------
render_page_context_callout(
    "This tool compares the lifetime cost of an air-to-water heat pump against a gas boiler, "
    "for a household installing in any year from 2026 to 2035. There are three pages:<br><br>"
    "&bull; <b>Lifetime cost comparison</b> - compares both systems given your assumptions<br>"
    "&bull; <b>Solve for subsidy</b> - what subsidy would make a heat pump as cheap as a gas boiler<br>"
    "&bull; <b>Solve for electricity-gas price ratio</b> - what electricity-to-gas price ratio would "
    "make a heat pump as cheap as a gas boiler"
)

# ---------------------------------------------------------------------------
# Explaining inputs
# ---------------------------------------------------------------------------
render_section_heading("Understanding the sidebar")
st.markdown(
    """
    <div style="font-size:14px; color:#333; line-height:1.7; margin-bottom:16px;">
    Use the sidebar on each page to set your <b>inputs</b>. The default settings are our standard ASF assumptions.
    The table below explains what each input means and which calculation it feeds into.
    </div>
    """,
    unsafe_allow_html=True,
)

input_rows = [
    (
        "Fixed",
        "Base year",
        "—",
        f"The year all costs are expressed in real terms relative to. Every £ figure in this tool is '{BASE_YEAR_DEFAULT} real £'.",
    ),
    (
        "Fixed",
        "Inflation rate",
        "%",
        "Used to convert nominal (actual cash) figures into real terms, and vice versa.",
    ),
    (
        "Fixed",
        "Discount rate",
        "%",
        "Converts future costs into present value. Used in every discounted and annualised (EAC) calculation.",
    ),
    (
        "Fixed",
        "Installation year range",
        "—",
        "The range of years a system can be installed in, across every chart and table in this tool (2026-2035).",
    ),
    (
        "Household",
        "Heat demand met by the gas boiler",
        "e.g. 16,840 kWh/yr",
        "The property's baseline heat need (space heat + hot water). Feeds directly into the gas boiler's running cost.",
    ),
    (
        "Household",
        "Extra heat demand with a heat pump",
        "%",
        "Applied on top of the gas boiler baseline to get the heat pump's heat demand.",
    ),
    (
        "Energy prices",
        "Gas / electricity unit price today",
        "p/kWh",
        "The starting point for each fuel's price trajectory. Feeds directly into running cost for both systems.",
    ),
    (
        "Energy prices",
        "Price trajectory (flat / annual % / custom)",
        "—",
        "How the unit price is assumed to change in future years. Changes every future year's running cost, and therefore lifetime and annualised cost.",
    ),
    (
        "Heat pump",
        "Lifespan",
        "years",
        "How many years the system operates for. Determines the annualisation period for calculating the Equivalent Annual Cost (EAC) and how many years of running/maintenance cost are summed.",
    ),
    (
        "Heat pump",
        "SCOP",
        "ratio",
        "Seasonal Coefficient of Performance - how much heat is produced per unit of electricity used. Directly divides down the electricity demand needed to meet the heat demand, so it scales running cost.",
    ),
    (
        "Heat pump",
        "Time-of-use tariff discount",
        "%",
        "The saving assumed on the electricity unit rate for a time-of-use tariff. Reduces the effective electricity price used in the heat pump's running cost only.",
    ),
    (
        "Heat pump",
        "Installation cost today",
        "£",
        "The upfront capital cost before any subsidy. Feeds into capital cost, and (if financed) the size of loan repayments.",
    ),
    (
        "Heat pump",
        "Installation cost trend",
        "flat / annual %",
        "How installation cost is assumed to change for later installation years. Changes the capital cost for systems installed later in the 2026–2035 range.",
    ),
    (
        "Heat pump",
        "Subsidy pathway",
        "£",
        "Reduces installation cost before financing/capital cost is calculated. Preset options from "
        "the dropdown (Flat, Slow stepdown, Fast stepdown, High, Zero from 2028, Smallest, No subsidy) "
        "reflect different possible futures for the Boiler Upgrade Scheme, and "
        "can be overridden year by year in the sidebar.",
    ),
    (
        "Heat pump",
        "Financing (on/off, rate, term)",
        "% / years",
        "If on, spreads the net installation cost over a loan (starting one year after installation) "
        "instead of paying it all upfront. This adds interest as a genuine extra cost, and also "
        "changes the timing of payments - both of which affect the resulting EAC.",
    ),
    (
        "Heat pump",
        "Maintenance cost",
        "£ / yr",
        "A fixed annual cost. Adds directly to maintenance cost.",
    ),
    (
        "Gas boiler",
        "Lifespan",
        "years",
        "Same role as heat pump lifespan, for the gas boiler's own EAC calculation.",
    ),
    (
        "Gas boiler",
        "Efficiency",
        "ratio",
        "How much of the gas burned converts to usable heat. Scales gas demand needed to meet the heat demand, so it scales running cost.",
    ),
    (
        "Gas boiler",
        "Installation cost",
        "£",
        "The upfront capital cost. No subsidy or financing option - always paid upfront.",
    ),
    (
        "Gas boiler",
        "Maintenance cost",
        "£ / yr",
        "A fixed annual cost. Adds directly to maintenance cost.",
    ),
    (
        "Gas boiler",
        "Include gas standing charge",
        "on/off",
        "If on, adds the daily gas standing charge to running cost - reflecting a household that could "
        "fully disconnect from gas if it switched to a heat pump (no other gas appliances). Uses the latest Ofgem price cap standing "
        "charge, held constant across the system's lifespan and every installation year.",
    ),
]

rows_html = "".join(
    f"<tr>"
    f'<td style="padding:8px 12px; font-weight:700; color:#0F294A; white-space:nowrap;">{category}</td>'
    f'<td style="padding:8px 12px; white-space:nowrap;">{input_name}</td>'
    f'<td style="padding:8px 12px; text-align:center; white-space:nowrap;">{units}</td>'
    f'<td style="padding:8px 12px; color:#444;">{meaning}</td>'
    f"</tr>"
    for category, input_name, units, meaning in input_rows
)

st.markdown(
    f"""
    <div style="overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:13px;">
            <tr style="background:#DDD9D6; font-weight:700; color:#0F294A;">
                <td style="padding:8px 12px;">Section</td>
                <td style="padding:8px 12px;">Input</td>
                <td style="padding:8px 12px; text-align:center;">Units</td>
                <td style="padding:8px 12px;">What it means / what it affects</td>
            </tr>
            {rows_html}
        </table>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Explaining calculations
# ---------------------------------------------------------------------------
render_section_heading("How the numbers are calculated")

st.markdown(
    """
    <div style="font-size:14px; color:#333; line-height:1.7;">
    All calculations in this tool (cost trajectories, annualised lifetime costs, and both
    solvers) are performed by <b>asf_lifetime_cost_model</b>, an open Python package built
    and maintained by ASF, separate from this Streamlit app.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="background-color:#D5F0F4; padding:10px 12px; margin:12px 0; font-size:14px; color:#333; line-height:1.7;">
    <b>Annualised lifetime cost</b> = <b>Equivalent Annual Cost (EAC)</b>. It's one constant
    £/year figure representing the true cost of owning a system over its whole lifetime,
    not a simple average (total cost &divide; years). It accounts for money spent later
    counting for slightly less than money spent now, so a heat pump (mostly paid upfront) and
    a gas boiler (cheaper upfront, pricier to run) can be compared fairly. See the explanation
    below for the full details.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="font-size:14px; color:#333; line-height:1.7;">
    In this app, we use this package to:<br>
    &bull; <b>Build year-by-year cost and price trajectories</b> that are either held flat, growing
    at a set rate, or set to custom values you've entered - for installation cost, subsidy, and
    energy prices.<br>
    &bull; <b>Calculate the lifetime cost of a heat pump or gas boiler</b>, via a
    <code>HeatingSystem</code> class with methods for capital, maintenance, and running cost
    calculations - including the effect that money spent later is worth less today than money
    spent now (discounting), converted into one comparable figure per year (Equivalent Annual
    Cost).<br>
    &bull; <b>Works out exactly what subsidy or electricity price</b> would make two systems'
    annualised costs equal.
    </div>
    """,
    unsafe_allow_html=True,
)
render_callout(
    "The full source code, including every calculation method, is available "
    'at <a href="https://github.com/nestauk/asf_lifetime_cost_model" target="_blank" '
    'style="color:#0F294A; font-weight:700; text-decoration:underline;">'
    "github.com/nestauk/asf_lifetime_cost_model</a>."
)

# ---------------------------------------------------------------------------
# Limitations and caveats
# ---------------------------------------------------------------------------
render_section_heading("Known limitations")
st.markdown(
    """
    <div style="font-size:14px; color:#333; line-height:1.8;">
    &bull; Financing assumes <b>no deposit</b> and the loan always covers 100% of the net installation cost.<br>
    &bull; Heat demand is assumed <b>flat across the year</b> with no month-by-month seasonality.<br>
    &bull; <b>SCOP is held constant</b> across every installation year - a system installed in 2035 is assumed
    to have the same efficiency as one installed in 2026, with no ability to model improvement over time.<br>
    &bull; Maintenance is assumed to occur <b>once a year</b>, at a fixed cost.<br>
    &bull; The comparison assumes the household stays in the property for the <b>full system lifespan</b>.<br>
    &bull; The electricity-gas price ratio solver assumes a <b>flat electricity price</b>. The
    solved value scales this flat baseline, so it comes out constant across the system's lifetime,
    not a realistic future price trend. The implied ratio to gas can still vary year to year if
    you've set gas prices to change over time.
    <p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
#  Equivalent Annual Cost (EAC)
# ---------------------------------------------------------------------------
render_section_heading("Why Equivalent Annual Cost (EAC)?")
st.markdown(
    """
    <div style="font-size:14px; color:#333; line-height:1.7;">
    Every annualised cost figure in this tool is shown as an <b>Equivalent Annual Cost (EAC)</b> -
    a level yearly payment that has the same present value as the system's real, uneven
    payment schedule. This is <b>not</b> the same as dividing a total cost by its lifespan.<br><br>

    For example, a £3,000 installation cost, paid entirely upfront, does <b>not</b> annualise
    to £3,000 &divide; 15 = £200/year. Its EAC comes out higher at around £252/year at a 3.5%
    discount rate because paying the full amount immediately is a genuinely more "expensive"
    way to spread a cost than paying it gradually over time. Money spent later is worth less,
    in today's terms, than money spent now. Aa lump sum paid today has to be converted into
    a <i>larger</i> level annual payment to be fairly comparable to a cost that's 
    spread across many years (like running costs).<br><br>

    EAC allows us to fairly compare two options with very different payment
    timing, like a heat pump (large upfront cost, lower running costs) against a gas boiler (small
    upfront cost, higher running costs), without one option looking artificially cheaper just
    because more of its cost happens later.
    </div>
    """,
    unsafe_allow_html=True,
)
render_callout(
    f"All figures are real terms ({BASE_YEAR_DEFAULT} £), discounted at "
    f"<b>{DISCOUNT_RATE_DEFAULT:.1%}</b> per HM Treasury Green Book guidance, using the "
    "annuity-due convention (the first operating year is undiscounted)."
)
