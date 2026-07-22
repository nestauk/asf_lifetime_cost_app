"""
Data and methodology page.
"""
# Package imports
import streamlit as st

# Local imports
from config.fonts_setup import NESTA_COLOURS
nesta_blue = NESTA_COLOURS[0]
from getters import data_getters

def about_data_page():
    """
    This function will setup an 'About the data' page for the energy-use profiles explorer dashboard.
    """
    st.markdown("# Data and methodology")

    st.markdown("## Overview")

    st.markdown("""
                The lifetime costs calculator allows you to estimate the lifetime costs of gas boilers and air source heat pumps (hydronic/air to water) for different property archetypes under different scenarios.

                There are 4 preset scenarios with the following defaults.

                | Scenario            | SCOP | Subsidy model  | ASHP annual cost decrease | Purchasing ASHP with loans  | Loan interest rate | Energy wholesale price projection                                | Policy costs on energy bills                              | 
                |---------------------|------|----------------|---------------------------|------------------------|--------------------|-----------------------------------------------------------|-----------------------------------------------|
                | Baseline            | 3.0  | Zero from 2028 | 1%                        | Yes                    | 5%                 | Reference                                                 | No rebalancing                                |
                | High innovation     | 3.5  | Fast stepdown  | 5%                        | Yes                    | 5%                 | Reference                                                 | Rebalance RO and FiT from electricity to gas  |
                | Cheaper electricity | 3.0  | Fast stepdown  | 1%                        | Yes                    | 5%                 | Low fossil fuel prices scenario | Rebalance RO and FiT from electricity to gas  |
                | High subsidy        | 3.5  | High           | 1%                        | Yes                    | 5%                 | Reference                                                 | Rebalance RO and FiT from electricity to gas  |
                
                In the 'scenario selection' page, users can select one of the preset scenarios or create a custom scenario by changing any of the parameters.
                The 'comparing scenarios' page compares lifetime costs of gas boilers and air source heat pumps under the above pre-set scenarios.

                Below you can find more information about the methodology and data sources used in the lifetime costs calculator.
                """
    )
    
    st.markdown("## Methodology")

    st.markdown(f"""Methodology for calculating lifetime costs of heating systems. 
                Parameters highlighted in <span style='color:{nesta_blue};'>blue</span> are changeable inputs by the user in the app.""", unsafe_allow_html=True)

    with st.expander("Total lifetime costs"):
        # Lifetime cost calculations
        st.markdown(f"""
                    **Total lifetime cost**: This is the total cost of owning a heating system over its entire lifetime.
                    
                    Total lifetime cost [£] = Upfront costs [£] + Maintenance costs over lifetime [£] + Running costs over lifetime [£]

                    **Annualised lifetime cost**: This is the lifetime cost averaged over the heating system's lifetime.

                    Annualised lifetime cost [£/year] = Total lifetime cost [£] / <span style='color:{nesta_blue};'>Lifespan</span> [years]

                    **Time series breakdown of total cost over the heating system's lifetime**: This is the total cost of having that heating system in each year of its lifetime. This cost will be different for each year of its lifetime.

                    For each year of the heating system's lifetime:

                    Total cost of owning the heating system [£/year] = Upfront cost [£/year] + Maintenance cost [£/year] + Running cost [£/year]
                    """, unsafe_allow_html=True)
        
    with st.expander("Upfront costs"):
        st.markdown(f"""
            **Adjusting installation cost based on year of purchase**:
            
            For each year:
                    
            Cost reduction = (1 - <span style='color:{nesta_blue};'>Annual cost reduction rate</span>) * Cost reduction in previous year
                    
            where <span style='color:{nesta_blue};'>annual cost reduction rate</span> is how much we expect cost to reduce annually e.g. 0.01 if 1% reduction expected
                    
            Adjusted installation cost [£] = Installation cost [£] x Cost reduction 
            
            **If purchasing with loan, calculate total loan repayment value**:
            
            Loan amount [£] =  Adjusted installation cost [£] - Subsidy available [£]
                    
            Annual loan payment [£/year] = (Loan amount x <span style='color:{nesta_blue};'>Interest rate</span>) / (1 - ((1 + <span style='color:{nesta_blue};'>Interest rate</span>) ^ -<span style='color:{nesta_blue};'>Lifespan</span>))
            
            Loan repayment value [£] = Annual loan payment [£/year] x <span style='color:{nesta_blue};'>Lifespan</span> [years]
                    
            **Upfront costs over lifetime**:
                    
            Upfront costs over lifetime = Loan amount + Loan Repayment value
            """, unsafe_allow_html=True)
        
    with st.expander("Maintenance costs"):
        st.markdown(f"""
                **Annual maintenance cost**: This is the total cost of maintaining the heating system in one year.

                Annual maintenance cost [£/year] = <span style='color:{nesta_blue};'>Cost of maintenance</span> [£/session] x <span style='color:{nesta_blue};'>Number of times heating system is serviced per year</span> [session/year]

                **Lifetime maintenance cost**: This is the total cost of maintaining the heating system over its entire lifetime.

                Lifetime maintenance cost [£] = Annual maintenance cost [£/year] x <span style='color:{nesta_blue};'>Lifespan</span> [years]
                    """,
    unsafe_allow_html=True)
        
    with st.expander("Running costs"):
        st.markdown(f"""    
                **Wholesale price projections scenario**: 
                When building a custom scenario, the user can select any of the three DESNZ wholesale price projection models: Reference, Low Fossil Fuel Prices or High Fossil Fuel Prices.
                These projections are used to estimate the future cost of electricity and gas in each year of the heating system's lifetime.
                    
                **Model the gas and electricity tariff (price cap) for each year of the heating system's lifetime**: Based on the heating system's purchase year and number of years in its lifespan, the price of electricity and gas in each year of its lifetime needs to be estimated.

                To do this, a time series of electricity and gas tariffs for each year of the heating system's lifetime is created:
                - Wholesale cost components (DF and CM in the Ofgem energy price cap) are set using DESNZ wholesale price projection values (see the section "Energy future price projections" below for more details).
                - Policy costs are assumed constant, at the level of the latest price cap or at the level set by the policy costs rebalancing scenario.
                - For other cost components (including network costs), we assume levels set in the latest Ofgem energy price cap.
                    
                In the section below you can read more about rebalancing scenarios for policy costs.

                **Energy demand for heating in each year of operation**: Based on the property's annual heating demand and assumed efficiency of the heating system, the amount of energy (kWh per year) that the heating system will require to meet that property's heat demand can be estimated.

                Energy demand [kWh] = Property heat demand [kWh] / <span style='color:{nesta_blue};'>Heating system efficiency</span>
                
                Heating system efficiency, also known as the Seasonal Coefficient of Performance (SCOP), measures how effectively a heating system converts energy into heat over an entire heating season. It is the ratio of the total heat output to the total energy input. For example, a SCOP of 3.0 means the system produces 3 kWh of heat for every 1 kWh of energy it consumes.

                **Cost of energy use for heating in each year of operation**: The time series of electricity and gas tariffs for each year of operation can be used to calculate the cost of energy usage in each year.

                For each year of operation (5% VAT included):
                
                Cost of running the heating system [£/year] = ((Energy demand [kWh/year] x Unit cost of energy [£/kWh]) + (Energy standing charge [£/customer/year])) x 1.05

                Note that the gas standing charge is included in the running costs of a gas boiler but the electricity standing charge is not included in the running costs of an air-source heat pump. This is because the standing charge on electricity will apply regardless of heat source, whereas households can disconnect from gas if they switch to a heat pump.

                **Total lifetime running costs**: The total lifetime cost of running the heating system is calculated by summing all annual running cost values. 

                The annualised lifetime running cost can then be calculated by dividing the total lifetime running cost by the number of years of its assumed lifetime. Note that the annualised lifetime running cost is different to the estimated running cost of the heating system in each year of its lifetime (which varies depending on future energy price projections).
                    """, unsafe_allow_html=True)
        
    with st.expander("Policy cost rebalancing"):
        st.markdown(f"""
                For calculating operating costs under a policy cost rebalancing scenario, the policy cost component (PC price cap component) is replaced with the policy costs from a rebalanced collection of levies.

                We directly use the code from the [asf_levies_model](https://github.com/nestauk/asf_levies_model)/ https://nesta-levies-model.streamlit.app/ and follow the same approach to rebalancing.

                Rebalancing options include:
                - No rebalancing
                - Rebalancing unit costs (slider): When this levy rebalancing option is chosen, the following levies that are ordinarily levied against electricity units are rebalanced: RO, FiT, ECO, AAHEDC, NCC. These levies can be rebalanced to proportions between being 100% levied against gas and 100% levied against electricity.
                - Remove unit costs from electricity to taxation: for the following levies RO, FiT, ECO, AAHEDC, NCC.
                    
                The preset scenarios use the following levy rebalancing options (with the exception of the baseline scenario which uses no rebalancing):
                - Rebalance RO and FiT from being levied on electricity units to gas units
                """)
        

    st.markdown("## Data sources")

    with st.expander("Property archetypes, heat demand and air source heat pump installation costs"):
        st.markdown("""
                    **Microgeneration Certification Scheme (MCS) data on heat pump installations**: This is a subset of the MCS Installations Database (MID), and contains one record for each MCS certificate associated with a heat pump installation. The dataset contains records of both domestic and non-domestic air source, water/ground source and other types of heat pump installations. MID data is used with permission from MCS and subject to the conditions of a data sharing agreement.

                    **Energy Performance Certificates (EPC) register data**: Property data comes from England & Wales and Scotland's EPC register. EPC records provide data on building characteristics and energy efficiency measures, including: property address and other location information; property characteristics such as number of rooms, property type and built form; heating system(s) installed; energy efficiency ratings. The EPC Register datasets are open data and accessible to everyone.

                    **Joint MCS-EPC dataset**: The joint MCS-EPC dataset is created by linking the MCS heat pump installations data with EPC data. The linkage is done using property address information. More information in this [GitHub repository](https://github.com/nestauk/asf_daps).

                    The joint MCS-EPC dataset is used to derive the following inputs to the lifetime cost model:
                    - Property archetypes
                    - Annual heat demand for property archetypes
                    - Air source heat pump installation costs for each property archetype and cost decile

                    #### Property archetypes
                    
                    Users can select/view results for 8 different housing archetypes: flats; semi-detached & terraced houses and maisonettes; detached houses; and bungalows; with each group split into pre- and post-1950 construction.

                    #### Annual heat demand for property archetypes

                    Annual heat demand (kWh) is estimated for the above archetypes. To learn more about how annual heat demand is estimated, please visit the [GitHub repository](https://github.com/nestauk/asf_heat_pump_affordability/blob/dev/asf_heat_pump_affordability/notebooks/Archetype_Heat_Demand.py)
                    The annual heat demand for property archetypes uses data from 2021 up to Q2 2023 and is shown below:
                    """)
        heat_demand = data_getters.get_property_heat_demand()
        st.dataframe(heat_demand)

        st.markdown("""
                    #### Air source heat pump installation costs for each property archetype and decile
                    Costs of installing air source heat pumps are estimated for the above housing archetypes and at different cost deciles. 

                    The air source heat pump installation costs for each property archetype and cost decile uses data from 2021 to Q2 2023 and is shown below. You can select the cost decile to view the corresponding installation costs in £ (adjusted for inflation and expressed in 2023 prices).         
                    """)
        cost_decile = st.selectbox(
                label="Select the cost decile (50 corresponds to the median)",
                options=range(10, 100, 10),
                index=4,
                key="income_decile_input",
                help="Select the cost decile, where 50 corresponds to the median.",
            )
        ashp_installation_costs = data_getters.get_ashp_installation_costs
        ashp_decile_costs = ashp_installation_costs()[[f"cost_percentile_{cost_decile}"]]
        st.dataframe(ashp_decile_costs)
        st.markdown("""
                    Users can select the rate at which air source heat pump installation costs reduce by annually. This percentage reduction will be applied to the 2023 installation costs to estimate installation costs in later years.
                    """)
    with st.expander("## Air source heat pump subsidy trajectories"):
        st.markdown("""
                    Users can select from different subsidy trajectories for air source heat pumps or input their own level of subsidy. The options are shown below. The subsidy values are in £ (nominal) and are for each year between 2025 and 2035.
                    """)
        ashp_subsidy_options = data_getters.get_ashp_subsidy_options_data()
        st.dataframe(ashp_subsidy_options)

    with st.expander("Gas boiler installation costs"):
        st.markdown("""
                    Gas boiler installation costs are presented each property archetype. These costs result from Nesta research and analysis of boiler prices online.

                    These refer to the period of XXX.
                    """)
        gas_boiler_installation_costs = data_getters.get_gas_boiler_installation_costs()
        st.dataframe(gas_boiler_installation_costs)

    with st.expander("Energy price projections"):
        st.markdown("""
                    [DESNZ's Energy and emissions projections](https://www.gov.uk/government/publications/energy-and-emissions-projections-2023-to-2050) (Annex M) are used as estimates of the wholesale cost components of the unit cost of electricity and gas in the years 2025 to 2050.
                    
                    **Projection scenarios**: Three scenarios with different projections are available:
                    - Reference
                    - Low Fossil Fuel Prices
                    - High Fossil Fuel Prices.

                    DESNZ projections provide wholesale price projections for natural gas in p/therm. These are converted to p/kWh (Therm to kWh conversion factor = 29.31).

                    **Classification of tariff cost components** For calculating future operating costs, the wholesale cost components (Direct Fuel, DF, and Capacity Market, CM) are replaced with DESNZ wholesale price projections for that year.
                    For calculating operating costs under a levy rebalancing scenario, the policy cost component (PC) is updated with the rebalanced policy costs.


                    **Metering arrangement for electricity**: the price cap costs for single-rate metering are used for the price of electricity (as opposed to multi-register metering). Assumed to be the most common metering arrangement.

                    Wholesale prices are projected by DESNZ up to 2050. In this model, DESNZ projections are modified such that (i) wholesale prices are held constant at 2040 levels from 2041 to 2050 in the reference scenario, (ii) wholesale prices are held constant at 2031 levels from 2032 to 2050 in the low fossil fuel prices and high fossil fuel prices scenarios.
                    """)

    with st.expander("Non-wholesale components of gas and electricity prices"):
        st.markdown("""
                    [Ofgem's energy price cap](https://www.ofgem.gov.uk/energy-policy-and-regulation/policy-and-regulatory-programmes/energy-price-cap-default-tariff-policy/energy-price-cap-default-tariff-levels) is used to set the cost of electricity and gas, as inputs to running cost calculations:
                    - Annex 9 for full Tariff cost components
                    - Annex 4 for policy costs only (individual levies).

                    The latest price cap period is used (XXX).
""")
    with st.expander("Building an average household"):
        st.markdown("""
                    The average household is built by weighting the property archetypes according to their distribution in the English housing stock, using English Housing Survey 2019-2020. These data are safeguarded and [accessed through the UK Data Service](https://datacatalogue.ukdataservice.ac.uk/studies/study/8923?id=8923#details).
                    There are a few caveats to this approach:
                    - The distribution of property archetypes is based on English housing stock only, whereas the heat demand and installation costs are based on properties in England, Wales and Scotland.
                    - The built year distribution is based on EHS data, whereas the heat demand and installation costs are based on EPC data, so there may be some differences in the built year distribution.                    
                    """)