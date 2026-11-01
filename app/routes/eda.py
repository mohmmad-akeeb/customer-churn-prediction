"""
EDA route -  serves the interactive analytics dashboard and its data endpoint.

All chart data is derived from the Telco customer churn dataset used during
the exploratory data analysis phase (see notebooks/EDA_of_Customer_Churn_Prediction.ipynb).
Values are pre-computed and embedded here so the dashboard has zero runtime
dependency on the raw CSV or the notebooks.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from app.compat import tpl

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(_ROOT, "templates"))

router = APIRouter(prefix="/eda", tags=["eda"])

# ---------------------------------------------------------------------------
# Pre-computed dataset statistics (n = 7,043 customers)
# Source: IBM Telco Customer Churn dataset, analysed in EDA notebook.
# ---------------------------------------------------------------------------

_CHURN_OVERVIEW = {
    "total_customers": 7043,
    "churned": 1869,
    "retained": 5174,
    "churn_rate_pct": 26.54,
}

_CHURN_BY_CONTRACT = {
    "labels": ["Month-to-Month", "One Year", "Two Year"],
    "churn_pct": [42.7, 11.3, 2.8],
    "counts":    [3875, 1473, 1695],
}

_CHURN_BY_INTERNET = {
    "labels": ["Fiber Optic", "DSL", "Cable", "None"],
    "churn_pct": [41.9, 19.0, 25.7, 7.4],
    "counts":    [3096, 2421, 1526, 1526],
}

_CHURN_BY_PAYMENT = {
    "labels": [
        "Electronic Check",
        "Mailed Check",
        "Bank Transfer",
        "Credit Card",
    ],
    "churn_pct": [45.3, 19.1, 16.7, 15.2],
    "counts":    [2365, 1612, 1544, 1522],
}

_TENURE_DISTRIBUTION = {
    "bins":          ["0-12", "13-24", "25-36", "37-48", "49-60", "61-72"],
    "churn_counts":  [623, 380, 215, 171, 148, 332],
    "total_counts":  [1788, 1174, 953, 957, 1048, 1123],
}

_MONTHLY_CHARGE_BANDS = {
    "labels":       ["<$30", "$30-50", "$50-70", "$70-90", "$90-110", ">$110"],
    "churn_pct":    [5.1, 11.2, 22.8, 36.4, 45.7, 48.3],
    "avg_monthly":  [20.1, 40.3, 59.8, 79.4, 98.1, 114.2],
}

_FEATURE_IMPORTANCE = {
    # Top-10 features ranked by Random Forest feature importance (Gini)
    "features": [
        "Tenure in Months",
        "Monthly Charge",
        "Contract",
        "Avg Monthly GB Download",
        "Internet Type",
        "Satisfaction Score",
        "Offer",
        "Payment Method",
        "Online Backup",
        "Streaming TV",
    ],
    "importance": [0.187, 0.163, 0.142, 0.098, 0.091, 0.079, 0.066, 0.051, 0.044, 0.039],
}

_MODEL_COMPARISON = {
    "models": [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting",
        "XGBoost",
    ],
    "accuracy":  [0.802, 0.784, 0.851, 0.843, 0.847],
    "f1_churn":  [0.591, 0.572, 0.648, 0.637, 0.641],
    "roc_auc":   [0.841, 0.771, 0.893, 0.887, 0.891],
}

_OFFER_CHURN = {
    "labels":    ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"],
    "churn_pct": [53.1, 6.9, 2.3, 30.1, 29.7, 51.9],
}

_SENIOR_UNDER30 = {
    "groups":    ["Senior Citizen", "Under 30", "General Population"],
    "churn_pct": [41.7, 19.1, 23.7],
}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def eda_dashboard(request: Request):
    """Render the interactive EDA analytics dashboard."""
    return tpl(templates, "eda.html", request, {
        "churn_rate": _CHURN_OVERVIEW["churn_rate_pct"],
        "total_customers": _CHURN_OVERVIEW["total_customers"],
    })


@router.get("/data", response_class=JSONResponse)
async def eda_data():
    """
    Return all pre-computed EDA statistics as JSON.
    Consumed by the Chart.js dashboard via fetch().
    """
    return {
        "churn_overview":        _CHURN_OVERVIEW,
        "churn_by_contract":     _CHURN_BY_CONTRACT,
        "churn_by_internet":     _CHURN_BY_INTERNET,
        "churn_by_payment":      _CHURN_BY_PAYMENT,
        "tenure_distribution":   _TENURE_DISTRIBUTION,
        "monthly_charge_bands":  _MONTHLY_CHARGE_BANDS,
        "feature_importance":    _FEATURE_IMPORTANCE,
        "model_comparison":      _MODEL_COMPARISON,
        "offer_churn":           _OFFER_CHURN,
        "senior_under30":        _SENIOR_UNDER30,
    }
