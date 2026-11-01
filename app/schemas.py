from pydantic import BaseModel


class CustomerData(BaseModel):
    senior_citizen: str
    under_30: str
    dependents: str
    referred_a_friend: str
    paperless_billing: str
    premium_tech_support: str
    unlimited_data: str
    multiple_lines: str
    online_backup: str
    device_protection_plan: str
    streaming_tv: str
    streaming_movies: str
    streaming_music: str
    tenure_in_months: float
    avg_monthly_gb_download: float
    monthly_charge: float
    contract: str
    payment_method: str
    offer: str
    internet_type: str
    satisfaction_score: int


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict
