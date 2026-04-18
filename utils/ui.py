from __future__ import annotations

import streamlit as st

from utils.content import APP_SUBTITLE, APP_TITLE, CONTACT, OWNER_NAME, OWNER_TITLE


def configure_page(page_title: str, icon: str = "📊") -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_theme()
    render_sidebar()


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            .hero-card, .info-card, .metric-card {
                border: 1px solid rgba(20, 76, 115, 0.12);
                border-radius: 16px;
                padding: 1.2rem 1.2rem;
                background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(247,249,252,0.96));
                box-shadow: 0 10px 25px rgba(17, 24, 39, 0.05);
                margin-bottom: 1rem;
            }
            .section-title {
                font-size: 1.1rem;
                font-weight: 700;
                color: #14324a;
                margin-bottom: 0.5rem;
            }
            .small-muted {
                color: #5f6b7a;
                font-size: 0.92rem;
            }
            .tag {
                display: inline-block;
                padding: 0.25rem 0.6rem;
                border-radius: 999px;
                background: rgba(20, 76, 115, 0.10);
                color: #144c73;
                font-size: 0.85rem;
                font-weight: 600;
                margin-right: 0.4rem;
                margin-bottom: 0.4rem;
            }
            .card-title {
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
                color: #10263a;
            }
            .card-subtitle {
                font-size: 0.95rem;
                color: #506172;
                margin-bottom: 0.7rem;
            }
            .divider-space {
                margin-top: 0.75rem;
                margin-bottom: 0.75rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.markdown(f"## {APP_TITLE}")
    st.sidebar.caption(APP_SUBTITLE)
    st.sidebar.markdown(f"**{OWNER_NAME}**")
    st.sidebar.write(OWNER_TITLE)
    st.sidebar.write(f"📧 {CONTACT['email']}")
    st.sidebar.write(f"📞 {CONTACT['phone']}")
    st.sidebar.info(
        "Use the Streamlit page navigation in the sidebar to move between app, Resume, General Projects, and FinAccess Project."
    )


def card(title: str, body: str, subtitle: str | None = None) -> None:
    subtitle_html = f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-title">{title}</div>
            {subtitle_html}
            <div>{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tags(items: list[str]) -> None:
    html = "".join([f'<span class="tag">{item}</span>' for item in items])
    st.markdown(html, unsafe_allow_html=True)


def metric_card(label: str, value: str, help_text: str | None = None) -> None:
    help_html = f'<div class="small-muted">{help_text}</div>' if help_text else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="small-muted">{label}</div>
            <div style="font-size:1.6rem;font-weight:700;color:#10263a;">{value}</div>
            {help_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
