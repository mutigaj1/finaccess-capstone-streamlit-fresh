from __future__ import annotations

import streamlit as st

from utils.artifacts import load_artifact_bundle
from utils.charts import render_skills_bar_chart
from utils.config import PROFILE_IMAGE, PROFESSIONAL_INFOGRAPHIC
from utils.content import (
    ACADEMIC_BACKGROUND,
    APP_SUBTITLE,
    CAREER_ASPIRATIONS,
    CAPSTONE_METRICS,
    HOME_INTRO,
    OWNER_NAME,
    OWNER_TITLE,
    PROFESSIONAL_INTERESTS,
    PROFESSIONAL_SUMMARY,
)
from utils.ui import card, configure_page, metric_card, tags


configure_page(f"{OWNER_NAME} | Home", icon="🏠")

bundle = load_artifact_bundle()

st.title(OWNER_NAME)
st.caption(f"{OWNER_TITLE} | {APP_SUBTITLE}")

hero_left, hero_right = st.columns([1.35, 1], gap="large")
with hero_left:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown("### About Me")
    st.write(HOME_INTRO)
    st.write(PROFESSIONAL_SUMMARY)
    tags([
        "Project delivery",
        "Business analysis",
        "Applied data science",
        "Financial services",
        "Digital transformation",
    ])
    st.markdown('</div>', unsafe_allow_html=True)
with hero_right:
    st.image(str(PROFILE_IMAGE), use_container_width=True)

st.markdown("### Snapshot")
metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Current role", OWNER_TITLE)
with metric_cols[1]:
    metric_card("Best current capstone model", CAPSTONE_METRICS["best_model"])
with metric_cols[2]:
    metric_card("Reported macro F1", f"{CAPSTONE_METRICS['macro_f1']:.4f}")
with metric_cols[3]:
    metric_card("Main sample", CAPSTONE_METRICS["main_sample"])

section_left, section_right = st.columns([1.1, 1], gap="large")
with section_left:
    card(
        "Academic background",
        "<ul>" + "".join([f"<li>{item}</li>" for item in ACADEMIC_BACKGROUND]) + "</ul>",
        subtitle="Study profile",
    )
    card(
        "Career direction",
        "<ul>" + "".join([f"<li>{item}</li>" for item in CAREER_ASPIRATIONS]) + "</ul>",
        subtitle="Professional positioning based on the supplied resume and project context",
    )
with section_right:
    card(
        "Professional interests",
        "<ul>" + "".join([f"<li>{item}</li>" for item in PROFESSIONAL_INTERESTS]) + "</ul>",
        subtitle="Where Jesse’s portfolio work is heading",
    )
    st.image(str(PROFESSIONAL_INFOGRAPHIC), use_container_width=True)

st.markdown("### Why this portfolio app exists")
st.write(
    "This fresh Streamlit build presents Jesse’s professional profile and capstone in one place. It is meant to be understandable "
    "to non-technical readers while still giving enough structure for a mentor, instructor, or reviewer to explore the project clearly."
)

st.markdown("### Current app status")
if bundle.prediction_mode == "artifact":
    st.success(
        f"Artifact-backed prediction is active. Loaded model: {bundle.model_name}. Metadata source: {bundle.metadata_source}."
    )
else:
    st.info(
        "The app is fully runnable right now. Prediction uses a clearly marked stub fallback until the final trained pipeline and aligned feature metadata are added."
    )

if bundle.warnings:
    for warning in bundle.warnings:
        st.warning(warning)

if bundle.errors:
    with st.expander("Artifact loading notes"):
        for error in bundle.errors:
            st.error(error)

st.markdown("### Next pages")
st.write(
    "Use the sidebar to move to the Resume page for experience details, the Projects page for a broader portfolio view, and the Capstone Project page for the model narrative, prediction interface, diagnostics, county context, and downloads."
)
