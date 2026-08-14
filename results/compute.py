"""Build tidy comparison DataFrames from AppInputs, across every installation year.

Calls HeatingSystem's own calculation methods (calculate_discounted_lifetime_cost,
calculate_annualised_discounted_lifetime_cost, etc.) — no calculation logic lives
here, only the looping/tabulation that turns HeatingSystem method calls into a
tidy pandas DataFrame.
"""

import pandas as pd

from config.defaults import (
    DISCOUNT_RATE_DEFAULT,
    INSTALL_END_YEAR,
    INSTALL_START_YEAR,
)
from model_integration.schema import AppInputs
from model_integration.systems import build_systems_for_year
from model_integration.trajectories import (
    build_ashp_electricity_prices,
    build_gas_prices,
)

INSTALLATION_YEARS = range(INSTALL_START_YEAR, INSTALL_END_YEAR + 1)


def _heat_demands(inputs: AppInputs) -> tuple[float, float]:
    """Return (ashp_heat_demand, boiler_heat_demand), both in kWh/year.

    boiler_heat_demand is the user-editable baseline (property heat need).
    ashp_heat_demand is derived by applying the uplift on top.
    """
    boiler_heat_demand = inputs.boiler_heat_demand
    ashp_heat_demand = boiler_heat_demand * (1 + inputs.heat_pump_heat_demand_uplift)
    return ashp_heat_demand, boiler_heat_demand


def build_comparison_rows(inputs: AppInputs, installation_year: int) -> list[dict]:
    """Build tidy rows for one installation year: one row per (system, metric)."""
    heat_pump, heat_pump_no_subsidy, gas_boiler = build_systems_for_year(
        inputs, installation_year
    )

    ashp_heat_demand, boiler_heat_demand = _heat_demands(inputs)
    ashp_electricity_prices = build_ashp_electricity_prices(inputs)
    gas_prices = build_gas_prices(inputs)
    gas_standing_charge = (
        inputs.gas_boiler.standing_charge
        if inputs.gas_boiler.include_standing_charge
        else 0.0
    )

    systems = {
        "Heat pump": (heat_pump, ashp_heat_demand, ashp_electricity_prices, {}),
        "Heat pump (no subsidy)": (
            heat_pump_no_subsidy,
            ashp_heat_demand,
            ashp_electricity_prices,
            {},
        ),
        "Gas boiler": (
            gas_boiler,
            boiler_heat_demand,
            gas_prices,
            {"standing_charge": gas_standing_charge},
        ),
    }

    rows = []
    for system_name, (
        system,
        heat_demand,
        energy_price_trajectory,
        extra_kwargs,
    ) in systems.items():
        metrics = {
            "Lifespan": system.lifespan,
            "Efficiency": system.efficiency,
            "Heat demand (kWh/year)": heat_demand,
            "Interest rate": system.interest_rate,
            "Loan term": system.loan_term,
            "Discounted capital cost (principal only)": system.calculate_discounted_lifetime_capital_cost(
                discount_rate=DISCOUNT_RATE_DEFAULT
            )
            - (
                system.calculate_discounted_lifetime_loan_interest(
                    discount_rate=DISCOUNT_RATE_DEFAULT
                )
                if system.is_financed
                else 0.0
            ),
            "Discounted lifetime loan interest": (
                system.calculate_discounted_lifetime_loan_interest(
                    discount_rate=DISCOUNT_RATE_DEFAULT
                )
                if system.is_financed
                else 0.0
            ),
            "Discounted capital cost (total, incl. interest)": system.calculate_discounted_lifetime_capital_cost(
                discount_rate=DISCOUNT_RATE_DEFAULT
            ),
            "Discounted lifetime maintenance cost": system.calculate_discounted_lifetime_maintenance_cost(
                discount_rate=DISCOUNT_RATE_DEFAULT
            ),
            "Discounted lifetime running cost": system.calculate_discounted_lifetime_running_cost(
                heat_demand=heat_demand,
                energy_price_trajectory=energy_price_trajectory,
                discount_rate=DISCOUNT_RATE_DEFAULT,
                **extra_kwargs,
            ),
            "Total discounted lifetime cost": system.calculate_discounted_lifetime_cost(
                heat_demand=heat_demand,
                energy_price_trajectory=energy_price_trajectory,
                discount_rate=DISCOUNT_RATE_DEFAULT,
                **extra_kwargs,
            ),
            "Equivalent Annual Cost: capital cost (principal only)": system.calculate_annualised_discounted_lifetime_capital_cost(
                discount_rate=DISCOUNT_RATE_DEFAULT
            )
            - (
                system.calculate_annualised_discounted_lifetime_loan_interest(
                    discount_rate=DISCOUNT_RATE_DEFAULT
                )
                if system.is_financed
                else 0.0
            ),
            "Equivalent Annual Cost: loan interest": (
                system.calculate_annualised_discounted_lifetime_loan_interest(
                    discount_rate=DISCOUNT_RATE_DEFAULT
                )
                if system.is_financed
                else 0.0
            ),
            "Equivalent Annual Cost: capital cost (total, incl. interest)": system.calculate_annualised_discounted_lifetime_capital_cost(
                discount_rate=DISCOUNT_RATE_DEFAULT
            ),
            "Equivalent Annual Cost: maintenance cost": system.calculate_annualised_discounted_lifetime_maintenance_cost(
                discount_rate=DISCOUNT_RATE_DEFAULT
            ),
            "Equivalent Annual Cost: running cost": system.calculate_annualised_discounted_lifetime_running_cost(
                heat_demand=heat_demand,
                energy_price_trajectory=energy_price_trajectory,
                discount_rate=DISCOUNT_RATE_DEFAULT,
                **extra_kwargs,
            ),
            "Annualised discounted lifetime cost (Equivalent Annual Cost)": system.calculate_annualised_discounted_lifetime_cost(
                heat_demand=heat_demand,
                energy_price_trajectory=energy_price_trajectory,
                discount_rate=DISCOUNT_RATE_DEFAULT,
                **extra_kwargs,
            ),
        }
        for metric_name, value in metrics.items():
            rows.append(
                {
                    "installation_year": installation_year,
                    "system": system_name,
                    "metric": metric_name,
                    "value": value,
                }
            )

    return rows


def build_comparison_df(inputs: AppInputs) -> pd.DataFrame:
    """Build the full comparison DataFrame across every installation year."""
    all_rows = [
        row
        for installation_year in INSTALLATION_YEARS
        for row in build_comparison_rows(inputs, installation_year)
    ]
    return pd.DataFrame(all_rows)


def build_annual_breakdown_rows(
    inputs: AppInputs, installation_year: int
) -> list[dict]:
    """Build tidy rows for one installation year: one row per (operating_year, system, metric)."""
    heat_pump, heat_pump_no_subsidy, gas_boiler = build_systems_for_year(
        inputs, installation_year
    )

    ashp_heat_demand, boiler_heat_demand = _heat_demands(inputs)
    ashp_electricity_prices = build_ashp_electricity_prices(inputs)
    gas_prices = build_gas_prices(inputs)
    gas_standing_charge = (
        inputs.gas_boiler.standing_charge
        if inputs.gas_boiler.include_standing_charge
        else 0.0
    )

    systems = {
        "Heat pump": (heat_pump, ashp_heat_demand, ashp_electricity_prices, {}),
        "Heat pump (no subsidy)": (
            heat_pump_no_subsidy,
            ashp_heat_demand,
            ashp_electricity_prices,
            {},
        ),
        "Gas boiler": (
            gas_boiler,
            boiler_heat_demand,
            gas_prices,
            {"standing_charge": gas_standing_charge},
        ),
    }

    rows = []
    for system_name, (
        system,
        heat_demand,
        energy_price_trajectory,
        extra_kwargs,
    ) in systems.items():
        operating_years = set(system.operating_years)

        if system.is_financed:
            loan_start_year = system.installation_year + 1
            loan_end_year = system.installation_year + system.loan_term
            loan_repayment_years = set(range(loan_start_year, loan_end_year + 1))
        else:
            loan_repayment_years = set()

        years_to_report = sorted(operating_years | loan_repayment_years)

        for operating_year in years_to_report:
            is_operating_this_year = operating_year in operating_years

            if is_operating_this_year:
                discounted_running_cost = system.calculate_discounted_running_cost(
                    year=operating_year,
                    heat_demand=heat_demand,
                    energy_price_trajectory=energy_price_trajectory,
                    discount_rate=DISCOUNT_RATE_DEFAULT,
                    **extra_kwargs,
                )
                discounted_maintenance_cost = (
                    system.calculate_discounted_maintenance_cost(
                        year=operating_year, discount_rate=DISCOUNT_RATE_DEFAULT
                    )
                )
                # Undiscounted (real-terms) equivalents — what the household actually pays that year
                running_cost = system.calculate_running_cost(
                    year=operating_year,
                    heat_demand=heat_demand,
                    energy_price_trajectory=energy_price_trajectory,
                    **extra_kwargs,
                )
                maintenance_cost = system.calculate_maintenance_cost_for_year(
                    year=operating_year
                )
            else:
                discounted_running_cost = 0.0
                discounted_maintenance_cost = 0.0
                running_cost = 0.0
                maintenance_cost = 0.0

            if system.is_financed:
                loan_start_year = system.installation_year + 1
                loan_end_year = system.installation_year + system.loan_term
                if loan_start_year <= operating_year <= loan_end_year:
                    discounted_capital_cost = (
                        system.calculate_discounted_loan_repayment(
                            year=operating_year, discount_rate=DISCOUNT_RATE_DEFAULT
                        )
                    )
                    capital_cost = system.calculate_annual_loan_repayment()
                else:
                    discounted_capital_cost = 0.0
                    capital_cost = 0.0
            else:
                if operating_year == installation_year:
                    discounted_capital_cost = (
                        system.calculate_discounted_lifetime_capital_cost(
                            discount_rate=DISCOUNT_RATE_DEFAULT
                        )
                    )
                    capital_cost = system.capital_cost
                else:
                    discounted_capital_cost = 0.0
                    capital_cost = 0.0

            metrics = {
                "Discounted running cost": discounted_running_cost,
                "Discounted maintenance cost": discounted_maintenance_cost,
                "Discounted capital cost": discounted_capital_cost,
                "Discounted annual cost of ownership": (
                    discounted_running_cost
                    + discounted_maintenance_cost
                    + discounted_capital_cost
                ),
                "Running cost": running_cost,
                "Maintenance cost": maintenance_cost,
                "Capital cost": capital_cost,
                "Annual cost": running_cost + maintenance_cost + capital_cost,
                "System operating this year": is_operating_this_year,
            }
            for metric_name, value in metrics.items():
                rows.append(
                    {
                        "installation_year": installation_year,
                        "operating_year": operating_year,
                        "system": system_name,
                        "metric": metric_name,
                        "value": value,
                    }
                )

    return rows


def build_annual_breakdown_df(inputs: AppInputs) -> pd.DataFrame:
    """Build the full annual breakdown DataFrame across every installation year."""
    all_rows = [
        row
        for installation_year in INSTALLATION_YEARS
        for row in build_annual_breakdown_rows(inputs, installation_year)
    ]
    return pd.DataFrame(all_rows)


def build_required_subsidy_df(inputs: AppInputs) -> pd.DataFrame:
    """Solve for the subsidy the heat pump would need, for parity with the gas
    boiler, for every installation year.
    """
    rows = []

    for installation_year in INSTALLATION_YEARS:
        heat_pump, heat_pump_no_subsidy, gas_boiler = build_systems_for_year(
            inputs, installation_year
        )

        ashp_heat_demand, boiler_heat_demand = _heat_demands(inputs)
        ashp_electricity_prices = build_ashp_electricity_prices(inputs)
        gas_prices = build_gas_prices(inputs)
        gas_standing_charge = (
            inputs.gas_boiler.standing_charge
            if inputs.gas_boiler.include_standing_charge
            else 0.0
        )

        gas_boiler_eac = gas_boiler.calculate_annualised_discounted_lifetime_cost(
            heat_demand=boiler_heat_demand,
            energy_price_trajectory=gas_prices,
            standing_charge=gas_standing_charge,
            discount_rate=DISCOUNT_RATE_DEFAULT,
        )

        heat_pump_no_subsidy_eac = (
            heat_pump_no_subsidy.calculate_annualised_discounted_lifetime_cost(
                heat_demand=ashp_heat_demand,
                energy_price_trajectory=ashp_electricity_prices,
                discount_rate=DISCOUNT_RATE_DEFAULT,
            )
        )

        required_subsidy = heat_pump.solve_subsidy_for_parity(
            heat_demand=ashp_heat_demand,
            energy_price_trajectory=ashp_electricity_prices,
            target_eac=gas_boiler_eac,
            discount_rate=DISCOUNT_RATE_DEFAULT,
        )

        rows.append(
            {
                "installation_year": installation_year,
                "gas_boiler_eac": gas_boiler_eac,
                "heat_pump_no_subsidy_eac": heat_pump_no_subsidy_eac,
                "required_subsidy": required_subsidy,
                "installation_cost": heat_pump.installation_cost,
            }
        )

    return pd.DataFrame(rows)


def build_required_electricity_prices(
    inputs: AppInputs, installation_year: int
) -> dict[int, float]:
    """Solve for the electricity price cap rate (p/kWh, one value per operating
    year, before the time-of-use discount) the heat pump installed in this
    year would need for the household to reach parity with a gas boiler.

    Solves using the ToU-discounted trajectory, since that's what actually
    determines the heat pump's running cost — then converts the result back
    to the headline price cap rate for reporting.
    """
    heat_pump, _, gas_boiler = build_systems_for_year(inputs, installation_year)

    ashp_heat_demand, boiler_heat_demand = _heat_demands(inputs)
    gas_prices = build_gas_prices(inputs)
    gas_standing_charge = (
        inputs.gas_boiler.standing_charge
        if inputs.gas_boiler.include_standing_charge
        else 0.0
    )

    gas_boiler_eac = gas_boiler.calculate_annualised_discounted_lifetime_cost(
        heat_demand=boiler_heat_demand,
        energy_price_trajectory=gas_prices,
        standing_charge=gas_standing_charge,
        discount_rate=DISCOUNT_RATE_DEFAULT,
    )

    # Solve using the ToU-discounted trajectory
    # what actually determines the heat pump's running cost
    ashp_electricity_prices = build_ashp_electricity_prices(inputs)

    required_effective_electricity_prices = (
        heat_pump.solve_electricity_price_for_parity(
            heat_demand=ashp_heat_demand,
            energy_price_trajectory=ashp_electricity_prices,
            target_eac=gas_boiler_eac,
            discount_rate=DISCOUNT_RATE_DEFAULT,
        )
    )

    # Convert solved effective (ToU-discounted) prices back to the headline
    # price cap rate for reporting
    tou_tariff_discount = inputs.heat_pump.tou_tariff_discount
    required_price_cap_rates = {
        year: effective_price / (1 - tou_tariff_discount)
        for year, effective_price in required_effective_electricity_prices.items()
    }

    return required_price_cap_rates


def build_required_price_ratio(
    required_price_cap_rates: dict[int, float], gas_prices_by_year: dict[int, float]
) -> dict[int, float]:
    """Ratio of required electricity price to actual gas price, per year — the
    'target elec-gas price ratio' a household would need for parity.
    """
    return {
        year: required_price_cap_rates[year] / gas_prices_by_year[year]
        for year in required_price_cap_rates
    }


def build_required_electricity_price_summary_df(
    inputs: AppInputs, installation_year: int
) -> pd.DataFrame:
    """One row per operating year of the heat pump's lifetime (for the chosen
    installation year): gas boiler EAC, heat pump EAC at today's electricity
    price, the required rate for parity that year, and the implied ratio to
    gas that year.
    """
    gas_prices = build_gas_prices(inputs)

    heat_pump, _, gas_boiler = build_systems_for_year(inputs, installation_year)
    ashp_heat_demand, boiler_heat_demand = _heat_demands(inputs)
    gas_standing_charge = (
        inputs.gas_boiler.standing_charge
        if inputs.gas_boiler.include_standing_charge
        else 0.0
    )

    gas_boiler_eac = gas_boiler.calculate_annualised_discounted_lifetime_cost(
        heat_demand=boiler_heat_demand,
        energy_price_trajectory=gas_prices,
        standing_charge=gas_standing_charge,
        discount_rate=DISCOUNT_RATE_DEFAULT,
    )

    ashp_electricity_prices = build_ashp_electricity_prices(inputs)
    heat_pump_eac_today = heat_pump.calculate_annualised_discounted_lifetime_cost(
        heat_demand=ashp_heat_demand,
        energy_price_trajectory=ashp_electricity_prices,
        discount_rate=DISCOUNT_RATE_DEFAULT,
    )

    required_effective_prices = heat_pump.solve_electricity_price_for_parity(
        heat_demand=ashp_heat_demand,
        energy_price_trajectory=ashp_electricity_prices,
        target_eac=gas_boiler_eac,
        discount_rate=DISCOUNT_RATE_DEFAULT,
    )

    tou_tariff_discount = inputs.heat_pump.tou_tariff_discount

    rows = []
    for operating_year in sorted(required_effective_prices.keys()):
        required_rate = required_effective_prices[operating_year] / (
            1 - tou_tariff_discount
        )
        gas_price_that_year = gas_prices.get_price(year=operating_year)
        implied_ratio = (
            required_rate / gas_price_that_year if required_rate > 0 else None
        )

        rows.append(
            {
                "installation_year": installation_year,
                "operating_year": operating_year,
                "gas_boiler_eac": gas_boiler_eac,
                "heat_pump_eac_today": heat_pump_eac_today,
                "gas_price": gas_price_that_year,
                "required_rate": required_rate,
                "implied_ratio": implied_ratio,
            }
        )

    return pd.DataFrame(rows)
