"""
Unit tests for app.services.predictor
======================================
LLD contract: the predictor service is the single boundary between the
FastAPI layer and scikit-learn. Tests here verify:

  1. load_model() sets the global `model` correctly.
  2. is_loaded() reflects the model state.
  3. predict() maps raw model output into the expected domain dict.
  4. predict() selects the churn class index correctly for both
     'Yes'/'No' and 0/1 label conventions.
  5. predict() raises RuntimeError when the model is not loaded.
"""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_mock_model(classes, probas):
    """Build a minimal sklearn-compatible mock pipeline."""
    mock = MagicMock()
    mock.classes_ = classes
    mock.predict.return_value = [classes[np.argmax(probas)]]
    mock.predict_proba.return_value = np.array([probas])
    return mock


# ---------------------------------------------------------------------------
# load_model / is_loaded
# ---------------------------------------------------------------------------


class TestLoadModel:
    def test_load_model_success(self, tmp_path):
        """load_model() populates the global model when the file exists."""
        import pickle
        import app.services.predictor as svc

        # joblib can't serialise locally-defined classes; use pickle with a
        # plain dict as a stand-in for any picklable model object.
        model_path = tmp_path / "model.pkl"
        with open(model_path, "wb") as fh:
            pickle.dump({"stub": True}, fh)

        with patch.object(svc, "MODEL_PATH", str(model_path)):
            svc.model = None
            svc.load_model()
            assert svc.model is not None

    def test_load_model_missing_file(self):
        """load_model() sets model to None when the file is absent."""
        import app.services.predictor as svc

        with patch.object(svc, "MODEL_PATH", "/nonexistent/model.pkl"):
            svc.model = None
            svc.load_model()
            assert svc.model is None

    def test_is_loaded_true(self):
        import app.services.predictor as svc

        svc.model = MagicMock()
        assert svc.is_loaded() is True

    def test_is_loaded_false(self):
        import app.services.predictor as svc

        svc.model = None
        assert svc.is_loaded() is False


# ---------------------------------------------------------------------------
# predict() -  happy paths
# ---------------------------------------------------------------------------


class TestPredict:
    """Tests use direct module access to avoid HTTP overhead."""

    def _run(self, classes, probas, input_data=None):
        import app.services.predictor as svc

        if input_data is None:
            input_data = {
                "Senior Citizen": "No",
                "Under 30": "Yes",
                "Dependents": "No",
                "Referred a Friend": "No",
                "Paperless Billing": "Yes",
                "Premium Tech Support": "No",
                "Unlimited Data": "Yes",
                "Multiple Lines": "No",
                "Online Backup": "No",
                "Device Protection Plan": "No",
                "Streaming TV": "Yes",
                "Streaming Movies": "Yes",
                "Streaming Music": "No",
                "Tenure in Months": 6.0,
                "Avg Monthly GB Download": 45.0,
                "Monthly Charge": 95.50,
                "Contract": "Month-to-Month",
                "Payment Method": "Electronic Check",
                "Offer": "None",
                "Internet Type": "Fiber Optic",
                "Satisfaction Score": 2,
            }

        mock_model = _make_mock_model(classes, probas)
        svc.model = mock_model
        return svc.predict(input_data)

    # -- Churn predicted (Yes/No labels) ------------------------------------
    def test_predict_churn_yes_no_labels(self):
        result = self._run(classes=["No", "Yes"], probas=[0.13, 0.87])
        assert result["prediction"] == "WILL CHURN"
        assert result["status"] == "danger"
        assert "87" in result["churn_probability"]

    # -- No churn predicted (Yes/No labels) ----------------------------------
    def test_predict_no_churn_yes_no_labels(self):
        result = self._run(classes=["No", "Yes"], probas=[0.92, 0.08])
        assert result["prediction"] == "WILL NOT CHURN"
        assert result["status"] == "success"
        assert "92" in result["no_churn_probability"]

    # -- Churn predicted (0/1 integer labels) --------------------------------
    def test_predict_churn_integer_labels(self):
        result = self._run(classes=[0, 1], probas=[0.20, 0.80])
        assert result["prediction"] == "WILL CHURN"
        assert result["status"] == "danger"

    # -- Confidence percentage format ----------------------------------------
    def test_confidence_format(self):
        result = self._run(classes=["No", "Yes"], probas=[0.25, 0.75])
        assert result["confidence"].endswith("%")
        assert float(result["confidence"].rstrip("%")) == pytest.approx(75.0, abs=0.1)

    # -- Raw probabilities available for JSON API ----------------------------
    def test_raw_probabilities_present(self):
        result = self._run(classes=["No", "Yes"], probas=[0.30, 0.70])
        assert "_confidence_raw" in result
        assert "_prob_raw" in result
        assert isinstance(result["_prob_raw"], dict)
        assert len(result["_prob_raw"]) == 2

    # -- All required keys present ------------------------------------------
    def test_result_keys(self):
        result = self._run(classes=["No", "Yes"], probas=[0.40, 0.60])
        required = {
            "prediction",
            "confidence",
            "churn_probability",
            "no_churn_probability",
            "status",
        }
        assert required.issubset(result.keys())


# ---------------------------------------------------------------------------
# predict() -  error path
# ---------------------------------------------------------------------------


class TestPredictErrors:
    def test_raises_when_model_not_loaded(self):
        import app.services.predictor as svc

        svc.model = None
        with pytest.raises(RuntimeError, match="not loaded"):
            svc.predict({"dummy": "data"})
