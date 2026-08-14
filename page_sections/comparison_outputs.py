"""Functions to render output sections for the Lifetime Comparison page."""

import pandas as pd
import streamlit as st

from components.layout import render_section_heading
from config.defaults import (
    INSTALL_END_YEAR,
    INSTALL_START_YEAR,
    OPERATING_END_YEAR,
    OPERATING_START_YEAR,
)
from model_integration.schema import AppInputs
from model_integration.trajectories import (
    build_electricity_prices,
    build_gas_prices,
)
from results.charts import (
    ANNUAL_COST_METRIC,
    COMPONENT_COLORS,
    COMPONENT_LABELS,
    COMPONENT_ORDER,
    EAC_METRIC,
    SYSTEM_LABELS,
    SYSTEM_ORDER,
    build_cashflow_chart,
    build_cost_breakdown_chart,
    build_eac_by_year_chart,
    build_eac_headline_messages,
)

INSTALLATION_YEARS = range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)
OPERATING_YEARS = range(OPERATING_START_YEAR, OPERATING_END_YEAR + 1)


def render_eac_by_year_section(comparison_df: pd.DataFrame) -> None:

    eac_df = comparison_df[comparison_df["metric"] == EAC_METRIC].copy()
    eac_df["system_label"] = eac_df["system"].map(SYSTEM_LABELS)

    render_section_heading(
        "Annualised lifetime cost comparison by year the heating system is installed"
    )
    st.markdown(
        '<div style="font-size:13px; color:#666; margin-top:-20px; margin-bottom:0px;">'
        "Each point shows the annualised lifetime cost of a new system installed in that year - not the cost of operating over time.</div>",
        unsafe_allow_html=True,
    )
    with st.container(border=False):
        # Chart
        chart = build_eac_by_year_chart(comparison_df)
        st.altair_chart(chart, width="stretch")

        # Headline banner
        headlines = build_eac_headline_messages(eac_df)
        headline_html = "".join(
            f'<div style="margin-bottom:4px;">&bull; {msg}</div>' for msg in headlines
        )
        st.markdown(
            f'<div style="font-size:14px; color:#0F294A; '
            f"background:#EAF6F5; border-left:4px solid #97D9E3; padding:12px 16px; "
            f'border-radius:4px; margin-bottom:16px;">{headline_html}</div>',
            unsafe_allow_html=True,
        )

    # Prepare dataframe for export
    eac_df_for_export = (
        eac_df.copy()
        .drop(columns=["system"])
        .rename(
            columns={
                "installation_year": "Installation year",
                "system_label": "Heating system type",
                "metric": "Metric",
                "value": "Value",
            }
        )
    )
    eac_df_for_export = eac_df_for_export[
        ["Installation year", "Heating system type", "Metric", "Value"]
    ]

    with st.expander("▾ View/export underlying data"):
        st.dataframe(
            eac_df_for_export,
            width="stretch",
            hide_index=True,
        )
        st.download_button(
            "⬇ Export CSV",
            data=eac_df_for_export.to_csv(index=False),
            file_name="eac_by_installation_year.csv",
            mime="text/csv",
        )


def render_eac_breakdown_section(
    comparison_df: pd.DataFrame, annual_breakdown_df: pd.DataFrame
):

    render_section_heading("Cost breakdown")

    # Install year dropdown
    installation_year = st.selectbox(
        "Installation year",
        options=INSTALLATION_YEARS,
        key="cost_breakdown_year_select",
    )
    # Chart
    st.markdown(
        f'<div style="font-weight:700; color:#0F294A; font-size:16px; margin-bottom:2px;">'
        f"Annualised lifetime cost breakdown, installed {installation_year}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:13px; color:#666; margin-bottom:16px;">'
        "Annualised lifetime cost (£) split into capital cost, running cost and maintenance</div>",
        unsafe_allow_html=True,
    )
    chart = build_cost_breakdown_chart(comparison_df, installation_year)
    st.altair_chart(chart)

    # --- Legend table beneath the chart, matching mockup ---
    # Includes a "Total" row (the EAC) in addition to the components
    # that make up the stacked bars, without feeding it into the chart.
    legend_metrics = COMPONENT_ORDER + [EAC_METRIC]
    breakdown_df = comparison_df[
        (comparison_df["installation_year"] == installation_year)
        & (comparison_df["metric"].isin(legend_metrics))
    ]
    pivot = breakdown_df.pivot(
        index="metric", columns="system", values="value"
    ).reindex(legend_metrics)

    def _legend_row(metric: str) -> str:
        is_total = metric == EAC_METRIC
        swatch = (
            ""
            if is_total
            else f'<span style="display:inline-block; width:10px; height:10px; background:{COMPONENT_COLORS[COMPONENT_LABELS[metric]]}; margin-right:6px;"></span>'
        )
        row_style = (
            ' style="border-top:2px solid #ddd; font-weight:700; color:#0F294A;"'
            if is_total
            else ""
        )
        return f"""
        <tr{row_style}>
            <td style="padding:6px 12px;">{swatch}{COMPONENT_LABELS[metric]}</td>
            <td style="padding:6px 12px; text-align:right;">£{pivot.loc[metric, "Heat pump"]:,.0f}</td>
            <td style="padding:6px 12px; text-align:right;">£{pivot.loc[metric, "Gas boiler"]:,.0f}</td>
        </tr>
        """

    legend_rows = "".join(_legend_row(metric) for metric in legend_metrics)
    st.markdown(
        f"""
        <table style="width:100%; font-size:13px; border-collapse:collapse; margin-top:20px;">
            <tr style="border-bottom:2px solid #ddd; font-weight:700; color:#0F294A;">
                <td style="padding:6px 12px;">Cost component</td>
                <td style="padding:6px 12px; text-align:right;">Air-to-water heat pump</td>
                <td style="padding:6px 12px; text-align:right;">Gas boiler</td>
            </tr>
            {legend_rows}
        </table>
        """,
        unsafe_allow_html=True,
    )

    # Prepare dataframe for export
    EAC_METRICS_FOR_EXPORT = [EAC_METRIC] + COMPONENT_ORDER
    eac_breakdown_df_for_export = comparison_df[
        comparison_df["metric"].isin(EAC_METRICS_FOR_EXPORT)
    ].copy()
    eac_breakdown_df_for_export["system_label"] = eac_breakdown_df_for_export[
        "system"
    ].map(SYSTEM_LABELS)
    eac_breakdown_df_for_export = eac_breakdown_df_for_export.drop(
        columns=["system"]
    ).rename(
        columns={
            "installation_year": "Installation year",
            "system_label": "Heating system type",
            "metric": "Metric",
            "value": "Value",
        }
    )
    eac_breakdown_df_for_export = eac_breakdown_df_for_export[
        ["Installation year", "Heating system type", "Metric", "Value"]
    ]

    with st.expander("▾ View/export underlying data"):
        st.dataframe(
            eac_breakdown_df_for_export,
            width="stretch",
            hide_index=True,
        )
        st.download_button(
            "⬇ Export CSV",
            data=eac_breakdown_df_for_export.to_csv(index=False),
            file_name="eac_breakdown_by_installation_year.csv",
            mime="text/csv",
        )

    st.divider()

    st.markdown(
        f'<div style="font-weight:700; color:#0F294A; font-size:16px; margin-bottom:2px;">'
        f"Cost of ownership by year, installed {installation_year}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:13px; color:#666; margin-bottom:12px;">'
        "How much each system costs per year of ownership, in present-value (2026 real £) terms. "
        "Includes upfront cost in year 0.</div>",
        unsafe_allow_html=True,
    )

    cashflow_chart = build_cashflow_chart(annual_breakdown_df, installation_year)
    st.altair_chart(cashflow_chart, width="stretch")

    # Prepare dataframe for export
    cashflow_df_for_export = annual_breakdown_df[
        (annual_breakdown_df["installation_year"] == installation_year)
        & (annual_breakdown_df["metric"] == ANNUAL_COST_METRIC)
        & (annual_breakdown_df["system"].isin(SYSTEM_ORDER))
    ].copy()
    cashflow_df_for_export["system_label"] = cashflow_df_for_export["system"].map(
        SYSTEM_LABELS
    )
    cashflow_df_for_export = cashflow_df_for_export.drop(columns=["system"]).rename(
        columns={
            "installation_year": "Installation year",
            "operating_year": "Year in lifetime",
            "system_label": "Heating system type",
            "metric": "Metric",
            "value": "Value",
        }
    )
    cashflow_df_for_export = cashflow_df_for_export[
        [
            "Installation year",
            "Year in lifetime",
            "Heating system type",
            "Metric",
            "Value",
        ]
    ]

    with st.expander("▾ View/export underlying data"):
        st.dataframe(cashflow_df_for_export, width="stretch", hide_index=True)
        st.download_button(
            "⬇ Export CSV",
            data=annual_breakdown_df.to_csv(index=False),
            file_name="cost_of_ownership_annual_breakdown.csv",
            mime="text/csv",
        )


def render_price_ratio_table(inputs: AppInputs) -> None:
    """Render the electricity-to-gas price ratio table: one column per year."""
    render_section_heading("Electricity-to-gas price ratio trajectory modelled")

    electricity_prices = build_electricity_prices(inputs)
    gas_prices = build_gas_prices(inputs)

    price_ratio_by_year = {
        year: electricity_prices.get_price(year=year) / gas_prices.get_price(year=year)
        for year in OPERATING_YEARS
    }

    header_cells = "".join(
        f'<th style="padding:4px 11px; text-align:center; font-weight:700; color:#0F294A;">{year}</th>'
        for year in OPERATING_YEARS
    )
    value_cells = "".join(
        f'<td style="padding:4px 11px; text-align:center; color:#0F294A;">{price_ratio_by_year[year]:.2f}</td>'
        for year in OPERATING_YEARS
    )

    st.markdown(
        f"""
        <div style="overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:13px; min-width:900px;">
                <tr style="background:#DDD9D6;">
                    <th style="padding:4px 11px; text-align:left; font-weight:700; color:#0F294A; white-space:nowrap;">Year</th>
                    {header_cells}
                </tr>
                <tr style="background:#fff;">
                    <td style="padding:4px 11px; font-weight:700; color:#0F294A; white-space:nowrap;">Electricity to gas price ratio</td>
                    {value_cells}
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
