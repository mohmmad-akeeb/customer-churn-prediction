"""
JSON API routes -  programmatic access to the prediction model.
"""

from fastapi import APIRouter, HTTPException

from app.schemas import CustomerData, PredictionResponse
from app.services import predictor

router = APIRouter(prefix="/api")


@router.post("/predict", response_model=PredictionResponse)
async def predict_api(customer_data: CustomerData):
    """Programmatic prediction endpoint (JSON in / JSON out)."""
    if not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Model not available.")

    try:
        input_data = {
            "Senior Citizen": customer_data.senior_citizen,
            "Under 30": customer_data.under_30,
            "Dependents": customer_data.dependents,
            "Referred a Friend": customer_data.referred_a_friend,
            "Paperless Billing": customer_data.paperless_billing,
            "Premium Tech Support": customer_data.premium_tech_support,
            "Unlimited Data": customer_data.unlimited_data,
            "Multiple Lines": customer_data.multiple_lines,
            "Online Backup": customer_data.online_backup,
            "Device Protection Plan": customer_data.device_protection_plan,
            "Streaming TV": customer_data.streaming_tv,
            "Streaming Movies": customer_data.streaming_movies,
            "Streaming Music": customer_data.streaming_music,
            "Tenure in Months": customer_data.tenure_in_months,
            "Avg Monthly GB Download": customer_data.avg_monthly_gb_download,
            "Monthly Charge": customer_data.monthly_charge,
            "Contract": customer_data.contract,
            "Payment Method": customer_data.payment_method,
            "Offer": customer_data.offer,
            "Internet Type": customer_data.internet_type,
            "Satisfaction Score": customer_data.satisfaction_score,
        }
        result = predictor.predict(input_data)
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["_confidence_raw"],
            probabilities=result["_prob_raw"],
        )

    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(exc)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": predictor.is_loaded(),
    }
