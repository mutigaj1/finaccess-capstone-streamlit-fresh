from __future__ import annotations

from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROJECT_ROOT = APP_ROOT.parent

ASSETS_DIR = APP_ROOT / "assets"
LOCAL_ARTIFACTS_DIR = APP_ROOT / "artifacts"
SOURCE_ARTIFACTS_DIR = SOURCE_PROJECT_ROOT / "artifacts"
LOCAL_FIGURES_DIR = APP_ROOT / "figures"
SOURCE_FIGURES_DIR = SOURCE_PROJECT_ROOT / "figures"

PROFILE_IMAGE = ASSETS_DIR / "profile_placeholder.svg"
PROFESSIONAL_INFOGRAPHIC = ASSETS_DIR / "professional_focus.svg"

SOURCE_NOTEBOOK = SOURCE_PROJECT_ROOT / "FINACCESS_MASTER_PROJECT_NOTEBOOK.ipynb"
SOURCE_PROPOSAL_DOCX = SOURCE_PROJECT_ROOT / "Mutiga Proposal Feedback 2 updated.docx"
SOURCE_GUIDELINES_DOCX = SOURCE_PROJECT_ROOT / "_Project Guidelines- Machine Learning Project.docx"
SOURCE_MANUAL_PDF = SOURCE_PROJECT_ROOT / "FinAccess 2024 Manual.pdf"
SOURCE_QUESTIONNAIRE_PDF = SOURCE_PROJECT_ROOT / "2024 FinAccess Questionnaire.pdf"
SOURCE_DATA_FILE = SOURCE_PROJECT_ROOT / "2024_Finaccess_Publicdata.dta"

EXPECTED_ARTIFACT_FILENAMES = {
    "pipeline": "finaccess_final_pipeline.joblib",
    "selected_features": "final_selected_features.joblib",
    "model_name": "finaccess_final_model_name.txt",
    "feature_metadata": "feature_metadata.json",
    "model_comparison": "final_model_comparison.csv",
    "feature_importance": "final_model_feature_importance.csv",
    "subgroup_sex": "subgroup_performance_by_sex.csv",
    "subgroup_education": "subgroup_performance_by_education.csv",
    "subgroup_county": "subgroup_performance_by_county.csv",
    "county_exclusion": "weighted_top_excluded_counties_adults.csv",
    "target_summary": "weighted_target_summary_adults.csv",
    "correlations": "numeric_correlations.csv",
    "outlier_review": "numeric_outlier_review.csv",
}

EXPECTED_FIGURE_FILENAMES = {
    "confusion_matrix": "adult_confusion_matrix.png",
    "feature_importance": "adult_feature_importance.png",
    "target_distribution": "weighted_target_distribution_adults.png",
    "county_context": "weighted_top_excluded_counties_adults.png",
    "internet_profile": "weighted_profile_by_internet_adults.png",
    "financial_health_profile": "weighted_profile_by_financial_health_adults.png",
    "education_profile": "weighted_profile_by_education_adults.png",
    "sex_profile": "weighted_profile_by_sex_adults.png",
}
