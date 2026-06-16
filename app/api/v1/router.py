"""
app/api/v1/router.py
--------------------
Aggregates all v1 API routers into a single ``APIRouter``.

Add new feature routers here as they are created.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import exercises, foods, health, meal_templates, measurements, nutrition_logs, recipes, weights

api_v1_router = APIRouter(prefix="/api/v1")

# ---- Register sub-routers -------------------------------------------------
api_v1_router.include_router(health.router)
api_v1_router.include_router(weights.router)
api_v1_router.include_router(measurements.router)
api_v1_router.include_router(exercises.router)
api_v1_router.include_router(foods.router)
api_v1_router.include_router(recipes.router)
api_v1_router.include_router(meal_templates.router)
api_v1_router.include_router(nutrition_logs.router)
