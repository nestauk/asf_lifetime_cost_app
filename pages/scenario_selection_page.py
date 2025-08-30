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
                value="",
                key="custom_scenario_name_input",
            )

        if scenario_name != "":
            with st.expander("⚙️ Define your custom scenario parameters"):
                st.write(
                    "Expand the sections below to define your custom scenario parameters."
                )
                with st.expander("👨🏻‍🔧 Maintenance costs"):
                    ashp_maintenance_cost_col, boiler_maintenance_cost_col = st.columns(
                        2
                    )

                    with ashp_maintenance_cost_col:
                        ashp_maintenance_cost = st.slider(
                            label="ASHP annual maintenance cost (£)",
                            min_value=0,
                            max_value=500,
                            value=config.maintenance_costs_default["ashp"],
                            step=10,
                            key="custom_ashp_maintenance_cost_input",
                            help="Annual maintenance cost for the ASHP",
                        )
                    with boiler_maintenance_cost_col:
                        boiler_maintenance_cost = st.slider(
                            label="Boiler annual maintenance cost (£)",
                            min_value=0,
                            max_value=500,
                            value=config.maintenance_costs_default["boiler"],
                            step=10,
                            key="custom_boiler_maintenance_cost_input",
                            help="Annual maintenance cost for the gas boiler",
                        )

                with st.expander("📈 Effiency measures"):
                    ashp_efficiency_col, boiler_efficiency_col = st.columns(2)

                    with ashp_efficiency_col:
                        ashp_efficiency = st.selectbox(
                            label="ASHP efficiency",
                            options=[
                                "reference: SCOP = 3",  # SCOP 3
                                "high: SCOP > 3",  # SCOP > 3
                                "low: SCOP < 3",  # SCOP < 3
                            ],
                            index=0,
                            key="custom_ashp_efficiency_input",
                            help="Seasonal Coefficient of Performance (SCOP) of the ASHP",
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
                                        option["name"].capitalize()
                                        + ": "
                                        + option["helper"]
                                        for option in config.loan_interest_rate_options
                                    ],
                                    index=1,
                                    key="custom_ashp_loan_interest_rate_input",
                                    help="The interest rate of the ASHP loan",
                                )
                with st.expander("💰 Subsidy"):
                    col1, ashp_subsidy_col, col2 = st.columns([1, 4, 1])

                    with ashp_subsidy_col:
                        # --- Main selectbox (always visible) ---
                        ashp_subsid_model = st.selectbox(
                            label="Choose an ASHP subsidy model - visit the 'About the app' page for more details",
                            options=[
                                opt.capitalize() for opt in config.ashp_subsidy_options
                            ],
                            index=0,
                            key="ashp_subsidy_select",
                            help="Choose an ASHP subsidy model",
                        )

                        if ashp_subsid_model == "Custom subsidy model":
                            st.write("Edit the subsidy values below (£) for each year.")
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
                    levy_rebalancing_col, levies_to_rebalance_col = st.columns(2)

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
                        with levies_to_rebalance_col:
                            levies_to_rebalance = st.multiselect(
                                label="Select which levies to rebalance",
                                options=["A", "B", "C", "D", "E"],
                                default=["A", "B"],
                                key="custom_levies_to_rebalance_input",
                                help="Select which levies to rebalance between electricity and gas",
                            )

    st.markdown("### Results")

    col5, filter_archetypes_col, col6 = st.columns([1, 4, 1])
    with filter_archetypes_col:
        filter_archetypes = st.multiselect(
            label="Select or de-select archetypes to filter the results",
            options=["A", "B", "C"],
            default=["A", "B", "C"],
            key="filter_archetypes_input",
            help="Filter the results by archetype",
        )

    st.write("Dummy data just for testing...")
    dummy_data = pd.DataFrame(
        {
            "Archetype": ["A", "A", "B", "B", "C", "C"],
            "Technology": ["ASHP", "Boiler", "ASHP", "Boiler", "ASHP", "Boiler"],
            "Annualised cost of installation": [1000, 200, 3000, 100, 900, 133],
            "Running cost in each year of operation": [150, 200, 160, 210, 140, 190],
            "Annual maintenance cost": [80, 80, 80, 80, 80, 80],
            "Annualised subsidy": [500, 0, 500, 0, 500, 0],
        }
    )
    dummy_data = dummy_data[dummy_data["Archetype"].isin(filter_archetypes)]
    dummy_data["Annualised lifetime cost"] = (
        dummy_data["Annualised cost of installation"]
        + dummy_data["Running cost in each year of operation"]
        + dummy_data["Annual maintenance cost"]
        - dummy_data["Annualised subsidy"]
    )
    dummy_data.set_index(["Archetype", "Technology"], inplace=True)

    total_dummy_data = dummy_data * 15
    total_dummy_data.columns = [
        "Total cost of installation",
        "Total running cost over 15 years",
        "Total maintenance cost over 15 years",
        "Total subsidy",
        "Total lifetime cost",
    ]

    st.dataframe(dummy_data, use_container_width=True)
    st.dataframe(total_dummy_data, use_container_width=True)

    st.markdown("### Download data")
    csv_annual = dummy_data.to_csv()
    csv_total = total_dummy_data.to_csv()

    st.download_button(
        label="Download annualised costs data",
        data=csv_annual,
        file_name="annualised_costs_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )

    st.download_button(
        label="Download total costs data",
        data=csv_total,
        file_name="lifetime_costs_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
