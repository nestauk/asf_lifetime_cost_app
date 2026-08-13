"""Renders sidebar widgets, returns a fully populated AppInputs object.

Shared across all pages — each page calls render_sidebar() with a `mode`
argument selecting which section (if any) should be replaced with a
"solved for" note instead of its normal editable widgets.
"""

import pandas as pd
import streamlit as st

from components.callouts import render_callout, render_divider
from components.sidebar_builder import (
    render_locked_value,
    render_sidebar_section_header,
)
from config.defaults import (
    ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT,
    ASHP_HEAT_DEMAND_UPLIFT_PCT_MAX,
    ASHP_HEAT_DEMAND_UPLIFT_PCT_MIN,
    ASHP_INSTALLATION_COST_DEFAULT,
    ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT,
    ASHP_INSTALLATION_COST_GROWTH_RATE_MAX,
    ASHP_INSTALLATION_COST_GROWTH_RATE_MIN,
    ASHP_INTEREST_RATE_DEFAULT,
    ASHP_INTEREST_RATE_MAX,
    ASHP_INTEREST_RATE_MIN,
    ASHP_LIFESPAN_DEFAULT,
    ASHP_LIFESPAN_MAX,
    ASHP_LIFESPAN_MIN,
    ASHP_LOAN_TERM_DEFAULT,
    ASHP_LOAN_TERM_MAX,
    ASHP_LOAN_TERM_MIN,
    ASHP_MAINTENANCE_COST_DEFAULT,
    ASHP_MAINTENANCE_FREQUENCY_DEFAULT,
    ASHP_SCOP_DEFAULT,
    ASHP_SCOP_MAX,
    ASHP_SCOP_MIN,
    ASHP_SUBSIDY_SCENARIO_DEFAULT,
    ASHP_TOU_DISCOUNT_DEFAULT,
    ASHP_TOU_DISCOUNT_MAX,
    ASHP_TOU_DISCOUNT_MIN,
    BASE_YEAR_DEFAULT,
    BOILER_EFFICIENCY_DEFAULT,
    BOILER_EFFICIENCY_MAX,
    BOILER_EFFICIENCY_MIN,
    BOILER_HEAT_DEMAND_DEFAULT,
    BOILER_HEAT_DEMAND_MAX,
    BOILER_HEAT_DEMAND_MIN,
    BOILER_INCLUDE_STANDING_CHARGE_DEFAULT,
    BOILER_INSTALLATION_COST_DEFAULT,
    BOILER_LIFESPAN_DEFAULT,
    BOILER_LIFESPAN_MAX,
    BOILER_LIFESPAN_MIN,
    BOILER_MAINTENANCE_COST_DEFAULT,
    BOILER_MAINTENANCE_FREQUENCY_DEFAULT,
    DISCOUNT_RATE_DEFAULT,
    INFLATION_RATE_DEFAULT,
    INSTALL_END_YEAR,
    INSTALL_START_YEAR,
    OPERATING_END_YEAR,
    PROPERTY_DESCRIPTION,
    get_electricity_price_default,
    get_gas_price_default,
    get_latest_gas_standing_charge,
)
from model_integration.schema import (
    AppInputs,
    EnergyPriceInputs,
    GasBoilerInputs,
    HeatPumpInputs,
)
from model_integration.trajectories import (
    get_subsidy_scenario_options,
    get_subsidy_scenario_values,
)

GROWTH_MODE_LABELS = ["Flat", "Annual % change", "Custom"]
GROWTH_MODE_KEYS = {"Flat": "flat", "Annual % change": "annual_pct", "Custom": "custom"}
FUTURE_YEARS = list(range(INSTALL_START_YEAR + 1, OPERATING_END_YEAR + 1))  # 2027-2050


# ---------------------------------------------------------------------------
# Fixed section
# ---------------------------------------------------------------------------
def render_fixed_inputs() -> None:
    render_sidebar_section_header(
        "Fixed inputs", "Set for you. You can't change these."
    )
    # ---Inflation and discounting--- #
    col1, col2 = st.columns(2)
    with col1:
        render_locked_value("Base year", str(BASE_YEAR_DEFAULT))
    with col2:
        render_locked_value("Inflation rate", f"{INFLATION_RATE_DEFAULT * 100:.1f}%")
    st.markdown(
        "<div style='font-size:12px; color:#888; margin-bottom:12px;'>Inflation set at Bank of England's CPI target.</div>",
        unsafe_allow_html=True,
    )
    render_locked_value(
        "Discount rate",
        f"{DISCOUNT_RATE_DEFAULT * 100:.1f}%",
        "HM Treasury's The Green Book guidance for Social Time Preference Rate to convert future costs and benefits into present values.",
    )
    # ---Installation years range--- #
    render_locked_value(
        "Installation year range",
        str(INSTALL_START_YEAR) + " - " + str(INSTALL_END_YEAR),
    )
    # ---Reminder callout--- #
    render_callout(
        f"Every result is a <strong>present value in {BASE_YEAR_DEFAULT} real £</strong> - inflation-"
        "adjusted and discounted to what it's worth today. <strong>Real terms</strong> strips out "
        "inflation; <strong>nominal terms</strong> (not shown here) would be the actual cash on a "
        "future invoice."
    )


def render_user_inputs_heading() -> None:
    render_sidebar_section_header(
        "Your inputs",
        "Set today's value and, where it matters, how each assumption changes in future years.",
    )
    render_divider()


def render_solved_for_note(title: str, body: str) -> None:
    """Render an amber 'this input is solved for on this page' callout,
    replacing a section's normal editable widgets.
    """
    st.markdown(
        f"""
        <div style="
            background-color: #F5D98B;
            border-radius: 6px;
            padding: 16px 18px;
            margin-bottom: 16px;
        ">
            <div style="font-size:15px; font-weight:700; color:#0F294A; margin-bottom:4px;">{title}</div>
            <div style="font-size:13.5px; color:#0F294A; line-height:1.6;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Heat demand section
# ---------------------------------------------------------------------------


def render_household_section() -> tuple[float, float]:
    """Render the Property characteristics section: locked heat demand display + editable uplift slider.

    Returns the heat demand uplift value chosen by the user.
    """
    st.markdown(
        '<div style="font-size:16px; font-weight:700; color:#0F294A; margin-bottom:6px;">'
        "Household characteristics</div>",
        unsafe_allow_html=True,
    )

    boiler_heat_demand = st.number_input(
        "Heat demand met by the gas boiler (kWh/yr)",
        min_value=BOILER_HEAT_DEMAND_MIN,
        max_value=BOILER_HEAT_DEMAND_MAX,
        value=BOILER_HEAT_DEMAND_DEFAULT,
        step=100,
        key=_gen_key("boiler_heat_demand_input"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "The household's heat demand before switching to a heat pump. Default: median for a "
        "3-4 bed house fitting an 8-10 kW heat pump. Adjust for a larger, smaller, or "
        "better/worse insulated home.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size:14px; font-weight:700; color:#0F294A; margin-bottom:2px;">'
        "Extra heat demand with a heat pump</div>",
        unsafe_allow_html=True,
    )
    heat_pump_heat_demand_uplift_pct = st.slider(
        label="Extra heat demand with a heat pump",
        min_value=int(ASHP_HEAT_DEMAND_UPLIFT_PCT_MIN),
        max_value=int(ASHP_HEAT_DEMAND_UPLIFT_PCT_MAX),
        value=int(ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT),
        step=1,
        format="%d%%",
        label_visibility="collapsed",
        key=_gen_key("heat_pump_heat_demand_uplift"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "Heat pumps run at lower flow temperatures for longer, which can raise total heat demand "
        "compared with a gas boiler in the same home. Set this to 0 to assume no difference between "
        "the two systems.</div>",
        unsafe_allow_html=True,
    )
    render_divider()

    return boiler_heat_demand, heat_pump_heat_demand_uplift_pct / 100


# ---------------------------------------------------------------------------
# Energy prices section
# ---------------------------------------------------------------------------


def _render_fuel_price_inputs(
    fuel_label: str,
    default_current_price: float,
    key_prefix: str,
    disabled: bool = False,
) -> tuple[float | None, str | None, float | None, dict[int, float]]:
    """Render one fuel's price widgets: current price + Flat/Annual %/Custom future-years selector.

    Returns (current_price, growth_mode, growth_rate, overrides). If disabled,
    returns (None, None, None, {}) and shows a "solved for" note instead —
    used on the electricity-price-solver page.
    """
    if disabled:
        render_solved_for_note(
            title=f"{fuel_label} price is solved for on this page",
            body=(
                f"You don't set an {fuel_label.lower()} price here. The model works out the headline "
                "price cap rate — before any time-of-use discount — that each year would need to be "
                "for the heat pump's annual cost to match the gas boiler's. Gas price stays as you "
                "set it above."
            ),
        )
        return None, None, None, {}

    current_price = st.number_input(
        f"{fuel_label} unit price today (p/kWh)",
        value=round(default_current_price, 2),
        step=0.01,
        key=_gen_key(f"{key_prefix}_current_price"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        'Default: <a href="https://superset-asf.dap-tools.uk/superset/dashboard/asf-energy-bills/?standalone=true" '
        'target="_blank" style="color:#888; text-decoration:underline;">latest Ofgem price cap rate</a></div>',
        unsafe_allow_html=True,
    )

    growth_mode_label = st.segmented_control(
        f"{fuel_label} price in future years ({FUTURE_YEARS[0]}–{FUTURE_YEARS[-1]})",
        options=GROWTH_MODE_LABELS,
        default="Flat",
        key=_gen_key(f"{key_prefix}_growth_mode"),
    )

    if growth_mode_label is None:
        growth_mode_label = "Flat"

    growth_mode = GROWTH_MODE_KEYS[growth_mode_label]

    growth_rate: float | None = None
    overrides: dict[int, float] = {}

    if growth_mode == "flat":
        st.markdown(
            '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            "Flat: held at today's value in real terms (2026 £) - the underlying cost doesn't rise or "
            "fall in real terms, though the actual cash price still rises with inflation. Nothing more "
            "to set.</div>",
            unsafe_allow_html=True,
        )

    elif growth_mode == "annual_pct":
        growth_rate_pct = st.slider(
            f"{fuel_label} annual % change",
            min_value=-10,
            max_value=10,
            value=0,
            step=1,
            format="%d%%",
            label_visibility="collapsed",
            key=_gen_key(f"{key_prefix}_growth_rate"),
        )
        growth_rate = growth_rate_pct / 100
        st.markdown(
            '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            f"{growth_rate_pct:+d}% per year, applied from {FUTURE_YEARS[0]} onwards.</div>",
            unsafe_allow_html=True,
        )

    elif growth_mode == "custom":
        st.markdown(
            '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            f"Custom: set a price for each year. Pre-filled at today's value "
            f"({current_price:.2f} p/kWh) — edit any cell to override that year.</div>",
            unsafe_allow_html=True,
        )

        editor_key = _gen_key(f"{key_prefix}_overrides_editor")
        if editor_key not in st.session_state:
            st.session_state[editor_key] = pd.DataFrame(
                {
                    "Year": FUTURE_YEARS,
                    "Price (p/kWh)": [round(current_price, 2)] * len(FUTURE_YEARS),
                }
            )

        edited_df = st.data_editor(
            st.session_state[editor_key],
            hide_index=True,
            height=220,
            key=_gen_key(f"{key_prefix}_data_editor"),
            column_config={
                "Year": st.column_config.NumberColumn(disabled=True),
                "Price (p/kWh)": st.column_config.NumberColumn(format="%.2f"),
            },
        )
        st.session_state[editor_key] = edited_df

        overrides = {
            int(row["Year"]): float(row["Price (p/kWh)"])
            for _, row in edited_df.iterrows()
            if round(float(row["Price (p/kWh)"]), 2) != round(current_price, 2)
        }

        reset_col, count_col = st.columns([1, 1])
        with reset_col:
            if st.button("Reset to flat", key=_gen_key(f"{key_prefix}_reset_button")):
                st.session_state[editor_key] = pd.DataFrame(
                    {
                        "Year": FUTURE_YEARS,
                        "Price (p/kWh)": [round(current_price, 2)] * len(FUTURE_YEARS),
                    }
                )
                st.rerun()
        with count_col:
            plural = "year" if len(overrides) == 1 else "years"
            st.markdown(
                f'<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
                f"{len(overrides)} {plural} overridden</div>",
                unsafe_allow_html=True,
            )

    return current_price, growth_mode, growth_rate, overrides


def _estimate_price_series(
    current_price: float,
    growth_mode: str,
    growth_rate: float | None,
    overrides: dict[int, float],
    years: list[int],
) -> list[float]:
    """Lightweight preview-only price series for the ratio callout.

    This intentionally doesn't use EnergyPriceTrajectory — it's just for a
    quick sidebar preview, not a real calculation. The actual model layer
    (model_integration/trajectories.py) builds the real trajectory.
    """
    if growth_mode == "annual_pct" and growth_rate is not None:
        return [
            current_price * (1 + growth_rate) ** (year - years[0]) for year in years
        ]
    if growth_mode == "custom":
        return [overrides.get(year, current_price) for year in years]
    return [current_price] * len(years)  # flat


def _render_price_ratio_callout(
    gas_current_price: float,
    gas_growth_mode: str,
    gas_growth_rate: float | None,
    gas_overrides: dict[int, float],
    electricity_current_price: float | None,
    electricity_growth_mode: str | None,
    electricity_growth_rate: float | None,
    electricity_overrides: dict[int, float],
) -> None:
    """Render the light-blue 'Electricity to gas price ratio' callout box."""
    if electricity_current_price is None:
        return  # nothing to show on the electricity-solver page

    all_years = [INSTALL_START_YEAR] + FUTURE_YEARS
    gas_series = _estimate_price_series(
        gas_current_price, gas_growth_mode, gas_growth_rate, gas_overrides, all_years
    )
    electricity_series = _estimate_price_series(
        electricity_current_price,
        electricity_growth_mode,
        electricity_growth_rate,
        electricity_overrides,
        all_years,
    )
    ratios = [e / g for e, g in zip(electricity_series, gas_series)]

    current_ratio = ratios[0]
    min_ratio, max_ratio = min(ratios), max(ratios)

    st.markdown(
        f"""
        <div style="background-color:#D5F0F4; padding:10px 12px; margin:12px 0;">
            <div style="font-size:14px; font-weight:700; color:#0F294A; margin-bottom:4px;">Electricity to gas price ratio</div>
            <div style="display:flex; justify-content:space-between; font-size:13px; color:#1a3a3a; margin-bottom:4px;">
                <span><strong>{INSTALL_START_YEAR}:</strong> {current_ratio:.2f}</span>
                <span><strong>{INSTALL_START_YEAR}&ndash;{OPERATING_END_YEAR}:</strong> {min_ratio:.2f}&ndash;{max_ratio:.2f}</span>
            </div>
            <div style="font-size:12px; color:#557; line-height:1.4;">
                Updates as you change the prices above. The full year-by-year table is in the results section.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_energy_prices_section(
    solve_for_electricity: bool = False,
) -> EnergyPriceInputs:
    """Render the Energy prices section: gas + electricity price widgets, plus the price-ratio callout.

    If solve_for_electricity is True (Solve for electricity price page), the
    electricity widgets are replaced with a "solved for" note.
    """
    render_sidebar_section_header("Energy prices")

    gas_current_price, gas_growth_mode, gas_growth_rate, gas_overrides = (
        _render_fuel_price_inputs(
            fuel_label="Gas",
            default_current_price=get_gas_price_default(),
            key_prefix="gas",
        )
    )

    st.markdown(
        '<hr style="margin:4px 0; border-color:#e2e3e7;">',
        unsafe_allow_html=True,
    )

    (
        electricity_current_price,
        electricity_growth_mode,
        electricity_growth_rate,
        electricity_overrides,
    ) = _render_fuel_price_inputs(
        fuel_label="Electricity",
        default_current_price=get_electricity_price_default(),
        key_prefix="electricity",
        disabled=solve_for_electricity,
    )

    _render_price_ratio_callout(
        gas_current_price,
        gas_growth_mode,
        gas_growth_rate,
        gas_overrides,
        electricity_current_price,
        electricity_growth_mode,
        electricity_growth_rate,
        electricity_overrides,
    )

    return EnergyPriceInputs(
        gas_current_price=gas_current_price,
        gas_growth_mode=gas_growth_mode,
        gas_growth_rate=gas_growth_rate,
        gas_overrides=gas_overrides,
        electricity_current_price=electricity_current_price,
        electricity_growth_mode=electricity_growth_mode,
        electricity_growth_rate=electricity_growth_rate,
        electricity_overrides=electricity_overrides,
    )


# ---------------------------------------------------------------------------
# Heat pump section
# ---------------------------------------------------------------------------


def _render_subsidy_override(
    subsidy_scenario_values: dict[int, float],
) -> dict[int, float]:
    """Render the 'Advanced: override subsidy by year' expander."""
    overrides_key = "ashp_subsidy_overrides_dict"
    if overrides_key not in st.session_state:
        st.session_state[overrides_key] = {}

    with st.expander("🔍 Advanced: override subsidy by year"):
        st.markdown(
            '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            "Pre-filled from the selected scenario. Choose a year, set a value, and add it below "
            "to override that year.</div>",
            unsafe_allow_html=True,
        )

        year_col, value_col, button_col = st.columns([1.2, 1.2, 0.8])
        with year_col:
            selected_year = st.selectbox(
                "Year",
                options=sorted(subsidy_scenario_values.keys()),
                key=_gen_key("ashp_subsidy_year_select"),
            )
        with value_col:
            override_value = st.number_input(
                "Subsidy (£)",
                min_value=0.0,
                max_value=15_000.0,
                value=round(subsidy_scenario_values.get(selected_year, 0.0), 2),
                step=100.0,
                key=_gen_key("ashp_subsidy_value_input"),
            )
        with button_col:
            st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
            if st.button("Add", key=_gen_key("ashp_subsidy_add_button")):
                st.session_state[overrides_key][int(selected_year)] = float(
                    override_value
                )
                st.rerun()

        overrides = st.session_state[overrides_key]

        row_parts = []
        for year in sorted(subsidy_scenario_values.keys()):
            value = overrides.get(year, subsidy_scenario_values[year])
            marker = (
                ' <span style="color:#f59e0b;">●</span>' if year in overrides else ""
            )
            row_parts.append(
                f"<tr><td style='padding:4px 12px;'>{year}</td>"
                f"<td style='padding:4px 12px; text-align:right;'>{value:,.0f}{marker}</td></tr>"
            )
        rows_html = "".join(row_parts)
        st.markdown(
            f"""
            <table style="width:100%; font-size:13px; border-collapse:collapse;">
                <tr style="background:#f0f2f6; font-weight:700;">
                    <td style="padding:4px 12px;">Year</td>
                    <td style="padding:4px 12px; text-align:right;">Subsidy (£)</td>
                </tr>
                {rows_html}
            </table>
            """,
            unsafe_allow_html=True,
        )

        reset_col, count_col = st.columns([1, 1])
        with reset_col:
            if st.button(
                "Reset to scenario", key=_gen_key("ashp_subsidy_reset_button")
            ):
                st.session_state[overrides_key] = {}
                st.rerun()
        with count_col:
            plural = "year" if len(overrides) == 1 else "years"
            st.markdown(
                f'<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
                f"{len(overrides)} {plural} overridden</div>",
                unsafe_allow_html=True,
            )

    return st.session_state[overrides_key]


def render_heat_pump_section(solve_for_subsidy: bool = False) -> HeatPumpInputs:
    """Render the Air-to-water heat pump section."""
    render_sidebar_section_header("Air-to-water heat pump")

    lifespan = st.slider(
        "Lifespan (years)",
        min_value=ASHP_LIFESPAN_MIN,
        max_value=ASHP_LIFESPAN_MAX,
        value=ASHP_LIFESPAN_DEFAULT,
        format="%d years",
        key=_gen_key("ashp_lifespan_slider"),
    )

    scop = st.slider(
        "SCOP",
        min_value=ASHP_SCOP_MIN,
        max_value=ASHP_SCOP_MAX,
        value=ASHP_SCOP_DEFAULT,
        step=0.1,
        format="%.1f",
        key=_gen_key("ashp_scop_slider"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "Held constant across every installation year and throughout each system's lifetime.</div>",
        unsafe_allow_html=True,
    )

    tou_discount_pct = st.slider(
        "Time-of-use tariff discount",
        min_value=int(ASHP_TOU_DISCOUNT_MIN * 100),
        max_value=int(ASHP_TOU_DISCOUNT_MAX * 100),
        value=int(ASHP_TOU_DISCOUNT_DEFAULT * 100),
        step=1,
        format="%d%%",
        key=_gen_key("ashp_tou_discount_slider"),
    )
    tou_tariff_discount = tou_discount_pct / 100
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "The saving you assume a heat pump owner gets on their electricity unit rate with a "
        "time-of-use tariff. Set to 0 to use the standard price cap rate.</div>",
        unsafe_allow_html=True,
    )

    installation_cost_current = st.number_input(
        "Installation cost today (£)",
        min_value=0.0,
        value=ASHP_INSTALLATION_COST_DEFAULT,
        step=1.0,
        format="%.2f",
        key=_gen_key("ashp_current_installation_input"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        f"Default: Median installation cost for a {PROPERTY_DESCRIPTION}.</div>",
        unsafe_allow_html=True,
    )

    growth_mode_label = st.segmented_control(
        "Installation cost in future years (2027–2035)",
        options=["Flat", "% change per year"],
        default="% change per year",
        key=_gen_key("ashp_installation_cost_growth_mode"),
    )
    if growth_mode_label is None:
        growth_mode_label = "Flat"
    installation_cost_growth_mode = (
        "flat" if growth_mode_label == "Flat" else "annual_pct"
    )

    installation_cost_growth_rate = 0.0
    if installation_cost_growth_mode == "annual_pct":
        st.markdown(
            f'<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            f"Default: {ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT:+.1%} per year in real terms. "
            f"As observed in historical Boiler Upgrade Scheme (BUS) median installation cost statistics.</div>",
            unsafe_allow_html=True,
        )
        growth_rate_pct = st.slider(
            "Installation cost annual % change",
            min_value=ASHP_INSTALLATION_COST_GROWTH_RATE_MIN * 100,
            max_value=ASHP_INSTALLATION_COST_GROWTH_RATE_MAX * 100,
            value=ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT * 100,
            step=0.5,
            format="%.1f%% / year",
            label_visibility="collapsed",
            key=_gen_key("ashp_installation_growth_rate_slider"),
        )
        installation_cost_growth_rate = growth_rate_pct / 100

    # --- Subsidy pathway ---
    subsidy_options = get_subsidy_scenario_options()

    if solve_for_subsidy:
        render_solved_for_note(
            title="Subsidy is solved for on this page",
            body=(
                "You don't set a subsidy here. The model works out the subsidy each year would "
                "need to reach lifetime cost parity with the gas boiler."
            ),
        )
        subsidy_scenario = None
        subsidy_overrides: dict[int, float] = {}
    else:
        subsidy_scenario = st.selectbox(
            "Subsidy pathway",
            options=subsidy_options,
            index=subsidy_options.index(ASHP_SUBSIDY_SCENARIO_DEFAULT),
            key=_gen_key("ashp_subsidy_pathway_select"),
        )
        st.markdown(
            '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            "Today's value is £7,500 (Boiler Upgrade Scheme). "
            "Choose a preset future subsidy pathway, and/or override to set your own values.</div>",
            unsafe_allow_html=True,
        )

        subsidy_scenario_values = get_subsidy_scenario_values(
            subsidy_scenario
        )  # from model_integration/trajectories.py, or a lookup
        subsidy_overrides = _render_subsidy_override(subsidy_scenario_values)

    # --- Financing ---
    is_financed = st.toggle(
        "Include loan financing", key=_gen_key("ashp_is_financed_toggle")
    )

    interest_rate = None
    loan_term = None
    if is_financed:
        col1, col2 = st.columns(2)
        with col1:
            interest_rate_pct = st.slider(
                "Interest rate",
                min_value=int(ASHP_INTEREST_RATE_MIN * 100),
                max_value=int(ASHP_INTEREST_RATE_MAX * 100),
                value=int(ASHP_INTEREST_RATE_DEFAULT * 100),
                step=1,
                format="%d%%",
                key=_gen_key("ashp_interest_rate_slider"),
            )
            interest_rate = interest_rate_pct / 100
        with col2:
            loan_term = st.slider(
                "Loan term",
                min_value=ASHP_LOAN_TERM_MIN,
                max_value=ASHP_LOAN_TERM_MAX,
                value=ASHP_LOAN_TERM_DEFAULT,
                format="%d years",
                key=_gen_key("ashp_loan_term_slider"),
            )

    # --- Maintenance ---
    hp_maintenance_cost_per_visit = st.number_input(
        "Maintenance cost (£)",
        min_value=0.0,
        value=ASHP_MAINTENANCE_COST_DEFAULT,
        step=1.0,
        key=_gen_key("ashp_maintenance_cost_input"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "Assumes annual servicing.</div>",
        unsafe_allow_html=True,
    )

    return HeatPumpInputs(
        lifespan=lifespan,
        scop=scop,
        tou_tariff_discount=tou_tariff_discount,
        installation_cost_current=installation_cost_current,
        installation_cost_growth_mode=installation_cost_growth_mode,
        installation_cost_growth_rate=installation_cost_growth_rate,
        subsidy_scenario=subsidy_scenario,
        subsidy_overrides=subsidy_overrides,
        is_financed=is_financed,
        interest_rate=interest_rate,
        loan_term=loan_term,
        maintenance_cost_per_visit=hp_maintenance_cost_per_visit,
        maintenance_annual_frequency=ASHP_MAINTENANCE_FREQUENCY_DEFAULT,
    )


# ---------------------------------------------------------------------------
#  Gas boiler section
# ---------------------------------------------------------------------------


def render_gas_boiler_section() -> GasBoilerInputs:
    """Render the Gas boiler section."""
    render_sidebar_section_header("Gas boiler")

    lifespan = st.slider(
        "Lifespan (years)",
        min_value=BOILER_LIFESPAN_MIN,
        max_value=BOILER_LIFESPAN_MAX,
        value=BOILER_LIFESPAN_DEFAULT,
        format="%d years",
        key=_gen_key("boiler_lifespan_slider"),
    )

    installation_cost = st.number_input(
        "Installation cost (£)",
        min_value=0.0,
        value=BOILER_INSTALLATION_COST_DEFAULT,
        step=1.0,
        format="%.2f",
        key=_gen_key("boiler_installation_cost_input"),
    )
    st.markdown(
        f'<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        f"Held at the value set above, in real terms ({BASE_YEAR_DEFAULT} £), for every installation "
        f"year.</div>",
        unsafe_allow_html=True,
    )

    efficiency = st.slider(
        "Efficiency",
        min_value=BOILER_EFFICIENCY_MIN,
        max_value=BOILER_EFFICIENCY_MAX,
        value=BOILER_EFFICIENCY_DEFAULT,
        step=0.01,
        format="%.2f",
        key=_gen_key("boiler_efficiency_slider"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "Held constant across every installation year and throughout each system's lifetime.</div>",
        unsafe_allow_html=True,
    )

    maintenance_cost_per_visit = st.number_input(
        "Service cost (£)",
        min_value=0.0,
        value=BOILER_MAINTENANCE_COST_DEFAULT,
        step=1.0,
        format="%.2f",
        key=_gen_key("boiler_maintenance_cost_input"),
    )
    st.markdown(
        '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
        "Assumes annual servicing.</div>",
        unsafe_allow_html=True,
    )

    include_standing_charge = st.toggle(
        "Include gas standing charge",
        value=BOILER_INCLUDE_STANDING_CHARGE_DEFAULT,
        key=_gen_key("boiler_include_standing_charge_toggle"),
    )
    standing_charge = get_latest_gas_standing_charge()
    if include_standing_charge:
        st.markdown(
            f'<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            f"Included at {standing_charge:.2f} p/day, held constant in real terms ({BASE_YEAR_DEFAULT} £). "
            f"Assumes gas heating is the household's only use of gas, so switching to a heat pump would "
            f"let it disconnect entirely.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size:12px; color:#888; margin-top:-8px; margin-bottom:18px;">'
            "Not included. Assumes the household keeps a gas connection anyway (e.g. for cooking).</div>",
            unsafe_allow_html=True,
        )

    return GasBoilerInputs(
        lifespan=lifespan,
        efficiency=efficiency,
        installation_cost=installation_cost,
        maintenance_cost_per_visit=maintenance_cost_per_visit,
        maintenance_annual_frequency=BOILER_MAINTENANCE_FREQUENCY_DEFAULT,
        include_standing_charge=include_standing_charge,
        standing_charge=standing_charge,
    )


# ---------------------------------------------------------------------------
#  Building whole sidebar
# ---------------------------------------------------------------------------
def render_sidebar() -> dict:
    if "reset_generation" not in st.session_state:
        st.session_state["reset_generation"] = 0

    with st.sidebar:
        render_fixed_inputs()
        render_user_inputs_heading()
        boiler_heat_demand, heat_pump_heat_demand_uplift = render_household_section()
        energy_prices = render_energy_prices_section()
        heat_pump = render_heat_pump_section()
        gas_boiler = render_gas_boiler_section()

        st.divider()
        if st.button(
            "↺ Reset to defaults",
            key="reset_all_defaults_button",
            width="stretch",
        ):
            st.session_state["reset_generation"] += 1
            for key in list(st.session_state.keys()):
                if key not in ("reset_generation", "reset_all_defaults_button"):
                    del st.session_state[key]
            st.rerun()

    return AppInputs(
        boiler_heat_demand=boiler_heat_demand,
        heat_pump_heat_demand_uplift=heat_pump_heat_demand_uplift,
        heat_pump=heat_pump,
        gas_boiler=gas_boiler,
        energy_prices=energy_prices,
    )


def _gen_key(base_key: str) -> str:
    """Append the current reset-generation number to a widget key, so a
    'reset to defaults' click forces genuinely new widgets rather than
    reusing keys the browser frontend may still have stale values for.
    """
    gen = st.session_state.get("reset_generation", 0)
    return f"{base_key}_{gen}"
