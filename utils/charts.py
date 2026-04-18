from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


def render_probability_chart(probability_df: pd.DataFrame) -> None:
    chart = (
        alt.Chart(probability_df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Profile:N", sort="-y", title="Predicted profile"),
            y=alt.Y("Percent:Q", title="Probability (%)", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color(
                "Profile:N",
                scale=alt.Scale(
                    domain=["Excluded", "Mobile money only", "Banked"],
                    range=["#b74d4d", "#d89b2b", "#2f7d59"],
                ),
                legend=None,
            ),
            tooltip=["Profile", alt.Tooltip("Percent:Q", format=".1f")],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)


def render_resume_timeline(work_history: list[dict]) -> None:
    rows = []
    for item in work_history:
        rows.append(
            {
                "Organization": item["organization"],
                "Role": item["role"],
                "Start": item["start"],
                "End": item["end"] or "2026-12-31",
                "Period": item["period"],
            }
        )
    df = pd.DataFrame(rows)
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])
    df["Label"] = df["Role"] + " | " + df["Organization"]

    chart = (
        alt.Chart(df)
        .mark_bar(size=22, cornerRadius=6)
        .encode(
            x=alt.X("Start:T", title="Timeline"),
            x2="End:T",
            y=alt.Y("Label:N", sort=None, title="Role"),
            color=alt.Color(
                "Organization:N",
                scale=alt.Scale(range=["#144c73", "#2f7d59", "#b86b00", "#7a4d8b"]),
                legend=alt.Legend(title="Organization"),
            ),
            tooltip=["Organization", "Role", "Period"],
        )
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)


def render_skills_bar_chart(skills: list[str]) -> None:
    groups = pd.DataFrame(
        {
            "Focus area": [
                "Project delivery",
                "Business analysis",
                "Digital banking",
                "Cloud and data",
                "Testing and support",
            ],
            "Weight": [4, 3, 2, 2, 2],
        }
    )

    chart = (
        alt.Chart(groups)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#144c73")
        .encode(
            x=alt.X("Focus area:N", title="Professional focus"),
            y=alt.Y("Weight:Q", title="Relative emphasis"),
            tooltip=["Focus area", "Weight"],
        )
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)


def render_feature_importance_chart(df: pd.DataFrame) -> None:
    if df is None or df.empty:
        st.info("Feature importance data is not available yet. Add the saved artifact CSV to populate this section.")
        return

    columns = {col.lower(): col for col in df.columns}
    feature_col = columns.get("feature")
    importance_col = columns.get("importance") or columns.get("mean_importance")
    if not feature_col or not importance_col:
        st.dataframe(df, use_container_width=True)
        return

    chart_df = df[[feature_col, importance_col]].copy().sort_values(importance_col, ascending=False).head(15)
    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusEnd=5, color="#2f7d59")
        .encode(
            x=alt.X(f"{importance_col}:Q", title="Importance"),
            y=alt.Y(f"{feature_col}:N", sort="-x", title="Feature"),
            tooltip=[feature_col, alt.Tooltip(f"{importance_col}:Q", format=".4f")],
        )
        .properties(height=420)
    )
    st.altair_chart(chart, use_container_width=True)


def render_county_context_chart(df: pd.DataFrame) -> None:
    if df is None or df.empty:
        st.info("County context data is not available yet. Add the county exclusion CSV to show local context here.")
        return

    candidate_county_col = None
    candidate_value_col = None
    for col in df.columns:
        lower = col.lower()
        if candidate_county_col is None and ("county" in lower or "group" in lower):
            candidate_county_col = col
        if candidate_value_col is None and ("percent" in lower or "excluded" in lower or "value" in lower):
            candidate_value_col = col

    if candidate_county_col is None or candidate_value_col is None:
        st.dataframe(df, use_container_width=True)
        return

    chart_df = df[[candidate_county_col, candidate_value_col]].copy().head(10)
    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusEnd=5, color="#b86b00")
        .encode(
            x=alt.X(f"{candidate_value_col}:Q", title="Weighted excluded share"),
            y=alt.Y(f"{candidate_county_col}:N", sort="-x", title="County"),
            tooltip=[candidate_county_col, alt.Tooltip(f"{candidate_value_col}:Q", format=".2f")],
        )
        .properties(height=420)
    )
    st.altair_chart(chart, use_container_width=True)


def render_static_image(path: Path | None, caption: str) -> None:
    if path and path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(f"{caption} is not available yet. Add the saved figure file to the artifacts or figures folder.")
