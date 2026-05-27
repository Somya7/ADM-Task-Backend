from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.prompt import router as prompt_router

API_VERSION = "1.0.0"
OPENAPI_TAGS = [
    {
        "name": "health",
        "description": "Service health and readiness checks.",
    },
    {
        "name": "prompt",
        "description": "Submit prompts and receive AI middleware responses.",
    },
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Middleware API",
        version=API_VERSION,
        description=(
            "Middleware API between a frontend client and a simulated AI service. "
            "Use **Swagger UI** at `/api/docs` to try endpoints interactively."
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        openapi_tags=OPENAPI_TAGS,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(prompt_router)

    return app


app = create_app()

