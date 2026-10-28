"""Landing page — orients the user and links to the three tool pages and methodology guide."""

import streamlit as st

from components.layout import render_page_title

# Global CSS to style every st.page_link() on this page as a solid navy flag-shaped button
st.markdown(
    """
            <style>
                [data-testid="stPageLink"] {
                    background-color: #0000FF;
                    border-radius: 0;
                    clip-path: polygon(
                                    0 0,
                                    calc(100% - 14px) 0,
                                    100% 14px,
                                    100% 100%,
                                    14px 100%,
                                    0 calc(100% - 14px)
                                );
                    padding: 6px 6px !important;
                    width: 100% !important;
                    white-space: nowrap;
                    margin-top: 16px;
                }
                [data-testid="stPageLink"] p {
                    color: white !important;
                    font-weight: 700 !important;
                    font-size: 14px !important;
                    white-space: nowrap;
                }
                [data-testid="stPageLink"]:hover {
                    background-color: #0000CC;
                }
            </style>
            """,
    unsafe_allow_html=True,
)

# Center content
left_pad, main_col, right_pad = st.columns([1, 12, 1])

with main_col:
    render_page_title(
        title="Heat pump vs. gas boiler lifetime cost tool",
    )
    st.markdown(
        """
    <div style="font-size:15px; color:#333; line-height:1.7; margin-bottom:24px;">
        This tool compares the lifetime cost of an <b>air-to-water heat pump</b> against a <b>gas boiler</b>.
        It is designed for specialists working in clean heat to explore heat decarbonisation economics under different modelling assumptions and scenarios.
    </div>
    """,
        unsafe_allow_html=True,
    )

    # How to use this tool responsibly
    st.markdown(
        """
    <div style="background:#F6F4F2; border-left:4px solid #0000FF; padding:18px 24px; margin-bottom:24px;">
    <div style="font-size:15px; font-weight:700; color:#0F294A; margin-bottom:10px;">
        How to use this tool
    </div>
    <div style="font-size:14px; color:#333; line-height:1.7; margin-bottom:16px;">
        Set <b>your own assumptions</b> about heat demand, the heat pump and boiler, energy prices,
        installation costs, maintenance, financing and subsidy in the sidebar. The tool will then
        <b>calculate the lifetime costs</b> of an air-to-water heat pump and gas boiler under those
        assumptions.
    </div>
    <hr style="border:none; border-top:1px solid #ddd; margin:0 0 14px 0;">
    <div style="font-size:12px; font-weight:700; color:#666; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">
        Please note
    </div>
    <div style="font-size:13px; color:#333; line-height:1.6;">
        &bull; Results depend directly on the inputs and parameters you select in the sidebar.
        You are responsible for verifying the accuracy and appropriateness of any custom
        parameters you enter.<br>
        &bull; Default parameters are generic, illustrative benchmarks. They do not guarantee
        accuracy for any specific building, geographical location, or commercial scenario.<br>
        &bull; Treat all calculated outputs as illustrative, indicative estimates for
        exploratory purposes only.<br>
        &bull; If you share or distribute results, charts, or exported files from this tool,
        you must accurately attribute the tool and clearly state the input assumptions used
        to generate those figures.
    </div>
</div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="font-size:15px; color:#333; line-height:1.7; margin-bottom:6px; margin-top:10px;">
            There are three pages you can navigate to in the sidebar that calculate different outputs:
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="font-size:13px; color:#888; line-height:1.5; margin-bottom:16px;">
        Each page has its own sidebar for these assumptions, so you'll need to set them again
        if you switch pages.
    </div>
    """,
        unsafe_allow_html=True,
    )

    CARD_STYLE = (
        "background:#fff; border:1px solid #E0E0E0; border-radius:2px; padding:24px; "
        "height:100%; box-shadow:0 4px 12px rgba(0,0,0,0.15);"
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            f"""
    <div style="{CARD_STYLE}">
        <div style="font-size:17px; font-weight:700; color:#0F294A; margin-bottom:10px;">
            Lifetime cost comparison
        </div>
        <div style="font-size:14px; color:#333; line-height:1.6; margin-bottom:12px;">
            See the full lifetime cost of a heat pump against a gas boiler by installation
            year, broken down into upfront cost, running cost, financing and maintenance, and
            as a year-by-year cashflow.
        </div>
        <div style="font-size:13px; color:#666; line-height:1.5; margin-bottom:16px; padding-left:10px; border-left:2px solid #ddd;">
            e.g. Is a heat pump installed in 2028 cheaper overall than a gas boiler, when accounting for installation, running and
            maintenance costs?
        </div>
    </div>
    """,
            unsafe_allow_html=True,
        )
        st.page_link(
            "views/lifetime_cost_comparison.py",
            label="Open the cost comparison →",
            icon=None,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:17px; font-weight:700; color:#0F294A; margin-bottom:10px;">
                    Subsidy solver
                </div>
                <div style="font-size:14px; color:#333; line-height:1.6; margin-bottom:16px;">
                    For each installation year, determine the subsidy level needed for a heat pump to achieve total lifetime cost parity 
                    with a gas boiler - and see how that compares with the current subsidy scheme.
                </div>
                <div style="font-size:13px; color:#666; line-height:1.5; margin-bottom:16px; padding-left:10px; border-left:2px solid #ddd;">
                    e.g. What would the subsidy need to be in 2032, for cost parity with gas boilers, if heat pump installation
                    costs haven't fallen as expected?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(
            "views/solve_subsidy.py", label="Open the subsidy solver →", icon=None
        )

    with col3:
        st.markdown(
            f"""
            <div style="{CARD_STYLE}">
                <div style="font-size:17px; font-weight:700; color:#0F294A; margin-bottom:10px;">
                    Price ratio solver
                </div>
                <div style="font-size:14px; color:#333; line-height:1.6; margin-bottom:16px;">
                    For each installation year, determine the break-even electricity price cap that brings a heat pump to annualised lifetime cost parity 
                    with a gas boiler, holding gas prices and subsidies constant.
                </div>
                <div style="font-size:13px; color:#666; line-height:1.5; margin-bottom:16px; padding-left:10px; border-left:2px solid #ddd;">
                    e.g. How much cheaper would electricity need to be, relative to gas, to bring a heat pump installed today to cost parity?
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(
            "views/solve_price_ratio.py",
            label="Open the price ratio solver →",
            icon=None,
        )

    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

    # Guide and methodology
    st.markdown(
        """
    <div style="background:#F6F4F2; border-left:4px solid #0000FF; padding:20px 28px; display:flex; align-items:center; justify-content:space-between; gap:24px;">
        <div>
            <div style="font-size:17px; font-weight:700; color:#0F294A; margin-bottom:6px;">
                Want to know more about the underlying calculations and numbers?
            </div>
            <div style="font-size:14px; color:#333; line-height:1.6;">
                Find details on model assumptions, default parameters, present value and discounting calculations, caveats, and 
                access to the open-source Python code on the methodology page.
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.page_link("views/methodology.py", label="Go to Guide & methodology →", icon=None)

    # Disclaimer
    st.markdown(
        """
        <div style="
            background: #0F294A;
            padding: 20px 28px;
            margin-top: 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        ">
            <div>
                <div style="
                    font-size: 17px;
                    font-weight: 700;
                    color: #FFFFFF;
                    margin-bottom: 20px;
                ">
                    Nesta is a research and innovation foundation that designs,
                    tests and scales solutions for the biggest challenges of our
                    time. Our mission is to reduce home carbon emissions in the UK
                    by 30% from 2019 levels by 2030.
                </div>
                <div style="
                    font-size: 14px;
                    color: #FFFFFF;
                    line-height: 1.6;
                ">
                    This resource is made available to policy analysts,
                    researchers, government, and sector specialists for the
                    purposes of exploratory modeling and scenario analysis in heat
                    decarbonisation only. Calculations rely on illustrative
                    baseline parameters and custom user inputs; they do not
                    constitute financial, technical, or policy advice. While we
                    hope you find this useful for your research, analysis, and exploratory work,
                    please note that this resource is provided for information
                    purposes only. Nesta is not responsible for any reliance you
                    may choose to place on the resource, material or outputs it
                    makes available.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
