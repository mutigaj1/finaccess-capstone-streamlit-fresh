from __future__ import annotations

from pathlib import Path

import pandas as pd
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
from utils.content import CAPSTONE_METRICS, CAPSTONE_OVERVIEW, OWNER_NAME
from utils.prediction import (
    build_plain_language_explanation,
    format_probability_output,
    generate_prediction,
    validate_inputs,
)
from utils.ui import configure_page, metric_card


configure_page(f"{OWNER_NAME} | Capstone Project", icon="📈")

bundle = load_artifact_bundle()
metadata = bundle.metadata


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


st.title(CAPSTONE_OVERVIEW["title"])
st.caption("DTSC 691 Applied Data Science | Fresh local Streamlit build")

metrics = st.columns(6)
with metrics[0]:
    metric_card("Survey size", CAPSTONE_METRICS["dataset_responses"])
with metrics[1]:
    metric_card("Fields", CAPSTONE_METRICS["dataset_fields"])
with metrics[2]:
    metric_card("Main sample", CAPSTONE_METRICS["main_sample"])
with metrics[3]:
    metric_card("Best current model", CAPSTONE_METRICS["best_model"])
with metrics[4]:
    metric_card("Macro F1", f"{CAPSTONE_METRICS['macro_f1']:.4f}")
with metrics[5]:
    metric_card("Balanced accuracy", f"{CAPSTONE_METRICS['balanced_accuracy']:.4f}")

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

overview_tab, predict_tab, diagnostics_tab, county_tab, downloads_tab = st.tabs(
    ["Overview", "Predict", "Diagnostics", "County Context", "Downloads"]
)

with overview_tab:
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.markdown("### Business problem")
        st.write(CAPSTONE_OVERVIEW["problem"])

        st.markdown("### Why it matters in Kenya")
        st.write(CAPSTONE_OVERVIEW["why_it_matters"])

        st.markdown("### Target classes")
        for label in CAPSTONE_OVERVIEW["target_classes"]:
            st.markdown(f"- **{label}**")

        st.markdown("### Modeling approach")
        for item in CAPSTONE_OVERVIEW["modeling_approach"]:
            st.markdown(f"- {item}")

    with right:
        st.markdown("### What the current results mean")
        for item in CAPSTONE_OVERVIEW["results_summary"]:
            st.markdown(f"- {item}")

        st.markdown("### Important limits")
        for item in CAPSTONE_OVERVIEW["limitations"]:
            st.markdown(f"- {item}")

        st.warning(
            "This project is a prediction and interpretation exercise. It is not a causal analysis, and it should not be used as a production decision-making system."
        )

    st.markdown("### Interpretable predictors used in the app")
    st.markdown(
        "- County\n"
        "- Sex\n"
        "- Age\n"
        "- Household size\n"
        "- Education\n"
        "- Marital status\n"
        "- Number of children in household\n"
        "- Livelihood\n"
        "- Internet access\n"
        "- Internet frequency\n"
        "- Financial health"
    )

    st.markdown("### Leakage avoidance")
    st.write(
        "Target-defining fields such as current mobile money use and current bank use are intentionally excluded from the predictors so the model is not simply learning the answer directly."
    )

with predict_tab:
    st.markdown("### Interactive prediction interface")
    st.write(
        "Enter a profile below to generate a predicted financial access class, probability view, and plain-language explanation."
    )

    if metadata.get("fields", {}).get("livelihood", {}).get("is_grouped_placeholder"):
        st.info(
            "The fallback livelihood labels are grouped for UI clarity. When you connect the final saved pipeline, replace them with your exact training-time metadata mapping."
        )

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            county = _select_from_metadata("county")
            sex = _select_from_metadata("sex")
            age_years = st.number_input(
                "Age",
                min_value=18,
                max_value=105,
                value=30,
                step=1,
                help="Main analysis is restricted to adults aged 18 and above.",
            )
            household_size = st.number_input(
                "Household size",
                min_value=1,
                max_value=20,
                value=4,
                step=1,
            )
        with col2:
            education = _select_from_metadata("education")
            marital_status = _select_from_metadata("marital_status")
            children_in_household = st.number_input(
                "Number of children in household",
                min_value=0,
                max_value=19,
                value=2,
                step=1,
            )
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

            result_left, result_right = st.columns([0.9, 1.1], gap="large")
            with result_left:
                st.success(f"Predicted class: **{prediction['predicted_class']}**")
                st.write(build_plain_language_explanation(ui_inputs, prediction))
                st.caption(prediction["note"])
                st.warning(
                    "Educational capstone tool only. Do not use this output for customer-level decisions or policy actions without deeper validation."
                )
                st.dataframe(probability_df[["Profile", "Percent"]], use_container_width=True, hide_index=True)
            with result_right:
                render_probability_chart(probability_df)

with diagnostics_tab:
    st.markdown("### Model comparison summary")
    comparison_df = table_or_none(bundle, "model_comparison")
    if comparison_df is None:
        comparison_df = get_fallback_model_comparison()
        st.info("Using a built-in summary because final_model_comparison.csv has not been added yet.")
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    diag_left, diag_right = st.columns(2, gap="large")
    with diag_left:
        st.markdown("### Confusion matrix")
        render_static_image(figure_or_none(bundle, "confusion_matrix"), "Confusion matrix")
    with diag_right:
        st.markdown("### Permutation importance")
        render_feature_importance_chart(table_or_none(bundle, "feature_importance"))

    st.markdown("### Subgroup performance")
    subgroup_tabs = st.tabs(["By sex", "By education", "By county"])
    subgroup_map = {
        "By sex": "subgroup_sex",
        "By education": "subgroup_education",
        "By county": "subgroup_county",
    }
    for tab, label in zip(subgroup_tabs, subgroup_map.keys()):
        with tab:
            df = table_or_none(bundle, subgroup_map[label])
            if df is None or df.empty:
                st.info(f"{label} subgroup results are not available yet. Add the saved CSV artifact to populate this section.")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Additional diagnostics")
    corr_df = table_or_none(bundle, "correlations")
    outlier_df = table_or_none(bundle, "outlier_review")
    add_left, add_right = st.columns(2, gap="large")
    with add_left:
        st.markdown("#### Numeric correlation review")
        if corr_df is None or corr_df.empty:
            st.info("Numeric correlation output is not available yet.")
        else:
            st.dataframe(corr_df, use_container_width=True)
    with add_right:
        st.markdown("#### Numeric outlier review")
        if outlier_df is None or outlier_df.empty:
            st.info("Numeric outlier review is not available yet.")
        else:
            st.dataframe(outlier_df, use_container_width=True, hide_index=True)

with county_tab:
    st.markdown("### County-level context")
    st.write(
        "This section is meant to show how exclusion varies across counties using saved notebook outputs. It works best once the weighted county CSV and figure are added."
    )
    county_df = table_or_none(bundle, "county_exclusion")
    render_county_context_chart(county_df)
    render_static_image(figure_or_none(bundle, "county_context"), "Top counties by weighted exclusion share")

with downloads_tab:
    st.markdown("### Available downloads")
    st.write(
        "Buttons below activate when the corresponding file exists. This includes source project files and any notebook-generated artifacts you later add to the app."
    )

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

    st.markdown("### Artifact placement reminder")
    st.info(
        "For final artifact-backed prediction, place the trained pipeline, selected features, model-name text file, and feature_metadata.json inside this app’s artifacts folder or the source project’s artifacts folder."
    )
