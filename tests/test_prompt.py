from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_missing_prompt_returns_400():
    res = client.post("/api/prompt", json={"prompt": " ", "targetLanguage": "en"})
    assert res.status_code == 400
    assert res.json()["error"] == "MISSING_PROMPT"


def test_invalid_language_returns_400():
    res = client.post("/api/prompt", json={"prompt": "hello world", "targetLanguage": "xx"})
    assert res.status_code == 400
    assert res.json()["error"] == "INVALID_LANGUAGE"


def test_too_short_prompt_needs_clarification():
    res = client.post("/api/prompt", json={"prompt": "hey", "targetLanguage": "en"})
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "NEEDS_CLARIFICATION"
    assert "message" in body
    assert "contextId" in body


def test_success_returns_paginated_insights():
    res = client.post(
        "/api/prompt",
        json={
            "prompt": "explain caching strategies for apis",
            "targetLanguage": "en",
            "contextId": str(uuid4()),
            "page": 1,
            "pageSize": 10,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "SUCCESS"
    assert len(body["insights"]) == 10
    assert body["pagination"]["total"] >= 10
    assert body["pagination"]["page"] == 1

