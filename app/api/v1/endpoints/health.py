from fastapi import APIRouter, status, Response
from app.schemas.health import HealthResponse
from app.services.model_registry import ModelRegistry

router = APIRouter()

@router.get("/live", response_model=HealthResponse, summary="Liveness Probe")
def liveness_check():
    """Confirms that the web server process is running."""
    return HealthResponse(status="alive", models_loaded=ModelRegistry.is_ready())

@router.get("/ready", response_model=HealthResponse, summary="Readiness Probe")
def readiness_check(response: Response):
    """Confirms i ML models are fully loaded and ready for inference."""
    ready = ModelRegistry.is_ready()
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="loading", models_loaded=False)
    
    return HealthResponse(status="ready", models_loaded=True)
