"""
Scenario selection page.
"""

## Package imports
import streamlit as st
import altair as alt
import pandas as pd


# Local imports
from config.fonts_setup import nestafont, NESTA_COLOURS
from config.scenarios import scenarios
from config import config
from asf_lifetime_cost_model.pipeline.lifetime_cost_calculator import (
    LifetimeCostCalculator,
)

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")


def scenario_selection_page():
    """
    This function sets up the 'Scenario selection' page of the app.
    """

    st.markdown("# Lifetime costs: scenario selection")

    st.markdown("### Select a predefined scenario or build your own")
    st.write(
        """
             If you select a predefined scenario, the parameters will be set automatically. If you choose to build a custom scenario, start by naming it.
             Below you can also select the installation year and cost decile for your results. When you build a custom scenario, you can then define other the parameters in more detail.
             """
    )
    scenario_names = [scenarios[key]["name"] for key in scenarios.keys()]
    scenario_names = scenario_names + ["Build a custom scenario"]

    scenario_select_col, new_scenario_name_col = st.columns(2)

    with scenario_select_col:
        selected_scenario = st.selectbox(
            label="Select a scenario",
            options=scenario_names,
            index=0,
            key="selected_scenario",
        )

    with st.expander("📅 Expand to select installation year and cost decile"):
        installation_year_col, decile_col = st.columns(2)

        with installation_year_col:
            installation_year = st.slider(
                label="Select the installation year",
                min_value=2025,
                max_value=2035,
                value=2025,
                step=1,
                key="custom_installation_year_input",
                help="The year the heating system is installed",
            )

        with decile_col:
            cost_decile = st.selectbox(
                label="Select the cost decile (50 corresponds to the median)",
                options=range(10, 100, 10),
                index=4,
                key="income_decile_input",
                help="Select the cost decile, where 50 corresponds to the median.",
            )

    if selected_scenario == "Build a custom scenario":
        with new_scenario_name_col:
            scenario_name = st.text_input(
                label="Name your custom scenario",
                value="<My custom scenario>",
                key="custom_scenario_name_input",
            )

        if scenario_name != "":
            with st.expander("⚙️ Define your custom scenario parameters"):

                st.write(
                    "Expand the sections below to define your custom scenario parameters."
                )

                with st.expander("🗓️ Life span"):
                    ashp_lifetime_col, boiler_lifetime_col = st.columns(2)

                    with ashp_lifetime_col:
                        ashp_life_span = st.slider(
                            label="ASHP life span (years)",
                            min_value=1,
                            max_value=25,
                            value=config.life_span_default["ashp"],
                            step=1,
                            key="custom_ashp_life_span_input",
                            help="Number of years air source heat pump is assumed to be operational",
                        )
                    with boiler_lifetime_col:
                        boiler_life_span = st.slider(
                            label="Gas boiler life span (years)",
                            min_value=1,
                            max_value=25,
                            value=config.life_span_default["boiler"],
                            step=1,
                            key="custom_boiler_life_span_input",
                            help="Number of years gas boiler is assumed to be operational",
                        )

                with st.expander("👨🏻‍🔧 Maintenance costs"):
                    ashp_maintenance_cost_col, boiler_maintenance_cost_col = st.columns(
                        2
                    )

                    with ashp_maintenance_cost_col:
                        ashp_maintenance_cost = st.slider(
                            label="ASHP annual maintenance cost (£)",
                            min_value=0,
                            max_value=350,
                            value=config.maintenance_costs_default["ashp"],
                            step=5,
                            key="custom_ashp_maintenance_cost_input",
                            help="Annual maintenance cost for the ASHP",
                        )
                        ashp_maintenance_frequency = st.slider(
                            label="ASHP frequency of maintenance per year",
                            min_value=0.0,
                            max_value=4.0,
                            value=1.0,
                            step=0.2,
                            key="custom_ashp_maintenance_frequency_input",
                            help="Average number of times that ASHP is assumed to be serviced per year. Values less than 1 are possible, i.e. 0.5 means every two years.",
                        )
                    with boiler_maintenance_cost_col:
                        boiler_maintenance_cost = st.slider(
                            label="Boiler annual maintenance cost (£)",
                            min_value=0,
                            max_value=350,
                            value=config.maintenance_costs_default["boiler"],
                            step=5,
                            key="custom_boiler_maintenance_cost_input",
                            help="Annual maintenance cost for the gas boiler",
                        )
                        boiler_maintenance_frequency = st.slider(
                            label="Boiler frequency of maintenance per year",
                            min_value=0.0,
                            max_value=4.0,
                            value=1.0,
                            step=0.2,
                            key="custom_boiler_maintenance_frequency_input",
                            help="Average number of times that gas boiler is assumed to be serviced per year. Values less than 1 are possible, i.e. 0.5 means every two years.",
                        )

                with st.expander("📈 Effiency measures"):
                    ashp_efficiency_col, boiler_efficiency_col = st.columns(2)

                    with ashp_efficiency_col:
                        ashp_efficiency = st.slider(
                            label="ASHP efficiency",
                            min_value=1.0,
                            max_value=5.0,
                            value=3.0,
                            step=0.1,
                            key="custom_ashp_efficiency_input",
                            help="Efficiency of the air source heat pump",
                        )
                    with boiler_efficiency_col:
                        boiler_efficiency = st.slider(
                            label="Boiler efficiency",
                            min_value=0.7,
                            max_value=0.95,
                            value=0.85,
                            step=0.01,
                            key="custom_boiler_efficiency_input",
                            help="Efficiency of the gas boiler",
                        )
                with st.expander("🤝 Loan and interest rate"):
                    ashp_purchased_with_loan_flag_col, ashp_loan_interes_rate_col = (
                        st.columns(2)
                    )

                    with ashp_purchased_with_loan_flag_col:
                        ashp_purchased_with_loan = st.selectbox(
                            label="Is the ASHP purchased with a loan?",
                            options=["Yes", "No"],
                            index=0,
                            key="custom_ashp_loan_input",
                            help="Whether the ASHP is purchased with a loan",
                        )
                        if ashp_purchased_with_loan == "Yes":
                            with ashp_loan_interes_rate_col:
                                ashp_loan_interes_rate = st.selectbox(
                                    label="ASHP loan interest rate",
                                    options=[
                                        option
                                        for option in config.loan_interest_rate_options.keys()
                                    ],
                                    index=1,
                                    key="custom_ashp_loan_interest_rate_input",
                                    help="The interest rate of the ASHP loan",
                                )
                    st.markdown(
                        "Note: Loan repayment period is assumed to be over the ASHP's lifetime."
                    )
                with st.expander("💰 Subsidy"):
                    col1, ashp_subsidy_col, col2 = st.columns([1, 4, 1])

                    with ashp_subsidy_col:
                        # --- Main selectbox (always visible) ---
                        ashp_subsidy_model = st.selectbox(
                            label="Choose an ASHP subsidy model - visit the 'About the app' page for more details",
                            options=[opt for opt in config.ashp_subsidy_options],
                            index=0,
                            key="ashp_subsidy_select",
                            help="Choose an ASHP subsidy model",
                        )

                        if ashp_subsidy_model == "custom subsidy model":
                            st.write(
                                "Edit the subsidy values below (£) for each year by double-clicking on the cell."
                            )
                            column_config = {
                                "Year": st.column_config.NumberColumn(
                                    "Year",
                                    disabled=True,  # make the Year column non-editable
                                ),
                                "Subsidy (£)": st.column_config.NumberColumn(
                                    "Subsidy (£)", min_value=0, max_value=20000
                                ),
                            }

                            subsidies_table = pd.DataFrame(
                                {
                                    "Year": list(
                                        range(
                                            installation_year,
                                            installation_year
                                            + config.life_span_default["ashp"]
                                            + 1,
                                        )
                                    ),
                                    "Subsidy (£)": 7500,
                                }
                            )

                            user_inputted_subsidies = st.data_editor(
                                subsidies_table,
                                use_container_width=True,
                                column_config=column_config,
                                key="custom_ashp_subsidy_input",
                            )
                with st.expander("⚡ Wholesale price projection"):
                    col3, wholesale_price_proj_col, col4 = st.columns([1, 4, 1])

                    with wholesale_price_proj_col:
                        wholesale_price_projection = st.selectbox(
                            label="Wholesale price projection",
                            options=config.wholesale_price_projection_options,
                            index=0,
                            key="custom_wholesale_price_projection_input",
                            help="The wholesale price projection for electricity and gas prices",
                        )
                with st.expander("⚖️ Levy rebalancing options"):
                    levy_rebalancing_col, levies_inputs_col = st.columns(2)

                    with levy_rebalancing_col:
                        levy_rebalancing = st.selectbox(
                            label="Levy rebalancing scenario",
                            options=config.levy_rebalancing_options,
                            index=0,
                            key="custom_levy_rebalancing_input",
                            help="The approach to rebalancing electricity and gas levies",
                        )
                    if (
                        levy_rebalancing
                        == "rebalance unit costs between electricity and gas"
                    ):
                        with levies_inputs_col:
                            variable_electricity_weight = st.slider(
                                label="Rebalance between electricity (0) <-> gas (100)",
                                min_value=0.0,
                                max_value=100.0,
                                value=0.0,
                                step=10.0,
                                key="custom_levy_variable_electricity_weights_input",
                                help="Proportion of the scheme revenue that is levied against electricity units",
                            )
                            st.markdown(
                                "The following levies that are ordinarily levied against electricity units are rebalanced: "
                                "RO, FiT, ECO, AAHEDC, NCC."
                            )
                    if levy_rebalancing == "remove all electricity levies to taxation":
                        st.markdown(
                            "The following levies that are ordinarily levied against electricity (units or customers) are removed to raise revenue through general taxation: "
                            "RO, FiT, ECO (only proportion of revenue raised ordinarily via electricity units), WHD (only proportion of revenue raised ordinarily via electricity customers),"
                            " AAHEDC, NCC"
                        )  # ECO and WHD tricky to explain because they are currently levied on both gas and electricity
    else:  # if a predefined scenario is selected
        scenario_info = scenarios[selected_scenario]
        ashp_life_span = config.life_span_default["ashp"]
        boiler_life_span = config.life_span_default["boiler"]
        ashp_maintenance_cost = config.maintenance_costs_default["ashp"]
        boiler_maintenance_cost = config.maintenance_costs_default["boiler"]
        ashp_maintenance_frequency = 1.0
        boiler_maintenance_frequency = 1.0
        ashp_efficiency = (
            3.0
            if scenario_info["ashp_scop"] == "reference"
            else 3.5 if scenario_info["ashp_scop"] == "high" else 2.5
        )
        boiler_efficiency = config.boiler_efficiency_default
        ashp_purchased_with_loan = (
            "Yes" if scenario_info["purchasing_with_loans"] else "No"
        )
        if ashp_purchased_with_loan == "Yes":
            ashp_loan_interes_rate = scenario_info["loan_interest_rate"]
        else:
            ashp_loan_interes_rate = 0

        ashp_subsidy_model = scenario_info["ashp_subsidy"]

        wholesale_price_projection = scenario_info["wholesale_price_projection"]

        levy_rebalancing = scenario_info["levy_rebalancing"]

        with st.expander("⚙️ Scenario parameter values"):
            st.markdown(
                "Under the selected scenario, the following parameters are set as follows:"
            )

            st.markdown(
                f"""

                        | Parameter | Gas Boiler | ASHP |
                        |-----------|------------|-------|
                        | Life span (years) | {boiler_life_span} |{ashp_life_span} |
                        | Annual maintenance cost (£) | {boiler_maintenance_cost} |{ashp_maintenance_cost} |
                        | Frequency of maintenance per year | {boiler_maintenance_frequency} |{ashp_maintenance_frequency} |
                        | Efficiency | {boiler_efficiency} |{ashp_efficiency} |
                        | Heating system purchased with a loan? | - | {ashp_purchased_with_loan} |
                        | Loan interest rate |  - |{ashp_loan_interes_rate} |
                        | Subsidy model |  - |{ashp_subsidy_model} |

                        Additional parameters for the running cost calculations:

                        | Parameter                  | Value                        |
                        |----------------------------|------------------------------|
                        | Wholesale price projection  | {wholesale_price_projection} |
                        | Levy rebalancing scenario   | {levy_rebalancing}           |

                        """
            )

    name = (
        selected_scenario
        if selected_scenario != "Build a custom scenario"
        else scenario_name
    )
    st.markdown(
        f"### Observe how the lifetime cost of heat pumps compares to gas boilers under the **'{name}'** scenario"
    )
    st.markdown(f"Below you can see the results for the **'{name}'** scenario.")

    cost_calculator = LifetimeCostCalculator()

    col5, filter_archetypes_col, col6 = st.columns([1, 4, 1])
    with filter_archetypes_col:
        filter_archetypes = st.multiselect(
            label="Select or de-select archetypes to filter the results",
            options=cost_calculator.property_archetypes,
            default=cost_calculator.property_archetypes,
            key="filter_archetypes_input",
            help="Filter the results by archetype",
        )

    # Processing inputs before computations
    if ashp_purchased_with_loan == "Yes":
        ashp_purchased_with_loan = True
        ashp_loan_interes_rate = config.loan_interest_rate_options.get(
            ashp_loan_interes_rate
        )
    else:
        ashp_purchased_with_loan = False
        ashp_loan_interes_rate = 0.0

    if levy_rebalancing == "no rebalancing (current price cap)":
        levy_rebalancing = False
        levies_to_rebalance = None
        levies_rebalancing_weights = None
    elif levy_rebalancing == "rebalance unit costs between electricity and gas":
        levy_rebalancing = True
        levies_to_rebalance = ["ro", "fit", "eco", "aahedc", "ncc"]
        levies_rebalancing_weights = {
            "electricity_weight": 0,
            "gas_weight": 1,
            "tax_weight": 0,
            "fixed_electricity_weight": 0,
            "variable_electricity_weight": (
                variable_electricity_weight
                if levy_rebalancing
                == "rebalance unit costs between electricity and gas"
                else 0
            ),
            "fixed_gas_weight": 0,
            "variable_gas_weight": (
                1 - variable_electricity_weight
                if levy_rebalancing
                == "rebalance unit costs between electricity and gas"
                else 1
            ),
        }
    elif levy_rebalancing == "remove all electricity levies to taxation":
        levy_rebalancing = True
        levies_to_rebalance = ["ro", "fit", "eco", "whd", "aahedc", "ncc"]
        levies_rebalancing_weights = {
            "electricity_weight": 0,
            "gas_weight": 1,
            "tax_weight": 0,
            "fixed_electricity_weight": 0,
            "variable_electricity_weight": 0,
            "fixed_gas_weight": 0,
            "variable_gas_weight": 1,
        }
    elif levy_rebalancing == "rebalance RO and FiT from electricity to gas":
        levy_rebalancing = True
        levies_to_rebalance = ["ro", "fit"]
        levies_rebalancing_weights = {
            "electricity_weight": 0,
            "gas_weight": 1,
            "tax_weight": 0,
            "fixed_electricity_weight": 0,
            "variable_electricity_weight": 0,
            "fixed_gas_weight": 0,
            "variable_gas_weight": 1,
        }
    else:
        ValueError("Levy rebalancing option not recognised")

    # ASHP calculation
    ashp_upfront_costs = cost_calculator.compute_upfront_cost(
        heating_system="ashp",
        annual_cost_reduction=0.05,
        purchase_year=installation_year,
        life_span=ashp_life_span,
        decile=cost_decile,
        subsidy_model_or_input_values=(
            ashp_subsidy_model
            if ashp_subsidy_model != "custom subsidy model"
            else user_inputted_subsidies.set_index("Year")["Subsidy (£)"].to_dict()
        ),
        purchase_with_loan=ashp_purchased_with_loan,
        loan_interest_rate=ashp_loan_interes_rate,
    )

    ashp_maintenance_costs = cost_calculator.compute_total_maintenance_cost(
        maintenance_frequency_per_year=ashp_maintenance_frequency,
        maintenance_cost=ashp_maintenance_cost,
        life_span=ashp_life_span,
    )

    ashp_running_costs = cost_calculator.compute_running_cost_time_series(
        purchase_year=installation_year,
        life_span=ashp_life_span,
        heating_system_efficiency=ashp_efficiency,
        fuel_type="electricity",
        wholesale_price_projection_scenario=wholesale_price_projection,
        include_standing_charge=False,  # in phase 1 standing charge is not included in running costs for ASHP
        levy_rebalancing=levy_rebalancing,
        levies_to_rebalance=levies_to_rebalance,
        levy_rebalancing_weights=levies_rebalancing_weights,
        include_vat=True,
    )
    ashp_lifetime_costs = cost_calculator.compute_total_lifetime_costs(
        installation_costs=ashp_upfront_costs,
        maintenance_costs=ashp_maintenance_costs,
        running_costs=ashp_running_costs,
    )

    ashp_annualised_lifetime_costs = cost_calculator.compute_annualised_lifetime_costs(
        total_lifetime_costs=ashp_lifetime_costs,
        cost_column="total_lifetime_costs",
        life_span=ashp_life_span,
    )

    boiler_upfront_costs = cost_calculator.compute_upfront_cost(
        heating_system="boiler",
        annual_cost_reduction=0,
        purchase_year=installation_year,
        life_span=ashp_life_span,
    )
    boiler_maintenance_costs = cost_calculator.compute_total_maintenance_cost(
        maintenance_frequency_per_year=boiler_maintenance_frequency,
        maintenance_cost=boiler_maintenance_cost,
        life_span=boiler_life_span,
    )

    boiler_running_costs = cost_calculator.compute_running_cost_time_series(
        purchase_year=installation_year,
        life_span=boiler_life_span,
        heating_system_efficiency=boiler_efficiency,
        fuel_type="gas",
        wholesale_price_projection_scenario=wholesale_price_projection,
        include_standing_charge=True,  # in phase 1 of the project, we decided that the gas standing charge should only be included in the running costs of a gas boiler
        levy_rebalancing=levy_rebalancing,
        levies_to_rebalance=levies_to_rebalance,
        levy_rebalancing_weights=levies_rebalancing_weights,
        include_vat=True,
    )

    boiler_lifetime_costs = cost_calculator.compute_total_lifetime_costs(
        installation_costs=boiler_upfront_costs,
        maintenance_costs=boiler_maintenance_costs,
        running_costs=boiler_running_costs,
    )

    ashp_lifetime_costs["technology"] = "ASHP"
    boiler_lifetime_costs["technology"] = "Gas boiler"
    ashp_lifetime_costs["annualised_lifetime_cost"] = (
        ashp_lifetime_costs["total_lifetime_costs"] / ashp_life_span
    )
    boiler_lifetime_costs["annualised_lifetime_cost"] = (
        boiler_lifetime_costs["total_lifetime_costs"] / boiler_life_span
    )

    # Merging ASHP and boiler results
    lifetime_costs = pd.concat(
        [ashp_lifetime_costs, boiler_lifetime_costs]
    ).reset_index()

    lifetime_costs_selected_archetypes = lifetime_costs[
        lifetime_costs["archetype_label"].isin(filter_archetypes)
    ]

    lifetime_costs_selected_archetypes["installation_costs_after_subsidy"] = (
        lifetime_costs_selected_archetypes["installation_costs"]
        - lifetime_costs["subsidy_value"]
    )
    lifetime_costs_selected_archetypes.drop(
        columns=["installation_costs", "subsidy_value"], inplace=True
    )

    df_annualised = lifetime_costs_selected_archetypes.melt(
        id_vars=["archetype_label", "technology"],
        value_vars=["annualised_lifetime_cost"],
        var_name="cost_type",
        value_name="cost",
    )

    chart_annualised = (
        alt.Chart(df_annualised)
        .mark_bar()
        .encode(
            y=alt.Y("technology:N", axis=alt.Axis(title=None)),
            x=alt.X("sum(cost):Q", axis=alt.Axis(title="£ per year")),
            color=alt.Color(
                "cost_type:N",
                scale=alt.Scale(
                    domain=["annualised_lifetime_cost"], range=[NESTA_COLOURS[0]]
                ),
            ),
        )
        .facet(
            row=alt.Row(
                "archetype_label:N", header=alt.Header(labelAngle=0, labelAlign="left")
            )
        )
    )

    chart_annualised = chart_annualised.properties(
        title="Total lifetime costs divided by the lifespan of the heating system",
    )
    st.altair_chart(chart_annualised, use_container_width=True)

    # Reshape to long format for Install + Running
    df_comparing_costs = lifetime_costs_selected_archetypes.melt(
        id_vars=["archetype_label", "technology"],
        value_vars=[
            "lifetime_running_costs",
            "installation_costs_after_subsidy",
            "loan_interest",
            "lifetime_maintenance_costs",
        ],
        var_name="cost_type",
        value_name="cost",
    )

    # --- Base stacked bars (Install + Running) ---
    chart = (
        alt.Chart(df_comparing_costs)
        .mark_bar()
        .encode(
            y=alt.Y("technology:N", axis=alt.Axis(title=None)),
            x=alt.X("sum(cost):Q", axis=alt.Axis(title="£")),
            color=alt.Color(
                "cost_type:N",
                scale=alt.Scale(
                    domain=[
                        "lifetime_running_costs",
                        "installation_costs_after_subsidy",
                        "loan_interest",
                        "lifetime_maintenance_costs",
                    ],
                    range=NESTA_COLOURS[:5],
                ),
            ),
        )
        .facet(
            row=alt.Row(
                "archetype_label:N", header=alt.Header(labelAngle=0, labelAlign="left")
            )
        )
    )

    chart = chart.properties(
        title=["Lifetime costs of heating systems, broken down by installation costs (after subsidy),",
        "running costs, maintenance costs and loan interest (if applicable)"],
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("### Download data")

    csv_lifetime_costs = lifetime_costs.to_csv()
    csv_ashp_running_costs = ashp_running_costs.to_csv()

    st.download_button(
        label="Download lifetime costs data",
        data=csv_lifetime_costs,
        file_name="lifetime_costs_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
    st.download_button(
        label="Download ASHP running costs time series data",
        data=csv_ashp_running_costs,
        file_name="ashp_running_costs_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
