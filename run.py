#!/usr/bin/env python3
"""
Simple script to run the FastAPI Customer Churn Prediction app
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Customer Churn Prediction API...")
    print("📊 Web Interface: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )