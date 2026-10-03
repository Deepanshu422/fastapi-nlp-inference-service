import time
from typing import Dict, Any, List
from transformers import pipeline
from app.core.config import get_settings

settings = get_settings()

class ModelRegistry:
    """Thread-safe Singleton managing the lifecycle of transformer pipelines."""

    _zero_shot_pipeline = None
    _ner_pipeline = None
    _is_ready: bool = False

    @classmethod
    def load_models(cls) -> None:
        """Loads models into RAM when application starts."""
        if cls._is_ready:
            return

        # initialize zero-shot pipeline
        cls._zero_shot_pipeline = pipeline(
            task="zero-shot-classification",
            model=settings.ZERO_SHOT_MODEL,
            device=settings.DEVICE 
        )

        # initialize Named Entity Recognition (NER) Pipeline
        cls._ner_pipeline = pipeline(
            task="token-classification",
            model=settings.NER_MODEL,
            aggregation_strategy="simple",
            device=settings.DEVICE
        )

        # 3. Model Warmup (eliminates cold-start inference latencys)
        cls._zero_shot_pipeline("Warmup text", candidate_labels=["test", "warmup"])
        cls._ner_pipeline("Warmup entity")

        cls._is_ready = True

    @classmethod
    def is_ready(cls)-> bool:
        """Returns True if all pipelines are initialized & loaded in the memory."""
        return cls._is_ready

    @classmethod
    def get_zero_shot_pipeline(cls):
        if not cls._is_ready:
            raise RuntimeError("Zero-shot model is not loaded yet.")
        return cls._zero_shot_pipeline

    @classmethod
    def get_ner_pipeline(cls):
        if not cls._is_ready:
            raise RuntimeError("NER model is not loaded yet.")
        return cls._ner_pipeline