from __future__ import annotations

from datetime import datetime, timezone
from typing import Union
from uuid import UUID, uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.schemas.errors import ErrorResponse
from app.schemas.insights import (
    NeedsClarificationResponse,
    Pagination,
    PromptRequest,
    PromptSuccessResponse,
)
from app.services.ai_service import generate_dummy_insights

router = APIRouter(prefix="/api", tags=["prompt"])


@router.post(
    "/prompt",
    response_model=Union[PromptSuccessResponse, NeedsClarificationResponse],
    summary="Submit a prompt",
    description=(
        "Validates the prompt and target language, returns structured errors (4xx), "
        "clarification when the prompt is too short, or paginated insights on success."
    ),
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input (e.g. missing prompt, bad language)."},
        422: {"description": "Validation error (invalid request body)."},
    },
)
def submit_prompt(payload: PromptRequest):
    settings = get_settings()

    prompt = payload.prompt.strip()
    if not prompt:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error="MISSING_PROMPT", message="Prompt is required."
            ).model_dump(),
        )

    if payload.targetLanguage not in settings.supported_languages:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error="INVALID_LANGUAGE",
                message="Target language is not supported.",
            ).model_dump(),
        )

    if len(prompt) < settings.min_prompt_length:
        context_id = payload.contextId or uuid4()
        return NeedsClarificationResponse(
            message="Please provide more details.",
            contextId=context_id,
        )

    context_id = payload.contextId or uuid4()
    all_insights = generate_dummy_insights(prompt, payload.targetLanguage, context_id)

    page_size = payload.pageSize or settings.page_size_default
    page_size = max(1, min(page_size, settings.page_size_max))
    page = max(1, payload.page)

    total = len(all_insights)
    total_pages = max(1, (total + page_size - 1) // page_size)
    if page > total_pages:
        page = total_pages

    start = (page - 1) * page_size
    end = start + page_size
    insights = all_insights[start:end]

    return PromptSuccessResponse(
        contextId=context_id,
        targetLanguage=payload.targetLanguage,
        createdAt=datetime.now(timezone.utc),
        insights=insights,
        pagination=Pagination(
            page=page,
            pageSize=page_size,
            total=total,
            totalPages=total_pages,
            hasMore=page < total_pages,
        ),
    )

