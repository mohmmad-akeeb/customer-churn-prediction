"""
Web (HTML) routes - serves the prediction form and handles form submissions.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

from app.services import predictor
from app.compat import tpl

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(_ROOT, "templates"))

router = APIRouter()


def _build_input(
    senior_citizen, under_30, dependents, referred_a_friend,
    paperless_billing, premium_tech_support, unlimited_data,
    multiple_lines, online_backup, device_protection_plan,
    streaming_tv, streaming_movies, streaming_music,
    tenure_in_months, avg_monthly_gb_download, monthly_charge,
    contract, payment_method, offer, internet_type, satisfaction_score,
) -> dict:
    """Convert raw form values into the dict expected by the model pipeline."""
    return {
        "Senior Citizen": "Yes" if senior_citizen else "No",
        "Under 30": "Yes" if under_30 else "No",
        "Dependents": "Yes" if dependents else "No",
        "Referred a Friend": "Yes" if referred_a_friend else "No",
        "Paperless Billing": "Yes" if paperless_billing else "No",
        "Premium Tech Support": "Yes" if premium_tech_support else "No",
        "Unlimited Data": "Yes" if unlimited_data else "No",
        "Multiple Lines": "Yes" if multiple_lines else "No",
        "Online Backup": "Yes" if online_backup else "No",
        "Device Protection Plan": "Yes" if device_protection_plan else "No",
        "Streaming TV": "Yes" if streaming_tv else "No",
        "Streaming Movies": "Yes" if streaming_movies else "No",
        "Streaming Music": "Yes" if streaming_music else "No",
        "Tenure in Months": tenure_in_months,
        "Avg Monthly GB Download": avg_monthly_gb_download,
        "Monthly Charge": monthly_charge,
        "Contract": contract,
        "Payment Method": payment_method,
        "Offer": offer,
        "Internet Type": internet_type,
        "Satisfaction Score": satisfaction_score,
    }


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main prediction form."""
    return tpl(templates, "index.html", request)


@router.post("/predict", response_class=HTMLResponse)
async def predict_form(
    request: Request,
    senior_citizen: Optional[str] = Form(None),
    under_30: Optional[str] = Form(None),
    dependents: Optional[str] = Form(None),
    referred_a_friend: Optional[str] = Form(None),
    paperless_billing: Optional[str] = Form(None),
    premium_tech_support: Optional[str] = Form(None),
    unlimited_data: Optional[str] = Form(None),
    multiple_lines: Optional[str] = Form(None),
    online_backup: Optional[str] = Form(None),
    device_protection_plan: Optional[str] = Form(None),
    streaming_tv: Optional[str] = Form(None),
    streaming_movies: Optional[str] = Form(None),
    streaming_music: Optional[str] = Form(None),
    tenure_in_months: float = Form(...),
    avg_monthly_gb_download: float = Form(...),
    monthly_charge: float = Form(...),
    contract: str = Form(...),
    payment_method: str = Form(...),
    offer: str = Form(...),
    internet_type: str = Form(...),
    satisfaction_score: int = Form(...),
):
    """Handle form submission and return prediction result."""
    if not predictor.is_loaded():
        return tpl(templates, "index.html", request, {
            "error": "Model not loaded. Please check the model file.",
        })

    try:
        input_data = _build_input(
            senior_citizen, under_30, dependents, referred_a_friend,
            paperless_billing, premium_tech_support, unlimited_data,
            multiple_lines, online_backup, device_protection_plan,
            streaming_tv, streaming_movies, streaming_music,
            tenure_in_months, avg_monthly_gb_download, monthly_charge,
            contract, payment_method, offer, internet_type, satisfaction_score,
        )
        result = predictor.predict(input_data)
        return tpl(templates, "index.html", request, {"result": result})

    except Exception as exc:
        return tpl(templates, "index.html", request, {
            "error": f"Prediction error: {str(exc)}",
        })
