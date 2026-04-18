from __future__ import annotations

import streamlit as st

from utils.content import CONTACT, CORE_SKILLS, EDUCATION, CERTIFICATIONS, OWNER_NAME, OWNER_TITLE, PROFESSIONAL_SUMMARY, WORK_HISTORY
from utils.ui import configure_page, tags


configure_page(f"{OWNER_NAME} | Resume", icon="🧾")

st.title("Resume")
st.caption(f"{OWNER_NAME} | {OWNER_TITLE}")
st.write(PROFESSIONAL_SUMMARY)
st.write(f"**Phone:** {CONTACT['phone']}")
st.write(f"**Email:** {CONTACT['email']}")

tags(["PRINCE2 Agile", "Business Analysis", "Project Management", "Financial Services", "Data Science"])

left, right = st.columns([0.9, 1.1], gap="large")
with left:
    st.markdown("### Education")
    for entry in EDUCATION:
        with st.container(border=True):
            st.write(entry)

    st.markdown("### Certifications")
    for entry in CERTIFICATIONS:
        with st.container(border=True):
            st.write(entry)

with right:
    st.markdown("### Work Experience / Project Experience")
    for item in WORK_HISTORY:
        with st.container(border=True):
            st.subheader(item["role"])
            org_line = item["organization"]
            if item.get("period"):
                org_line = f"{org_line} | {item['period']}"
            st.caption(org_line)
            for bullet in item["highlights"]:
                st.markdown(f"- {bullet}")

st.markdown("### Technical Skills")
st.markdown("- " + "\n- ".join(CORE_SKILLS))
