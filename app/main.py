"""
FastAPI application factory.
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.services import predictor
from app.routes import web, api, eda

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    predictor.load_model()
    yield
    print("Shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Customer Churn Prediction",
        description="ML-powered churn prediction API with web interface.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Static files
    static_dir = os.path.join(_ROOT, "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Routers
    app.include_router(web.router)
    app.include_router(api.router)
    app.include_router(eda.router)

    return app


app = create_app()
