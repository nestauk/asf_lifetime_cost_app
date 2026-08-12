"""Structured representation of every user-configurable input in the sidebar."""

from dataclasses import dataclass, field

from config.defaults import (
    ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT,
    ASHP_INSTALLATION_COST_DEFAULT,
    ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT,
    ASHP_INTEREST_RATE_DEFAULT,
    ASHP_LIFESPAN_DEFAULT,
    ASHP_LOAN_TERM_DEFAULT,
    ASHP_MAINTENANCE_COST_DEFAULT,
    ASHP_MAINTENANCE_FREQUENCY_DEFAULT,
    ASHP_SCOP_DEFAULT,
    ASHP_SUBSIDY_SCENARIO_DEFAULT,
    ASHP_TOU_DISCOUNT_DEFAULT,
    BOILER_EFFICIENCY_DEFAULT,
    BOILER_HEAT_DEMAND_DEFAULT,
    BOILER_INCLUDE_STANDING_CHARGE_DEFAULT,
    BOILER_INSTALLATION_COST_DEFAULT,
    BOILER_LIFESPAN_DEFAULT,
    BOILER_MAINTENANCE_COST_DEFAULT,
    BOILER_MAINTENANCE_FREQUENCY_DEFAULT,
    get_electricity_price_default,
    get_gas_price_default,
    get_latest_gas_standing_charge,
)


@dataclass
class HeatPumpInputs:
    """Configured inputs for an air-to-water heat pump."""

    lifespan: int = ASHP_LIFESPAN_DEFAULT
    scop: float = ASHP_SCOP_DEFAULT
    tou_tariff_discount: float = ASHP_TOU_DISCOUNT_DEFAULT

    installation_cost_current: float = ASHP_INSTALLATION_COST_DEFAULT
    installation_cost_growth_mode: str = "annual_pct"
    installation_cost_growth_rate: float = ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT

    subsidy_scenario: str | None = ASHP_SUBSIDY_SCENARIO_DEFAULT
    subsidy_overrides: dict[int, float] = field(default_factory=dict)

    is_financed: bool = False
    interest_rate: float | None = ASHP_INTEREST_RATE_DEFAULT
    loan_term: int | None = ASHP_LOAN_TERM_DEFAULT

    maintenance_cost_per_visit: float = ASHP_MAINTENANCE_COST_DEFAULT
    maintenance_annual_frequency: float = ASHP_MAINTENANCE_FREQUENCY_DEFAULT


@dataclass
class GasBoilerInputs:
    """Configured inputs for a gas boiler."""

    lifespan: int = BOILER_LIFESPAN_DEFAULT
    efficiency: float = BOILER_EFFICIENCY_DEFAULT
    installation_cost: float = BOILER_INSTALLATION_COST_DEFAULT
    maintenance_cost_per_visit: float = BOILER_MAINTENANCE_COST_DEFAULT
    maintenance_annual_frequency: float = BOILER_MAINTENANCE_FREQUENCY_DEFAULT
    include_standing_charge: bool = BOILER_INCLUDE_STANDING_CHARGE_DEFAULT
    standing_charge: float = field(default_factory=get_latest_gas_standing_charge)


@dataclass
class EnergyPriceInputs:
    """Configured inputs for gas and electricity prices."""

    gas_current_price: float = field(default_factory=get_gas_price_default)
    gas_growth_mode: str = "flat"
    gas_growth_rate: float | None = None
    gas_overrides: dict[int, float] = field(default_factory=dict)

    electricity_current_price: float | None = field(
        default_factory=get_electricity_price_default
    )
    electricity_growth_mode: str | None = "flat"
    electricity_growth_rate: float | None = None
    electricity_overrides: dict[int, float] = field(default_factory=dict)


@dataclass
class AppInputs:
    """All inputs collected from the sidebar, in one object.

    Note: no installation_year here. These are year-independent assumptions
    (trajectories, scenarios, rates) — the model-integration/results layer
    is responsible for building a HeatingSystem for each installation year
    in config["install_start_year"]..config["install_end_year"], reusing
    this single AppInputs across all of them.

    Fixed inputs (base_year, inflation_rate, discount_rate, installation
    year range) also aren't included, since they're never user-configurable.
    """

    boiler_heat_demand: float = BOILER_HEAT_DEMAND_DEFAULT
    heat_pump_heat_demand_uplift: float = ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT
    heat_pump: HeatPumpInputs = field(default_factory=HeatPumpInputs)
    gas_boiler: GasBoilerInputs = field(default_factory=GasBoilerInputs)
    energy_prices: EnergyPriceInputs = field(default_factory=EnergyPriceInputs)
