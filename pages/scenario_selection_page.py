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
    st.markdown(
        """
        This page allows you to select a predefined scenario or build your own custom scenario by defining various parameters.
        Once you have selected or built a scenario, the lifetime costs of air source heat pumps (ASHP) and gas boilers will be calculated and compared.

        The results will be displayed in a series of charts and tables, allowing you to see how the lifetime costs of ASHPs compare to gas boilers for different property archetypes.
        You can also filter the results by property archetype and download the data for further analysis.
        """
    )

    st.markdown("### Select a predefined scenario or build your own")
    st.write(
        """
             If you select a predefined scenario, the parameters will be set automatically. If you choose to build a custom scenario, start by naming it.
             Below you can also select the installation year and air source heat pump cost decile for your results. When building a custom scenario, you can then define other the parameters in more detail.
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
        st.markdown(
            "Installation year is the year the heating system purchased and installed. Cost decile refers to the distribution of upfront costs for air source heat pumps, where 50 corresponds to the median cost."
        )
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

                with st.expander("🗓️ Lifespan"):
                    ashp_lifetime_col, boiler_lifetime_col = st.columns(2)

                    with ashp_lifetime_col:
                        ashp_life_span = st.slider(
                            label="ASHP lifespan (years)",
                            min_value=1,
                            max_value=25,
                            value=config.life_span_default["ashp"],
                            step=1,
                            key="custom_ashp_life_span_input",
                            help="Number of years air source heat pump is assumed to be operational",
                        )
                    with boiler_lifetime_col:
                        boiler_life_span = st.slider(
                            label="Gas boiler lifespan (years)",
                            min_value=1,
                            max_value=25,
                            value=config.life_span_default["boiler"],
                            step=1,
                            key="custom_boiler_life_span_input",
                            help="Number of years gas boiler is assumed to be operational",
                        )

                with st.expander(" Installation costs"):
                    ashp_installation_cost_col, boiler_installation_cost_col = (
                        st.columns(2)
                    )

                    with ashp_installation_cost_col:
                        ashp_annual_cost_reduction = (
                            st.slider(
                                label="Annual cost reduction in ASHP installation cost (%)",
                                min_value=-1.0,
                                max_value=5.0,
                                value=config.ashp_annual_cost_decrease_default * 100,
                                step=1.0,
                                key="custom_ashp_annual_cost_reduction_input",
                                help="Percentage reduction in ASHP installation cost each future year. 5% refers to 5% annual cost reduction and -1% refers to a 1% annual cost increase.",
                            )
                            / 100
                        )
                    with boiler_installation_cost_col:
                        st.markdown(
                            "Boiler installation costs are always assumed to stay constant in future years."
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
                                ashp_loan_interest_rate_option_name = st.selectbox(
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
                            subsidy_value = st.number_input(
                                label=f"Subsidy value for year {installation_year} in £",
                                min_value=0,
                                max_value=15000,
                                value=7500,
                                step=100,
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
                            custom_gas_weight = (
                                st.slider(
                                    label="Rebalance between electricity (0% on gas) <-> gas (100% on gas)",
                                    min_value=0.0,
                                    max_value=100.0,
                                    value=0.0,
                                    step=10.0,
                                    key="custom_levy_gas_weights_input",
                                    help="Proportion of the scheme revenue that is levied against gas units. Electricity (0) setting is 0% of scheme revenue is levied on gas units (i.e. 100% on electricity) and gas (100) setting is 100% of scheme revenue on gas units.",
                                )
                                / 100
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
            else 3.5
            if scenario_info["ashp_scop"] == "high"
            else 2.5
        )
        boiler_efficiency = config.boiler_efficiency_default
        ashp_purchased_with_loan = (
            "Yes" if scenario_info["purchasing_with_loans"] else "No"
        )
        if ashp_purchased_with_loan == "Yes":
            ashp_loan_interest_rate_option_name = scenario_info["loan_interest_rate"]
        else:
            ashp_loan_interest_rate = 0

        ashp_subsidy_model = scenario_info["ashp_subsidy"]

        wholesale_price_projection = scenario_info["wholesale_price_projection"]

        levy_rebalancing = scenario_info["levy_rebalancing"]

        ashp_annual_cost_reduction = scenario_info["ashp_annual_cost_decrease"]

        with st.expander("⚙️ Scenario parameter values"):
            st.markdown(
                "Under the selected scenario, the following parameters are set as follows:"
            )

            st.markdown(
                f"""

                        | Parameter | Gas Boiler | ASHP |
                        |-----------|------------|-------|
                        | Lifespan (years) | {boiler_life_span} |{ashp_life_span} |
                        | Cost of maintenance service (£) | {boiler_maintenance_cost} |{ashp_maintenance_cost} |
                        | Frequency of maintenance per year | {boiler_maintenance_frequency} |{ashp_maintenance_frequency} |
                        | Efficiency | {boiler_efficiency} |{ashp_efficiency} |
                        | Heating system purchased with a loan? | - | {ashp_purchased_with_loan} |
                        | Loan interest rate |  - |{ashp_loan_interest_rate_option_name} |
                        | Subsidy model |  - |{ashp_subsidy_model} |
                        | Annual cost reduction in market price of heating system installation  | 0% | {scenario_info["ashp_annual_cost_decrease"] * 100}% |

                        Additional parameters for the running cost calculations:

                        | Parameter                  | Value                        |
                        |----------------------------|------------------------------|
                        | Wholesale price projection  | {wholesale_price_projection} |
                        | Levy rebalancing scenario   | {levy_rebalancing}           |

                        """
            )
            st.markdown(
                "To know more about these parameters, visit the 'About the app' page."
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

    archetype_name_mapping = {
        "pre_1950_flat": "Pre-1950 flat",
        "post_1950_flat": "Post-1950 flat",
        "pre_1950_semi_terraced_house": "Pre-1950 semi/terraced house",
        "post_1950_semi_terraced_house": "Post-1950 semi/terraced house",
        "pre_1950_bungalow": "Pre-1950 bungalow",
        "post_1950_bungalow": "Post-1950 bungalow",
        "pre_1950_detached_house": "Pre-1950 detached house",
        "post_1950_detached_house": "Post-1950 detached house",
    }

    mapped_archetype_options = [
        archetype_name_mapping[x] for x in cost_calculator.property_archetypes
    ]

    st.markdown(
        "As default, results are shown for all archetypes and the weighted average archetype. You can filter the results by archetype below."
    )
    col5, filter_archetypes_col, col6 = st.columns([1, 4, 1])
    with filter_archetypes_col:
        filter_archetypes = st.multiselect(
            label="Select or de-select archetypes to filter the results",
            options=mapped_archetype_options + ["Weighted average archetype"],
            default=mapped_archetype_options + ["Weighted average archetype"],
            key="filter_archetypes_input",
            help="Filter the results by archetype",
        )

    # Processing inputs before computations
    if ashp_purchased_with_loan == "Yes":
        ashp_purchased_with_loan = True
        ashp_loan_interest_rate = config.loan_interest_rate_options[
            ashp_loan_interest_rate_option_name
        ]
    else:
        ashp_purchased_with_loan = False
        ashp_loan_interest_rate = 0.0

    if levy_rebalancing == "no rebalancing (current price cap)":
        levy_rebalancing = False
        levies_to_rebalance = None
        levies_rebalancing_weights = None
    elif levy_rebalancing == "rebalance unit costs between electricity and gas":
        levy_rebalancing = True
        levies_to_rebalance = ["ro", "fit", "eco", "aahedc", "ncc"]
        levies_rebalancing_weights = {
            "electricity_weight": (1 - custom_gas_weight),
            "gas_weight": custom_gas_weight,
            "tax_weight": 0,
            "fixed_electricity_weight": 0,
            "variable_electricity_weight": 1,
            "fixed_gas_weight": 0,
            "variable_gas_weight": 1,
        }
    elif levy_rebalancing == "remove all electricity levies to taxation":
        levy_rebalancing = True
        levies_to_rebalance = ["ro", "fit", "eco", "whd", "aahedc", "ncc"]
        levies_rebalancing_weights = {
            "electricity_weight": 0,
            "gas_weight": 0,
            "tax_weight": 1,
            "fixed_electricity_weight": 0,
            "variable_electricity_weight": 0,
            "fixed_gas_weight": 0,
            "variable_gas_weight": 0,
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
        annual_cost_reduction=ashp_annual_cost_reduction,
        purchase_year=installation_year,
        life_span=ashp_life_span,
        decile=cost_decile,
        subsidy_model_or_input_values=(
            ashp_subsidy_model
            if ashp_subsidy_model != "custom subsidy model"
            else {installation_year: subsidy_value}
        ),
        purchase_with_loan=ashp_purchased_with_loan,
        loan_interest_rate=ashp_loan_interest_rate,
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

    boiler_upfront_costs = cost_calculator.compute_upfront_cost(
        heating_system="boiler",
        annual_cost_reduction=0,
        purchase_year=installation_year,
        life_span=boiler_life_span,
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
    ashp_lifetime_costs["life_span"] = ashp_life_span
    boiler_lifetime_costs["technology"] = "Gas boiler"
    boiler_lifetime_costs["life_span"] = boiler_life_span

    # Merging ASHP and boiler results
    lifetime_costs = pd.concat(
        [ashp_lifetime_costs, boiler_lifetime_costs]
    ).reset_index()

    lifetime_costs["installation_costs_after_subsidy"] = (
        lifetime_costs["installation_costs"] - lifetime_costs["subsidy_value"]
    )
    lifetime_costs.drop(columns=["installation_costs", "subsidy_value"], inplace=True)

    lifetime_costs["archetype_label"] = lifetime_costs["archetype_label"].map(
        archetype_name_mapping
    )

    # needs to be QAed
    number_of_properties = {
        "Post-1950 semi/terraced house": 6841365,
        "Pre-1950 semi/terraced house": 5602441,
        "Post-1950 flat": 4076569,
        "Post-1950 detached house": 3103702,
        "Post-1950 bungalow": 1564001,
        "Pre-1950 flat": 1415792,
        "Pre-1950 detached house": 1059425,
        "Pre-1950 bungalow": 205582,
    }

    lifetime_costs["number_of_properties"] = lifetime_costs["archetype_label"].map(
        number_of_properties
    )
    # Adding weighted average archetype
    weighted_lifetime_costs = (
        lifetime_costs.groupby("technology")
        .apply(
            lambda x: pd.Series(
                {
                    "lifetime_running_costs": (
                        x["lifetime_running_costs"] * x["number_of_properties"]
                    ).sum()
                    / x["number_of_properties"].sum(),
                    "installation_costs_after_subsidy": (
                        x["installation_costs_after_subsidy"]
                        * x["number_of_properties"]
                    ).sum()
                    / x["number_of_properties"].sum(),
                    "loan_interest": (
                        x["loan_interest"] * x["number_of_properties"]
                    ).sum()
                    / x["number_of_properties"].sum(),
                    "lifetime_maintenance_costs": (
                        x["lifetime_maintenance_costs"] * x["number_of_properties"]
                    ).sum()
                    / x["number_of_properties"].sum(),
                    "number_of_properties": x["number_of_properties"].sum(),
                }
            )
        )
        .reset_index()
    )
    weighted_lifetime_costs["archetype_label"] = "Weighted average archetype"
    life_span_map = {"ASHP": ashp_life_span, "Gas boiler": boiler_life_span}
    weighted_lifetime_costs["life_span"] = weighted_lifetime_costs["technology"].map(
        life_span_map
    )
    lifetime_costs = pd.concat([lifetime_costs, weighted_lifetime_costs]).reset_index(
        drop=True
    )

    lifetime_costs_selected_archetypes = lifetime_costs[
        lifetime_costs["archetype_label"].isin(filter_archetypes)
    ]

    df_comparing_costs = lifetime_costs_selected_archetypes.melt(
        id_vars=["archetype_label", "technology", "life_span"],
        value_vars=[
            "lifetime_running_costs",
            "installation_costs_after_subsidy",
            "loan_interest",
            "lifetime_maintenance_costs",
        ],
        var_name="cost_type",
        value_name="cost",
    )

    cost_type_name_mapping = {
        "lifetime_maintenance_costs": "Maintenance costs",
        "loan_interest": "Loan interest",
        "installation_costs_after_subsidy": "Installation costs (after subsidy)",
        "lifetime_running_costs": "Running costs",
    }

    df_comparing_costs["cost_type"] = df_comparing_costs["cost_type"].map(
        cost_type_name_mapping
    )

    # Convert column to ordered categorical
    df_comparing_costs["archetype_label"] = pd.Categorical(
        df_comparing_costs["archetype_label"],
        categories=mapped_archetype_options + ["Weighted average archetype"],
        ordered=True,
    )
    df_comparing_costs["cost_type"] = pd.Categorical(
        df_comparing_costs["cost_type"],
        categories=list(cost_type_name_mapping.values()),
        ordered=True,
    )
    df_comparing_costs = df_comparing_costs.sort_values(by=["archetype_label", "cost"])

    cost_component_order = {
        "Loan interest": 0,
        "Maintenance costs": 1,
        "Installation costs (after subsidy)": 2,
        "Running costs": 3,
    }
    df_comparing_costs["cost_type_order"] = df_comparing_costs["cost_type"].map(
        cost_component_order
    )
    df_comparing_costs["total_cost"] = df_comparing_costs.groupby(
        ["technology", "archetype_label"]
    )["cost"].transform("sum")
    chart = (
        alt.Chart(df_comparing_costs)
        .mark_bar()
        .encode(
            y=alt.Y("technology:N", axis=alt.Axis(title=None)),
            x=alt.X("sum(cost):Q", axis=alt.Axis(title="£")),
            color=alt.Color(
                "cost_type:N",
                title="Cost component",
                scale=alt.Scale(
                    domain=cost_type_name_mapping.values(),
                    range=[
                        NESTA_COLOURS[10],
                        NESTA_COLOURS[2],
                        NESTA_COLOURS[1],
                        NESTA_COLOURS[0],
                    ],
                ),
            ),
            order=alt.Order("cost_type_order:N", sort="descending"),
            tooltip=[
                alt.Tooltip("archetype_label:N", title="Archetype"),
                alt.Tooltip("technology:N", title="Technology"),
                alt.Tooltip("cost_type:N", title="Cost component type"),
                alt.Tooltip("cost:Q", title="Cost component (£)", format=",.2f"),
                alt.Tooltip("total_cost:Q", title="Total cost (£)", format=",.2f"),
            ],
        )
        .facet(
            row=alt.Row(
                "archetype_label:N",
                header=alt.Header(labelAngle=0, labelAlign="left"),
                title=None,
            )
        )
    )

    st.markdown(
        "You can toggle between annualised lifetime costs and total lifetime costs below. By default, annualised lifetime costs are shown, i.e. total lifetime costs divided by the lifespan of the heating system."
    )

    toggle_total_lifetime_costs = st.toggle(
        label="Show total lifetime costs instead of annualised lifetime costs",
        value=False,
        key="toggle_total_lifetime_costs",
        help="Toggle between annualised lifetime costs and total lifetime costs",
    )

    if toggle_total_lifetime_costs:
        title = [
            "Total lifetime costs of heating systems, broken down by installation costs (after subsidy),",
            " running costs, maintenance costs and loan interest (if applicable)",
        ]
    else:
        df_comparing_costs["cost"] = (
            df_comparing_costs["cost"] / df_comparing_costs["life_span"]
        )
        df_comparing_costs["total_cost"] = (
            df_comparing_costs["total_cost"] / df_comparing_costs["life_span"]
        )
        title = [
            "Annualised lifetime costs of heating systems, broken down by installation costs (after subsidy),",
            " running costs, maintenance costs and loan interest (if applicable)",
        ]

    chart = (
        chart.properties(title=title)
        .configure_title(fontSize=20)
        .configure_axis(labelFontSize=14, titleFontSize=14)
        .configure_legend(labelFontSize=14, titleFontSize=14)
        .configure_header(labelFontSize=14)
    )

    col7, cost_component_chart_col, col8 = st.columns([1, 8, 1])
    with cost_component_chart_col:
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
