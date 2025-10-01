"""
About the app page.
"""

import streamlit as st

def about_dashboard_page():
    """
    This function will setup an 'About the app' page.
    """
    st.markdown("# :moneybag: Lifetime costs explorer")

    st.markdown(
        """
        ## An interactive tool to explore the lifetime costs of heat pumps and gas boilers under different scenarios

        The **Lifetime costs explorer** can be used to explore how various factors affect the whole-life costs of heat pumps and boilers. You can do this by exploring a set of pre-defined scenarios, or by creating your own custom scenario.

        ### Pre-defined scenarios and how to get to cost parity
        We identified conditions that could lead to price parity between heat pumps and gas boilers over the next decade. These are presented through three scenarios which demonstrate the trade-offs between policy choices and interactions with market and technological developments.
        These are compared to a **baseline** scenario in which no policy action is taken. The three scenarios are:

        - A **High innovation** scenario, in which upfront costs of heat pumps fall quickly and efficiency increases
        - A **Cheaper electricity** scenario, in which electricity costs fall more rapidly compared to gas
        - A **High subsidy** scenario, in which subsidies for heat pumps remain higher for longer.
        
        Each of these scenarios gets heat pumps to, or close to, **cost parity** with gas boilers for most households over the next decade. The **High innovation** scenario offers the largest advantage for the longest.

        The scenarios involve varying five main factors that will influence the cost of a heat pump relative to a gas boiler:

        **The upfront cost of installation**: This currently defaults to upfront costs falling by 2.5% each year from 202X to 2035.

        **The level of government subsidy**: We created different government trajectories, for example one where the existing £7,500 subsidy remains until at least 2028 before gradually reducing at different rates.
        
        **The cost of electricity relative to gas**: A key factor in the cost of electricity and gas is the levies, which are currently higher on electricity than gas. Our scenarios involve rebalancing the levies away from electricity and towards gas to different extents.

        **The efficiency of the heat pump (and gas boiler)**: Seasonal Coefficient of Performance (SCOP) is a measure of how much heat is produced by a heat pump for a unit of electricity used.

        **The interest rate for financing a heat pump**: Our scenarios assume all households will purchase heat pumps on finance, with 5% interest rates. Even where households do not use finance, the interest rate reflects the opportunity cost of not investing the money elsewhere.

        The whole-life cost of each device in the scenarios is calculated by adding up the cost of installation and running costs and dividing them by the assumed heating system lifespan (defaults to 15 for both heat pumps and boilers) to get the average annual cost. Our analysis includes interest rates, so is intended to approximate the full yearly cost a household would pay if buying a heating system on finance.

        When creating your own custom scenario, you can adjust each of these five factors to see how they affect the lifetime costs of heat pumps and gas boilers.

        ### Housing archetypes
        The resulting costs are presented separately for different types of homes. The price of a heat pump and a gas boiler varies depending on size requirements (determined largely by floor area); and larger homes use more energy for heating. We split homes into eight archetypes defined by built form and property age.
        The are 1) flats, 2) bungalows, 3) semi-detached, terraced houses and maisonettes, 4) detached houses; each divided into pre-1950 vs. post-1950 construction.
        We also present outcomes for an "average" household, defined as the weighted average according to how these archetypes are distributed in the English housing stock.
        """
    )
