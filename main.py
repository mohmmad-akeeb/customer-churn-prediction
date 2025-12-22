from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pandas as pd
import joblib
import warnings
from typing import Optional
import os

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="joblib")

# Global model variable
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load model
    global model
    try:
        model = joblib.load('best_model_pipeline.pkl')
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
    
    yield
    
    # Shutdown: Cleanup (if needed)
    print("Shutting down...")

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using machine learning",
    version="1.0.0",
    lifespan=lifespan
)

# Templates setup
templates = Jinja2Templates(directory="templates")

# Pydantic models for API
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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main prediction form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
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
    satisfaction_score: int = Form(...)
):
    """Handle form submission and return prediction"""
    if model is None:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Model not loaded. Please check the model file."
        })
    
    try:
        # Prepare data for prediction - convert checkbox values to Yes/No
        data = {
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
            "Satisfaction Score": satisfaction_score
        }
        
        # Create DataFrame and make prediction
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Debug: Print model classes and predictions
        print(f"Model classes: {model.classes_}")
        print(f"Prediction: {prediction}")
        print(f"Prediction probabilities: {prediction_proba}")
        
        # Format results
        # The probabilities are ordered according to model.classes_
        # prediction_proba[0] corresponds to model.classes_[0]
        # prediction_proba[1] corresponds to model.classes_[1]
        
        # Find which class was predicted
        try:
            predicted_class_index = list(model.classes_).index(prediction)
            confidence_percentage = prediction_proba[predicted_class_index] * 100
        except ValueError:
            # If prediction not in classes, use max probability
            predicted_class_index = prediction_proba.argmax()
            confidence_percentage = prediction_proba[predicted_class_index] * 100
            print(f"Warning: Prediction '{prediction}' not found in classes. Using max probability.")
        
        # Determine churn vs no-churn
        # Assuming model.classes_ is like ['No', 'Yes'] or [0, 1]
        # We need to identify which index represents "churn"
        classes_str = [str(c).lower() for c in model.classes_]
        
        # Try to identify churn class (usually 'Yes', 'yes', 1, or similar)
        if 'yes' in classes_str:
            churn_index = classes_str.index('yes')
        elif '1' in classes_str:
            churn_index = classes_str.index('1')
        else:
            # Assume index 1 is churn by default
            churn_index = 1
        
        no_churn_index = 1 - churn_index  # The other index
        
        churn_probability = prediction_proba[churn_index] * 100
        no_churn_probability = prediction_proba[no_churn_index] * 100
        will_churn = predicted_class_index == churn_index
        
        print(f"Churn index: {churn_index}, No-churn index: {no_churn_index}")
        print(f"Will churn: {will_churn}, Confidence: {confidence_percentage:.1f}%")
        
        result = {
            "prediction": "WILL CHURN" if will_churn else "WILL NOT CHURN",
            "confidence": f"{confidence_percentage:.1f}%",
            "churn_probability": f"{churn_probability:.1f}%",
            "no_churn_probability": f"{no_churn_probability:.1f}%",
            "status": "danger" if will_churn else "success"
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result
        })
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Prediction error: {str(e)}"
        })

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_api(customer_data: CustomerData):
    """API endpoint for programmatic predictions"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        # Convert to the format expected by the model
        data = {
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
            "Satisfaction Score": customer_data.satisfaction_score
        }
        
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        # Convert prediction to string for API response
        prediction_str = "WILL CHURN" if prediction == model.classes_[1] else "WILL NOT CHURN"
        
        return PredictionResponse(
            prediction=prediction_str,
            confidence=float(prediction_proba.max()),
            probabilities={
                str(model.classes_[0]): float(prediction_proba[0]),
                str(model.classes_[1]): float(prediction_proba[1])
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)