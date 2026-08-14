"""Functions to render output sections for the Subsidy Solver page."""

import pandas as pd
import streamlit as st

from components.layout import render_section_heading
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
        heat_pump_no_subsidy_eac = row.get("heat_pump_no_subsidy_eac", None)
        required_subsidy = row["required_subsidy"]
        installation_cost = row.get("installation_cost", None)

        row_bg = ""
        message = ""
        if required_subsidy < 0:
            row_bg = "background:#B7E4D8;"
            message = "Already cheaper — no subsidy needed"
        elif installation_cost is not None and required_subsidy > installation_cost:
            row_bg = "background:#F6C6D3;"
            message = (
                "More than the installation cost - subsidy alone can't close the gap"
            )

        rows_html += (
            f'<tr style="{row_bg}">'
            f'<td style="padding:10px 16px;">{year}</td>'
            f'<td style="padding:10px 16px; text-align:right;">{gas_boiler_eac:,.0f}</td>'
            f'<td style="padding:10px 16px; text-align:right;">{heat_pump_no_subsidy_eac:,.0f}</td>'
            f'<td style="padding:10px 16px; text-align:right; font-weight:700;">£{required_subsidy:,.0f}</td>'
            f'<td style="padding:10px 16px; color:#444;">{message}</td>'
            f"</tr>"
        )

    table_html = (
        '<div style="overflow-x:auto;">'
        '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
        '<tr style="background:#DDD9D6; font-weight:700; color:#0F294A;">'
        '<td style="padding:10px 16px;">Installation year</td>'
        '<td style="padding:10px 16px; text-align:right;">Gas boiler, £/yr</td>'
        '<td style="padding:10px 16px; text-align:right;">Heat pump with no subsidy, £/yr</td>'
        '<td style="padding:10px 16px; text-align:right;">Subsidy needed</td>'
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
    st.download_button(
        "⬇ Export CSV",
        data=required_subsidy_df.to_csv(index=False),
        file_name="required_subsidy_by_installation_year.csv",
        mime="text/csv",
        key="download_required_subsidy_by_installation_year",
    )
