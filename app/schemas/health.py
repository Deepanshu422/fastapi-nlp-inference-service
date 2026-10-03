from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Operational status of the service")
    models_loaded: bool = Field(..., description="True if pipelines are resident in RAM, False otherwise")