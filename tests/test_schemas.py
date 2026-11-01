"""
Unit tests for Pydantic schemas (app.schemas)
==============================================
LLD contract: schemas form the public API contract. These tests pin the
accepted types and field names so breaking changes surface immediately.
"""
import pytest
from pydantic import ValidationError

from app.schemas import CustomerData, PredictionResponse
from tests.conftest import SAMPLE_CUSTOMER_PAYLOAD


class TestCustomerDataSchema:
    def test_valid_payload_accepted(self):
        customer = CustomerData(**SAMPLE_CUSTOMER_PAYLOAD)
        assert customer.tenure_in_months == 6.0

    def test_yes_no_strings_accepted(self):
        customer = CustomerData(**SAMPLE_CUSTOMER_PAYLOAD)
        assert customer.senior_citizen in ("Yes", "No")

    def test_satisfaction_score_is_int(self):
        customer = CustomerData(**SAMPLE_CUSTOMER_PAYLOAD)
        assert isinstance(customer.satisfaction_score, int)

    def test_missing_field_raises_validation_error(self):
        incomplete = {k: v for k, v in SAMPLE_CUSTOMER_PAYLOAD.items()
                      if k != "monthly_charge"}
        with pytest.raises(ValidationError):
            CustomerData(**incomplete)

    def test_non_numeric_tenure_raises_validation_error(self):
        bad = {**SAMPLE_CUSTOMER_PAYLOAD, "tenure_in_months": "not-a-float"}
        with pytest.raises(ValidationError):
            CustomerData(**bad)

    def test_all_21_fields_present(self):
        assert len(CustomerData.model_fields) == 21


class TestPredictionResponseSchema:
    def test_valid_response_accepted(self):
        resp = PredictionResponse(
            prediction="WILL CHURN",
            confidence=0.87,
            probabilities={"No": 0.13, "Yes": 0.87},
        )
        assert resp.prediction == "WILL CHURN"

    def test_confidence_is_float(self):
        resp = PredictionResponse(
            prediction="WILL NOT CHURN",
            confidence=0.91,
            probabilities={"No": 0.91, "Yes": 0.09},
        )
        assert isinstance(resp.confidence, float)

    def test_missing_prediction_raises(self):
        with pytest.raises(ValidationError):
            PredictionResponse(
                confidence=0.5,
                probabilities={},
            )
