from __future__ import annotations

import streamlit as st

from utils.charts import render_resume_timeline, render_skills_bar_chart
from utils.config import PROFILE_IMAGE
from utils.content import (
    ACCOMPLISHMENTS,
    CONTACT,
    CORE_SKILLS,
    EDUCATION,
    OWNER_NAME,
    OWNER_TITLE,
    PROFESSIONAL_SUMMARY,
    CERTIFICATIONS,
    WORK_HISTORY,
)
from utils.ui import configure_page, tags


configure_page(f"{OWNER_NAME} | Resume", icon="🧾")

st.title("Resume")
st.caption(f"{OWNER_NAME} | {OWNER_TITLE}")

intro_col, image_col = st.columns([1.5, 0.85], gap="large")
with intro_col:
    st.markdown("### Professional summary")
    st.write(PROFESSIONAL_SUMMARY)
    st.write(f"**Phone:** {CONTACT['phone']}")
    st.write(f"**Email:** {CONTACT['email']}")
    tags(["PRINCE2 Agile", "Business Analysis", "Data Science", "Financial Services", "Delivery Leadership"])
with image_col:
    st.image(str(PROFILE_IMAGE), use_container_width=True)

st.markdown("### Core skills")
st.markdown("- " + "\n- ".join(CORE_SKILLS))

chart_left, chart_right = st.columns(2, gap="large")
with chart_left:
    st.markdown("### Career timeline")
    render_resume_timeline(WORK_HISTORY)
with chart_right:
    st.markdown("### Professional focus graphic")
    render_skills_bar_chart(CORE_SKILLS)

st.markdown("### Work experience")
for item in WORK_HISTORY:
    with st.container(border=True):
        st.subheader(item["role"])
        st.caption(f"{item['organization']} | {item['period']}")
        for bullet in item["highlights"]:
            st.markdown(f"- {bullet}")

edu_col, cert_col = st.columns(2, gap="large")
with edu_col:
    st.markdown("### Education")
    for entry in EDUCATION:
        st.markdown(f"- {entry}")
with cert_col:
    st.markdown("### Certifications")
    for entry in CERTIFICATIONS:
        st.markdown(f"- {entry}")

st.markdown("### Key accomplishments")
for item in ACCOMPLISHMENTS:
    st.markdown(f"- {item}")

st.markdown("### Notes")
st.info(
    "If you want this page to look more personal before submission, the easiest manual upgrade is to replace the placeholder image with a headshot or branded resume graphic."
)
