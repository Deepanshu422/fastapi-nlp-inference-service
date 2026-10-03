import time
from fastapi import APIRouter, HTTPException, status
from app.schemas.extraction import ExtractionRequest, ExtractionResponse, ExtractedEntity
from app.services.model_registry import ModelRegistry
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/extract", response_model=ExtractionResponse, summary="Extract named entities")
def extract_entities(payload: ExtractionRequest):
    """Identifies and extracts entities (Persons, Organizations, Locations) from text."""

    try:
        pipeline = ModelRegistry.get_ner_pipeline()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    start_time = time.perf_counter()
    raw_entities = pipeline(payload.text)
    latency_ms = (time.perf_counter() - start_time) * 1000

    # filter & construct entity models
    filtered_entities = []
    for item in raw_entities:
        score = round(float(item["score"]), 4)

        if score >= payload.confidence_threshold:
            filtered_entities.append(
                ExtractedEntity(
                    entity_group=item["entity_group"],
                    word=item["word"].strip(),
                    score=score,
                    start=item["start"],
                    end=item["end"]
                )
            )

    return ExtractionResponse(
        status="success",
        model_name=settings.NER_MODEL,
        latency_ms=round(latency_ms, 2),
        entities_count=len(filtered_entities),
        entities=filtered_entities
    )