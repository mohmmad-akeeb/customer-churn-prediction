"""
Shared pytest fixtures for the ChurnSight test suite.

Architecture note (LLD):
  - conftest.py is the composition root for the test layer.
  - The `client` fixture spins up a TestClient backed by the real FastAPI
    application, but with the ML model replaced by a lightweight stub.
  - `mock_predictor` patches app.services.predictor so unit tests have
    zero dependency on the ~2 MB .pkl file and on scikit-learn.
  - All fixtures are function-scoped (default) to ensure test isolation.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Canonical customer payload used across multiple tests.
# Represents a high-risk Month-to-Month / Fiber Optic customer.
# ---------------------------------------------------------------------------
SAMPLE_CUSTOMER_PAYLOAD = {
    "senior_citizen": "No",
    "under_30": "Yes",
    "dependents": "No",
    "referred_a_friend": "No",
    "paperless_billing": "Yes",
    "premium_tech_support": "No",
    "unlimited_data": "Yes",
    "multiple_lines": "No",
    "online_backup": "No",
    "device_protection_plan": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "Yes",
    "streaming_music": "No",
    "tenure_in_months": 6.0,
    "avg_monthly_gb_download": 45.0,
    "monthly_charge": 95.50,
    "contract": "Month-to-Month",
    "payment_method": "Electronic Check",
    "offer": "None",
    "internet_type": "Fiber Optic",
    "satisfaction_score": 2,
}

# What the stubbed predictor returns for a churn prediction
CHURN_PREDICTION_RESULT = {
    "prediction": "WILL CHURN",
    "confidence": "87.3%",
    "churn_probability": "87.3%",
    "no_churn_probability": "12.7%",
    "status": "danger",
    "_confidence_raw": 0.873,
    "_prob_raw": {"No": 0.127, "Yes": 0.873},
}

# What the stubbed predictor returns for a no-churn prediction
NO_CHURN_PREDICTION_RESULT = {
    "prediction": "WILL NOT CHURN",
    "confidence": "91.2%",
    "churn_probability": "8.8%",
    "no_churn_probability": "91.2%",
    "status": "success",
    "_confidence_raw": 0.912,
    "_prob_raw": {"No": 0.912, "Yes": 0.088},
}


@pytest.fixture()
def mock_predictor():
    """
    Replace the real predictor with a mock.
    Returns the mock so tests can configure return values per-scenario.
    """
    with patch("app.services.predictor.model", new=MagicMock()):
        with patch("app.services.predictor.is_loaded", return_value=True):
            with patch(
                "app.services.predictor.predict",
                return_value=CHURN_PREDICTION_RESULT,
            ) as mock_predict:
                yield mock_predict


@pytest.fixture()
def client(mock_predictor):  # noqa: F811
    """
    FastAPI TestClient with a stubbed predictor.
    Import app *inside* the fixture so patches applied above are in effect.
    """
    from app.main import app  # local import -  patches must be active first

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


@pytest.fixture()
def client_no_model():
    """
    FastAPI TestClient where the predictor reports no model loaded.
    Used to test graceful degradation paths.
    """
    with patch("app.services.predictor.is_loaded", return_value=False):
        with patch("app.services.predictor.model", new=None):
            from app.main import app

            with TestClient(app, raise_server_exceptions=False) as c:
                yield c
