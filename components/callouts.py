"""Shared callout and divider front end components used across multiple pages."""

import streamlit as st


def render_callout(html_content: str) -> None:
    """Render a light-teal callout box with a teal left border accent."""
    st.markdown(
        f"""
        <div style="
            background-color: #EAF6F5;
            border-left: 4px solid #18A48C;
            padding: 12px 14px;
            border-radius: 4px;
            font-size: 13px;
            color: #1a3a3a;
            margin: 12px 0;
        ">{html_content}</div>
        """,
        unsafe_allow_html=True,
    )


def render_divider(color: str = "#0000FF") -> None:
    """Render a colored horizontal divider (default: Nesta purple)."""
    st.markdown(
        f'<hr style="border: none; border-top: 3px solid {color}; margin: 12px 0;">',
        unsafe_allow_html=True,
    )


def render_page_context_callout(message: str) -> None:
    """Render a page-level orientation callout — e.g. explaining what a solver page solves for.

    Distinct from render_solved_for_note (which flags one specific sidebar
    section as solved-for); this is a single note at the top of the page,
    explaining the whole page's purpose.
    """
    st.markdown(
        f"""
        <div style="
            background:#F6F4F2;
            border-left:4px solid #0000FF;
            padding:16px 20px;
            border-radius:4px;
            margin-bottom:20px;
            font-size:14px;
            color:#0F294A;
            line-height:1.6;
        ">{message}</div>
        """,
        unsafe_allow_html=True,
    )
