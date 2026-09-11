"""Functions to render output sections for the Subsidy Solver page."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from components.layout import render_section_heading
from config.defaults import BASE_YEAR_DEFAULT
from results.charts import build_required_subsidy_chart


def render_required_subsidy_chart_section(required_subsidy_df: pd.DataFrame) -> None:
    render_section_heading("Subsidy needed to reach cost parity by installation year")
    st.markdown(
        '<div style="font-size:13px; color:#666; margin-top:-10px; margin-bottom:16px;">'
        "The level of subsidy needed in each installation year for the heat pump to have the same annualised lifetime cost as the gas boiler. </div>",
        unsafe_allow_html=True,
    )

    chart = build_required_subsidy_chart(required_subsidy_df)
    st.altair_chart(chart, width="stretch")


def render_required_subsidy_table_section(required_subsidy_df: pd.DataFrame) -> None:
    """Render the year-by-year required subsidy table, with conditional
    highlighting for already-at-parity and subsidy-exceeds-cost cases.
    """
    render_section_heading("Year by year")

    rows_html = ""
    for _, row in required_subsidy_df.iterrows():
        year = int(row["installation_year"])
        gas_boiler_eac = row["gas_boiler_eac"]
        heat_pump_no_subsidy_eac = row["heat_pump_no_subsidy_eac"]
        required_subsidy_real = row["required_subsidy_real"]
        required_subsidy_nominal = row["required_subsidy_nominal"]
        installation_cost = row["installation_cost"]

        row_bg = ""
        message = ""
        if required_subsidy_real < 0:
            row_bg = "background:#B7E4D8;"
            message = "Already cheaper — no subsidy needed"
        elif required_subsidy_real > installation_cost:
            row_bg = "background:#F6C6D3;"
            message = (
                "More than the installation cost - subsidy alone can't close the gap"
            )

        rows_html += (
            f'<tr style="{row_bg}">'
            f'<td style="padding:10px 16px;">{year}</td>'
            f'<td style="padding:10px 16px; text-align:right;">{gas_boiler_eac:,.0f}</td>'
            f'<td style="padding:10px 16px; text-align:right;">{heat_pump_no_subsidy_eac:,.0f}</td>'
            f'<td style="padding:10px 16px; text-align:right; font-weight:700;">£{required_subsidy_real:,.0f}</td>'
            f'<td style="padding:10px 16px; text-align:right; font-weight:700;">£{required_subsidy_nominal:,.0f}</td>'
            f'<td style="padding:10px 16px; color:#444;">{message}</td>'
            f"</tr>"
        )

    table_html = (
        '<div style="overflow-x:auto;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<tr style="background:#DDD9D6; font-weight:700; color:#0F294A;">'
        '<td style="padding:10px 16px;">Installation year</td>'
        '<td style="padding:10px 16px; text-align:right;">Gas boiler annualised lifetime cost, £/yr</td>'
        '<td style="padding:10px 16px; text-align:right;">Heat pump (no subsidy) annualised lifetime cost, £/yr</td>'
        f'<td style="padding:10px 16px; text-align:right;">Subsidy needed, £ ({BASE_YEAR_DEFAULT} real)</td>'
        '<td style="padding:10px 16px; text-align:right;">Subsidy needed, £ (nominal)</td>'
        '<td style="padding:10px 16px;">What this means</td>'
        "</tr>" + rows_html + "</table>"
        "</div>"
        '<div style="margin-top:12px; font-size:13px; display:flex; gap:20px;">'
        '<div><span style="display:inline-block; width:12px; height:12px; background:#B7E4D8; margin-right:6px;"></span>Already at parity without a subsidy</div>'
        '<div><span style="display:inline-block; width:12px; height:12px; background:#F6C6D3; margin-right:6px;"></span>Subsidy needed is more than the installation cost<p></div>'
        "</div>"
    )

    st.markdown(table_html, unsafe_allow_html=True)


def render_download_required_subsidy_section(required_subsidy_df: pd.DataFrame) -> None:

    # Prepare dataframe for export
    required_subsidy_df_for_export = required_subsidy_df.copy().rename(
        columns={
            "installation_year": "Installation year",
            "gas_boiler_eac": f"Annualised lifetime cost of gas boiler, £/yr ({BASE_YEAR_DEFAULT} real)",
            "heat_pump_no_subsidy_eac": f"Annualised lifetime cost of heat pump, with no subsidy, £/yr ({BASE_YEAR_DEFAULT} real)",
            "installation_cost": f"Heat pump installation cost, £ ({BASE_YEAR_DEFAULT} real)",
            "required_subsidy_real": f"Heat pump subsidy needed for cost parity, £ ({BASE_YEAR_DEFAULT} real)",
            "required_subsidy_nominal": "Heat pump subsidy needed for cost parity, £ (nominal)",
        }
    )

    timestamp = datetime.now(ZoneInfo("Europe/London")).strftime("%Y%m%d_%H%M")

    st.download_button(
        "⬇ Export CSV",
        data=required_subsidy_df_for_export.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"required_subsidy_by_installation_year_{timestamp}.csv",
        mime="text/csv",
        key="download_required_subsidy_by_installation_year",
    )
