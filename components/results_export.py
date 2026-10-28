"""Licence and attribution statement and helper for building export content."""

import io
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
from openpyxl.styles import Font

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
    "This dataset was generated using the Heating System Lifetime Cost Tool created by Nesta (2026).",
    "",
    "Licence: CC BY-NC-SA 4.0",
    "This dataset is made available under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International "
    "(CC BY-NC-SA 4.0) License.",
    "You are free to share and adapt this material for non-commercial purposes, "
    "provided you give appropriate credit, provide a link to the license, and distribute your contributions under "
    "the same license as the original.",
    "When reusing, sharing, or redistributing this workbook or its derived charts, you must keep intact all "
    "embedded licensing notices, copyright tags, and source attributions provided within the file.",
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
    if (
        used_mcs_heat_demand
        or used_mcs_install_cost
        or used_gas_price_cap
        or used_electricity_price_cap
    ):
        sources.append(
            "If you use these results in any reports, products or publications, please include the following data source attributions for default inputs used:"
        )

    if used_mcs_heat_demand:
        sources.append(
            "• MCS Installations Database (https://certificate.microgenerationcertification.org/):"
        )
        sources.append(
            " - Used for default annual heat demand estimate, corresponding to the median of homes fitting an 8-10 kW air-to-water heat pump "
            "in FY 2025/26, derived from Nesta analysis of the MCS Installations Database."
        )
        sources.append(
            " - The underlying MCS Installations Database is not openly available. You can contact MCS to request "
            "access to the data or visit their dashboard at https://datadashboard.mcscertified.com/Welcome."
        )
        sources.append("• Domestic Energy Performance Certificate (EPC) Registers:")
        sources.append(
            " - Used to align median heat demand with typical dwelling specifications (5-room / 2–3 bedroom detached house)."
        )
        sources.append(
            " - England & Wales EPC Data (https://get-energy-performance-data.communities.gov.uk/). Used under Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )
        sources.append(
            " - Scotland EPC Data (https://statistics.gov.scot/data/domestic-energy-performance-certificates). Used under Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )
    if used_mcs_install_cost:
        sources.append(
            "• MCS Installations Database (https://certificate.microgenerationcertification.org/):"
        )
        sources.append(
            " - Used for default installation cost, corresponding to the median of homes fitting an 8-10 kW air-to-water heat pump "
            "in FY 2025/26, derived from Nesta analysis of the MCS Installations Database."
        )
    if used_gas_price_cap:
        sources.append(
            "• Ofgem energy price cap for gas (https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges)"
        )
        sources.append(
            " - Latest published GB average Ofgem price cap was used as the starting price for the current year in the user-modelled gas price trajectory."
        )
        sources.append(
            " - Used under Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )
    if used_electricity_price_cap:
        sources.append(
            "• Ofgem energy price cap for electricity (https://www.ofgem.gov.uk/your-energy-supply/your-energy-bill/energy-price-cap-unit-rates-and-standing-charges)"
        )
        sources.append(
            " - Latest published GB average Ofgem price cap was used as the starting price for the current year in the user-modelled electricity price trajectory."
        )
        sources.append(
            " - Used under Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)."
        )

    return sources


def create_excel_content_with_licence(
    inputs: AppInputs,
    assumptions_text: str,
    df_for_export: pd.DataFrame,
    results_sheet_name: str,
) -> bytes:
    """Build a two-sheet Excel workbook: Sheet 1 (Licence & assumptions) holds
    the licence statement, attribution statement, and assumptions summary;
    Sheet 2 (Results) holds the actual results dataframe.
    """
    sheet1_lines = (
        LICENCE_STATEMENT
        + [""]
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
        df_for_export.to_excel(writer, sheet_name=results_sheet_name, index=False)

        # Bold specific lines in the Licence & assumptions sheet
        worksheet = writer.sheets["Licence & assumptions"]
        bold_font = Font(bold=True)
        bold_line_texts = {
            "This dataset was generated using the Heating System Lifetime Cost Tool created by Nesta (2026).",
            "Licence: CC BY-NC-SA 4.0",
            "If you use these results in any reports, products, or publications, please cite it as:",
            "If you use these results in any reports, products or publications, please include the following data source attributions for default inputs used:",
            "The assumptions set by the user to generate these results:",
        }
        for row_idx, line in enumerate(sheet1_lines, start=1):
            if line in bold_line_texts:
                worksheet.cell(row=row_idx, column=1).font = bold_font

    return output.getvalue()
