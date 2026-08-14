"""Single source of truth for every default value used both as a dataclass
default and as a Streamlit widget's starting value.

Keeping these in one place means the schema's defaults and the sidebar
widgets' initial values can never silently drift apart.
"""

import streamlit as st
from asf_lifetime_cost_model import config as model_config
from asf_lifetime_cost_model.getters import data_getters

# Time horizon
BASE_YEAR_DEFAULT = 2026
OPERATING_START_YEAR = model_config["operating_start_year"]
OPERATING_END_YEAR = model_config["operating_end_year"]
INSTALL_START_YEAR = model_config["install_start_year"]
INSTALL_END_YEAR = model_config["install_end_year"]

# Discounting and inflation
DISCOUNT_RATE_DEFAULT = model_config["default_discount_rate"]
INFLATION_RATE_DEFAULT = model_config["default_inflation_rate"]

# 'Typical' household parameters
PROPERTY_DESCRIPTION = "3-4 bed house fitting an 8-10 kW air-to-water heat pump"
ASHP_SPACE_HEAT_DEMAND = 13_690  # kWh/year
ASHP_DOMESTIC_HOT_WATER_HEAT_DEMAND = 3_150  # kWh/year
ASHP_TOTAL_HEAT_DEMAND_DEFAULT = (
    ASHP_SPACE_HEAT_DEMAND + ASHP_DOMESTIC_HOT_WATER_HEAT_DEMAND
)

ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT = 0  # %
ASHP_HEAT_DEMAND_UPLIFT_PCT_MIN = 0
ASHP_HEAT_DEMAND_UPLIFT_PCT_MAX = 20

BOILER_HEAT_DEMAND_MIN = 5_000
BOILER_HEAT_DEMAND_MAX = 20_000
BOILER_HEAT_DEMAND_DEFAULT = round(
    ASHP_TOTAL_HEAT_DEMAND_DEFAULT / (1 + (ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT / 100))
)


# Energy prices
@st.cache_data(ttl=3600)
def get_gas_price_default() -> float:
    """Latest gas price cap rate (p/kWh), fetched live. Cached for 1 hour."""
    return data_getters.get_latest_price_cap_rate("gas")


@st.cache_data(ttl=3600)
def get_electricity_price_default() -> float:
    """Latest electricity price cap rate (p/kWh), fetched live. Cached for 1 hour."""
    return data_getters.get_latest_price_cap_rate("electricity")


@st.cache_data(ttl=3600)
def get_latest_gas_standing_charge() -> float:
    """Latest gas standing charge (p/day), fetched live. Cached for 1 hour."""
    return data_getters.get_latest_price_cap_standing_charge(fuel="gas")


# Heat pump
ASHP_LIFESPAN_DEFAULT = 15  # years
ASHP_LIFESPAN_MIN = 15
ASHP_LIFESPAN_MAX = 20

ASHP_SCOP_DEFAULT = 3.0  # heat output / energy in
ASHP_SCOP_MIN = 2.5
ASHP_SCOP_MAX = 5.0

ASHP_TOU_DISCOUNT_DEFAULT = 0.15
ASHP_TOU_DISCOUNT_MIN = 0.0
ASHP_TOU_DISCOUNT_MAX = 0.50

ASHP_INSTALLATION_COST_DEFAULT = 12_309.0  # £
ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT = -0.025
ASHP_INSTALLATION_COST_GROWTH_RATE_MIN = -0.20
ASHP_INSTALLATION_COST_GROWTH_RATE_MAX = 0.10

ASHP_SUBSIDY_SCENARIO_DEFAULT = "Flat"

ASHP_INTEREST_RATE_DEFAULT = 0.05
ASHP_INTEREST_RATE_MIN = 0.0
ASHP_INTEREST_RATE_MAX = 0.20

ASHP_LOAN_TERM_DEFAULT = 10
ASHP_LOAN_TERM_MIN = 5
ASHP_LOAN_TERM_MAX = 20

ASHP_MAINTENANCE_COST_DEFAULT = 80.0  # £
ASHP_MAINTENANCE_FREQUENCY_DEFAULT = 1.0  # times/year

# Gas boiler
BOILER_LIFESPAN_DEFAULT = 15
BOILER_LIFESPAN_MIN = 15
BOILER_LIFESPAN_MAX = 20

BOILER_INSTALLATION_COST_DEFAULT = 3_000.0

BOILER_EFFICIENCY_DEFAULT = 0.85
BOILER_EFFICIENCY_MIN = 0.70
BOILER_EFFICIENCY_MAX = 1.0

BOILER_MAINTENANCE_COST_DEFAULT = 80.0  # £
BOILER_MAINTENANCE_FREQUENCY_DEFAULT = 1.0  # times/year

BOILER_INCLUDE_STANDING_CHARGE_DEFAULT = True
