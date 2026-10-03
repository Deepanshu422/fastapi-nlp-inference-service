from typing import List
from pydantic import BaseModel, Field
from app.schemas.base import BaseInferenceResponse


class ClassificationRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=3, 
        max_length=2000, 
        description="The raw text document or snippet to classify."
    )
    candidate_labels: List[str] = Field(
        ..., 
        min_length=1, 
        description="List of target categories to classify against on-the-fly."
    )
    multi_label: bool = Field(
        default=False, 
        description="If True, labels can independently score high (non-mutually exclusive)."
    )


class LabelScore(BaseModel):
    label: str = Field(..., description="Candidate category name")
    score: float = Field(..., description="Softmax confidence score (0.0 to 1.0)")


class ClassificationResponse(BaseInferenceResponse):
    top_label: str = Field(..., description="Highest-scoring candidate category")
    top_score: float = Field(..., description="Confidence score for top_label")
    scores: List[LabelScore] = Field(..., description="Full ranking of all candidate labels")