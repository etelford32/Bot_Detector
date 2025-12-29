"""Text embedding module."""

from embeddings.embedder import (
    TextEmbedder,
    cosine_distance,
    euclidean_distance,
)
from embeddings.cache import (
    EmbeddingCache,
    CachedEmbedder,
)

__all__ = [
    "TextEmbedder",
    "cosine_distance",
    "euclidean_distance",
    "EmbeddingCache",
    "CachedEmbedder",
]
