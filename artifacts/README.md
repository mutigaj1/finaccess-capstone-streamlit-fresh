# Artifacts folder

Place final trained-model outputs here when you are ready to connect the Streamlit UI to the saved notebook artifacts.

## Recommended files

From the notebook, copy these files here after you generate them:

- `finaccess_final_pipeline.joblib`
- `final_selected_features.joblib`
- `finaccess_final_model_name.txt`
- `final_model_comparison.csv`
- `final_model_feature_importance.csv`
- `subgroup_performance_by_sex.csv`
- `subgroup_performance_by_education.csv`
- `subgroup_performance_by_county.csv`
- `weighted_target_summary_adults.csv`
- `weighted_top_excluded_counties_adults.csv`
- `numeric_outlier_review.csv`
- `numeric_correlations.csv`

## Metadata requirement

To safely run real predictions, also add:

- `feature_metadata.json`

This is important because the app needs the exact training-time category mapping for fields like county, livelihood, education, marital status, internet frequency, and financial health.

If the trained pipeline exists but `feature_metadata.json` is missing, the app will stay in clearly marked stub mode instead of guessing codes.

## Figures

If you saved notebook figures, place them in either:

- `../figures/` in the source project root, or
- `./figures/` inside this app folder

The app looks for files such as:

- `adult_confusion_matrix.png`
- `adult_feature_importance.png`
- `weighted_target_distribution_adults.png`
- `weighted_top_excluded_counties_adults.png`
- `weighted_profile_by_internet_adults.png`
- `weighted_profile_by_financial_health_adults.png`
- `weighted_profile_by_education_adults.png`
- `weighted_profile_by_sex_adults.png`
