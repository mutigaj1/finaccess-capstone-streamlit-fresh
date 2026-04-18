from __future__ import annotations

import streamlit as st

from utils.artifacts import load_artifact_bundle
from utils.content import APP_SUBTITLE, CAPSTONE_METRICS, CONTACT, OWNER_NAME, OWNER_TITLE
from utils.ui import configure_page, metric_card


configure_page(f"{OWNER_NAME} | app", icon="🏠")

bundle = load_artifact_bundle()
current_best_model = bundle.model_name if bundle.prediction_mode == "artifact" else CAPSTONE_METRICS["best_model"]

st.title("Predicting Financial Access Profiles in Kenya Using FinAccess 2024")
st.caption(APP_SUBTITLE)

st.markdown("### 1. What this project is")
st.write(
    "This project is a DTSC 691 Applied Data Science capstone built around one practical question: can a small set "
    "of interpretable survey features be used to estimate a respondent’s current financial access profile in Kenya? "
    "The app turns that analysis into a guided, human-readable experience instead of leaving the work buried inside a notebook."
)

metric_cols = st.columns(4)
with metric_cols[0]:
    metric_card("Dataset", "FinAccess 2024 public survey")
with metric_cols[1]:
    metric_card("Responses", CAPSTONE_METRICS["dataset_responses"])
with metric_cols[2]:
    metric_card("Fields", CAPSTONE_METRICS["dataset_fields"])
with metric_cols[3]:
    metric_card("Counties", "47")

st.markdown("### 2. The problem")
st.write(
    "The project focuses on predicting whether an adult respondent is most likely to be **Excluded**, **Mobile money only**, or **Banked**. "
    "The goal is not to make a production decision system for real customers. The goal is to study patterns in financial access and explain them clearly."
)

st.markdown("### 3. Why this matters in Kenya")
st.write(
    "Kenya is widely known for mobile money adoption, but financial access is still uneven. Some people remain excluded, some rely mainly on mobile money, and others have stronger access to bank services. "
    "Using a Kenya-specific public survey makes the capstone more meaningful than a generic classroom dataset."
)

st.markdown("### 4. The data")
st.write(
    "The project uses the **FinAccess 2024 public survey for Kenya**. The full public dataset contains **20,871 responses** and **3,816 fields**. "
    "For the main modeling workflow, the analysis focuses on adults aged 18 and above and uses a compact feature set that is easier to explain and deploy."
)

st.markdown("### 5. The target and features")
left, right = st.columns([0.9, 1.1], gap="large")
with left:
    st.markdown("**Target classes**")
    st.write("- Excluded")
    st.write("- Mobile money only")
    st.write("- Banked")
with right:
    st.markdown("**11-feature compact workflow**")
    st.write(
        "- county\n"
        "- sex\n"
        "- age\n"
        "- household size\n"
        "- education\n"
        "- marital status\n"
        "- number of children in household\n"
        "- livelihood\n"
        "- internet access\n"
        "- internet frequency\n"
        "- financial health"
    )
    st.caption(
        "Target-defining fields such as current mobile money use and current bank use are intentionally excluded from the predictors to avoid leakage."
    )

st.markdown("### 6. The modeling approach")
st.write(
    "At a high level, the workflow includes weighted exploratory data analysis, preprocessing, model comparison, tuning, evaluation, interpretation, and deployment. "
    "The app reflects the compact 11-feature workflow described in the approved proposal and notebook outputs."
)
st.write(
    "Missing values such as survey nonresponse codes are handled during preprocessing, numeric inputs are imputed with medians, categorical inputs are imputed with most-frequent values, and multiple models are compared before selecting the strongest current one."
)

st.markdown("### 7. What the analysis showed")
result_cols = st.columns(4)
with result_cols[0]:
    metric_card("Current best model", current_best_model)
with result_cols[1]:
    metric_card("Macro F1", f"{CAPSTONE_METRICS['macro_f1']:.4f}")
with result_cols[2]:
    metric_card("Balanced accuracy", f"{CAPSTONE_METRICS['balanced_accuracy']:.4f}")
with result_cols[3]:
    metric_card("Main sample", CAPSTONE_METRICS["main_sample"])

st.write(
    "The strongest current model in the project is **Gradient Boosting**, unless saved artifacts indicate a different trained model is active. "
    "The results should be interpreted as pattern-based prediction results from a public survey, not as proof that one variable causes another."
)

st.markdown("### 8. What the app does")
st.write(
    "This multipage app separates the capstone into clear roles. This page explains the full story. The Resume page presents the professional profile. The General Projects page holds broader portfolio material. The FinAccess Project page is the actual interactive prediction tool."
)

st.markdown("### 9. How to use the FinAccess Project page")
st.write("1. Open **FinAccess Project** from the sidebar or the button below.")
st.write("2. Enter a respondent profile using the survey-style form.")
st.write("3. Generate a prediction to estimate the most likely financial access class.")
st.write("4. Review the probability output and the plain-language interpretation.")
st.write("5. Use the tabs on that page to explore model interpretation, comparison, county context, and downloads.")

st.markdown("### 10. Open the project")
st.page_link("pages/03_FinAccess_Project.py", label="Open the FinAccess Project page")

st.info(
    f"Contact: {CONTACT['email']} | {CONTACT['phone']} | {OWNER_TITLE}"
)
