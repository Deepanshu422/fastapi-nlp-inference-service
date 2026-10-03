import time
from fastapi import APIRouter, HTTPException, status
from app.schemas.classification import ClassificationRequest, ClassificationResponse, LabelScore
from app.services.model_registry import ModelRegistry
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/classify", response_model=ClassificationResponse, summary="Classify text dynamically")
def classify_text(payload: ClassificationRequest):
    """Classifies input text against arbitrary candidate labels on-the-fly."""
    try:
        pipeline = ModelRegistry.get_zero_shot_pipeline()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    # measure inference duration
    start_time = time.perf_counter()
    raw_result = pipeline(
        payload.text,
        candidate_labels=payload.candidate_labels,
        multi_label=payload.multi_label
    )

    latency_ms = (time.perf_counter() - start_time) * 1000

    # map raw Hugging Face outputs to our pydantic schema
    labels = raw_result["labels"]
    scores = raw_result["scores"]

    label_scores = [
        LabelScore(label=label, score=round(score, 4))
        for label, score in zip(labels, scores)
    ]

    return ClassificationResponse(
        status="success",
        model_name=settings.ZERO_SHOT_MODEL,
        latency_ms=round(latency_ms, 2),
        top_label=labels[0],
        top_score=round(scores[0], 4),
        scores=label_scores
    )