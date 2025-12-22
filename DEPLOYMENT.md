# 🚀 Deployment Guide

## ✅ Files Created

1. **`.gitignore`** - Excludes unnecessary files from Git
2. **`.env`** - Environment variables (not committed to Git)
3. **`.env.example`** - Template for environment variables
4. **`Procfile`** - For Render/Heroku deployment
5. **`runtime.txt`** - Specifies Python version
6. **`render.yaml`** - Render.com configuration
7. **`vercel.json`** - Vercel configuration
8. **`DEPLOYMENT.md`** - Comprehensive deployment guide
9. **`README.md`** - Project documentation

## ✅ Requirements File Status

**Updated and Verified:**
- ✅ FastAPI 0.104.1
- ✅ Uvicorn 0.24.0 (with standard extras)
- ✅ Pandas 2.2.2
- ✅ scikit-learn 1.7.1
- ✅ Joblib 1.4.2
- ✅ python-multipart 0.0.6
- ✅ Jinja2 3.1.2
- ✅ NumPy (added as dependency)

## 🚀 Deployment Steps (Render.com)

### Step 1: Prepare Git Repository
```bash
git init
git add .
git commit -m "Initial commit - Customer Churn Prediction App"
```

### Step 2: Push to GitHub
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/churn-prediction.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your repository
5. Configure:
   - **Name**: `customer-churn-prediction`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Your app is live! 🎉

### Step 4: Test Your Deployment
```
https://customer-churn-prediction.onrender.com/
https://customer-churn-prediction.onrender.com/health
https://customer-churn-prediction.onrender.com/docs
```

## 🔧 Environment Variables (Optional)

On Render dashboard, you can add:
```
PYTHON_VERSION=3.11.9
```

## ⚡ Quick Commands

### Local Testing
```bash
python run.py
# Visit: http://localhost:8000
```

### Check Model
```bash
python test_model.py
python inspect_model.py
```

### Git Commands
```bash
git status
git add .
git commit -m "Your message"
git push
```

