from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import streamlit as st

from utils.config import (
    APP_ROOT,
    EXPECTED_ARTIFACT_FILENAMES,
    EXPECTED_FIGURE_FILENAMES,
    LOCAL_ARTIFACTS_DIR,
    LOCAL_FIGURES_DIR,
    SOURCE_ARTIFACTS_DIR,
    SOURCE_FIGURES_DIR,
    SOURCE_PROJECT_ROOT,
)
from utils.content import CLASS_ORDER, DEFAULT_METADATA, MODEL_FEATURE_ORDER


@dataclass
class ArtifactBundle:
    prediction_mode: str
    model: Any | None = None
    model_name: str = "Stub heuristic predictor"
    selected_features: list[str] = field(default_factory=lambda: MODEL_FEATURE_ORDER.copy())
    metadata: dict[str, Any] = field(default_factory=lambda: DEFAULT_METADATA)
    metadata_source: str = "fallback"
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    files: dict[str, Path] = field(default_factory=dict)
    figures: dict[str, Path] = field(default_factory=dict)
    tables: dict[str, pd.DataFrame] = field(default_factory=dict)


def _candidate_artifact_dirs() -> list[Path]:
    return [LOCAL_ARTIFACTS_DIR, SOURCE_ARTIFACTS_DIR]


def _candidate_figure_dirs() -> list[Path]:
    return [LOCAL_FIGURES_DIR, SOURCE_FIGURES_DIR]


def _find_first_existing(filename: str, directories: list[Path]) -> Path | None:
    for directory in directories:
        candidate = directory / filename
        if candidate.exists():
            return candidate
    return None


def _candidate_source_dirs() -> list[Path]:
    return [APP_ROOT, SOURCE_PROJECT_ROOT]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _load_csv_if_exists(path: Path | None) -> pd.DataFrame | None:
    if path is None or not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_artifact_bundle() -> ArtifactBundle:
    bundle = ArtifactBundle(prediction_mode="stub")

    for key, filename in EXPECTED_ARTIFACT_FILENAMES.items():
        found = _find_first_existing(filename, _candidate_artifact_dirs())
        if found:
            bundle.files[key] = found

    for key, filename in EXPECTED_FIGURE_FILENAMES.items():
        found = _find_first_existing(filename, _candidate_figure_dirs())
        if found:
            bundle.figures[key] = found

    metadata_path = bundle.files.get("feature_metadata")
    if metadata_path:
        try:
            bundle.metadata = _read_json(metadata_path)
            bundle.metadata_source = str(metadata_path)
        except Exception as exc:
            bundle.errors.append(f"Could not read feature_metadata.json: {exc}")
            bundle.metadata = DEFAULT_METADATA
            bundle.metadata_source = "fallback"
    else:
        bundle.metadata = DEFAULT_METADATA
        bundle.metadata_source = "fallback"
        bundle.warnings.append(
            "No feature_metadata.json was found. The app is using fallback UI metadata. "
            "Add your final metadata file for artifact-backed prediction."
        )

    selected_features_path = bundle.files.get("selected_features")
    if selected_features_path:
        try:
            loaded_features = joblib.load(selected_features_path)
            if isinstance(loaded_features, list) and loaded_features:
                bundle.selected_features = loaded_features
        except Exception as exc:
            bundle.errors.append(f"Could not load selected features: {exc}")

    model_name_path = bundle.files.get("model_name")
    if model_name_path:
        try:
            bundle.model_name = _read_text(model_name_path)
        except Exception as exc:
            bundle.errors.append(f"Could not read model name: {exc}")

    pipeline_path = bundle.files.get("pipeline")
    if pipeline_path and metadata_path:
        try:
            bundle.model = joblib.load(pipeline_path)
            bundle.prediction_mode = "artifact"
            if not bundle.model_name or bundle.model_name == "Stub heuristic predictor":
                bundle.model_name = "Artifact-backed model"
        except Exception as exc:
            bundle.errors.append(f"Could not load pipeline artifact: {exc}")
            bundle.prediction_mode = "stub"
    elif pipeline_path and not metadata_path:
        bundle.warnings.append(
            "A trained pipeline was found, but prediction stays in stub mode because feature_metadata.json is missing. "
            "This prevents accidental category-code mismatches."
        )

    table_keys = [
        "model_comparison",
        "feature_importance",
        "subgroup_sex",
        "subgroup_education",
        "subgroup_county",
        "county_exclusion",
        "target_summary",
        "correlations",
        "outlier_review",
    ]
    for key in table_keys:
        df = _load_csv_if_exists(bundle.files.get(key))
        if df is not None:
            bundle.tables[key] = df

    return bundle


def get_reference_files() -> list[dict[str, Any]]:
    source_dirs = _candidate_source_dirs()
    files = [
        {
            "label": "Notebook (.ipynb)",
            "path": _find_first_existing("FINACCESS_MASTER_PROJECT_NOTEBOOK.ipynb", source_dirs),
            "mime": "application/x-ipynb+json",
            "category": "Source project file",
        },
        {
            "label": "Proposal update (.docx)",
            "path": _find_first_existing("Mutiga Proposal Feedback 2 updated.docx", source_dirs),
            "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "category": "Source project file",
        },
        {
            "label": "Project guidelines (.docx)",
            "path": _find_first_existing("_Project Guidelines- Machine Learning Project.docx", source_dirs),
            "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "category": "Source project file",
        },
        {
            "label": "FinAccess manual (.pdf)",
            "path": _find_first_existing("FinAccess 2024 Manual.pdf", source_dirs),
            "mime": "application/pdf",
            "category": "Source project file",
        },
        {
            "label": "FinAccess questionnaire (.pdf)",
            "path": _find_first_existing("2024 FinAccess Questionnaire.pdf", source_dirs),
            "mime": "application/pdf",
            "category": "Source project file",
        },
        {
            "label": "Project overview PDF",
            "path": _find_first_existing("project_overview.pdf", _candidate_artifact_dirs()),
            "mime": "application/pdf",
            "category": "Artifact",
        },
        {
            "label": "Model comparison CSV",
            "path": _find_first_existing(EXPECTED_ARTIFACT_FILENAMES["model_comparison"], _candidate_artifact_dirs()),
            "mime": "text/csv",
            "category": "Artifact",
        },
        {
            "label": "Feature importance CSV",
            "path": _find_first_existing(EXPECTED_ARTIFACT_FILENAMES["feature_importance"], _candidate_artifact_dirs()),
            "mime": "text/csv",
            "category": "Artifact",
        },
        {
            "label": "Selected features joblib",
            "path": _find_first_existing(EXPECTED_ARTIFACT_FILENAMES["selected_features"], _candidate_artifact_dirs()),
            "mime": "application/octet-stream",
            "category": "Artifact",
        },
        {
            "label": "County context CSV",
            "path": _find_first_existing(EXPECTED_ARTIFACT_FILENAMES["county_exclusion"], _candidate_artifact_dirs()),
            "mime": "text/csv",
            "category": "Artifact",
        },
        {
            "label": "Cleaned survey data (.dta)",
            "path": _find_first_existing("2024_Finaccess_Publicdata.dta", source_dirs),
            "mime": "application/octet-stream",
            "category": "Source project file",
        },
    ]
    return files


def read_binary(path: Path | None) -> bytes | None:
    if path is None or not path.exists():
        return None
    return path.read_bytes()


def get_metadata_options(metadata: dict[str, Any], field_name: str) -> list[dict[str, Any]]:
    return metadata.get("fields", {}).get(field_name, {}).get("options", [])


def get_metadata_label(metadata: dict[str, Any], field_name: str) -> str:
    return metadata.get("fields", {}).get(field_name, {}).get("label", field_name)


def get_fallback_model_comparison() -> pd.DataFrame:
    from utils.content import DEFAULT_MODEL_COMPARISON_ROWS

    return pd.DataFrame(DEFAULT_MODEL_COMPARISON_ROWS)


def figure_or_none(bundle: ArtifactBundle, key: str) -> Path | None:
    return bundle.figures.get(key)


def table_or_none(bundle: ArtifactBundle, key: str) -> pd.DataFrame | None:
    return bundle.tables.get(key)
