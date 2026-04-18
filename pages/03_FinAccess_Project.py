from __future__ import annotations

import streamlit as st

from utils.artifacts import (
    figure_or_none,
    get_fallback_model_comparison,
    get_metadata_label,
    get_metadata_options,
    get_reference_files,
    load_artifact_bundle,
    read_binary,
    table_or_none,
)
from utils.charts import (
    render_county_context_chart,
    render_feature_importance_chart,
    render_probability_chart,
    render_static_image,
)
from utils.content import CAPSTONE_METRICS, OWNER_NAME
from utils.prediction import build_plain_language_explanation, format_probability_output, generate_prediction, validate_inputs
from utils.ui import configure_page, metric_card


configure_page(f"{OWNER_NAME} | FinAccess Project", icon="📈")

bundle = load_artifact_bundle()
metadata = bundle.metadata
current_best_model = bundle.model_name if bundle.prediction_mode == "artifact" else CAPSTONE_METRICS["best_model"]


def _select_from_metadata(field_name: str, *, default_index: int = 0, help_text: str | None = None):
    options = get_metadata_options(metadata, field_name)
    labels = [item["label"] for item in options]
    if not labels:
        st.error(f"No options are configured for {field_name}. Add them to feature_metadata.json.")
        return None

    selected_label = st.selectbox(
        get_metadata_label(metadata, field_name),
        options=labels,
        index=min(default_index, len(labels) - 1),
        help=help_text,
    )
    mapping = {item["label"]: item["value"] for item in options}
    return mapping[selected_label]


st.title("FinAccess Project")
st.caption(
    "This page is the interactive prediction tool for the FinAccess 2024 capstone. Enter a respondent profile below to estimate whether the person is most likely to be Excluded, Mobile money only, or Banked. Use the tabs below to explore model interpretation, comparisons, county context, and supporting downloads."
)
st.page_link("app.py", label="Read the full project story on app")

metrics = st.columns(5)
with metrics[0]:
    metric_card("Survey size", CAPSTONE_METRICS["dataset_responses"])
with metrics[1]:
    metric_card("Fields", CAPSTONE_METRICS["dataset_fields"])
with metrics[2]:
    metric_card("Main sample", CAPSTONE_METRICS["main_sample"])
with metrics[3]:
    metric_card("Current best model", current_best_model)
with metrics[4]:
    metric_card("Macro F1", f"{CAPSTONE_METRICS['macro_f1']:.4f}")

if bundle.prediction_mode == "artifact":
    st.success(f"Artifact-backed prediction is active. Model: {bundle.model_name}.")
else:
    st.info(
        "The prediction interface is active in stub mode. This keeps the fresh app runnable locally even before the final model artifacts are connected."
    )

for warning in bundle.warnings:
    st.warning(warning)

if bundle.errors:
    with st.expander("Artifact loading notes"):
        for error in bundle.errors:
            st.error(error)

left, right = st.columns([1.05, 0.95], gap="large")
with left:
    st.markdown("### Prediction interface")
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            county = _select_from_metadata("county")
            sex = _select_from_metadata("sex")
            age_years = st.number_input("Age", min_value=18, max_value=105, value=30, step=1)
            household_size = st.number_input("Household size", min_value=1, max_value=20, value=4, step=1)
        with col2:
            education = _select_from_metadata("education")
            marital_status = _select_from_metadata("marital_status")
            children_in_household = st.number_input("Number of children in household", min_value=0, max_value=19, value=2, step=1)
            livelihood = _select_from_metadata("livelihood")
        with col3:
            can_access_internet = _select_from_metadata("can_access_internet")
            internet_frequency = _select_from_metadata(
                "internet_frequency",
                help_text="If the respondent does not have internet access, the selected frequency is treated as a simple profile input for this educational UI.",
            )
            financial_health = _select_from_metadata("financial_health")

        submitted = st.form_submit_button("Generate prediction", type="primary")

    if submitted:
        ui_inputs = {
            "county": county,
            "sex": sex,
            "age_years": int(age_years),
            "household_size": int(household_size),
            "education": education,
            "marital_status": marital_status,
            "children_in_household": int(children_in_household),
            "livelihood": livelihood,
            "can_access_internet": can_access_internet,
            "internet_frequency": internet_frequency,
            "financial_health": financial_health,
        }

        issues = validate_inputs(ui_inputs)
        if issues:
            for issue in issues:
                st.error(issue)
        else:
            prediction = generate_prediction(bundle, ui_inputs)
            probability_df = format_probability_output(prediction["probabilities"])
            st.success(f"Predicted class: **{prediction['predicted_class']}**")
            st.write(build_plain_language_explanation(ui_inputs, prediction))
            st.caption(prediction["note"])
            st.dataframe(probability_df[["Profile", "Percent"]], use_container_width=True, hide_index=True)
            render_probability_chart(probability_df)

with right:
    st.markdown("### Quick context")
    st.write(
        "This page is meant to feel like the working tool. Use the form to generate a prediction, then use the tabs below to review interpretation, comparison, county context, and downloads."
    )
    st.warning(
        "This is a capstone prediction and interpretation tool. Do not use it for customer-level decisions, policy actions, or causal claims."
    )

tabs = st.tabs(["Model interpretation", "Model comparison", "County view", "Downloads and limitations"])

with tabs[0]:
    st.write("This section shows which inputs matter most in the current workflow and includes key diagnostic visuals when available.")
    render_static_image(figure_or_none(bundle, "feature_importance"), "Permutation importance / feature importance")
    render_feature_importance_chart(table_or_none(bundle, "feature_importance"))
    st.markdown("### Confusion matrix")
    render_static_image(figure_or_none(bundle, "confusion_matrix"), "Confusion matrix")

with tabs[1]:
    comparison_df = table_or_none(bundle, "model_comparison")
    if comparison_df is None:
        comparison_df = get_fallback_model_comparison()
        st.info("Using the built-in comparison summary because the final model comparison artifact has not been added yet.")
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    if {"Model", "Macro F1", "Balanced Accuracy"}.issubset(comparison_df.columns):
        chart_df = comparison_df[["Model", "Macro F1", "Balanced Accuracy"]].set_index("Model")
    elif {"model", "test_macro_f1", "test_balanced_accuracy"}.issubset(comparison_df.columns):
        chart_df = comparison_df[["model", "test_macro_f1", "test_balanced_accuracy"]].rename(
            columns={"model": "Model", "test_macro_f1": "Macro F1", "test_balanced_accuracy": "Balanced Accuracy"}
        ).set_index("Model")
    else:
        chart_df = None

    if chart_df is not None:
        st.bar_chart(chart_df)

with tabs[2]:
    county_df = table_or_none(bundle, "county_exclusion")
    render_county_context_chart(county_df)
    render_static_image(figure_or_none(bundle, "county_context"), "Top counties by weighted exclusion share")

with tabs[3]:
    for item in get_reference_files():
        with st.container(border=True):
            st.write(f"**{item['label']}**")
            st.caption(item["category"])
            file_bytes = read_binary(item["path"]) if item["path"] else None
            if file_bytes is not None and item["path"] is not None:
                st.download_button(
                    label=f"Download {item['label']}",
                    data=file_bytes,
                    file_name=item["path"].name,
                    mime=item["mime"],
                    key=f"download_{item['label']}",
                    use_container_width=True,
                )
            else:
                st.download_button(
                    label=f"Unavailable: {item['label']}",
                    data=b"",
                    file_name="unavailable.txt",
                    disabled=True,
                    key=f"download_disabled_{item['label']}",
                    use_container_width=True,
                )

    st.markdown("### Limitations")
    st.write("- This project focuses on prediction and interpretation, not causation.")
    st.write("- The Banked class can include respondents who also use mobile money.")
    st.write("- This is an educational capstone interface, not a production decision system.")
