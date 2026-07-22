# List of possible arguments and default values for a variety of parameters
# that enable the calculation of lifetime costs for different heating systems

ashp_efficiency_options = [
    "reference",  # SCOP 3
    "high",  # SCOP > 3
    "low",  # SCOP < 3
]

boiler_efficiency_default = 0.85  # boiler efficiency

life_span_default = {"ashp": 15, "boiler": 15}  # in years  # years  # years

maintenance_costs_default = {"ashp": 80, "boiler": 80}  # GBP  # GBP

ashp_subsidy_options = [
    "flat",
    "slow stepdown",
    "fast stepdown",
    "high",
    "zero from 2028",
    "smallest",
    "no subsidy",
    "custom subsidy model",  # for custom subsidy input
]

ashp_annual_cost_decrease_range = [
    -0.01,
    0.05,
]  # range for annual cost decrease for ASHPs -1% to +5%

ashp_annual_cost_decrease_default = 0.01  # 1% annual cost decrease for ASHPs

loan_interest_rate_options = {
    "0%: fully subsidised loan": 0,
    "5%: government borrowing or morgage": 0.05,
    "10%: personal finance": 0.1
}
loan_interest_rate_default_option = "5%: government borrowing or mortgage"

wholesale_price_projection_options = [
    "reference",  # DESNZ_Ref
    "low fossil fuel prices",  # DESNZ_Low
    "high fossil fuel prices",  # DESNZ_High
]

levy_rebalancing_options = [
    "no rebalancing (current price cap)",
    "rebalance unit costs between electricity and gas",
    "remove all electricity levies to taxation",
]

cost_data_reference_year = 2023  # reference year for ashp cost data
cost_year_max = 2035
