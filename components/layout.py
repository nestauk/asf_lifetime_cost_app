"""Pre-built front-end components that are commonly used across all pages."""

import streamlit as st


def render_top_bar(
    tool_name: str = "Heating system lifetime cost tool",
    badge_text: str = "a sustainable future",
) -> None:
    """Render the dark navy top bar with Nesta logo, tool name, and a right-aligned badge."""
    st.markdown(
        f"""
        <div style="
            background-color: #0F294A;
            padding: 14px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            box-sizing: border-box;
        ">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="color: white; font-weight: 700; font-size: 18px;">nesta</span>
                <span style="color: rgba(255,255,255,0.3); font-size: 18px;">|</span>
                <span style="color: white; font-weight: 700; font-size: 20px;">{tool_name}</span>
            </div>
            <div style="
                background-color: #18A48C;
                color: white;
                font-size: 13px;
                padding: 5px 12px;
                white-space: nowrap;
            ">{badge_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_beta_banner(
    message: str = "This tool is in beta. We're still making improvements",
    feedback_link: str = "https://forms.gle/Y191WJrkY2vZzUUX9",
) -> None:
    """Render the bright blue BETA notice banner beneath the top bar, with a
    link to a feedback form.
    """
    st.markdown(
        f"""
        <div style="
            background-color: #0000FF;
            padding: 10px 24px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 12px;
            width: 100%;
            box-sizing: border-box;
        ">
            <span style="
                background-color: white;
                color: #0000FF;
                font-size: 11px;
                font-weight: 700;
                padding: 3px 8px;
                letter-spacing: 0.5px;
            ">BETA</span>
            <span style="color: white; font-size: 13px;">
                {message} &mdash;
                <a href="{feedback_link}" style="color: white; text-decoration: underline; font-weight: 700;">
                    tell us what would make it more useful</a>.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_title(title: str, subtitle: str = "") -> None:
    """Render the large navy page title with a grey subtitle underneath."""
    st.markdown(
        f"""
        <h2 style="
            color:#0F294A;
            font-size: 26px;
            font-weight:600;
            line-height:1.15;
            margin:10px 0 0px 0;
        ">{title}</h2>
        """,
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<div style="color:#666; font-size:16px; margin:0 0 28px 0;">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def render_section_heading(title: str) -> None:
    """Render a bold navy section heading with a thick black underline."""
    st.markdown(
        f"""
        <h3 style="color:#0F294A; font-weight:600; font-size:20px; margin:0 0 -14px 0; line-height:1.2; font-family:'Averta', sans-serif !important;">{title}</h3>
        <hr style="border:none; border-top:3px solid #0F294A; margin:0 0 28px 0;">
        """,
        unsafe_allow_html=True,
    )
