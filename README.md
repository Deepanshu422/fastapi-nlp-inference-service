# NLP Pipeline Service

An asynchronous, containerized NLP inference microservice built with **FastAPI**, **Pydantic v2**, and **Hugging Face Transformers**.

The service provides optimized endpoints for zero-shot text classification and token-level Named Entity Recognition (NER). It uses a singleton memory registry pattern to preload transformer models on startup, eliminating cold-start latency during inference requests.

---

## 🚀 Key Features

* **Dual NLP Capabilities:**
  * **Named Entity Recognition (NER):** Extracts real-world entities (`PER`, `ORG`, `LOC`, `MISC`) with boundary indices and score filtering.
  * **Zero-Shot Classification:** Dynamic topic/intent categorization against on-the-fly candidate labels without retraining.
* **In-Memory Singleton Architecture:** Models load once into RAM during the FastAPI lifespan cycle.
* **Persistent Cache Management:** Dedicated local volume caching (`./model_cache`) prevents redundant model re-downloads across container rebuilds.
* **Production Observability:** Built-in latency metrics per request (`latency_ms`) and dedicated liveness/readiness probes (`/health/live`, `/health/ready`).
* **Complete CI/CD & Automation:** Standardized task runner via `Makefile`, end-to-end `pytest` suite, and automated GitHub Actions workflow.

---

## 📁 Repository Structure

```text
nlp-pipeline-service/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow (lint, test, build)
├── app/
│   ├── core/                  # App configuration & settings (.env schema)
│   ├── schemas/               # Pydantic request & response models
│   ├── services/              # Hugging Face ModelRegistry singleton
│   ├── routers/               # API endpoints (/extract, /classify, /health)
│   └── main.py                # FastAPI lifecycle & application entrypoint
├── model_cache/               # Local cache mount for Hugging Face model weights
├── tests/                     # Automated Pytest test suite
│   ├── conftest.py            # Test fixtures and TestClient setups
│   ├── test_health.py         # Liveness and readiness probe validations
│   └── test_inference.py      # NER & zero-shot classification endpoint tests
├── .dockerignore              # Files excluded from Docker builds
├── .env.example               # Template environment configuration
├── docker-compose.yml         # Container orchestration with volume mounts
├── Dockerfile                 # Multi-stage lightweight production build
├── Makefile                   # Standardized CLI commands
├── pyproject.toml             # Ruff and Pytest tooling configurations
├── requirements.txt           # Pinned application dependencies
└── README.md


🤖 Models & Architecture



3. Populate Model Cache (Recommended)If you already have model weights saved on your host machine, copy them to prevent internet downloads:Bashcp -r ~/.cache/huggingface/* model_cache/
4. Run Development ServerBashmake run
Access the interactive Swagger UI documentation at:👉 http://localhost:8000/docs🐳 Running with Docker ComposeRun the pipeline in an isolated, production-grade container. The container mounts ./model_cache to preserve weights across runs.1. Build and Start ContainerBashmake compose-up
(To run on a custom host port, run: make compose-up PORT=8001)2. View Real-Time LogsBashmake compose-logs
3. Tear Down ContainerBashmake compose-down
🧪 Testing & Code QualityRun the test suite covering input validation, inference outputs, and health endpoints:Bashmake test
Clean bytecode, caches, and test artifacts:Bashmake clean
📡 API Contract & Usage Samples1. Named Entity RecognitionEndpoint: POST /extractRequest Payload:JSON{
  "text": "Sundar Pichai announced new Gemini models at Google headquarters in Mountain View.",
  "confidence_threshold": 0.85
}
Response Body:JSON{
  "status": "success",
  "model_name": "dslim/bert-base-NER",
  "latency_ms": 32.4,
  "entities_count": 3,
  "entities": [
    {
      "entity_group": "PER",
      "word": "Sundar Pichai",
      "score": 0.9982,
      "start": 0,
      "end": 13
    },
    {
      "entity_group": "ORG",
      "word": "Google",
      "score": 0.9951,
      "start": 45,
      "end": 51
    },
    {
      "entity_group": "LOC",
      "word": "Mountain View",
      "score": 0.9924,
      "start": 68,
      "end": 81
    }
  ]
}
2. Zero-Shot Topic ClassificationEndpoint: POST /classifyRequest Payload:JSON{
  "text": "The transaction failed and money was debited from my bank account.",
  "candidate_labels": ["Billing Issue", "Account Security", "General Inquiry"],
  "multi_label": false
}
Response Body:JSON{
  "status": "success",
  "model_name": "valhalla/distilbart-mnli-12-3",
  "latency_ms": 54.1,
  "top_label": "Billing Issue",
  "scores": {
    "Billing Issue": 0.9421,
    "Account Security": 0.0458,
    "General Inquiry": 0.0121
  }
}

3.  Health & Readiness ProbesLiveness: GET /health/live — Returns 200 OK if the web service process is active.
    Readiness: GET /health/ready — Returns 200 OK once both models are completely loaded into RAM.