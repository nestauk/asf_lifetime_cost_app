"""Licence and attribution statement and helper for building export content."""

import io
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

from config.defaults import (
    ASHP_INSTALLATION_COST_DEFAULT,
    BOILER_HEAT_DEMAND_DEFAULT,
    get_electricity_price_default,
    get_gas_price_default,
)
from model_integration.schema import AppInputs

yearstamp = datetime.now(ZoneInfo("Europe/London")).strftime("%Y")
datestamp = datetime.now(ZoneInfo("Europe/London")).strftime("%d/%m/%Y")

LICENCE_STATEMENT = [
    "These results were calculated using the Heating System Lifetime Cost Tool created by Nesta (2026).",
    "",
    "Licence: CC BY 4.0",
    "This dataset is made available under the Creative Commons Attribution 4.0 International "
    "(CC BY 4.0) License. You are free to use, share, and adapt this data for any purpose, "
    "including commercial use, provided you include the appropriate acknowledgements below.",
    "",
    "If you use these results in any reports, products, or publications, please cite it as:",
    f"Heating System Lifetime Cost Tool (2026), Nesta, https://lifetime-costs-explorer.dap-tools.uk/. Accessed on {datestamp}.",
]


def build_attribution_statement(inputs: AppInputs) -> list[str]:
    """Build a list of attribution lines, one source per line, included only
    if the user has kept specific defaults sourced from third-party licensed
    data (Ofgem price caps, MCS installation statistics). If the user has
    overridden all of these, returns a single "custom inputs" line instead,
    since the result no longer reflects that source data.
    """
    used_mcs_heat_demand = inputs.boiler_heat_demand == BOILER_HEAT_DEMAND_DEFAULT
    used_mcs_install_cost = (
        inputs.heat_pump.installation_cost_current == ASHP_INSTALLATION_COST_DEFAULT
    )
    used_gas_price_cap = (
        inputs.energy_prices.gas_current_price == get_gas_price_default()
    )
    used_electricity_price_cap = (
        inputs.energy_prices.electricity_current_price
        == get_electricity_price_default()
    )

    sources = []
    if used_mcs_heat_demand:
        sources.append(
            "• Median heat demand for homes fitting an 8-10 kW air-to-water heat pump in financial "
            "year 2025/26 from analysis of the MCS Installations Database "
            "(https://certificate.microgenerationcertification.org/)."
        )
        sources.append(
            "This median heat demand typically corresponded to a 5-room (2-3 bedroom) detached house, estimated "
            "using data in the Domestic EPC for England and Wales "
            "(https://get-energy-performance-data.communities.gov.uk/) (Open Government Licence "
            "v.3.0: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) "
            "and Domestic EPC for Scotland "
            "(https://statistics.gov.scot/data/domestic-energy-performance-certificates) (Open "
            "Government Licence v.3.0: "
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )
    if used_mcs_install_cost:
        sources.append(
            "• Median installation cost for homes fitting an 8-10 kW air-to-water heat pump in "
            "financial year 2025/26 from analysis of the MCS Installations Database "
            "(https://certificate.microgenerationcertification.org/)."
        )
    if used_gas_price_cap:
        sources.append(
            "• Modelled gas price trajectory started with the latest published GB average Ofgem price cap for the current year "
            "(https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges) "
            "(Open Government Licence v.3.0: "
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )
    if used_electricity_price_cap:
        sources.append(
            "• Modelled electricity price trajectory started with the latest published GB average Ofgem price cap for the current year "
            "(https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges) "
            "(Open Government Licence v.3.0: "
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )

    if not sources:
        return ["Calculated using custom user inputs."]

    return [
        "Calculated using custom user inputs and default input figures sourced from:"
    ] + sources


def create_excel_content_with_licence(
    inputs: AppInputs,
    assumptions_text: str,
    df_for_export: pd.DataFrame,
    results_sheet_name: str,
) -> bytes:
    """Build a two-sheet Excel workbook: Sheet 1 (Licence & assumptions) holds
    the licence statement, attribution statement, and assumptions summary;
    Sheet 2 (Results) holds the actual results DataFrame.
    """

    sheet1_lines = (
        LICENCE_STATEMENT
        + build_attribution_statement(inputs=inputs)
        + [""]
        + assumptions_text
    )
    sheet1_df = pd.DataFrame(sheet1_lines, columns=[""])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        sheet1_df.to_excel(
            writer, sheet_name="Licence & assumptions", index=False, header=False
        )
        df_for_export.to_excel(writer, sheet_name=f"{results_sheet_name}", index=False)

    return output.getvalue()


def create_assumptions_summary_with_licence(inputs: AppInputs) -> str:
    """Prepend licence and attributions to the assumptions summary."""
    from page_sections.assumptions_summary import build_assumptions_text

    all_lines = (
        LICENCE_STATEMENT
        + build_attribution_statement(inputs=inputs)
        + [""]
        + build_assumptions_text(inputs=inputs)
    )
    return "\n".join(all_lines) + "\n\n"
