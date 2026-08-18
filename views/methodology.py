"""Methodology and data documentation page."""

import streamlit as st

from components.callouts import render_callout, render_page_context_callout
from components.layout import render_page_title, render_section_heading
from config.defaults import (
    BASE_YEAR_DEFAULT,
    DISCOUNT_RATE_DEFAULT,
    INFLATION_RATE_DEFAULT,
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
render_section_heading("Understanding the sidebar and each input")
st.markdown(
    """
    <div style="font-size:14px; color:#333; line-height:1.7; margin-bottom:16px;">
    Use the sidebar on each page to set your <b>inputs</b>. Default settings are our standard ASF assumptions.
    The table below explains what each input means and which calculation it feeds into.
    </div>
    """,
    unsafe_allow_html=True,
)

input_rows = [
    (
        "Fixed",
        "Base year",
        f"{BASE_YEAR_DEFAULT}",
        f"The year all costs are expressed in real terms relative to. "
        f"Unless stated otherwise, all figures are in '{BASE_YEAR_DEFAULT} real £'.",
    ),
    (
        "Fixed",
        "Inflation rate",
        f"{INFLATION_RATE_DEFAULT:.1%}",
        "Used to convert nominal (actual cash) figures into real terms, and vice versa. Set at the Bank of England's CPI target.",
    ),
    (
        "Fixed",
        "Discount rate",
        f"{DISCOUNT_RATE_DEFAULT:.1%}",
        "Converts future costs into present value. Used in every discounted and annualised (EAC) calculation. Set to HM Treasury's "
        "The Green Book guidance for Social Time Preference Rate to convert future costs and benefits into present values.",
    ),
    (
        "Fixed",
        "Installation year range",
        "2026 - 2035",
        "The range of years a system can be installed in, across every chart and table in this tool (2026-2035).",
    ),
    (
        "Household",
        "Heat demand met by the gas boiler",
        "16,823 kWh/yr",  # Update as our views on typical heat demand change
        "The property's baseline heat need (space heat + hot water) met by a gas boiler, before "
        "switching to a heat pump. Used to calculate the gas boiler's running cost. Default value "
        "matches the median heat demand for a home installing an 8-10 kW air-to-water heat pump in "
        "the 2025/26 financial year (Source: Nesta analysis of MCS installations data), since the "
        "heat pump uplift defaults to 0% — at any other uplift setting, this figure would be lower "
        "than the heat pump's own demand.",
    ),
    (
        "Household",
        "Extra heat demand with a heat pump",
        "0%",
        "Applied on top of the gas boiler baseline to get the heat pump's heat demand. Default assumes "
        "no difference between the two systems",
    ),
    (
        "Energy prices",
        "Gas / electricity unit price today",
        "Latest price cap unit rate p/kWh",
        "The starting point for each fuel's price trajectory (2026). This is the final retail price (Direct Debit, GB average), including "
        "VAT where applied (Note: VAT has been removed from electricity bills from Oct 26 - Mar 27). Feeds directly into "
        "running cost for both systems.",
    ),
    (
        "Heat pump",
        "Lifespan",
        "15 years",
        "How many years the system operates for. Determines the annualisation period for calculating the Equivalent Annual Cost (EAC) and how many years of running/maintenance cost are summed.",
    ),
    (
        "Heat pump",
        "SCOP",
        "3.0",
        "Seasonal Coefficient of Performance - how much heat is produced per unit of electricity used. "
        "Directly divides down the electricity demand needed to meet the heat demand, so it scales "
        "running cost.",
    ),
    (
        "Heat pump",
        "Time-of-use tariff discount",
        "15%",
        "The saving assumed on the electricity unit rate for a time-of-use tariff. Reduces the effective electricity price used in the heat pump's running cost only. "
        "Default assumes that households use a time of use tariff and get a 15% discount on running costs compared to the price cap. This reflects the results of modelling "
        "done by Cornwall Insights for Nesta, although other estimates find similar results.",
    ),
    (
        "Heat pump",
        "Installation cost today",
        "£12,500",
        "The installation cost before any subsidy. Feeds into capital cost, and (if financed) the size of loan repayments. Default value "
        "is the median cost for a home installing an 8-10 kW air-to-water heat pump in "
        "the 2025/26 financial year (Source: Nesta analysis of MCS installations data)",
    ),
    (
        "Heat pump",
        "Installation cost trend",
        "-2.5% / yr",
        "How installation cost is assumed to change for later installation years. Options are "
        "<b>Flat</b> (held at today's value) or <b>% change per year</b>. Changes the capital cost "
        "for systems installed later in the 2026–2035 range. Default value is based on Nesta's "
        "analysis of historical Boiler Upgrade Scheme statistics.",
    ),
    (
        "Heat pump",
        "Subsidy pathway",
        "Flat (£7,500 today, held constant in the future)",
        "Reduces installation cost before financing/capital cost is calculated. Preset options from "
        "the dropdown (Flat, Slow stepdown, Fast stepdown, High, Zero from 2028, Smallest, No subsidy) "
        "reflect different possible futures for the Boiler Upgrade Scheme, and can be overridden year "
        "by year in the sidebar. These trajectories were previously modelled by Nesta - see "
        '<a href="https://www.nesta.org.uk/report/how-to-make-heat-pumps-more-affordable/" target="_blank" '
        'style="color:#0F294A; text-decoration:underline;">How to make heat pumps more affordable</a>.',
    ),
    (
        "Heat pump",
        "Financing (on/off, interest rate, term)",
        "Off",
        "If on, spreads the net installation cost over a loan (starting one year after installation) "
        "instead of paying it all upfront. This adds interest as a genuine extra cost, and also "
        "changes the timing of payments - both of which affect the resulting EAC.",
    ),
    (
        "Heat pump",
        "Maintenance cost",
        "£80 / yr",
        "A fixed annual cost. Adds directly to the maintenance "
        "cost component of the heat pump's lifetime cost.",
    ),
    (
        "Gas boiler",
        "Lifespan",
        "15 years",
        "Same role as heat pump lifespan, for the gas boiler's own lifetime cost calculation.",
    ),
    (
        "Gas boiler",
        "Efficiency",
        "0.85",
        "How much of the gas burned converts to usable heat. Scales gas demand needed to meet the heat demand, so it scales running cost.",
    ),
    (
        "Gas boiler",
        "Installation cost",
        "£3,000",
        "The upfront capital cost. No subsidy or financing option - always paid upfront.",
    ),
    (
        "Gas boiler",
        "Maintenance cost",
        "£80 / yr",
        "A fixed annual cost. Adds directly to the maintenance "
        "cost component of the gas boiler's lifetime cost.",
    ),
    (
        "Gas boiler",
        "Include gas standing charge",
        "Included",
        "If included in the gas boiler's cost calculation, adds the daily gas standing charge to running cost - reflecting a household that could "
        "fully disconnect from gas if it switched to a heat pump (no other gas appliances). Uses the latest Ofgem price cap standing "
        "charge, held constant across the system's lifespan and every installation year.",
    ),
]

SECTION_COLORS = {
    "Fixed": "#646363",
    "Household": "#18A48C",
    "Energy prices": "#FDB633",
    "Heat pump": "#0000FF",
    "Gas boiler": "#EB003B",
}

rows_html = "".join(
    f"<tr>"
    f'<td style="padding:8px 12px; font-weight:700; color:#0F294A; white-space:nowrap; '
    f'border-left:4px solid {SECTION_COLORS.get(category, "#DDD")};">{category}</td>'
    f'<td style="padding:8px 12px; white-space:nowrap;">{input_name}</td>'
    f'<td style="padding:8px 12px; text-align:center; white-space:nowrap;">{default}</td>'
    f'<td style="padding:8px 12px; color:#444;">{meaning}</td>'
    f"</tr>"
    for category, input_name, default, meaning in input_rows
)

st.markdown(
    f"""
    <div style="overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:13px;">
            <tr style="background:#DDD9D6; font-weight:700; color:#0F294A;">
                <td style="padding:8px 12px; border-left:4px solid #000;">Section</td>
                <td style="padding:8px 12px;">Input</td>
                <td style="padding:8px 12px;">Default</td>
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
    solvers) are performed by
    <a href="https://github.com/nestauk/asf_lifetime_cost_model" target="_blank"
    style="color:#0F294A; font-weight:700; text-decoration:underline;">asf_lifetime_cost_model</a>,
    an open Python package built and maintained by ASF, separate from this Streamlit app.
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
    &bull; <b>Solve directly for the subsidy or electricity price</b> that would make two systems'
    annualised costs equal (algebraically).
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
render_section_heading("Limitations and caveats")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="background:#F6F4F2; border-left:4px solid #0F294A; padding:16px 20px;">
            <div style="font-size:15px; font-weight:700; color:#0F294A; margin-bottom:8px;">
                Known limitations
            </div>
            <div style="font-size:14px; color:#333; line-height:1.8;">
            &bull; <b>Efficiency is held constant.</b> SCOP and boiler efficiency don't degrade over a
            system's life, and don't improve for later installation years - a system installed in 2035
            is assumed exactly as efficient as one installed in 2026.<br><br>
            &bull; <b>Financing assumes no deposit.</b> A loan always covers 100% of the net installation
            cost.<br><br>
            &bull; <b>Maintenance cost is fixed.</b> It doesn't change year to year, and doesn't depend on
            installation year.<br><br>
            &bull; <b>No month-by-month detail.</b> Heat demand is a single annual total, and energy
            prices are a single flat annual rate. The model can't capture things like a heat pump running
            less efficiently in cold months, or bills changing with quarterly price cap updates.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="background:#F6F4F2; border-left:4px solid #0F294A; padding:16px 20px;">
            <div style="font-size:15px; font-weight:700; color:#0F294A; margin-bottom:8px;">
                Caveats on interpreting the numbers
            </div>
            <div style="font-size:14px; color:#333; line-height:1.8;">
            &bull; <b>"Today's price" means {BASE_YEAR_DEFAULT}.</b> Every system starts from
            {BASE_YEAR_DEFAULT}'s prices and costs, whatever installation year is selected — a system
            installed in 2035 still applies its growth trend starting from {BASE_YEAR_DEFAULT}, not
            2035.<br><br>
            &bull; <b>Default energy prices reflect the latest published Ofgem rates, which may not yet be in
            effect.</b> Ofgem announces each new price cap ahead of its start date, so the default shown can
            be a rate that's been confirmed but hasn't started. It will update once the next cap is
            published.<br><br>
            &bull; <b>The electricity-gas price ratio solver assumes a flat electricity price.</b> The
            solved value is constant across the system's lifetime. The ratio to gas can still change year
            to year if gas prices are set to change.<br><br>
            &bull; <b>Gas standing charge doesn't change over time.</b> It's held at the latest price cap
            value for every year and every installation year, unlike energy unit prices, which can follow
            a trend.
            </div>
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
    in today's terms, than money spent now. A lump sum paid today has to be converted into
    a <i>larger</i> level annual payment to be fairly comparable to a cost that's 
    spread across many years (like running costs).<br><br>

    EAC is useful because it puts costs with different timing onto a <b>like-for-like annual
    basis</b>. This allows us to fairly compare options with different cost profiles - for
    example, a heat pump with a large upfront cost and lower running costs against a gas
    boiler with a smaller upfront cost and higher running costs.
    </div>
    """,
    unsafe_allow_html=True,
)
render_callout(
    f"All figures are in real terms ({BASE_YEAR_DEFAULT} £) and discounted at "
    f"<b>{DISCOUNT_RATE_DEFAULT:.1%}</b> in line with HM Treasury Green Book guidance. "
    "EAC takes account of the timing of each cost: the upfront installation cost is counted "
    "at its full value, while future running and maintenance costs are discounted.<br><br>"
    "<b>Two payment conventions are used:</b> EAC uses an <b>annuity-due</b> convention "
    "because the first operating year's cost is counted immediately. Loan repayments use an "
    "<b>ordinary annuity</b> because the first repayment is made one year after installation. "
    "This reflects the different timing of the two types of payment.<br><br>"
    "If a purchase is financed, the repayments occur in future years and are therefore "
    "discounted as future costs. In all cases, EAC converts the different payment schedules "
    "into one annual figure for fair comparison."
)
