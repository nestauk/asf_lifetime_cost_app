"""Build HeatingSystem instances from AppInputs, for a specific installation year."""

from asf_lifetime_cost_model.models.heating_system import HeatingSystem

from model_integration.schema import AppInputs
from model_integration.trajectories import (
    build_ashp_installation_costs,
    build_ashp_subsidies,
    build_boiler_installation_costs,
    build_gas_boiler_subsidies,
)


def build_heat_pump_for_year(
    inputs: AppInputs, installation_year: int
) -> HeatingSystem:
    """Build the heat pump HeatingSystem for a given installation year."""
    hp = inputs.heat_pump
    return HeatingSystem(
        system_type="air_to_water_heat_pump",
        installation_year=installation_year,
        lifespan=hp.lifespan,
        efficiency=hp.scop,
        installation_cost_trajectory=build_ashp_installation_costs(inputs),
        subsidy_trajectory=build_ashp_subsidies(inputs),
        maintenance_cost_per_visit=hp.maintenance_cost_per_visit,
        maintenance_annual_frequency=hp.maintenance_annual_frequency,
        interest_rate=hp.interest_rate if hp.is_financed else None,
        loan_term=hp.loan_term if hp.is_financed else None,
    )


def build_heat_pump_no_subsidy_for_year(
    inputs: AppInputs, installation_year: int
) -> HeatingSystem:
    """Build a heat pump HeatingSystem with zero subsidy, for the 'Heat pump (no subsidy)' comparison line.

    Reuses the same trajectory-building logic, but constructs its own
    zero-subsidy SubsidyTrajectory directly rather than calling
    build_ashp_subsidies (which reads inputs.heat_pump.subsidy_scenario).
    """
    from asf_lifetime_cost_model.models.trajectory import SubsidyTrajectory

    from config.defaults import BASE_YEAR_DEFAULT

    hp = inputs.heat_pump
    zero_subsidy = SubsidyTrajectory(
        "air_to_water_heat_pump",
        starting_subsidy=0.0,
        price_basis="real",
        base_year=BASE_YEAR_DEFAULT,
    )
    return HeatingSystem(
        system_type="air_to_water_heat_pump",
        installation_year=installation_year,
        lifespan=hp.lifespan,
        efficiency=hp.scop,
        installation_cost_trajectory=build_ashp_installation_costs(inputs),
        subsidy_trajectory=zero_subsidy,
        maintenance_cost_per_visit=hp.maintenance_cost_per_visit,
        maintenance_annual_frequency=hp.maintenance_annual_frequency,
        interest_rate=hp.interest_rate if hp.is_financed else None,
        loan_term=hp.loan_term if hp.is_financed else None,
    )


def build_gas_boiler_for_year(
    inputs: AppInputs, installation_year: int
) -> HeatingSystem:
    """Build the gas boiler HeatingSystem for a given installation year."""
    gb = inputs.gas_boiler
    return HeatingSystem(
        system_type="gas_boiler",
        installation_year=installation_year,
        lifespan=gb.lifespan,
        efficiency=gb.efficiency,
        installation_cost_trajectory=build_boiler_installation_costs(inputs),
        subsidy_trajectory=build_gas_boiler_subsidies(),
        maintenance_cost_per_visit=gb.maintenance_cost_per_visit,
        maintenance_annual_frequency=gb.maintenance_annual_frequency,
    )


def build_systems_for_year(
    inputs: AppInputs, installation_year: int
) -> tuple[HeatingSystem, HeatingSystem, HeatingSystem, HeatingSystem]:
    """Build all four HeatingSystem variants for a given installation year.

    Returns (heat_pump, heat_pump_no_subsidy, gas_boiler) for
    results/compute.py to unpack.
    """
    heat_pump = build_heat_pump_for_year(inputs, installation_year)
    heat_pump_no_subsidy = build_heat_pump_no_subsidy_for_year(
        inputs, installation_year
    )
    gas_boiler = build_gas_boiler_for_year(inputs, installation_year)
    return heat_pump, heat_pump_no_subsidy, gas_boiler
