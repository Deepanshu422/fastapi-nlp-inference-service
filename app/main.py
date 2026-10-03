from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.services.model_registry import ModelRegistry
from app.api.v1.router import api_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager handling startup model loading and shutdown cleanup."""
    print("Initializing Model Registry & Loading Pipelines into RAM...")
    ModelRegistry.load_models()
    print("Pipelines loaded & warmed up successfully, Ready for inference.")
    yield
    print("Shutting down NLP service & releasing resources.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",   # Interactive Swagger UI URL
    redoc_url="/redoc"
)

# mount the centralized V1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)