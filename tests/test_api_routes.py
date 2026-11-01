"""
Integration tests for the JSON API routes (/api/predict, /api/health)
======================================================================
LLD contract: the API layer validates input via Pydantic schemas, delegates
inference to the predictor service, and serialises results as PredictionResponse.

Test boundaries:
  - HTTP contract (status codes, Content-Type, response shape)
  - Input validation (missing fields, wrong types)
  - Graceful 503 when the model is unavailable
  - Healthy state reporting

The predictor is stubbed via conftest.mock_predictor -  no .pkl file required.
"""
import pytest
from tests.conftest import SAMPLE_CUSTOMER_PAYLOAD, NO_CHURN_PREDICTION_RESULT


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200

    def test_health_response_shape(self, client):
        data = client.get("/api/health").json()
        assert "status" in data
        assert "model_loaded" in data

    def test_health_model_loaded_true(self, client):
        data = client.get("/api/health").json()
        assert data["model_loaded"] is True

    def test_health_model_loaded_false_when_no_model(self, client_no_model):
        data = client_no_model.get("/api/health").json()
        assert data["model_loaded"] is False


# ---------------------------------------------------------------------------
# POST /api/predict -  happy path
# ---------------------------------------------------------------------------

class TestPredictEndpoint:
    def test_predict_returns_200(self, client):
        resp = client.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD)
        assert resp.status_code == 200

    def test_predict_content_type_json(self, client):
        resp = client.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD)
        assert "application/json" in resp.headers["content-type"]

    def test_predict_response_has_prediction_field(self, client):
        data = client.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD).json()
        assert "prediction" in data
        assert data["prediction"] in ("WILL CHURN", "WILL NOT CHURN")

    def test_predict_response_has_confidence_field(self, client):
        data = client.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD).json()
        assert "confidence" in data
        assert isinstance(data["confidence"], float)
        assert 0.0 <= data["confidence"] <= 1.0

    def test_predict_response_has_probabilities(self, client):
        data = client.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD).json()
        assert "probabilities" in data
        assert isinstance(data["probabilities"], dict)

    def test_predict_no_churn_scenario(self, client, mock_predictor):
        mock_predictor.return_value = NO_CHURN_PREDICTION_RESULT
        data = client.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD).json()
        assert data["prediction"] == "WILL NOT CHURN"


# ---------------------------------------------------------------------------
# POST /api/predict -  validation errors
# ---------------------------------------------------------------------------

class TestPredictValidation:
    def test_missing_required_field_returns_422(self, client):
        payload = {k: v for k, v in SAMPLE_CUSTOMER_PAYLOAD.items()
                   if k != "tenure_in_months"}
        resp = client.post("/api/predict", json=payload)
        assert resp.status_code == 422

    def test_wrong_type_for_numeric_field_returns_422(self, client):
        payload = {**SAMPLE_CUSTOMER_PAYLOAD, "monthly_charge": "not-a-number"}
        resp = client.post("/api/predict", json=payload)
        assert resp.status_code == 422

    def test_empty_body_returns_422(self, client):
        resp = client.post("/api/predict", json={})
        assert resp.status_code == 422

    def test_satisfaction_score_accepts_integer(self, client):
        payload = {**SAMPLE_CUSTOMER_PAYLOAD, "satisfaction_score": 5}
        resp = client.post("/api/predict", json=payload)
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /api/predict -  model unavailable
# ---------------------------------------------------------------------------

class TestPredictModelUnavailable:
    def test_returns_503_when_model_not_loaded(self, client_no_model):
        resp = client_no_model.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD)
        assert resp.status_code == 503

    def test_503_has_detail_message(self, client_no_model):
        data = client_no_model.post("/api/predict", json=SAMPLE_CUSTOMER_PAYLOAD).json()
        assert "detail" in data
