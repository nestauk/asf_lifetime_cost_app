"""Functions to render output sections for the Subsidy Solver page."""

import pandas as pd
import streamlit as st

from components.layout import render_section_heading
from results.charts import build_required_subsidy_chart


def render_required_subsidy_chart_section(required_subsidy_df: pd.DataFrame) -> None:
    render_section_heading("Subsidy needed to reach parity, by installation year")

    with st.container(border=True):
        st.markdown(
            '<div style="font-size:14px; font-weight:700; color:#0F294A; margin-bottom:12px;">'
            "Installation year (2026–2035) against required subsidy (£)</div>",
            unsafe_allow_html=True,
        )
        chart = build_required_subsidy_chart(required_subsidy_df)
        st.altair_chart(chart, width="stretch")

        with st.expander("▾ View underlying data"):
            st.dataframe(required_subsidy_df, width="stretch")
            st.download_button(
                "⬇ Export CSV",
                data=required_subsidy_df.to_csv(index=False),
                file_name="required_subsidy_by_installation_year.csv",
                mime="text/csv",
            )
