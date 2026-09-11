"""Functions to render output sections for the Lifetime Comparison page."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from components.layout import render_section_heading
from config.defaults import (
    BASE_YEAR_DEFAULT,
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
    COMPONENT_COLORS,
    COMPONENT_LABELS,
    COMPONENT_ORDER,
    EAC_METRIC,
    SYSTEM_LABELS,
    SYSTEM_ORDER,
    build_cashflow_chart,
    build_cost_breakdown_chart,
    build_eac_by_year_chart,
    build_eac_headline_metrics,
)

INSTALLATION_YEARS = range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)
OPERATING_YEARS = range(OPERATING_START_YEAR, OPERATING_END_YEAR + 1)

timestamp = datetime.now(ZoneInfo("Europe/London")).strftime("%Y%m%d_%H%M")


def render_eac_headline_metrics(metrics: dict[str, dict]) -> None:
    """Render the two headline saving stat tiles: bold title, large value with
    a directional triangle, a "vs gas boiler" delta line, and a subsidy
    saving line specific to that installation year.
    """

    def _card_html(m: dict) -> str:
        year = m["year"]
        saving = m["saving"]
        saving_pct = m["saving_pct"]
        subsidy_saving = m["subsidy_saving"]

        if saving >= 0:
            title = "Heat pump costs less than gas boiler"
            value_text = f"£{saving:,.0f}/yr"
            value_color = "#18A48C"
            arrow = "&#9660;"  # ▼ cost is lower
            pct_sign = "-"
            card_bg = "#EAF6F5"
            card_border = "#18A48C"
        else:
            title = "Heat pump costs more than gas boiler"
            value_text = f"£{abs(saving):,.0f}/yr"
            value_color = "#EB003B"
            arrow = "&#9650;"  # ▲ cost is higher
            pct_sign = "+"
            card_bg = "#FDEFF1"
            card_border = "#EB003B"

        subtitle = f"Both systems installed in {year}"

        return f"""
        <div style="background:{card_bg}; border-left: 4px solid {card_border};border-radius:4px; padding:16px;">
            <div style="font-size:14px; font-weight:600; color:#0F294A; margin-bottom:2px;">{title}</div>
            <div style="font-size:12px; color:#888; margin-bottom:8px;">{subtitle}</div>
            <div style="font-size:20px; font-weight:600; color:{value_color};">{value_text} <span style="font-size:14px;">{arrow}</span><span style="color:{value_color}; font-size:14px;font-weight:500;">
                {pct_sign}{abs(saving_pct):.0f}%</span></div>
            <div style="font-size:12px; color:#666; margin-top:4px;">
                vs gas boiler 
            </div>
            <div style="font-size:12px; color:#666; margin-top:2px;">
                Subsidy saves <span style="color:#0F6E56; font-weight:500;">£{subsidy_saving:,.0f}/yr</span>
            </div>
        </div>
        """

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_card_html(metrics["first_year"]), unsafe_allow_html=True)
    with col2:
        st.markdown(_card_html(metrics["last_year"]), unsafe_allow_html=True)


def render_eac_by_year_section(comparison_df: pd.DataFrame) -> None:

    eac_df = comparison_df[comparison_df["metric"] == EAC_METRIC].copy()
    eac_df["system_label"] = eac_df["system"].map(SYSTEM_LABELS)

    render_section_heading(
        "Annualised lifetime cost comparison by year the heating system is installed"
    )

    with st.container(border=False):
        # Headline metrics
        metrics = build_eac_headline_metrics(eac_df)
        render_eac_headline_metrics(metrics)

        st.markdown(
            '<div style="font-size:13px; color:#666; margin-top:16px; margin-bottom:0px;">'
            "Each point shows the annualised lifetime cost of a new system installed in that year - not the cost of operating over time.</div>",
            unsafe_allow_html=True,
        )

        # Chart
        chart = build_eac_by_year_chart(comparison_df)
        st.altair_chart(chart, width="stretch")

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
            data=eac_df_for_export.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"equivalent_annualised_cost_by_installation_year_{timestamp}.csv",
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

    # --- Legend table beneath the chart ---
    legend_metrics = COMPONENT_ORDER + [EAC_METRIC]
    breakdown_df = comparison_df[
        (comparison_df["installation_year"] == installation_year)
        & (comparison_df["metric"].isin(legend_metrics))
    ]

    duplicate_check = breakdown_df.duplicated(subset=["metric", "system"])
    if duplicate_check.any():
        raise ValueError(
            f"Duplicate (metric, system) rows found for installation_year={installation_year}: "
            f"{breakdown_df[duplicate_check][['metric', 'system']].to_dict('records')}"
        )

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
        return (
            f"<tr{row_style}>"
            f'<td style="padding:6px 12px;">{swatch}{COMPONENT_LABELS[metric]}</td>'
            f'<td style="padding:6px 12px; text-align:right;">£{pivot.loc[metric, "Heat pump"]:,.0f}</td>'
            f'<td style="padding:6px 12px; text-align:right;">£{pivot.loc[metric, "Gas boiler"]:,.0f}</td>'
            f"</tr>"
        )

    legend_rows = "".join(_legend_row(metric) for metric in legend_metrics)

    # --- Difference row: heat pump EAC minus gas boiler EAC ---
    heat_pump_total = pivot.loc[EAC_METRIC, "Heat pump"]
    gas_boiler_total = pivot.loc[EAC_METRIC, "Gas boiler"]
    difference = heat_pump_total - gas_boiler_total
    difference_color = "#EB003B" if difference > 0 else "#18A48C"
    difference_sign = "+" if difference > 0 else "\u2212"

    difference_row = (
        '<tr style="border-top:2px solid #ddd; font-weight:700;">'
        '<td style="padding:6px 12px; color:#0F294A;">Difference (heat pump - gas boiler)</td>'
        f'<td style="padding:6px 12px; text-align:right; color:{difference_color};">'
        f"{difference_sign}£{abs(difference):,.0f}</td>"
        '<td style="padding:6px 12px;"></td>'
        "</tr>"
    )

    table_html = (
        '<table style="width:100%; font-size:13px; border-collapse:collapse; margin-top:20px;">'
        '<tr style="border-bottom:2px solid #ddd; font-weight:700; color:#0F294A;">'
        '<td style="padding:6px 12px;">Cost component</td>'
        '<td style="padding:6px 12px; text-align:right;">Air-to-water heat pump</td>'
        '<td style="padding:6px 12px; text-align:right;">Gas boiler</td>'
        "</tr>" + legend_rows + difference_row + "</table>"
    )

    st.markdown(table_html, unsafe_allow_html=True)

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
            data=eac_breakdown_df_for_export.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"equivalent_annualised_cost_breakdown_by_installation_year_{timestamp}.csv",
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
        f"How much each system will cost the household in each year of ownership, in present-value ({BASE_YEAR_DEFAULT} real £) terms. "
        "Includes upfront cost in year 0.</div>",
        unsafe_allow_html=True,
    )

    cashflow_chart = build_cashflow_chart(annual_breakdown_df, installation_year)
    st.altair_chart(cashflow_chart, width="stretch")

    # Prepare dataframe for export
    annual_cost_metrics_for_export = [
        "Discounted running cost",
        "Discounted maintenance cost",
        "Discounted capital cost",
        "Discounted annual cost of ownership",
    ]

    cashflow_df_for_export = annual_breakdown_df[
        (annual_breakdown_df["installation_year"] == installation_year)
        & (annual_breakdown_df["metric"].isin(annual_cost_metrics_for_export))
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

    with st.expander("▾ View/export more detailed underlying data"):
        st.dataframe(cashflow_df_for_export, width="stretch", hide_index=True)
        installation_year = int(cashflow_df_for_export["Installation year"].iloc[0])
        st.download_button(
            "⬇ Export CSV",
            data=annual_breakdown_df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"cost_of_ownership_annual_breakdown_installed_{installation_year}_{timestamp}.csv",
            mime="text/csv",
        )


def render_price_ratio_table(inputs: AppInputs) -> None:
    """Render the electricity-to-gas price ratio table: one column per year."""
    render_section_heading("Electricity-to-gas price ratio trajectory modelled")

    electricity_prices = build_electricity_prices(inputs)
    gas_prices = build_gas_prices(inputs)

    price_ratio_by_year = {}
    for year in OPERATING_YEARS:
        gas_price = gas_prices.get_price(year=year)
        electricity_price = electricity_prices.get_price(year=year)
        price_ratio_by_year[year] = (
            electricity_price / gas_price if gas_price > 0 else None
        )

    header_cells = "".join(
        f'<th style="padding:4px 11px; text-align:center; font-weight:700; color:#0F294A;">{year}</th>'
        for year in OPERATING_YEARS
    )
    value_cells = "".join(
        (
            f'<td style="padding:4px 11px; text-align:center; color:#0F294A;">{price_ratio_by_year[year]:.2f}</td>'
            if price_ratio_by_year[year] is not None
            else '<td style="padding:4px 11px; text-align:center; color:#999;">n/a (gas prize is zero)</td>'
        )
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
                    <td style="padding:4px 11px; font-weight:700; color:#0F294A;">Electricity to gas price ratio</td>
                    {value_cells}
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
