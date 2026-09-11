"""Convert AppInputs into asf_lifetime_cost_model trajectory objects.

Each function here takes the whole AppInputs object and returns one
trajectory, ready to be passed into a HeatingSystem. No Streamlit imports
here at all — these are pure functions, testable with a hand-built
AppInputs and no running app.
"""

import pandas as pd
import streamlit as st
from asf_lifetime_cost_model.getters import data_getters as model_data_getters
from asf_lifetime_cost_model.models.trajectory import (
    EnergyPriceTrajectory,
    InstallationCostTrajectory,
    SubsidyTrajectory,
)
from asf_lifetime_cost_model.utils.utils import deflate_to_real

from config.defaults import (
    BASE_YEAR_DEFAULT,
    INFLATION_RATE_DEFAULT,
    INSTALL_END_YEAR,
    INSTALL_START_YEAR,
)
from model_integration.schema import AppInputs

BASE_YEAR = BASE_YEAR_DEFAULT
INFLATION_RATE = INFLATION_RATE_DEFAULT
INSTALLATION_YEARS = range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)


def build_ashp_installation_costs(inputs: AppInputs) -> InstallationCostTrajectory:
    """Build the heat pump's installation cost trajectory from user inputs."""
    hp = inputs.heat_pump

    trajectory = InstallationCostTrajectory(
        "air_to_water_heat_pump",
        starting_cost=hp.installation_cost_current,
        price_basis="real",
        base_year=BASE_YEAR,
    )

    if hp.installation_cost_growth_mode == "flat":
        pass  # starting_cost is already flat across every year — nothing more to do
    elif hp.installation_cost_growth_mode == "annual_pct":
        trajectory.set_trajectory(
            hp.installation_cost_growth_rate, from_year=BASE_YEAR + 1
        )
    else:
        raise ValueError(
            f"Unknown installation_cost_growth_mode {hp.installation_cost_growth_mode!r}; "
            "expected 'flat' or 'annual_pct'"
        )

    return trajectory


def build_boiler_installation_costs(inputs: AppInputs) -> InstallationCostTrajectory:
    """Build the gas boiler's installation cost trajectory from user inputs.

    Currently always flat in real terms — GasBoilerInputs has no growth_mode
    field, since the boiler's installation cost isn't user-adjustable for
    future years (matching the original run script's assumption).
    """
    gb = inputs.gas_boiler
    return InstallationCostTrajectory(
        "gas_boiler",
        starting_cost=gb.installation_cost,
        price_basis="real",
        base_year=BASE_YEAR,
    )


@st.cache_data()
def _get_ashp_subsidy_options_data() -> pd.DataFrame:
    return model_data_getters.get_ashp_subsidy_options_data()


def get_subsidy_scenario_values(subsidy_scenario: str) -> dict[int, float]:
    """Look up a named ASHP subsidy scenario's £ values for every installation year.

    Used both to pre-fill the sidebar's subsidy override table (a preview,
    no model objects involved) and inside build_ashp_subsidies (to actually
    construct the real SubsidyTrajectory).
    """
    subsidy_df = _get_ashp_subsidy_options_data()
    scenario_row = (
        subsidy_df[subsidy_df["model"].str.lower() == subsidy_scenario.lower()]
        .drop(columns="model")
        .iloc[0]
    )
    return {
        int(year): float(value)
        for year, value in scenario_row.items()
        if int(year) in range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)
    }


def get_subsidy_scenario_options() -> list[str]:
    """List every named ASHP subsidy scenario available in the underlying data,
    nicely capitalised for display in the sidebar dropdown.
    """
    subsidy_df = _get_ashp_subsidy_options_data()
    raw_names = sorted(subsidy_df["model"].dropna().unique().tolist())
    return [name.capitalize() for name in raw_names]


def build_ashp_subsidies(inputs: AppInputs) -> SubsidyTrajectory:
    """Build the heat pump's subsidy trajectory from user inputs."""
    hp = inputs.heat_pump

    if hp.subsidy_scenario is None:
        trajectory = SubsidyTrajectory(
            "air_to_water_heat_pump",
            starting_subsidy=0.0,
            price_basis="real",
            base_year=BASE_YEAR_DEFAULT,
        )
    else:
        scenario_values = get_subsidy_scenario_values(hp.subsidy_scenario)
        trajectory = SubsidyTrajectory(
            "air_to_water_heat_pump",
            starting_subsidy=scenario_values[INSTALL_START_YEAR],
        )
        trajectory.set_trajectory(scenario_values)
        trajectory.to_real(
            base_year=BASE_YEAR_DEFAULT, inflation_rate=INFLATION_RATE_DEFAULT
        )

    if hp.subsidy_overrides:
        # hp.subsidy_overrides are in nominal terms (matching what the user
        # sees/types in the sidebar)
        # need to convert each to real terms per its own year
        # since `trajectory` needs to be in real terms
        overrides_real = {
            year: deflate_to_real(
                value, year, BASE_YEAR_DEFAULT, INFLATION_RATE_DEFAULT
            )
            for year, value in hp.subsidy_overrides.items()
        }
        trajectory.set_trajectory(overrides_real)

    return trajectory


def build_gas_boiler_subsidies() -> SubsidyTrajectory:
    """Build a flat, zero-value subsidy trajectory for the gas boiler (no subsidy scheme)."""
    return SubsidyTrajectory(
        "gas_boiler", starting_subsidy=0.0, price_basis="real", base_year=BASE_YEAR
    )


def build_gas_prices(inputs: AppInputs) -> EnergyPriceTrajectory:
    """Build the gas price trajectory from user inputs."""
    prices = inputs.energy_prices

    trajectory = EnergyPriceTrajectory(
        "gas",
        starting_price=prices.gas_current_price,
        price_basis="real",
        base_year=BASE_YEAR,
    )

    if prices.gas_growth_mode == "flat":
        pass
    elif prices.gas_growth_mode == "annual_pct":
        trajectory.set_trajectory(prices.gas_growth_rate, from_year=BASE_YEAR + 1)
    elif prices.gas_growth_mode == "custom":
        trajectory.set_trajectory(prices.gas_overrides)
    else:
        raise ValueError(f"Unknown gas_growth_mode {prices.gas_growth_mode!r}")

    return trajectory


def build_electricity_prices(inputs: AppInputs) -> EnergyPriceTrajectory:
    """Build the (headline, pre-ToU-discount) electricity price trajectory from user inputs.

    If electricity_current_price is None (on the electricity-price-solver
    page, where the price cap rate is being solved for), returns a flat
    trajectory seeded at the latest price cap rate as a safe baseline —
    the actual value used at construction time doesn't affect
    solve_electricity_price_for_parity's result.
    """
    prices = inputs.energy_prices

    if prices.electricity_current_price is None:
        starting_price = model_data_getters.get_latest_price_cap_rate("electricity")
        return EnergyPriceTrajectory(
            "electricity",
            starting_price=starting_price,
            price_basis="real",
            base_year=BASE_YEAR,
        )

    trajectory = EnergyPriceTrajectory(
        "electricity",
        starting_price=prices.electricity_current_price,
        price_basis="real",
        base_year=BASE_YEAR,
    )

    if prices.electricity_growth_mode == "flat":
        pass
    elif prices.electricity_growth_mode == "annual_pct":
        trajectory.set_trajectory(
            prices.electricity_growth_rate, from_year=BASE_YEAR + 1
        )
    elif prices.electricity_growth_mode == "custom":
        trajectory.set_trajectory(prices.electricity_overrides)
    else:
        raise ValueError(
            f"Unknown electricity_growth_mode {prices.electricity_growth_mode!r}"
        )

    return trajectory


def build_ashp_electricity_prices(inputs: AppInputs) -> EnergyPriceTrajectory:
    """Build the heat pump's effective electricity price trajectory: the
    headline price cap rate (build_electricity_prices), discounted by the
    ToU tariff discount.
    """
    trajectory = build_electricity_prices(inputs)
    ashp_electricity_prices = EnergyPriceTrajectory(
        "electricity",
        starting_price=trajectory.get_price(year=BASE_YEAR),
        price_basis="real",
        base_year=BASE_YEAR,
    )
    ashp_electricity_prices.series = trajectory.prices.copy()
    ashp_electricity_prices.apply_percentage_discount(
        inputs.heat_pump.tou_tariff_discount
    )
    return ashp_electricity_prices
