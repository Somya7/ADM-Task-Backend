from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Insight(BaseModel):
    id: str
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)


class Pagination(BaseModel):
    page: int
    pageSize: int
    total: int
    totalPages: int
    hasMore: bool


class PromptRequest(BaseModel):
    prompt: str
    targetLanguage: str
    contextId: Optional[UUID] = None
    page: int = 1
    pageSize: Optional[int] = None


class PromptSuccessResponse(BaseModel):
    status: str = "SUCCESS"
    contextId: UUID
    targetLanguage: str
    createdAt: datetime
    insights: list[Insight]
    pagination: Pagination


class NeedsClarificationResponse(BaseModel):
    status: str = "NEEDS_CLARIFICATION"
    message: str
    contextId: UUID

