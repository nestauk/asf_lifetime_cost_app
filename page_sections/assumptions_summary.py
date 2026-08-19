"""Assumptions summary card, shown at the top of the main content area.

Reads directly from the AppInputs object returned by render_sidebar(), so
this doubles as a live test that every sidebar section is correctly
flowing through into the dataclass.

Layout note: Streamlit's st.columns() cannot be nested inside a single
HTML <div> opened via st.markdown() — each column is its own independent
layout region. So instead of one continuous card spanning the header and
both columns, this renders as: one card for the header, then two
side-by-side cards (one per column) directly beneath it. Every div here
is self-contained (opened and closed within the same block) to avoid the
"forgot to close a div" bugs from earlier iterations.
"""

import streamlit as st

from config.defaults import (
    BASE_YEAR_DEFAULT,
    DISCOUNT_RATE_DEFAULT,
    INFLATION_RATE_DEFAULT,
)
from model_integration.schema import AppInputs

CARD_BG = "#F6F4F2"
CARD_SHADOW = "0 1px 3px rgba(0,0,0,0.06)"
NAVY = "#0F294A"
TEAL = "#18A48C"
BLUE = "#0000FF"
PURPLE = "#9A1BBE"
PINK = "#F6A4B7"


def _card_open(border_color: str = NAVY, extra_style: str = "") -> str:
    """Opening tag for a card: navy left border, shared background/shadow. Caller must close with </div>."""
    return (
        f'<div style="border-left:4px solid {border_color}; background:{CARD_BG}; '
        f'box-shadow:{CARD_SHADOW}; padding:16px 20px; {extra_style}">'
    )


def _section_title(text: str, underline_color: str) -> str:
    """A bold title with a colored underline, used inside a card (e.g. 'Heat pump')."""
    return (
        f'<div style="font-size:15px; font-weight:700; color:{NAVY}; '
        f'border-bottom:2px solid {underline_color}; padding-bottom:6px; margin-bottom:8px;">{text}</div>'
    )


def _row(label: str, value: str) -> str:
    """One label/value row, with a light divider beneath it."""
    return (
        f"<div style='display:flex; justify-content:space-between; padding:8px 0; "
        f"font-size:13.5px; border-bottom:1px solid #ddd8d4;'>"
        f"<span style='color:#666;'>{label}</span>"
        f"<span style='color:{NAVY}; font-weight:400; text-align:right;'>{value}</span>"
        f"</div>"
    )


def _rows(pairs: list[tuple[str, str]]) -> str:
    return "".join(_row(label, value) for label, value in pairs)


def render_assumptions_summary(inputs: AppInputs) -> None:
    """Render the full assumptions summary: header card, then Heat pump / Gas boiler cards side by side."""
    hp = inputs.heat_pump
    gb = inputs.gas_boiler
    ep = inputs.energy_prices

    # ------------------------------------------------------------------
    # Header card (self-contained: opened and closed here)
    # ------------------------------------------------------------------
    st.markdown(
        f"""
        {_card_open(extra_style="margin-bottom:16px;")}
            <div style="font-size:20px; font-weight:800; color:{NAVY}; margin-bottom:6px;">
                The assumptions behind these results
            </div>
            <div style="font-size:13px; color:#666; margin-bottom:4px;">
                Base year {BASE_YEAR_DEFAULT} &middot;
                {INFLATION_RATE_DEFAULT:.1%} inflation &middot; {DISCOUNT_RATE_DEFAULT:.1%} discount rate
            </div>
            <div style="font-size:13px; font-weight:700; color:{NAVY};">
                Shown as present value, {BASE_YEAR_DEFAULT} real £
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Household + Heat pump cards (col1) / Gas boiler + Energy prices cards (col2)
    # Each card below is opened and closed within its own st.markdown call.
    # ------------------------------------------------------------------
    col1, col2 = st.columns(2, gap="small")

    with col1:
        ashp_heat_demand = inputs.boiler_heat_demand * (
            1 + inputs.heat_pump_heat_demand_uplift
        )

        household_rows = _rows(
            [
                (
                    "Heat demand met by the gas boiler",
                    f"{inputs.boiler_heat_demand:,.0f} kWh/yr",
                ),
                (
                    "Heat demand met by the heat pump",
                    f"{ashp_heat_demand:,.0f} kWh/yr ({inputs.heat_pump_heat_demand_uplift:.0%} uplift)",
                ),
            ]
        )

        subsidy_line = (
            "Solved for on this page"
            if hp.subsidy_scenario is None
            else f"{hp.subsidy_scenario}, {len(hp.subsidy_overrides)} year(s) overridden"
        )
        financing_line = (
            f"{hp.interest_rate:.1%} interest over {hp.loan_term} years"
            if hp.is_financed
            else "Not financed"
        )
        installation_growth = (
            "flat in real terms"
            if hp.installation_cost_growth_mode == "flat"
            else f"{hp.installation_cost_growth_rate:+.1%} a year in real terms"
        )

        heat_pump_rows = _rows(
            [
                ("Lifespan", f"{hp.lifespan} years"),
                ("SCOP", f"{hp.scop:.1f}"),
                (
                    "Installation",
                    f"£{hp.installation_cost_current:,.0f} in {BASE_YEAR_DEFAULT}, {installation_growth}",
                ),
                ("Subsidy", subsidy_line),
                ("Financing", financing_line),
                (
                    "Maintenance",
                    f"£{hp.maintenance_cost_per_visit:,.0f} per service, {hp.maintenance_annual_frequency:.1f} times a year",
                ),
                (
                    "Time-of-use tariff discount",
                    f"{hp.tou_tariff_discount:.0%} off the electricity unit rate price cap",
                ),
            ]
        )

        st.markdown(
            f"""
            {_card_open(border_color=NAVY)}
                {_section_title("Household", underline_color=PINK)}
                {household_rows}
            </div>
            {_card_open(border_color=NAVY, extra_style="margin-bottom:12px;")}
                {_section_title("Heat pump", underline_color=TEAL)}
                {heat_pump_rows}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        standing_charge_line = (
            f"Included &mdash; {gb.standing_charge:.2f} p/day, held constant"
            if gb.include_standing_charge
            else "Not included"
        )

        gas_boiler_rows = _rows(
            [
                ("Lifespan", f"{gb.lifespan} years"),
                ("Efficiency", f"{gb.efficiency:.2f}"),
                ("Installation", f"£{gb.installation_cost:,.0f}, flat in real terms"),
                (
                    "Maintenance",
                    f"£{hp.maintenance_cost_per_visit:,.0f} per service, {hp.maintenance_annual_frequency:.1f} times a year",
                ),
                ("Standing charge", standing_charge_line),
            ]
        )

        gas_growth_desc = (
            "flat in all future years"
            if ep.gas_growth_mode == "flat"
            else f"{ep.gas_growth_rate:+.1%} a year"
            if ep.gas_growth_mode == "annual_pct"
            else f"custom table, {len(ep.gas_overrides)} year(s) overridden"
        )
        if ep.electricity_current_price is None:
            electricity_desc = "Solved for on this page"
        elif ep.electricity_growth_mode == "flat":
            electricity_desc = f"{ep.electricity_current_price:.2f} p/kWh in {BASE_YEAR_DEFAULT}, flat in all future years"
        elif ep.electricity_growth_mode == "annual_pct":
            electricity_desc = f"{ep.electricity_current_price:.2f} p/kWh in {BASE_YEAR_DEFAULT}, {ep.electricity_growth_rate:+.1%} a year"
        else:
            electricity_desc = (
                f"{ep.electricity_current_price:.2f} p/kWh in {BASE_YEAR_DEFAULT}, custom table, "
                f"{len(ep.electricity_overrides)} year(s) overridden"
            )

        energy_price_rows = _rows(
            [
                ("Gas", f"{ep.gas_current_price:.2f} p/kWh, {gas_growth_desc}"),
                ("Electricity", electricity_desc),
            ]
        )

        st.markdown(
            f"""
            {_card_open(border_color=NAVY)}
                {_section_title("Energy prices", underline_color=PURPLE)}
                {energy_price_rows}
            </div>
            {_card_open(border_color=NAVY, extra_style="margin-bottom:12px;")}
                {_section_title("Gas boiler", underline_color=BLUE)}
                {gas_boiler_rows}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------
    # Download button
    # ------------------------------------------------------------------
    st.markdown(
        """
        <style>
            [data-testid="stDownloadButton"] button {
                background-color: #0000FF;
                color: white;
                font-weight: 700;
                border: none;
                clip-path: polygon(
                                0 0,
                                calc(100% - 14px) 0,
                                100% 14px,
                                100% 100%,
                                14px 100%,
                                0 calc(100% - 14px)
                            );
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.download_button(
        label="⬇ Download these assumptions",
        data=_build_assumptions_text(inputs),
        file_name="assumptions.txt",
        mime="text/plain",
    )


def _build_assumptions_text(inputs: AppInputs) -> str:
    """Plain-text version of the assumptions summary, for the download button."""
    hp = inputs.heat_pump
    gb = inputs.gas_boiler
    ep = inputs.energy_prices

    ashp_heat_demand = inputs.boiler_heat_demand * (
        1 + inputs.heat_pump_heat_demand_uplift
    )
    subsidy_line = (
        "Solved for on this page"
        if hp.subsidy_scenario is None
        else f"{hp.subsidy_scenario}, {len(hp.subsidy_overrides)} year(s) overridden"
    )
    financing_line = (
        f"{hp.interest_rate:.1%} interest over {hp.loan_term} years"
        if hp.is_financed
        else "Not financed"
    )
    installation_growth = (
        "flat in real terms"
        if hp.installation_cost_growth_mode == "flat"
        else f"{hp.installation_cost_growth_rate:+.1%} a year in real terms"
    )
    standing_charge_line = (
        f"Included, {gb.standing_charge:.2f} p/day, held constant"
        if gb.include_standing_charge
        else "Not included"
    )
    gas_growth_desc = (
        "flat in all future years"
        if ep.gas_growth_mode == "flat"
        else f"{ep.gas_growth_rate:+.1%} a year"
        if ep.gas_growth_mode == "annual_pct"
        else f"custom table, {len(ep.gas_overrides)} year(s) overridden"
    )
    if ep.electricity_current_price is None:
        electricity_desc = "Solved for on this page"
    elif ep.electricity_growth_mode == "flat":
        electricity_desc = f"{ep.electricity_current_price:.2f} p/kWh in {BASE_YEAR_DEFAULT}, flat in all future years"
    elif ep.electricity_growth_mode == "annual_pct":
        electricity_desc = f"{ep.electricity_current_price:.2f} p/kWh in {BASE_YEAR_DEFAULT}, {ep.electricity_growth_rate:+.1%} a year"
    else:
        electricity_desc = (
            f"{ep.electricity_current_price:.2f} p/kWh in {BASE_YEAR_DEFAULT}, custom table, "
            f"{len(ep.electricity_overrides)} year(s) overridden"
        )

    lines = [
        "The assumptions behind these results",
        f"Base year {BASE_YEAR_DEFAULT}, "
        f"{INFLATION_RATE_DEFAULT:.1%} inflation, {DISCOUNT_RATE_DEFAULT:.1%} discount rate",
        f"Shown as present value, {BASE_YEAR_DEFAULT} real £",
        "",
        "HOUSEHOLD",
        f"  Heat demand met by the gas boiler: {inputs.boiler_heat_demand:,.0f} kWh/yr",
        f"  Heat demand met by the heat pump: {ashp_heat_demand:,.0f} kWh/yr ({inputs.heat_pump_heat_demand_uplift:.0%} uplift)",
        "",
        "HEAT PUMP",
        f"  Lifespan: {hp.lifespan} years",
        f"  SCOP: {hp.scop:.1f}",
        f"  Installation: £{hp.installation_cost_current:,.0f} in {BASE_YEAR_DEFAULT}, {installation_growth}",
        f"  Subsidy: {subsidy_line}",
        f"  Financing: {financing_line}",
        f"  Maintenance: £{hp.maintenance_cost_per_visit:,.0f} per service, {hp.maintenance_annual_frequency:.1f} times a year",
        f"  Time-of-use tariff discount: {hp.tou_tariff_discount:.0%} off the electricity unit rate price cap",
        "",
        "GAS BOILER",
        f"  Lifespan: {gb.lifespan} years",
        f"  Efficiency: {gb.efficiency:.2f}",
        f"  Installation: £{gb.installation_cost:,.0f}, flat in real terms",
        f"  Maintenance: £{hp.maintenance_cost_per_visit:,.0f} per service, {hp.maintenance_annual_frequency:.1f} times a year",
        f"  Standing charge: {standing_charge_line}",
        "",
        "ENERGY PRICES",
        f"  Gas: {ep.gas_current_price:.2f} p/kWh, {gas_growth_desc}",
        f"  Electricity: {electricity_desc}",
    ]
    return "\n".join(lines)
