"""Single source of truth for every default value used both as a dataclass
default and as a Streamlit widget's starting value.

Keeping these in one place means the schema's defaults and the sidebar
widgets' initial values can never silently drift apart.
"""

import streamlit as st
from asf_lifetime_cost_model.getters import data_getters

# ---------------------------------------------------------------------------
# Time horizon (fixed, not user-editable)
# ---------------------------------------------------------------------------
# Note: INSTALL_END_YEAR + max system lifespan must stay <= OPERATING_END_YEAR,
# or price trajectories won't cover a system's full operating life.
OPERATING_START_YEAR = 2026
OPERATING_END_YEAR = 2055  # for max 20 year lifespan heating systems installed in 2035
INSTALL_START_YEAR = 2026
INSTALL_END_YEAR = 2035

# ---------------------------------------------------------------------------
# Discounting and inflation (fixed, not user-editable)
# ---------------------------------------------------------------------------
BASE_YEAR_DEFAULT = 2026  # The reference year every result is expressed in real terms
# relative to. All figures throughout are shown as present value in this
# year's £ — inflation-adjusted and discounted to what they're worth today

DISCOUNT_RATE_DEFAULT = 0.035  # fraction where 0.035 is 3.5%
INFLATION_RATE_DEFAULT = 0.02  # fraction where 0.02 is 2%

# ---------------------------------------------------------------------------
# Default household heat demand
# ---------------------------------------------------------------------------
PROPERTY_DESCRIPTION = "average home fitting an 8-10 kW air-to-water heat pump"

# Heat pump demand
# median heat demand for homes fitting an 8-10 kW A2W heat pump in FY 2025/26
# Source: analysis of MCS data `raw_historical_mcs_installations_20260705.csv`
# TODO: Link to final analysis notebook in asf_lifetime_cost_model
ASHP_SPACE_HEAT_DEMAND = 13_668  # kWh/year
ASHP_DOMESTIC_HOT_WATER_HEAT_DEMAND = 3_155  # kWh/year
ASHP_TOTAL_HEAT_DEMAND_DEFAULT = (
    ASHP_SPACE_HEAT_DEMAND + ASHP_DOMESTIC_HOT_WATER_HEAT_DEMAND
)

# Extra heat demand with a heat pump compared to heating with a gas boiler
ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT = 0  # %
ASHP_HEAT_DEMAND_UPLIFT_PCT_MIN = 0  # %
ASHP_HEAT_DEMAND_UPLIFT_PCT_MAX = 20  # %

# Annual heat demand of a household with a gas boiler, before switching to
# a heat pump
BOILER_HEAT_DEMAND_MIN = 100  # kWh/year
BOILER_HEAT_DEMAND_MAX = 20_000  # kWh/year
BOILER_HEAT_DEMAND_DEFAULT = round(
    ASHP_TOTAL_HEAT_DEMAND_DEFAULT / (1 + (ASHP_HEAT_DEMAND_UPLIFT_PCT_DEFAULT / 100))
)  # kWh/year, Derived by dividing the heat pump demand (MCS-sourced) by
# (1 + uplift), since MCS data reflects heat pump demand directly, not the
# gas boiler baseline. At the default 0% uplift this equals
# ASHP_TOTAL_HEAT_DEMAND_DEFAULT.


# ---------------------------------------------------------------------------
# Latest published energy prices (Ofgem price cap)
# ---------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def get_gas_price_default() -> float:
    """Latest gas price cap rate (p/kWh), fetched live. Cached for 1 hour so
    the app doesn't re-fetch on every rerun, while still picking up updates
    within the hour.
    """
    return data_getters.get_latest_price_cap_rate("gas")


@st.cache_data(ttl=3600)
def get_electricity_price_default() -> float:
    """Latest electricity price cap rate (p/kWh), fetched live. Cached for 1
    hour so the app doesn't re-fetch on every rerun, while still picking up
    updates within the hour.
    """
    return data_getters.get_latest_price_cap_rate("electricity")


@st.cache_data(ttl=3600)
def get_latest_gas_standing_charge() -> float:
    """Latest gas standing charge (p/day), fetched live. Cached for 1 hour
    so the app doesn't re-fetch on every rerun, while still picking up
    updates within the hour.
    """
    return data_getters.get_latest_price_cap_standing_charge(fuel="gas")


# ---------------------------------------------------------------------------
# Heat pump (ASHP)
# ---------------------------------------------------------------------------
ASHP_LIFESPAN_DEFAULT = 15  # years
ASHP_LIFESPAN_MIN = 15
ASHP_LIFESPAN_MAX = 20

# Efficiency (heat output / energy in)
ASHP_SCOP_DEFAULT = 3.0
ASHP_SCOP_MIN = 2.5
ASHP_SCOP_MAX = 5.0

# Assumed discount on electricity unit rate if on a time-of-use tariff
# (fraction, where 0.10 is a 10% discount; 0 means the same rate as the
# price cap)
ASHP_TOU_DISCOUNT_DEFAULT = 0.0
ASHP_TOU_DISCOUNT_MIN = 0.0
ASHP_TOU_DISCOUNT_MAX = 0.50

# Median installation cost for homes fitting an 8-10 kW A2W heat pump in FY 2025/26
# Source: analysis of MCS data `raw_historical_mcs_installations_20260705.csv`
# TODO: Link to final analysis notebook in asf_lifetime_cost_model
ASHP_INSTALLATION_COST_DEFAULT = 12_500  # £

# Rate of change of installation cost in future years
# (fraction, where -0.025 is -2.5% per year)
ASHP_INSTALLATION_COST_GROWTH_RATE_DEFAULT = -0.025
ASHP_INSTALLATION_COST_GROWTH_RATE_MIN = -0.20
ASHP_INSTALLATION_COST_GROWTH_RATE_MAX = 0.10

# Assumed future BUS subsidy scenario
# Valid strings are outputs of
# model_integration.trajectories.get_subsidy_scenario_options()
ASHP_SUBSIDY_SCENARIO_DEFAULT = "Flat"

# Interest rate on ASHP loan (fraction, where 0.05 is 5%)
ASHP_INTEREST_RATE_DEFAULT = 0.05
ASHP_INTEREST_RATE_MIN = 0.0
ASHP_INTEREST_RATE_MAX = 0.20

# Loan repayment term on ASHP loan
ASHP_LOAN_TERM_DEFAULT = 10  # years
ASHP_LOAN_TERM_MIN = 5
ASHP_LOAN_TERM_MAX = 20

# Cost of maintenance / servicing
ASHP_MAINTENANCE_COST_DEFAULT = 80  # £
ASHP_MAINTENANCE_FREQUENCY_DEFAULT = 1.0  # times/year

# ---------------------------------------------------------------------------
# Gas boiler
# ---------------------------------------------------------------------------
BOILER_LIFESPAN_DEFAULT = 15  # years
BOILER_LIFESPAN_MIN = 15
BOILER_LIFESPAN_MAX = 20

BOILER_INSTALLATION_COST_DEFAULT = 3_000  # £

BOILER_EFFICIENCY_DEFAULT = 0.85  # fraction where 0.85 is 85%
BOILER_EFFICIENCY_MIN = 0.70
BOILER_EFFICIENCY_MAX = 1.0

# Cost of maintenance / servicing
BOILER_MAINTENANCE_COST_DEFAULT = 80  # £
BOILER_MAINTENANCE_FREQUENCY_DEFAULT = 1.0  # times/year

# Whether gas standing charge should be included in gas boiler running costs
BOILER_INCLUDE_STANDING_CHARGE_DEFAULT = False
