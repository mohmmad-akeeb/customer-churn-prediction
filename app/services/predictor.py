"""
Predictor service -  handles model loading and inference.
"""

import os
import warnings
import joblib
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="joblib")

# Resolve model path relative to project root regardless of working directory
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(_ROOT, "models", "best_model_pipeline.pkl")

model = None


def load_model() -> None:
    """Load the ML pipeline from disk. Called once at app startup."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as exc:
        print(f"Error loading model: {exc}")
        model = None


def is_loaded() -> bool:
    return model is not None


def predict(input_data: dict) -> dict:
    """
    Run inference on a single customer record.

    Parameters
    ----------
    input_data : dict
        Keys must match the column names expected by the pipeline.

    Returns
    -------
    dict with keys: prediction, confidence, churn_probability,
                    no_churn_probability, status
    """
    if model is None:
        raise RuntimeError("Model is not loaded.")

    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]

    # Locate the churn class index (handles 'Yes'/'No', 0/1, etc.)
    classes_str = [str(c).lower() for c in model.classes_]
    if "yes" in classes_str:
        churn_index = classes_str.index("yes")
    elif "1" in classes_str:
        churn_index = classes_str.index("1")
    else:
        churn_index = 1

    no_churn_index = 1 - churn_index

    predicted_class_index = list(model.classes_).index(prediction)
    confidence_pct = prediction_proba[predicted_class_index] * 100
    churn_pct = prediction_proba[churn_index] * 100
    no_churn_pct = prediction_proba[no_churn_index] * 100
    will_churn = predicted_class_index == churn_index

    return {
        "prediction": "WILL CHURN" if will_churn else "WILL NOT CHURN",
        "confidence": f"{confidence_pct:.1f}%",
        "churn_probability": f"{churn_pct:.1f}%",
        "no_churn_probability": f"{no_churn_pct:.1f}%",
        "status": "danger" if will_churn else "success",
        # raw floats for the JSON API
        "_confidence_raw": float(prediction_proba.max()),
        "_prob_raw": {
            str(model.classes_[0]): float(prediction_proba[0]),
            str(model.classes_[1]): float(prediction_proba[1]),
        },
    }
