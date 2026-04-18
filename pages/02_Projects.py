from __future__ import annotations

import streamlit as st

from utils.content import OWNER_NAME, PROJECT_CARDS
from utils.ui import configure_page, tags


configure_page(f"{OWNER_NAME} | Projects", icon="📁")

st.title("Projects")
st.caption("A portfolio-style summary of capstone and professional project themes")

st.write(
    "This page keeps the portfolio professional and presentation-friendly. The capstone is highlighted, and the other cards give room for broader delivery, business analysis, and data work without linking to public assignment solutions."
)

tags(["Capstone", "AML", "Digital banking", "Azure", "Delivery portfolio"])

primary, secondary = st.columns([1.15, 0.85], gap="large")
with primary:
    featured = PROJECT_CARDS[0]
    with st.container(border=True):
        st.subheader(featured["title"])
        st.caption(f"{featured['tag']} | {featured['status']}")
        st.write(featured["summary"])
        st.success(
            "Recommended talking point: this project combines a real Kenya dataset, interpretable modeling, evaluation, and a usable local web interface."
        )
with secondary:
    st.markdown("### Portfolio positioning")
    st.write(
        "Together, these cards show a profile that spans project leadership, business analysis, compliance and AML delivery, digital channels, and applied analytics."
    )

st.markdown("### Project cards")
rows = [PROJECT_CARDS[1:3], PROJECT_CARDS[3:]]
for card_row in rows:
    cols = st.columns(len(card_row), gap="large")
    for col, item in zip(cols, card_row):
        with col:
            with st.container(border=True):
                st.subheader(item["title"])
                st.caption(f"{item['tag']} | {item['status']}")
                st.write(item["summary"])
                st.write("**Link status:** Placeholder summary card, no public link attached.")

st.markdown("### Portfolio use")
st.info(
    "If you want to refine this page manually, the next best upgrade is adding 1 or 2 outcome metrics or screenshots for each professional card while keeping any sensitive or internal material private."
)
