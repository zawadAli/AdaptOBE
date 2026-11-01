"""Help-article retrieval for chatbot Phase 1.

Finds the help articles most relevant to a question using the same
`all-MiniLM-L6-v2` embeddings the CLO/PLO mapping engine uses. Article vectors
are computed once and cached in-process (the corpus is a few dozen short,
static articles), never re-encoded per request. Only articles the caller's role
may see are ever considered.
"""

import logging

from app.core.help_docs import HELP_ARTICLES, HelpArticle, articles_for_role
from app.ml import embeddings

logger = logging.getLogger(__name__)

TOP_K = 3
#: Below this cosine similarity an article is treated as unrelated.
MIN_SCORE = 0.2

# No lock: two concurrent first-time encodes of the same article just compute
# the same vector twice, which is harmless, and a module-level asyncio.Lock
# would bind to whichever event loop touched it first.
_vectors: dict[str, list[float]] = {}


def _article_text(article: HelpArticle) -> str:
    return f"{article.title}. {article.body}"


def _dot(a: list[float], b: list[float]) -> float:
    # Embeddings are L2-normalised, so the dot product is the cosine similarity.
    return sum(x * y for x, y in zip(a, b))


async def _vector_for(article: HelpArticle) -> list[float]:
    if article.id not in _vectors:
        _vectors[article.id] = await embeddings.aencode_text(_article_text(article))
    return _vectors[article.id]


def reset_cache() -> None:
    _vectors.clear()


async def warm_up() -> None:
    """Load the embedding model and encode every article ahead of the first question.

    Started as a background task at app startup, so the first chatbot user
    doesn't wait ~20s for the model to load. A failure here is only logged;
    search() still encodes lazily on demand.
    """
    try:
        for article in HELP_ARTICLES:
            await _vector_for(article)
        logger.info("Help articles encoded: %d", len(_vectors))
    except Exception:  # noqa: BLE001 - warm-up must never affect the running app
        logger.exception("Help-article warm-up failed; articles will be encoded on first use")


async def search(question: str, role: str, top_k: int = TOP_K) -> list[tuple[HelpArticle, float]]:
    """Return up to `top_k` (article, score) pairs visible to `role`, best first."""
    candidates = articles_for_role(role)
    if not candidates or not question.strip():
        return []

    query = await embeddings.aencode_text(question)
    scored = []
    for article in candidates:
        score = _dot(query, await _vector_for(article))
        if score >= MIN_SCORE:
            scored.append((article, score))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]
