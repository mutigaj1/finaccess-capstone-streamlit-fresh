from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from utils.content import CLASS_ORDER, MODEL_FEATURE_ORDER, NUMERIC_BOUNDS


def validate_inputs(ui_inputs: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field_name, rule in NUMERIC_BOUNDS.items():
        value = ui_inputs.get(field_name)
        if value is None:
            issues.append(f"{rule['label']} is required.")
            continue
        if value < rule["min"] or value > rule["max"]:
            issues.append(f"{rule['label']} must be between {rule['min']} and {rule['max']}.")

    children = ui_inputs.get("children_in_household", 0)
    household_size = ui_inputs.get("household_size", 1)
    if children > household_size:
        issues.append("Number of children in household cannot be greater than total household size.")

    return issues


def encode_ui_inputs(ui_inputs: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    encoded = {
        "county": ui_inputs["county"],
        "sex": ui_inputs["sex"],
        "age_years": ui_inputs["age_years"],
        "household_size": ui_inputs["household_size"],
        "education": ui_inputs["education"],
        "marital_status": ui_inputs["marital_status"],
        "children_in_household": ui_inputs["children_in_household"],
        "livelihood": ui_inputs["livelihood"],
        "can_access_internet": ui_inputs["can_access_internet"],
        "internet_frequency": ui_inputs["internet_frequency"],
        "financial_health": ui_inputs["financial_health"],
    }
    return encoded


def format_probability_output(probabilities: dict[str, float]) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "Profile": list(probabilities.keys()),
            "Probability": list(probabilities.values()),
        }
    )
    df["Percent"] = (df["Probability"] * 100).round(1)
    return df.sort_values("Probability", ascending=False).reset_index(drop=True)


def _normalize(scores: dict[str, float]) -> dict[str, float]:
    arr = np.array(list(scores.values()), dtype=float)
    arr = np.clip(arr, 0.001, None)
    arr = arr / arr.sum()
    return {label: float(value) for label, value in zip(scores.keys(), arr)}


def heuristic_stub_prediction(ui_inputs: dict[str, Any]) -> dict[str, Any]:
    education = ui_inputs["education"]
    internet = ui_inputs["can_access_internet"]
    frequency = ui_inputs["internet_frequency"]
    financial_health = ui_inputs["financial_health"]
    age = ui_inputs["age_years"]
    livelihood = ui_inputs["livelihood"]

    excluded = 0.30
    mobile = 0.34
    banked = 0.36

    if internet == 0.0:
        excluded += 0.20
        banked -= 0.12
    else:
        banked += 0.10
        mobile += 0.04

    if education in {1, 2}:
        excluded += 0.15
        banked -= 0.08
    elif education in {5, 7, 8, 9}:
        banked += 0.18
        excluded -= 0.08

    if financial_health == 3:
        excluded += 0.18
        banked -= 0.08
    elif financial_health == 1:
        banked += 0.17
        excluded -= 0.07

    if frequency == 1:
        banked += 0.10
    elif frequency == 2:
        banked += 0.05
        mobile += 0.03
    elif frequency in {4, 5}:
        excluded += 0.06

    if livelihood in {2, 4}:
        mobile += 0.06
        banked += 0.07
    if livelihood == 1:
        mobile += 0.04

    if age >= 55 and internet == 0.0:
        excluded += 0.05
    if 25 <= age <= 45 and internet == 1.0:
        mobile += 0.03
        banked += 0.03

    probabilities = _normalize(
        {
            "Excluded": excluded,
            "Mobile money only": mobile,
            "Banked": banked,
        }
    )
    predicted_class = max(probabilities, key=probabilities.get)
    return {
        "predicted_class": predicted_class,
        "probabilities": probabilities,
        "mode": "stub",
        "note": (
            "Stub mode is active because a final artifact-backed pipeline and aligned feature metadata were not both found. "
            "The output below is a clearly marked UI fallback for local testing only."
        ),
    }


def artifact_prediction(model: Any, encoded_inputs: dict[str, Any]) -> dict[str, Any]:
    input_df = pd.DataFrame([[encoded_inputs[column] for column in MODEL_FEATURE_ORDER]], columns=MODEL_FEATURE_ORDER)

    if not hasattr(model, "predict"):
        raise AttributeError("Loaded model does not expose predict().")

    predicted_class = model.predict(input_df)[0]

    if hasattr(model, "predict_proba"):
        probabilities_array = model.predict_proba(input_df)[0]
        classes = list(getattr(model, "classes_", CLASS_ORDER))
        probability_map = {str(label): float(probabilities_array[index]) for index, label in enumerate(classes)}
        full_probabilities = {label: probability_map.get(label, 0.0) for label in CLASS_ORDER}
        total = sum(full_probabilities.values()) or 1.0
        full_probabilities = {label: value / total for label, value in full_probabilities.items()}
    else:
        full_probabilities = {label: (1.0 if label == predicted_class else 0.0) for label in CLASS_ORDER}

    return {
        "predicted_class": str(predicted_class),
        "probabilities": full_probabilities,
        "mode": "artifact",
        "note": "Prediction generated from the saved trained pipeline.",
    }


def generate_prediction(bundle: Any, ui_inputs: dict[str, Any]) -> dict[str, Any]:
    encoded = encode_ui_inputs(ui_inputs, bundle.metadata)
    if bundle.prediction_mode == "artifact" and bundle.model is not None:
        try:
            return artifact_prediction(bundle.model, encoded)
        except Exception as exc:
            fallback = heuristic_stub_prediction(ui_inputs)
            fallback["note"] = (
                "The app found a trained pipeline, but prediction fell back to stub mode because the artifact call failed. "
                f"Details: {exc}"
            )
            return fallback
    return heuristic_stub_prediction(ui_inputs)


def build_plain_language_explanation(ui_inputs: dict[str, Any], prediction: dict[str, Any]) -> str:
    predicted = prediction["predicted_class"]
    internet = "has internet access" if ui_inputs["can_access_internet"] == 1.0 else "does not report internet access"
    health = {1: "stronger", 2: "middle", 3: "weaker"}.get(ui_inputs["financial_health"], "mixed")

    if predicted == "Banked":
        return (
            f"This profile leans toward Banked. In plain language, the combination of education, digital access, and a {health} "
            f"financial-health signal makes the respondent look more like adults in the survey who had bank-based access."
        )
    if predicted == "Mobile money only":
        return (
            f"This profile leans toward Mobile money only. In plain language, the respondent {internet} and looks more similar to "
            "adults who appear connected to digital payments but not fully represented in the banked group."
        )
    return (
        f"This profile leans toward Excluded. In plain language, the combination of lower digital access and a {health} "
        "financial-health signal looks closer to adults who were outside the current banked or mobile-money-only categories."
    )
