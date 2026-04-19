# FinAccess 2024 Capstone Streamlit App

A completely fresh Streamlit portfolio app for the DTSC 691 Applied Data Science capstone project.

## Project title

**Predicting Financial Access Profiles in Kenya Using FinAccess 2024**

## What this app includes

- An **app / project story** page
- A **Resume** page
- A **General Projects** page
- A **FinAccess Project** page with:
  - plain-language project narrative
  - interactive prediction form
  - prediction result summary
  - probability chart
  - diagnostics placeholders or live artifact rendering
  - county-level context section
  - downloads section

## Design intent

This app was built as a new greenfield project with a clean file structure and without reusing prior Streamlit UI code.

## Local project structure

```text
finaccess_capstone_streamlit_fresh/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── assets/
│   ├── profile_placeholder.svg
│   └── professional_focus.svg
├── artifacts/
│   ├── README.md
│   └── feature_metadata.template.json
├── figures/
│   └── README.md
├── pages/
│   ├── 01_Resume.py
│   ├── 02_General_Projects.py
│   └── 03_FinAccess_Project.py
└── utils/
    ├── __init__.py
    ├── artifacts.py
    ├── charts.py
    ├── config.py
    ├── content.py
    ├── prediction.py
    └── ui.py
```

## Run locally

### 1. Open a terminal in this folder

```bash
cd "C:\Users\jesse\OneDrive - eastern.edu\DTSC 691\final project\finaccess_capstone_streamlit_fresh"
```

### 2. Create and activate a virtual environment (recommended)

**PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run app.py
```

## Prediction modes

### Stub mode

The app is runnable immediately in **stub mode**.

That means:
- the UI works
- the form validates inputs
- the result area renders
- the probabilities come from a clearly marked fallback heuristic
- the app does **not** pretend the fallback is the trained model

### Artifact-backed mode

To enable real trained-model prediction, add the final notebook outputs to the app.

## Where to place model artifacts

Place them in either:

- `./artifacts/` inside this app folder, or
- `../artifacts/` in the parent project folder if you prefer to keep notebook outputs there

Recommended files:

- `finaccess_final_pipeline.joblib`
- `final_selected_features.joblib`
- `finaccess_final_model_name.txt`
- `feature_metadata.json`
- `final_model_comparison.csv`
- `final_model_feature_importance.csv`
- `subgroup_performance_by_sex.csv`
- `subgroup_performance_by_education.csv`
- `subgroup_performance_by_county.csv`
- `weighted_target_summary_adults.csv`
- `weighted_top_excluded_counties_adults.csv`
- `numeric_outlier_review.csv`
- `numeric_correlations.csv`

### Important metadata note

The app will only use the real pipeline for prediction when **both** of these are present:

- the saved pipeline file
- `feature_metadata.json`

This is intentional. It avoids category-code mismatches for fields like county, livelihood, and education.

Use `artifacts/feature_metadata.template.json` as your starting template.

## Figures the app can render if available

Place these in `./figures/` or `../figures/`:

- `adult_confusion_matrix.png`
- `adult_feature_importance.png`
- `weighted_target_distribution_adults.png`
- `weighted_top_excluded_counties_adults.png`
- `weighted_profile_by_internet_adults.png`
- `weighted_profile_by_financial_health_adults.png`
- `weighted_profile_by_education_adults.png`
- `weighted_profile_by_sex_adults.png`

## Source project files the app can expose in Downloads

If these exist in the parent project folder, the app can surface them as downloads:

- notebook
- proposal update docx
- project guidelines docx
- FinAccess manual pdf
- FinAccess questionnaire pdf
- source survey data file

## Content used in this build

This fresh app reflects the supplied project and resume context, including:

- DTSC 691 Applied Data Science
- FinAccess 2024 project scope
- target classes: Excluded, Mobile money only, Banked
- interpretable predictors used in the notebook
- tuned Gradient Boosting as the strongest current model
- reported macro F1 and balanced accuracy from the approved proposal and notebook outputs
- supplied resume, education, certification, and accomplishment content

## Manual polish ideas before final submission

You may still want to refine:

1. **Profile image**
   - replace the placeholder SVG with a headshot or branded image

2. **Feature metadata**
   - add the exact category mapping used by the trained pipeline

3. **Notebook artifacts**
   - copy the final CSVs, figures, and model files into the expected folders

4. **Downloads section**
   - add a final `project_overview.pdf` if you generate one for submission

5. **Portfolio cards**
   - add screenshots, outcome metrics, or sanitized visuals for AML and digital banking work if appropriate

6. **Capstone county context**
   - connect the county exclusion CSV and figure for richer local context

## Submission alignment

This app was structured to fit the course UI requirements by including:

- a biographical homepage
- a resume page
- a general projects page
- a specific project page with explanation and interaction

## Repo split and current expectation

There are now two separate GitHub repos in play:

- `mutigaj1/finaccess-capstone-streamlit-fresh` is the intended source-of-truth for the fresh greenfield capstone app
- `mutigaj1/finaccess-streamlit` is the older repo and should not be treated as the fresh app unless you intentionally sync or migrate content into it

If the hosted Streamlit deployment should reflect the fresh app, point Streamlit Cloud at the fresh repo, not the old empty one.

## Suggested next step

After the UI review, the best next move is to export the final notebook artifacts and connect the real trained pipeline with aligned metadata.
