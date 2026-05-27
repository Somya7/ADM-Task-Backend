from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])

SERVICE_NAME = "ai-middleware-api"
API_VERSION = "1.0.0"


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns service status. Use for load balancers and deployment probes.",
)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
        version=API_VERSION,
    )
