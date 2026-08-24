from datetime import datetime

import pandas as pd
import streamlit as st

from components.layout import render_section_heading
from config.defaults import BASE_YEAR_DEFAULT, INSTALL_END_YEAR, INSTALL_START_YEAR
from model_integration.schema import AppInputs
from model_integration.trajectories import build_gas_prices
from results.charts import build_required_price_ratio_chart
from results.compute import (
    build_required_electricity_price_summary_df,
    build_required_electricity_prices,
    build_required_price_ratio,
)

INSTALLATION_YEARS = range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)


def render_required_price_ratio_section(
    inputs: AppInputs, current_ratio: float
) -> None:
    render_section_heading(
        "Electricity-to-gas price ratio needed over the heat pump's lifetime for annualised lifetime cost parity with a gas boiler"
    )
    installation_year = st.selectbox(
        "Installation year",
        options=INSTALLATION_YEARS,
        key="electricity_solver_year_select",
    )
    st.markdown("")

    required_price_cap_rates = build_required_electricity_prices(
        inputs, installation_year
    )

    gas_prices_trajectory = build_gas_prices(inputs)
    gas_prices_by_year = {
        year: gas_prices_trajectory.get_price(year=year)
        for year in required_price_cap_rates.keys()
    }

    required_price_ratio = build_required_price_ratio(
        required_price_cap_rates, gas_prices_by_year
    )

    chart = build_required_price_ratio_chart(required_price_ratio, current_ratio)
    st.altair_chart(chart, width="stretch")

    st.divider()

    st.markdown(
        f'<div style="font-weight:700; color:#0F294A; font-size:16px; margin-bottom:2px;">'
        f"Year by year breakdown, installed {installation_year}</div>",
        unsafe_allow_html=True,
    )
    electricity_price_summary_df = build_required_electricity_price_summary_df(
        inputs=inputs, installation_year=installation_year
    )

    render_required_electricity_price_table_section(electricity_price_summary_df)

    render_download_required_electricity_price_summary_section(
        electricity_price_summary_df
    )


def render_required_electricity_price_table_section(
    electricity_price_summary_df: pd.DataFrame,
) -> None:
    st.markdown(
        f'<div style="font-size:12px; color:#888; margin-bottom:12px;">'
        f"All £ and p/kWh figures  are in {BASE_YEAR_DEFAULT} real terms.</div>",
        unsafe_allow_html=True,
    )

    # gas_boiler_eac and heat_pump_eac_today are constant across every row
    # displaying them once rather than repeating in table
    gas_boiler_eac = electricity_price_summary_df["gas_boiler_eac"].iloc[0]
    heat_pump_eac_today = electricity_price_summary_df["heat_pump_eac_today"].iloc[0]

    st.markdown(
        f"""
        <div style="display:flex; gap:24px; margin-bottom:16px;">
            <div style="font-size:14px; color:#333;">
                <span style="color:#666;">Gas boiler annualised lifetime cost:</span>
                <strong style="color:#0F294A;"> £{gas_boiler_eac:,.0f}/yr</strong>
            </div>
            <div style="font-size:14px; color:#333;">
                <span style="color:#666;">Heat pump annualised lifetime cost at today's electricity price:</span>
                <strong style="color:#0F294A;"> £{heat_pump_eac_today:,.0f}/yr</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rows_html = ""
    for _, row in electricity_price_summary_df.iterrows():
        row_bg, message = "", ""
        if heat_pump_eac_today < gas_boiler_eac:
            row_bg = "background:#B7E4D8;"
            message = "Already cheaper - electricity could rise this far before parity is lost"
        elif row["required_rate"] < 0:
            row_bg = "background:#F6C6D3;"
            message = "Negative - electricity price alone can't close the gap"

        ratio_text = (
            f"{row['implied_ratio']:.2f}" if pd.notna(row["implied_ratio"]) else "—"
        )

        rows_html += (
            f'<tr style="{row_bg}">'
            f'<td style="padding:10px 16px;">{int(row["operating_year"])}</td>'
            f'<td style="padding:10px 16px; text-align:right;">{row["gas_price"]:.2f}</td>'
            f'<td style="padding:10px 16px; text-align:right; font-weight:700;">{row["required_rate"]:,.1f}</td>'
            f'<td style="padding:10px 16px; text-align:right;">{ratio_text}</td>'
            f'<td style="padding:10px 16px; color:#444;">{message}</td>'
            f"</tr>"
        )

    table_html = (
        '<div style="overflow-x:auto;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<tr style="background:#DDD9D6; font-weight:700; color:#0F294A;">'
        '<td style="padding:10px 16px;">Year in lifetime</td>'
        '<td style="padding:10px 16px; text-align:right;">Gas price set in sidebar, p/kWh</td>'
        '<td style="padding:10px 16px; text-align:right;">Electricity price needed in that year, p/kWh</td>'
        '<td style="padding:10px 16px; text-align:right;">Implied price ratio needed for cost parity</td>'
        '<td style="padding:10px 16px;">What this means</td>'
        "</tr>" + rows_html + "</table>"
        "</div>"
        '<div style="margin-top:12px; font-size:13px; display:flex; gap:20px;">'
        '<div><span style="display:inline-block; width:12px; height:12px; background:#B7E4D8; margin-right:6px;"></span>'
        "Already at parity - the rate shown is the headroom before parity is lost</div>"
        '<div><span style="display:inline-block; width:12px; height:12px; background:#F6C6D3; margin-right:6px;"></span>'
        "No physically meaningful rate reaches parity<p></div>"
        "</div>"
    )

    st.markdown(table_html, unsafe_allow_html=True)


def render_download_required_electricity_price_summary_section(
    electricity_price_summary_df: pd.DataFrame,
) -> None:

    # Prepare dataframe for export
    electricity_price_summary_df_for_export = electricity_price_summary_df.copy().rename(
        columns={
            "installation_year": "Installation year",
            "operating_year": "Year in lifetime",
            "gas_boiler_eac": "Annualised lifetime cost of gas boiler, £/yr",
            "heat_pump_eac_today": "Annualised lifetime cost of heat pump at today's electricity price, £/yr",
            "gas_price": "Gas price set in sidebar, p/kWh",
            "required_rate": "Electricity price needed in that year, p/kWh",
            "implied_ratio": "Electricity-to-gas price ratio needed for cost parity",
        }
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    installation_year = int(electricity_price_summary_df["installation_year"].iloc[0])

    st.download_button(
        "⬇ Export CSV",
        data=electricity_price_summary_df_for_export.to_csv(index=False).encode(
            "utf-8-sig"
        ),
        file_name=f"electricity_gas_price_ratio_installed_{installation_year}_{timestamp}.csv",
        mime="text/csv",
        key="download_required_electricity_price_summary",
    )
