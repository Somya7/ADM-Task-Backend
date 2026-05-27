from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_health_returns_ok():
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["service"] == "ai-middleware-api"
    assert body["version"] == "1.0.0"


def test_swagger_docs_available():
    res = client.get("/api/docs")
    assert res.status_code == 200
    assert "swagger" in res.text.lower() or "openapi" in res.text.lower()


def test_openapi_json_available():
    res = client.get("/api/openapi.json")
    assert res.status_code == 200
    spec = res.json()
    assert spec["info"]["title"] == "AI Middleware API"
    assert "/health" in spec["paths"]
    assert "/api/prompt" in spec["paths"]
