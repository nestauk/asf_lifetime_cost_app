"""Landing page — orients the user and links to the three tool pages and methodology guide."""

import streamlit as st

from components.layout import render_page_title

# Global CSS to style ebery st.page_link() on this page as a solid navy flag-shaped button
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
    <div style="font-size:22px; font-weight:800; color:#0F294A; margin-bottom:10px;">
        About this tool
    </div>
    <div style="font-size:15px; color:#333; line-height:1.7; margin-bottom:10px;">
        This tool compares the lifetime cost of an air-to-water heat pump against a gas boiler.
        Set your own assumptions about heat demand, the heat pump and boiler, energy prices,
        installation costs, maintenance, financing and subsidy.
    </div>
    <div style="font-size:15px; color:#333; line-height:1.7; margin-bottom:6px;">
        Then explore the results across three pages: a direct cost comparison, and two pages
        that solve for the subsidy or the electricity price a heat pump would need to match a
        gas boiler.
    </div>
    <div style="font-size:13px; color:#888; line-height:1.5; margin-bottom:32px;">
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
