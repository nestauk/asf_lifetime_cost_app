"""
Comparing scenarios page.
"""

## Package imports
import streamlit as st
import altair as alt
import pandas as pd

# Local imports
from config.fonts_setup import nestafont, NESTA_COLOURS

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")

def comparing_scenarios_page():
    """
    This function sets up the 'Comparing scenarios' page of the app.
    """

    st.markdown("# Lifetime costs: comparing scenarios")
    st.markdown(
        """
        This page allows you to compare the development of lifetime cost difference between boilers and air source heat pumps over time, across different preset scenarios for an average household. 
        """
    )

    with st.expander("📅 Select the cost decile"):
        st.markdown("Cost decile refers to the distribution of upfront costs for air source heat pumps, where 50 corresponds to the median cost.")
        cost_decile = st.selectbox(
            label="Select the cost decile (50 corresponds to the median)",
            options=range(10, 100, 10),
            index=4,
            key="income_decile_input",
            help="Select the cost decile, where 50 corresponds to the median.",
        )

    st.markdown("<MISSING: TEXT EXPLAINING PLOT BELOW, e.g. the impact of subsidy trajectories and levy rebalancing in the results.>")

    results = pd.read_csv("s3://asf-lifetime-cost-model/outputs/cost_dif_by_year_decile_" + str(cost_decile) + ".csv")
    results.rename(columns={"Unnamed: 0": "installation_year"}, inplace=True)
    results = results.melt(
        id_vars=["installation_year"],
        var_name="scenario",
        value_name="cost_difference_ashp_minus_boiler"
    )    
    scenarios_list = results["scenario"].unique().tolist()

    st.markdown("By default, the chart shows the difference in annualised lifetime costs between scenarios, i.e. the difference in average yearly costs over the lifetime of the heating systems. You can toggle to see the difference in total lifetime costs instead.")
    toggle_total_lifetime_costs = st.toggle(
        label="Show difference in total lifetime costs instead of difference in annualised lifetime costs",
        value=False,
        key="toggle_total_lifetime_costs",
        help="Toggle between difference in annualised lifetime costs and difference in total lifetime costs",
    )

    if toggle_total_lifetime_costs:
        title = ["Difference in total lifetime costs of air source heat pumps vs. gas boilers by installation year and scenario for average household",
                 "(values below zero indicate air source heat pumps are cheaper)"]
    else:
        results["cost_difference_ashp_minus_boiler"] = (
            results["cost_difference_ashp_minus_boiler"] / 15  # annualise over 15 years
        )
        title = ["Difference in annualised lifetime costs of air source heat pumps vs. gas boilers by installation year and scenario for average household",
                 "(values below zero indicate air source heat pumps are cheaper)"]
    line_chart = (
        alt.Chart(results)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("installation_year:O", title="Installation year"),
            y=alt.Y("cost_difference_ashp_minus_boiler:Q", title="Cost difference (heat pump - boiler, £)"),
            color=alt.Color("scenario:N", title="Scenario", scale=alt.Scale(domain=scenarios_list, range=NESTA_COLOURS)),
            tooltip=[
                alt.Tooltip("installation_year:O", title="Installation year"),
                alt.Tooltip("scenario:N", title="Scenario"),
                alt.Tooltip("cost_difference_ashp_minus_boiler:Q", title="Cost difference (heat pump - boiler)", format=".2f"),
            ],
        )
    )

    # Shaded area for y < 0
    min_value = results["cost_difference_ashp_minus_boiler"].min()

    # Create dummy DataFrame covering the x-axis
    area_df = pd.DataFrame({
        "installation_year": results["installation_year"].unique(),
        "y": [min_value] * len(results["installation_year"].unique())
    })

    area_below_zero = (
        alt.Chart(area_df)
        .mark_area(color="lightgray", opacity=0.3)
        .encode(
            x=alt.X("installation_year:O"),
            y=alt.Y("y:Q", title=""),
            y2=alt.Y2(value=0),
            tooltip=alt.value(None),
        )
    )
    label = (
        alt.Chart(pd.DataFrame({"installation_year": [results["installation_year"].iloc[0]], "y": [-100]}))
        .mark_text(text="Air source heat pumps are cheaper", fontSize=16, color="grey", align="left")
        .encode(
            x=alt.X("installation_year:O"),
            y=alt.Y("y:Q"),
        )
    )

    # Combine charts
    final_chart = (area_below_zero + line_chart + label).properties(
            width=800,
            height=500,
            title=title
        ).configure_title(fontSize=20
        ).configure_axis(labelFontSize=16, titleFontSize=16
        ).configure_legend(labelFontSize=16, titleFontSize=16)
    
    st.altair_chart(final_chart, use_container_width=True)

    st.markdown("### Download data")
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'scenario_comparison_cost_decile_{cost_decile}.csv',
        mime='text/csv',
        icon=":material/download:",
    )

    st.markdown(
        """
                ### Preset scenarios explained
                
                The assumptions underlying each preset scenario are:

                <INSERT UPDATED TABLE FROM about_data_page.py ONCE IT IS FINALISED>

                You can find more information about the methodology and data sources used on the Data and methodology page.
                """
    )
