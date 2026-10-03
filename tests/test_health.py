def test_liveness_probe(client):
    """Verifies that the web server is alive."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "models_loaded" in data


def test_readiness_probe(client):
    """Verifies that the ML models are fully warmed up in RAM."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["models_loaded"] is True