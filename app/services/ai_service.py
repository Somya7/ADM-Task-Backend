from __future__ import annotations

import hashlib
from uuid import UUID

from app.schemas.insights import Insight


def _stable_id(*parts: str) -> str:
    raw = "|".join(parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def generate_dummy_insights(prompt: str, target_language: str, context_id: UUID) -> list[Insight]:
    """
    Deterministic dummy insights generator.

    This simulates an "AI middleware" without any external LLM calls.
    """
    seed_words = [w.strip(".,!?;:()[]{}\"'").lower() for w in prompt.split()]
    seed_words = [w for w in seed_words if w]
    if not seed_words:
        seed_words = ["insight"]

    insights: list[Insight] = []
    for idx in range(1, 26):  # generate >10 to exercise pagination
        word = seed_words[(idx - 1) % len(seed_words)]
        title = f"{word.title()} – Insight {idx}"
        content = (
            f"This is a simulated insight for '{word}' in '{target_language}'. "
            f"It is tied to context {str(context_id)[:8]}."
        )
        tags = ["dummy", target_language, word]
        insights.append(
            Insight(
                id=_stable_id(str(context_id), target_language, word, str(idx)),
                title=title,
                content=content,
                tags=tags,
            )
        )

    return insights

