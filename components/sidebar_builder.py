"""Sidebar components: section headers and read-only 'locked' value displays."""

import streamlit as st


def render_sidebar_section_header(title: str, subtitle: str = "") -> None:
    """Render a dark navy section header with top-right and bottom-left corners chamfered."""
    st.markdown(
        f"""
        <div style="
            background-color: #0F294A;
            color: white;
            font-weight: 600;
            font-size: 16px;
            padding: 8px 16px;
            margin: 8px 0 4px 0;
            clip-path: polygon(
                0 0,
                calc(100% - 14px) 0,
                100% 14px,
                100% 100%,
                14px 100%,
                0 calc(100% - 14px)
            );
        ">{title}</div>
        """,
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<div style="font-size:13px; color:#6b6f7a; margin-bottom:10px;">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def render_locked_value(label: str, value: str, caption: str = "") -> None:
    """Render a read-only, greyed-out input box with a 'Locked' pill, matching the mockup."""
    st.markdown(
        f'<div style="font-size:14px; font-weight:600; color:#0F294A; margin-bottom:4px;">{label}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="
            background-color: #DDD9D6;
            border: 1px solid #DDD9D6;
            padding: 8px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        ">
            <span style="font-size: 14px; color: #646363;">{value}</span>
            <span style="font-size: 12px; color: #646363; background: #DDD9D6; padding: 2px 8px;">Locked</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if caption:
        st.markdown(
            f'<div style="font-size:12px; color:#888; margin-bottom:12px;">{caption}</div>',
            unsafe_allow_html=True,
        )
