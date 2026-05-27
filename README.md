# Backend (FastAPI) — AI Middleware API

This folder contains the backend “middleware” API for the challenge. It validates incoming prompt requests, decides whether the request needs clarification, and (for success cases) returns deterministic dummy AI insights with pagination metadata.

## Requirements

- Python 3.x

## Run locally

```bash
cd backend
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/uvicorn app.main:app --reload --port 8000
```

## Useful URLs

- Health check: http://localhost:8000/health
- Swagger UI (interactive API testing): http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json

## API overview

### `GET /health`

Returns a simple status payload for readiness / liveness checks.

### `POST /api/prompt`

Accepts:

```json
{
  "prompt": "string (required)",
  "targetLanguage": "en|es|fr|de (required)",
  "contextId": "uuid (optional)",
  "page": 1,
  "pageSize": 10
}
```

#### Success (`status = SUCCESS`)

Returns:
- `insights[]` (array of insight objects)
- `pagination` metadata (`page`, `pageSize`, `total`, `totalPages`, `hasMore`)

#### Clarification (`status = NEEDS_CLARIFICATION`)

If the prompt is too short (fewer than 5 characters), the API returns:

```json
{
  "status": "NEEDS_CLARIFICATION",
  "message": "Please provide more details.",
  "contextId": "..."
}
```

This happens **before** any downstream “AI” work (even though the AI is simulated here).

#### Structured 4xx errors

- Missing/empty prompt:

```json
{ "error": "MISSING_PROMPT", "message": "Prompt is required." }
```

- Unsupported language:

```json
{ "error": "INVALID_LANGUAGE", "message": "Target language is not supported." }
```

## Run tests

```bash
cd backend
./.venv/bin/pytest -q
```

