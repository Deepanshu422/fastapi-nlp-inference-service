from typing import List
from pydantic import BaseModel, Field
from app.schemas.base import BaseInferenceResponse

class ExtractionRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=3, 
        max_length=2000, 
        description="The raw text containing entities to extract or redact."
    )
    confidence_threshold: float = Field(
        default=0.5, 
        ge=0.0, 
        le=1.0, 
        description="Minimum confidence score required to include an extracted entity."
    )

class ExtractedEntity(BaseModel):
    entity_group: str = Field(..., description="Category: PER (Person), ORG (Organization), LOC (Location), MISC")
    word: str = Field(..., description="The reconstructed entity text string")
    score: float = Field(..., description="Confidence score (0.0 to 1.0)")
    start: int = Field(..., description="Character start index in input text")
    end: int = Field(..., description="Character end index in input text")


class ExtractionResponse(BaseInferenceResponse):
    entities_count: int = Field(..., description="Total number of entities detected above threshold")
    entities: List[ExtractedEntity] = Field(..., description="Extracted entity objects")