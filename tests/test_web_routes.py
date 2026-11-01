"""
Integration tests for the HTML web routes (GET /, POST /predict)
=================================================================
LLD contract: the web layer renders Jinja2 templates and exposes the
prediction form. Tests verify HTTP contracts and rendered content
without asserting on exact HTML structure (fragile), focusing instead
on status codes, presence of key strings, and error handling.
"""
import pytest
from tests.conftest import NO_CHURN_PREDICTION_RESULT


# ── GET / ───────────────────────────────────────────────────────────────────

class TestHomePage:
    def test_home_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_home_content_type_html(self, client):
        resp = client.get("/")
        assert "text/html" in resp.headers["content-type"]

    def test_home_contains_form(self, client):
        resp = client.get("/")
        assert b"<form" in resp.content

    def test_home_contains_brand_name(self, client):
        resp = client.get("/")
        assert b"ChurnSight" in resp.content

    def test_home_contains_submit_button(self, client):
        resp = client.get("/")
        assert b"Run Prediction" in resp.content


# ── POST /predict ────────────────────────────────────────────────────────────

class TestPredictForm:
    # Form payloads use HTTP form encoding (not JSON)
    FORM_PAYLOAD = {
        "senior_citizen":         "Yes",
        "under_30":               "",
        "dependents":             "",
        "referred_a_friend":      "",
        "paperless_billing":      "Yes",
        "premium_tech_support":   "",
        "unlimited_data":         "Yes",
        "multiple_lines":         "",
        "online_backup":          "",
        "device_protection_plan": "",
        "streaming_tv":           "Yes",
        "streaming_movies":       "Yes",
        "streaming_music":        "",
        "tenure_in_months":       "6",
        "avg_monthly_gb_download":"45",
        "monthly_charge":         "95.5",
        "contract":               "Month-to-Month",
        "payment_method":         "Electronic Check",
        "offer":                  "None",
        "internet_type":          "Fiber Optic",
        "satisfaction_score":     "2",
    }

    def test_predict_form_returns_200(self, client):
        resp = client.post("/predict", data=self.FORM_PAYLOAD)
        assert resp.status_code == 200

    def test_predict_form_shows_churn_result(self, client):
        resp = client.post("/predict", data=self.FORM_PAYLOAD)
        assert b"WILL CHURN" in resp.content

    def test_predict_form_shows_no_churn_result(self, client, mock_predictor):
        mock_predictor.return_value = NO_CHURN_PREDICTION_RESULT
        resp = client.post("/predict", data=self.FORM_PAYLOAD)
        assert b"WILL NOT CHURN" in resp.content

    def test_predict_form_model_unavailable_shows_error(self, client_no_model):
        resp = client_no_model.post("/predict", data=self.FORM_PAYLOAD)
        assert resp.status_code == 200  # soft error -  page still renders
        assert b"error" in resp.content.lower() or b"Error" in resp.content


# ── EDA dashboard ────────────────────────────────────────────────────────────

class TestEdaDashboard:
    def test_eda_page_returns_200(self, client):
        resp = client.get("/eda")
        assert resp.status_code == 200

    def test_eda_page_content_type_html(self, client):
        resp = client.get("/eda")
        assert "text/html" in resp.headers["content-type"]

    def test_eda_page_contains_charts(self, client):
        resp = client.get("/eda")
        assert b"churnDonut" in resp.content

    def test_eda_data_endpoint_returns_200(self, client):
        resp = client.get("/eda/data")
        assert resp.status_code == 200

    def test_eda_data_endpoint_returns_json(self, client):
        resp = client.get("/eda/data")
        assert "application/json" in resp.headers["content-type"]

    def test_eda_data_has_required_keys(self, client):
        data = client.get("/eda/data").json()
        expected_keys = {
            "churn_overview", "churn_by_contract", "churn_by_internet",
            "churn_by_payment", "tenure_distribution", "monthly_charge_bands",
            "feature_importance", "model_comparison", "offer_churn",
            "senior_under30",
        }
        assert expected_keys.issubset(data.keys())

    def test_eda_data_churn_overview_shape(self, client):
        data = client.get("/eda/data").json()
        ov = data["churn_overview"]
        assert ov["total_customers"] == 7043
        assert ov["churned"] + ov["retained"] == ov["total_customers"]

    def test_eda_data_feature_importance_lengths_match(self, client):
        data = client.get("/eda/data").json()
        fi = data["feature_importance"]
        assert len(fi["features"]) == len(fi["importance"])
