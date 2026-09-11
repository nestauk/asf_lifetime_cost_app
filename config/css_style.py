"""
.streamlit/config.toml provides the configuration for the Streamlit app.

Additional configuration options require CSS styling to be applied globally.
This file sets the CSS style for the Streamlit app to center the metrics and
use the Averta font globally and it ensures that all UI elements use this font.
"""

import base64

import streamlit as st

from config.fonts_setup import FONT, TITLE_FONT


def font_to_base64(path: str) -> str:
    """Converts a font file to a base64 encoded string."""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:font/woff2;base64,{encoded}"


averta_regular = font_to_base64("fonts/Averta-Regular.woff2")
averta_bold = font_to_base64("fonts/Averta-Bold.woff2")
zosia_display = font_to_base64("fonts/Zosia-Display.woff2")


def set_css_style():
    """
    This function sets the CSS style for the Streamlit app.
    It applies the Averta font globally for body text, and Zosia-Display
    for page/section headings (h1-h6).
    """
    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Averta';
            src: url("{averta_regular}") format('woff2');
            font-weight: normal;
            font-style: normal;
        }}

        @font-face {{
            font-family: 'Averta';
            src: url("{averta_bold}") format('woff2');
            font-weight: bold;
            font-style: normal;
        }}

        @font-face {{
            font-family: '{TITLE_FONT}';
            src: url("{zosia_display}") format('woff2');
            font-weight: normal;
            font-style: normal;
        }}

        html, body, .stApp, .stMarkdown,
        .stButton button, .stMetric, .stTextInput, .stNumberInput,
        .stSelectbox, .stSidebar, label, div {{
            font-family: 'Averta', sans-serif !important;
        }}

        /* Headings use Zosia-Display instead of Averta */
        h1, h2 {{
            font-family: '{TITLE_FONT}', sans-serif !important;
        }}

        h3, h4, h5, h6 {{
                    font-family: '{FONT}', sans-serif !important;
                }}

        .stMetric > div:nth-child(1),
        .stMetric > div:nth-child(2) {{
            font-family: 'Averta', sans-serif !important;
        }}

        [data-testid="stMetric"] {{
        text-align: center;
        padding: 15px 0;
        }}

        [data-testid="stMetricLabel"] {{
        display: flex;
        justify-content: center;
        align-items: center;
        }}

        [data-testid="stMetricDeltaIcon-Up"] {{
            position: relative;
            left: 15%;
            -webkit-transform: translateX(-50%);
            -ms-transform: translateX(-50%);
            transform: translateX(-50%);
        }}

        [data-testid="stMetricDeltaIcon-Down"] {{
            position: relative;
            left: 15%;
            -webkit-transform: translateX(-50%);
            -ms-transform: translateX(-50%);
            transform: translateX(-50%);
        }}

        /* Style the native sidebar page-nav section title (e.g. "Pages") */
        [data-testid="stSidebarNav"] span {{
            color: #0F294A !important;
            font-size: 14px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
