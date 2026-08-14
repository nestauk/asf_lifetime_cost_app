"""Altair charts built from comparison_df / annual_breakdown_df.

Pure charting functions — take a DataFrame, return an alt.Chart. No
Streamlit imports, no model imports; this file only knows about pandas
and Altair.
"""

import altair as alt
import pandas as pd

SYSTEM_COLORS = {
    "Heat pump": "#18A48C",
    "Heat pump (no subsidy)": "#646363",
    "Gas boiler": "#0000FF",
}
SYSTEM_LABELS = {
    "Heat pump": "Air-to-water heat pump",
    "Heat pump (no subsidy)": "Air-to-water heat pump (no subsidy)",
    "Gas boiler": "Gas boiler",
}
COMPONENT_ORDER = [
    "Equivalent Annual Cost: capital cost (principal only)",
    "Equivalent Annual Cost: loan interest",
    "Equivalent Annual Cost: running cost",
    "Equivalent Annual Cost: maintenance cost",
]
COMPONENT_LABELS = {
    "Equivalent Annual Cost: capital cost (principal only)": "Capital cost (principal only)",
    "Equivalent Annual Cost: loan interest": "Loan interest",
    "Equivalent Annual Cost: maintenance cost": "Maintenance",
    "Equivalent Annual Cost: running cost": "Running cost",
    "Annualised discounted lifetime cost (Equivalent Annual Cost)": "Total annualised lifetime cost",
}
COMPONENT_COLORS = {
    "Capital cost (principal only)": "#0F294A",
    "Loan interest": "#F6A4B7",
    "Maintenance": "#97D9E3",
    "Running cost": "#9A1BBE",
}

EAC_METRIC = "Annualised discounted lifetime cost (Equivalent Annual Cost)"
ANNUAL_COST_METRIC = "Discounted annual cost"

# Canonical ordering for the three-system charts/filters, and its label/color
# projections, so callers don't each re-derive or re-hardcode these lists.
SYSTEM_ORDER = ["Heat pump", "Heat pump (no subsidy)", "Gas boiler"]
SYSTEM_LABEL_ORDER = [SYSTEM_LABELS[s] for s in SYSTEM_ORDER]
SYSTEM_COLOR_RANGE = [SYSTEM_COLORS[s] for s in SYSTEM_ORDER]


def get_eac(comparison_df: pd.DataFrame, installation_year: int, system: str) -> float:
    """Look up a single system's Equivalent Annual Cost for one installation year."""
    return comparison_df[
        (comparison_df["installation_year"] == installation_year)
        & (comparison_df["system"] == system)
        & (comparison_df["metric"] == EAC_METRIC)
    ]["value"].iloc[0]


# ---------------------------------------------------------------------------
#  Annualised lifetime cost by installation year
# ---------------------------------------------------------------------------


def build_eac_by_year_chart(comparison_df: pd.DataFrame) -> alt.Chart:
    """Line chart: annualised lifetime cost (EAC) by installation year, one line per system.

    The no-subsidy heat pump line is drawn dashed/lighter since it's a
    reference line, not part of the core comparison.
    """
    eac_df = comparison_df[comparison_df["metric"] == EAC_METRIC].copy()
    eac_df["system_label"] = eac_df["system"].map(SYSTEM_LABELS)

    NO_SUBSIDY_SYSTEM = "Heat pump (no subsidy)"

    # Compute the y-axis domain from the actual data with padding on each side
    data_min = eac_df["value"].min()
    data_max = eac_df["value"].max()
    data_range = data_max - data_min
    padding = data_range * 0.5 if data_range > 0 else data_max * 0.1
    y_domain = [0, data_max + padding]

    max_year = eac_df["installation_year"].max()

    base = alt.Chart(eac_df).encode(
        x=alt.X(
            "installation_year:O",
            title="Installation year",
            axis=alt.Axis(labelAngle=0, titleFontWeight="bold"),
            scale=alt.Scale(padding=0),
        ),
        y=alt.Y(
            "value:Q",
            title="Annualised lifetime cost (£)",
            scale=alt.Scale(domain=y_domain),
            axis=alt.Axis(
                tickCount=6,
                titleFontWeight="bold",
            ),
        ),
        color=alt.Color(
            "system_label:N",
            sort=SYSTEM_LABEL_ORDER,
            scale=alt.Scale(domain=SYSTEM_LABEL_ORDER, range=SYSTEM_COLOR_RANGE),
            legend=None,  # end-of-line labels instead
        ),
        tooltip=[
            alt.Tooltip("system_label:N", title="System"),
            alt.Tooltip("installation_year:O", title="Installation year"),
            alt.Tooltip("value:Q", title="Annualised lifetime cost (£)", format=",.0f"),
        ],
    )

    solid_lines = base.transform_filter(
        alt.datum.system != NO_SUBSIDY_SYSTEM
    ).mark_line(point=True, strokeWidth=2.5)

    dashed_line = base.transform_filter(
        alt.datum.system == NO_SUBSIDY_SYSTEM
    ).mark_line(point=True, strokeWidth=2, strokeDash=[6, 4], opacity=0.6)

    end_labels = (
        base.transform_filter(alt.datum.installation_year == max_year)
        .transform_calculate(
            label_text="replace(datum.system_label, ' (no subsidy)', '\\n(no subsidy)')"
        )
        .mark_text(
            align="left",
            dx=8,
            fontSize=12,
            fontWeight="bold",
            font="Averta",
            lineBreak="\n",
            lineHeight=14,
        )
        .encode(text="label_text:N")
    )

    return (dashed_line + solid_lines + end_labels).properties(
        height=500, padding={"top": 20, "bottom": 10, "left": 0, "right": 0}
    )


def _value_for_label(year_df: pd.DataFrame, system_label: str) -> float:
    return year_df[year_df["system_label"] == system_label]["value"].iloc[0]


def build_eac_headline_messages(eac_df: pd.DataFrame) -> list[str]:
    """Build the full set of headline messages: cost comparison, subsidy effect, and trend consistency."""
    messages = []

    # --- Direct comparison in the first installation year ---
    first_year = eac_df["installation_year"].min()
    year_df = eac_df[eac_df["installation_year"] == first_year]

    heat_pump_eac = _value_for_label(year_df, SYSTEM_LABELS["Heat pump"])
    gas_boiler_eac = _value_for_label(year_df, SYSTEM_LABELS["Gas boiler"])
    difference = heat_pump_eac - gas_boiler_eac

    comparison_word = "more" if difference > 0 else "less"
    messages.append(
        f"A heat pump installed in {first_year} costs <strong>£{abs(difference):,.0f}</strong> "
        f"{comparison_word} a year than a gas boiler."
    )

    # --- Subsidy effect, in the first installation year ---
    no_subsidy_eac = _value_for_label(year_df, SYSTEM_LABELS["Heat pump (no subsidy)"])
    subsidy_saving = no_subsidy_eac - heat_pump_eac
    messages.append(
        f"The subsidy saves <strong>£{subsidy_saving:,.0f}</strong> a year on the heat pump's cost."
    )

    # --- Winner across installation years ---
    pivot = eac_df.pivot(
        index="installation_year", columns="system_label", values="value"
    )
    hp_col, gb_col = SYSTEM_LABELS["Heat pump"], SYSTEM_LABELS["Gas boiler"]
    diff_series = pivot[hp_col] - pivot[gb_col]

    if (diff_series > 0).all():
        messages.append(
            "The gas boiler stays cheaper across every installation year shown."
        )
    elif (diff_series < 0).all():
        messages.append(
            "The heat pump stays cheaper across every installation year shown."
        )
    else:
        crossover_year = diff_series[
            diff_series.apply(lambda x: x * diff_series.iloc[0] < 0)
        ].index.min()
        messages.append(
            f"The cheaper option switches around <strong>{crossover_year}</strong>."
        )

    return messages


# ---------------------------------------------------------------------------
#  Annualised lifetime cost breakdown for a chosen install year
# ---------------------------------------------------------------------------


def build_cost_breakdown_chart(
    comparison_df: pd.DataFrame, installation_year: int
) -> alt.Chart:
    """Stacked bar: EAC broken into upfront/loan interest/maintenance/running cost, for one installation year."""
    breakdown_df = comparison_df[
        (comparison_df["installation_year"] == installation_year)
        & (comparison_df["metric"].isin(COMPONENT_ORDER))
        & (comparison_df["system"].isin(["Heat pump", "Gas boiler"]))
    ].copy()
    breakdown_df["system_label"] = breakdown_df["system"].map(SYSTEM_LABELS)
    breakdown_df["component_label"] = breakdown_df["metric"].map(COMPONENT_LABELS)

    component_label_order = [COMPONENT_LABELS[c] for c in COMPONENT_ORDER]
    component_rank = {label: i for i, label in enumerate(component_label_order)}
    breakdown_df["component_rank"] = breakdown_df["component_label"].map(component_rank)

    color_range = [COMPONENT_COLORS[c] for c in component_label_order]
    system_order = [SYSTEM_LABELS[s] for s in ["Heat pump", "Gas boiler"]]

    heat_pump_eac = get_eac(comparison_df, installation_year, "Heat pump")
    no_subsidy_eac = get_eac(comparison_df, installation_year, "Heat pump (no subsidy)")
    subsidy_saving = no_subsidy_eac - heat_pump_eac

    # Shared y-domain across every layer
    max_value = max(
        breakdown_df.groupby("system_label")["value"].sum().max(), no_subsidy_eac
    )
    y_domain = [0, max_value * 1.15]
    y_scale = alt.Scale(domain=y_domain)

    x_enc = alt.X(
        "system_label:N",
        title=None,
        sort=system_order,
        axis=alt.Axis(labelAngle=0, labelLimit=200, labelFontWeight="bold"),
    )

    bars = (
        alt.Chart(breakdown_df)
        .mark_bar(size=300)
        .encode(
            x=x_enc,
            y=alt.Y(
                "value:Q",
                title="Annualised lifetime cost (£)",
                stack="zero",
                scale=y_scale,
                axis=alt.Axis(tickCount=6),
            ),
            color=alt.Color(
                "component_label:N",
                title="Cost component",
                sort=component_label_order,
                scale=alt.Scale(domain=component_label_order, range=color_range),
                legend=None,
            ),
            order=alt.Order("component_rank:Q", sort="ascending"),
            tooltip=[
                alt.Tooltip("system_label:N", title="System"),
                alt.Tooltip("component_label:N", title="Component"),
                alt.Tooltip("value:Q", title="£/year", format=",.0f"),
            ],
        )
    )

    breakdown_df_sorted = breakdown_df.sort_values(["system_label", "component_rank"])
    breakdown_df_sorted["cum_end"] = breakdown_df_sorted.groupby("system_label")[
        "value"
    ].cumsum()
    breakdown_df_sorted["cum_start"] = (
        breakdown_df_sorted["cum_end"] - breakdown_df_sorted["value"]
    )
    breakdown_df_sorted["mid"] = (
        breakdown_df_sorted["cum_start"] + breakdown_df_sorted["cum_end"]
    ) / 2

    labels_df = breakdown_df_sorted[breakdown_df_sorted["value"] > 100]

    labels = (
        alt.Chart(labels_df)
        .transform_calculate(label_text="'£' + format(datum.value, ',.0f')")
        .mark_text(color="white", fontSize=11, font="Averta")
        .encode(
            x=x_enc,
            y=alt.Y("mid:Q"),
            text=alt.Text("label_text:N"),
            order=alt.Order("component_rank:Q", sort="ascending"),
            tooltip=alt.value(None),
        )
    )
    totals_df = breakdown_df.groupby("system_label", as_index=False)["value"].sum()

    totals = (
        alt.Chart(totals_df)
        .transform_calculate(label_text="'£' + format(datum.value, ',.0f')")
        .mark_text(
            dy=-8, fontSize=12, fontWeight="bold", color="#0F294A", font="Averta"
        )
        .encode(
            x=x_enc,
            y=alt.Y("value:Q", scale=y_scale),
            text=alt.Text("label_text:N"),
            tooltip=alt.value(None),
        )
    )

    annotation_df = pd.DataFrame(
        {
            "system_label": ["Air-to-water heat pump"],
            "y_bottom": [heat_pump_eac],
            "y_top": [no_subsidy_eac],
        }
    )

    subsidy_box = (
        alt.Chart(annotation_df)
        .mark_rect(
            fill=None,
            stroke="#888",
            strokeDash=[4, 3],
            strokeWidth=1.5,
            width=300,
        )
        .encode(
            x=x_enc,
            y=alt.Y("y_bottom:Q", scale=y_scale),
            y2=alt.Y2("y_top:Q"),
        )
    )

    subsidy_label = (
        alt.Chart(annotation_df)
        .mark_text(
            align="left",
            dx=-60,
            dy=-14,
            fontSize=11,
            color="#444",
            # fontWeight="bold",
            font="Averta",
        )
        .encode(
            x=x_enc,
            y=alt.Y("y_top:Q", scale=y_scale),
            text=alt.value(f"Subsidy saving: £{subsidy_saving:,.0f}/year"),
        )
    )

    return alt.layer(bars, labels, totals, subsidy_box, subsidy_label).properties(
        height=400,
    )


# ---------------------------------------------------------------------------
#  Cost during each year of heating system's lifespan
# ---------------------------------------------------------------------------


def build_cashflow_chart(
    annual_breakdown_df: pd.DataFrame, installation_year: int
) -> alt.Chart:
    """Line chart: total yearly cost by calendar year, one line per system.

    The no-subsidy heat pump line is a reference line: dashed/lighter,
    consistent with the EAC-by-installation-year chart. Since Altair legend
    swatches don't reflect stroke-dash, the no-subsidy series uses a
    distinct (lighter) shade of the same hue instead, so it's visually
    distinguishable in the legend too.
    """
    cashflow_df = annual_breakdown_df[
        (annual_breakdown_df["installation_year"] == installation_year)
        & (annual_breakdown_df["metric"] == ANNUAL_COST_METRIC)
        & (annual_breakdown_df["system"].isin(SYSTEM_ORDER))
    ].copy()
    cashflow_df["system_label"] = cashflow_df["system"].map(SYSTEM_LABELS)

    NO_SUBSIDY_SYSTEM = "Heat pump (no subsidy)"

    base = alt.Chart(cashflow_df).encode(
        x=alt.X(
            "operating_year:O",
            title="Year in lifetime",
            axis=alt.Axis(labelAngle=0, titleFontWeight="bold"),
        ),
        y=alt.Y(
            "value:Q",
            title="Annual cost of ownership (£)",
            axis=alt.Axis(labelAngle=0, titleFontWeight="bold"),
        ),
        color=alt.Color(
            "system_label:N",
            title="Heating system",
            sort=SYSTEM_LABEL_ORDER,
            scale=alt.Scale(domain=SYSTEM_LABEL_ORDER, range=SYSTEM_COLOR_RANGE),
            legend=alt.Legend(
                orient="bottom",
                columns=3,
                labelLimit=300,
                symbolLimit=0,
                titleOrient="left",
                titleFontSize=12,
                titleFontWeight="bold",
                titleColor="#0F294A",
                labelFontSize=12,
                labelColor="#0F294A",
            ),
        ),
        tooltip=[
            alt.Tooltip("system_label:N", title="System"),
            alt.Tooltip("operating_year:O", title="Year"),
            alt.Tooltip("value:Q", title="£/year", format=",.0f"),
        ],
    )

    solid_lines = base.transform_filter(
        alt.datum.system != NO_SUBSIDY_SYSTEM
    ).mark_line(point=True, strokeWidth=2.5)

    dashed_line = base.transform_filter(
        alt.datum.system == NO_SUBSIDY_SYSTEM
    ).mark_line(point=True, strokeWidth=2, strokeDash=[6, 4])

    return (dashed_line + solid_lines).properties(height=500)


def build_required_subsidy_chart(
    required_subsidy_df: pd.DataFrame, current_subsidy: float = 7_500.0
) -> alt.Chart:
    """Line chart: required subsidy by installation year, with a dashed reference line
    showing the current/default subsidy level for comparison.
    """
    installation_years = sorted(required_subsidy_df["installation_year"].unique())

    line = (
        alt.Chart(required_subsidy_df)
        .mark_line(
            point=alt.OverlayMarkDef(filled=True, color="#0000FF"),
            strokeWidth=2.5,
            color="#0000FF",
        )
        .encode(
            x=alt.X(
                "installation_year:O",
                title="Installation year",
                axis=alt.Axis(labelAngle=0, titleFontWeight="bold"),
                scale=alt.Scale(
                    domain=installation_years,
                    padding=0,
                ),
            ),
            y=alt.Y(
                "required_subsidy:Q",
                title="Required subsidy (£)",
                axis=alt.Axis(titleFontWeight="bold"),
            ),
            tooltip=[
                alt.Tooltip("installation_year:O", title="Installation year"),
                alt.Tooltip(
                    "required_subsidy:Q", title="Required subsidy (£)", format=",.0f"
                ),
            ],
        )
    )

    reference_df = pd.DataFrame({"y": [current_subsidy]})

    reference_line = (
        alt.Chart(reference_df)
        .mark_rule(strokeDash=[4, 3], color="#888", strokeWidth=1.5)
        .encode(y=alt.Y("y:Q"))
    )

    reference_label = (
        alt.Chart(reference_df)
        .mark_text(
            align="left",
            dx=5,
            dy=-6,
            fontSize=11,
            color="#444",
            fontWeight="bold",
            font="Averta",
        )
        .encode(
            y=alt.Y("y:Q"), text=alt.value(f"Current subsidy: £{current_subsidy:,.0f}")
        )
    )

    return alt.layer(line, reference_line, reference_label).properties(height=400)


def build_required_electricity_price_chart(
    required_price_cap_rates: dict[int, float],
    current_price_cap_rate: float | None = None,
) -> alt.Chart:
    """Line chart: required electricity price cap rate by operating year, for one
    installation year's heat pump. Optionally overlays a dashed reference line
    showing today's actual price cap rate, for comparison.
    """
    price_df = pd.DataFrame(
        {
            "operating_year": list(required_price_cap_rates.keys()),
            "required_price": list(required_price_cap_rates.values()),
        }
    )

    line = (
        alt.Chart(price_df)
        .mark_line(
            point=alt.OverlayMarkDef(filled=True, color="#18A48C"),
            strokeWidth=2.5,
            color="#18A48C",
        )
        .encode(
            x=alt.X(
                "operating_year:O",
                title="Year",
                axis=alt.Axis(labelAngle=0),
                scale=alt.Scale(
                    domain=sorted(required_price_cap_rates.keys()), padding=0
                ),
            ),
            y=alt.Y("required_price:Q", title="Required electricity price (p/kWh)"),
            tooltip=[
                alt.Tooltip("operating_year:O", title="Year"),
                alt.Tooltip(
                    "required_price:Q", title="Required price (p/kWh)", format=",.1f"
                ),
            ],
        )
    )

    if current_price_cap_rate is None:
        return line.properties(height=340)

    reference_df = pd.DataFrame({"y": [current_price_cap_rate]})

    reference_line = (
        alt.Chart(reference_df)
        .mark_rule(strokeDash=[4, 3], color="#888", strokeWidth=1.5)
        .encode(y=alt.Y("y:Q"))
    )

    reference_label = (
        alt.Chart(reference_df)
        .mark_text(
            align="left",
            dx=5,
            dy=-6,
            fontSize=11,
            color="#444",
            fontWeight="bold",
            font="Averta",
        )
        .encode(
            y=alt.Y("y:Q"),
            text=alt.value(f"Current price cap: {current_price_cap_rate:.1f}p/kWh"),
        )
    )

    return alt.layer(line, reference_line, reference_label).properties(height=340)


def build_required_price_ratio_chart(
    required_ratio_by_year: dict[int, float], current_ratio: float | None = None
) -> alt.Chart:
    """Line chart: required electricity-to-gas price ratio by operating year, with data labels."""
    ratio_df = pd.DataFrame(
        {
            "operating_year": list(required_ratio_by_year.keys()),
            "ratio": list(required_ratio_by_year.values()),
        }
    )
    years_sorted = sorted(required_ratio_by_year.keys())

    x_enc = alt.X(
        "operating_year:O",
        title="Year",
        axis=alt.Axis(labelAngle=0),
        scale=alt.Scale(domain=years_sorted, padding=0),
    )

    line = (
        alt.Chart(ratio_df)
        .mark_line(
            point=alt.OverlayMarkDef(filled=True, color="#0000FF"),
            strokeWidth=2.5,
            color="#0000FF",
        )
        .encode(
            x=x_enc,
            y=alt.Y("ratio:Q", title="Required electricity-to-gas price ratio"),
            tooltip=[
                alt.Tooltip("operating_year:O", title="Year"),
                alt.Tooltip("ratio:Q", title="Required ratio", format=",.2f"),
            ],
        )
    )

    labels = (
        alt.Chart(ratio_df)
        .mark_text(
            dy=-14, fontSize=11, fontWeight="bold", color="#0000FF", font="Averta"
        )
        .encode(
            x=x_enc,
            y=alt.Y("ratio:Q"),
            text=alt.Text("ratio:Q", format=".2f"),
            tooltip=alt.value(None),
        )
    )

    layers = [line, labels]

    if current_ratio is not None:
        reference_df = pd.DataFrame({"y": [current_ratio]})
        reference_line = (
            alt.Chart(reference_df)
            .mark_rule(strokeDash=[4, 3], color="#888", strokeWidth=1.5)
            .encode(y=alt.Y("y:Q"))
        )
        reference_label = (
            alt.Chart(reference_df)
            .mark_text(
                align="left",
                dx=5,
                dy=-6,
                fontSize=11,
                color="#444",
                fontWeight="bold",
                font="Averta",
            )
            .encode(
                y=alt.Y("y:Q"), text=alt.value(f"Current ratio: {current_ratio:.2f}")
            )
        )
        layers.extend([reference_line, reference_label])

    return alt.layer(*layers).properties(height=340)
