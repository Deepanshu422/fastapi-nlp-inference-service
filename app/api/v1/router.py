from fastapi import APIRouter
from app.api.v1.endpoints import health, classify, extract

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health & Probes"])
api_router.include_router(classify.router, tags=["Zero-Shot Classification"])
api_router.include_router(extract.router, tags=["Named Entity Extraction"])
