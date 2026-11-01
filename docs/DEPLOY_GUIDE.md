# Deployment Guide

This guide covers everything from first run on your machine to a live URL on Render.com, plus Docker and CI/CD setup.

---

## 1. Run locally

### Prerequisites

- Python 3.11 or 3.12
- Git

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/mohmmad-akeeb/customer-churn-prediction.git
cd customer-churn-prediction

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python run.py
```

Open these in your browser:

- Prediction form: http://localhost:8000
- EDA dashboard: http://localhost:8000/eda
- API docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

To stop the server press Ctrl+C.

---

## 2. Run tests

```bash
pytest tests/ -v
```

Expected output: `53 passed`

To run a single test file:

```bash
pytest tests/test_api_routes.py -v
```

---

## 3. Deploy to Render.com

Render is the recommended deployment platform. The `render.yaml` file is already configured.

### Step 1: Push to GitHub

```bash
# If you haven't initialised git yet
git init
git add .
git commit -m "initial commit"

# Create a new repo on github.com, then connect it
git remote add origin https://github.com/YOUR_USERNAME/customer-churn-prediction.git
git branch -M main
git push -u origin main
```

### Step 2: Create a Web Service on Render

1. Go to https://render.com and sign in with GitHub
2. Click **New** and select **Web Service**
3. Select your repository
4. Fill in the settings:

| Field | Value |
|---|---|
| Name | customer-churn-prediction |
| Environment | Python 3 |
| Region | Pick the closest to your users |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

5. Click **Create Web Service**
6. Render builds and deploys automatically. Takes 2-4 minutes on first deploy.

### Step 3: Verify the deployment

Replace `your-app-name` with whatever Render assigned:

```bash
curl https://your-app-name.onrender.com/api/health
# Expected: {"status":"healthy","model_loaded":true}
```

### Environment variables (optional)

On the Render dashboard go to your service, then **Environment**, and add:

```
PYTHON_VERSION=3.11.9
```

### Auto-deploy on push

Render auto-deploys whenever you push to `main`. You can disable this in Dashboard > Settings > Auto-Deploy.

---

## 4. Enable CI/CD with GitHub Actions

The workflow file is at `.github/workflows/ci.yml`. It runs lint, tests, Docker build, and deploy automatically.

### What you need to add

In your GitHub repo go to **Settings > Secrets and variables > Actions**.

Add these secrets:

| Name | Where to find it |
|---|---|
| `RENDER_DEPLOY_HOOK_URL` | Render dashboard > your service > Settings > Deploy Hook > Copy URL |

Add these variables:

| Name | Value |
|---|---|
| `RENDER_APP_URL` | Your Render app URL, e.g. `https://customer-churn-prediction.onrender.com` |

Once set, every push to `main` will:
1. Lint the code with ruff
2. Run the full test suite on Python 3.11 and 3.12
3. Build the Docker image
4. Trigger a deploy to Render

Pull requests trigger lint and tests only (no deploy).

---

## 5. Run with Docker

### Using Docker Compose (easiest)

```bash
docker compose up
```

The app will be available at http://localhost:8000.

To stop it:

```bash
docker compose down
```

### Using Docker CLI

```bash
# Build the image
docker build -t churnsight:latest .

# Run a container
docker run -d \
  --name churnsight \
  -p 8000:8000 \
  churnsight:latest

# Check logs
docker logs -f churnsight

# Stop
docker stop churnsight
docker rm churnsight
```

### Build for production (no cache, multi-arch)

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t churnsight:v1.0.0 \
  --no-cache .
```

---

## 6. Push Docker image to Docker Hub

```bash
# Log in
docker login

# Tag
docker tag churnsight:latest YOUR_DOCKERHUB_USERNAME/churnsight:latest
docker tag churnsight:latest YOUR_DOCKERHUB_USERNAME/churnsight:v1.0.0

# Push
docker push YOUR_DOCKERHUB_USERNAME/churnsight:latest
docker push YOUR_DOCKERHUB_USERNAME/churnsight:v1.0.0
```

---

## 7. Deploy to other platforms

### Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Fly.io

```bash
fly launch
fly deploy
```

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/churnsight
gcloud run deploy churnsight \
  --image gcr.io/PROJECT_ID/churnsight \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 8. Test the API manually

### Health check

```bash
curl https://your-app.onrender.com/api/health
```

### Predict (high-risk customer)

```bash
curl -X POST https://your-app.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "tenure_in_months": 6,
    "avg_monthly_gb_download": 45,
    "monthly_charge": 95.50,
    "contract": "Month-to-Month",
    "payment_method": "Electronic Check",
    "offer": "None",
    "internet_type": "Fiber Optic",
    "satisfaction_score": 2
  }'
```

Expected response:

```json
{
  "prediction": "WILL CHURN",
  "confidence": 0.93,
  "probabilities": { "0": 0.07, "1": 0.93 }
}
```

### Predict (low-risk customer)

```bash
curl -X POST https://your-app.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "senior_citizen": "No",
    "under_30": "No",
    "dependents": "Yes",
    "referred_a_friend": "Yes",
    "paperless_billing": "No",
    "premium_tech_support": "Yes",
    "unlimited_data": "Yes",
    "multiple_lines": "Yes",
    "online_backup": "Yes",
    "device_protection_plan": "Yes",
    "streaming_tv": "No",
    "streaming_movies": "No",
    "streaming_music": "No",
    "tenure_in_months": 48,
    "avg_monthly_gb_download": 20,
    "monthly_charge": 55.00,
    "contract": "Two Year",
    "payment_method": "Credit Card (automatic)",
    "offer": "Offer B",
    "internet_type": "DSL",
    "satisfaction_score": 5
  }'
```

---

## 9. Troubleshooting

**Model not loading**

Check that `models/best_model_pipeline.pkl` exists:

```bash
ls -lh models/
```

If missing, re-run the model training notebook: `notebooks/ModelSelection.ipynb`

**Port already in use**

```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

**Dependency conflicts**

```bash
pip install -r requirements.txt --force-reinstall
```

**Docker out of memory**

```bash
docker run -d \
  --name churnsight \
  -p 8000:8000 \
  --memory="512m" \
  churnsight:latest
```

**Render deploy stuck**

Check the build logs in the Render dashboard. The most common cause is a dependency failing to install. Check that `requirements.txt` has pinned versions.
