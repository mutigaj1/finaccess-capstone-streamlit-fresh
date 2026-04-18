from __future__ import annotations

import streamlit as st

from utils.content import PROJECT_CARDS
from utils.ui import configure_page, tags


configure_page("General Projects", icon="📁")

st.title("General Projects")
st.caption("Portfolio and supporting materials related to the DTSC 691 capstone")

st.write(
    "This page stays light on purpose. It is here to show the broader portfolio context and supporting project material without turning into another copy of the capstone story page."
)

tags(["Capstone", "AML", "Digital banking", "Azure", "Portfolio"])

featured = PROJECT_CARDS[0]
with st.container(border=True):
    st.subheader(featured["title"])
    st.caption(f"{featured['tag']} | {featured['status']}")
    st.write(featured["summary"])
    st.page_link("pages/03_FinAccess_Project.py", label="Open in this app")

st.markdown("### Other project themes")
for item in PROJECT_CARDS[1:]:
    with st.container(border=True):
        st.subheader(item["title"])
        st.caption(f"{item['tag']} | {item['status']}")
        st.write(item["summary"])

st.info(
    "If you want to polish this page later, the easiest upgrade is to add one or two outcome metrics or screenshots for each portfolio item while keeping any sensitive work private."
)
