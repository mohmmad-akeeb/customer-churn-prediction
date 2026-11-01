#!/usr/bin/env python3
"""
Entry point — start the Customer Churn Prediction app locally.

Usage:
    python run.py
"""
import uvicorn

if __name__ == "__main__":
    print("Starting Customer Churn Prediction API...")
    print("Web Interface : http://localhost:8000")
    print("API Docs      : http://localhost:8000/docs")
    print("Health Check  : http://localhost:8000/api/health")
    print("\nPress Ctrl+C to stop.\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
