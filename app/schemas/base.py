from pydantic import BaseModel, Field

class BaseInferenceResponse(BaseModel):
    status: str = Field(default="success", description="Execution status of the inference pipeline")
    model_name: str = Field(..., description="Exact Hugging Face model identifier executed")
    latency_ms: float = Field(..., description="End-to-end inference processing time in milliseconds")