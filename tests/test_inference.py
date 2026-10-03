def test_classify_endpoint_success(client):
    """Verifies valid zero-shot text classification inference."""
    payload = {
        "text": "Lupin Pharma announced strong quarterly earnings with a 24% revenue surge.",
        "candidate_labels": ["Quarterly Earnings", "Litigation", "Sports"],
        "multi_label": False
    }
    response = client.post("/api/v1/classify", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["top_label"] == "Quarterly Earnings"
    assert 0.0 <= data["top_score"] <= 1.0
    assert data["latency_ms"] > 0
    assert len(data["scores"]) == 3


def test_classify_validation_error(client):
    """Verifies that Pydantic rejects invalid or empty payloads."""
    payload = {
        "text": "",  # Violates min_length=3
        "candidate_labels": []  # Violates min_length=1
    }
    response = client.post("/api/v1/classify", json=payload)
    # Must fail at the gateway before reaching the model
    assert response.status_code == 422


def test_extract_endpoint_success(client):
    """Verifies valid Named Entity Recognition inference and schema output."""
    payload = {
        "text": "Sundar Pichai visited Google headquarters in California.",
        "confidence_threshold": 0.6
    }
    response = client.post("/api/v1/extract", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["entities_count"] >= 1
    
    # Check that entities contain required schema fields
    first_entity = data["entities"][0]
    assert "entity_group" in first_entity
    assert "word" in first_entity
    assert "score" in first_entity
    assert first_entity["score"] >= 0.6