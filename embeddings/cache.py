"""Embedding cache for efficient reuse."""

import hashlib
import pickle
from typing import Optional, Dict, List
import numpy as np
from pathlib import Path

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class EmbeddingCache:
    """Cache for text embeddings."""

    def __init__(
        self,
        cache_type: str = "memory",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        file_cache_dir: Optional[str] = None,
    ):
        """Initialize embedding cache.

        Args:
            cache_type: Cache type (memory, redis, file)
            redis_host: Redis host (for redis cache)
            redis_port: Redis port (for redis cache)
            redis_db: Redis database number
            file_cache_dir: Directory for file cache
        """
        self.cache_type = cache_type
        self.memory_cache: Dict[str, np.ndarray] = {}

        if cache_type == "redis":
            if not REDIS_AVAILABLE:
                raise ImportError("Redis not installed. Install with: pip install redis")
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=False,
            )
        elif cache_type == "file":
            self.cache_dir = Path(file_cache_dir or "embeddings_cache")
            self.cache_dir.mkdir(exist_ok=True)

    def _get_key(self, text: str, model_name: str) -> str:
        """Generate cache key for text and model.

        Args:
            text: Input text
            model_name: Model name

        Returns:
            Cache key (hash)
        """
        content = f"{model_name}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, model_name: str) -> Optional[np.ndarray]:
        """Retrieve embedding from cache.

        Args:
            text: Input text
            model_name: Model name

        Returns:
            Cached embedding or None
        """
        key = self._get_key(text, model_name)

        if self.cache_type == "memory":
            return self.memory_cache.get(key)

        elif self.cache_type == "redis":
            data = self.redis_client.get(key)
            if data:
                return pickle.loads(data)

        elif self.cache_type == "file":
            cache_file = self.cache_dir / f"{key}.npy"
            if cache_file.exists():
                return np.load(cache_file)

        return None

    def set(self, text: str, model_name: str, embedding: np.ndarray) -> None:
        """Store embedding in cache.

        Args:
            text: Input text
            model_name: Model name
            embedding: Embedding vector
        """
        key = self._get_key(text, model_name)

        if self.cache_type == "memory":
            self.memory_cache[key] = embedding

        elif self.cache_type == "redis":
            data = pickle.dumps(embedding)
            self.redis_client.set(key, data)

        elif self.cache_type == "file":
            cache_file = self.cache_dir / f"{key}.npy"
            np.save(cache_file, embedding)

    def get_batch(
        self,
        texts: List[str],
        model_name: str,
    ) -> tuple[List[Optional[np.ndarray]], List[int]]:
        """Retrieve multiple embeddings from cache.

        Args:
            texts: List of texts
            model_name: Model name

        Returns:
            Tuple of (embeddings list, missing indices)
        """
        embeddings = []
        missing_indices = []

        for idx, text in enumerate(texts):
            emb = self.get(text, model_name)
            embeddings.append(emb)
            if emb is None:
                missing_indices.append(idx)

        return embeddings, missing_indices

    def set_batch(
        self,
        texts: List[str],
        model_name: str,
        embeddings: np.ndarray,
    ) -> None:
        """Store multiple embeddings in cache.

        Args:
            texts: List of texts
            model_name: Model name
            embeddings: Array of embeddings
        """
        for text, embedding in zip(texts, embeddings):
            self.set(text, model_name, embedding)

    def clear(self) -> None:
        """Clear the cache."""
        if self.cache_type == "memory":
            self.memory_cache.clear()

        elif self.cache_type == "redis":
            self.redis_client.flushdb()

        elif self.cache_type == "file":
            for cache_file in self.cache_dir.glob("*.npy"):
                cache_file.unlink()

    def size(self) -> int:
        """Get number of cached items.

        Returns:
            Number of cached embeddings
        """
        if self.cache_type == "memory":
            return len(self.memory_cache)

        elif self.cache_type == "redis":
            return self.redis_client.dbsize()

        elif self.cache_type == "file":
            return len(list(self.cache_dir.glob("*.npy")))

        return 0


class CachedEmbedder:
    """Text embedder with caching."""

    def __init__(
        self,
        embedder,
        cache: Optional[EmbeddingCache] = None,
    ):
        """Initialize cached embedder.

        Args:
            embedder: TextEmbedder instance
            cache: EmbeddingCache instance (defaults to memory cache)
        """
        self.embedder = embedder
        self.cache = cache or EmbeddingCache(cache_type="memory")
        self.hits = 0
        self.misses = 0

    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings with caching.

        Args:
            texts: List of texts

        Returns:
            Array of embeddings
        """
        # Check cache
        cached_embeddings, missing_indices = self.cache.get_batch(
            texts, self.embedder.model_name
        )

        # Track hits/misses
        self.hits += len(texts) - len(missing_indices)
        self.misses += len(missing_indices)

        # Generate missing embeddings
        if missing_indices:
            missing_texts = [texts[i] for i in missing_indices]
            new_embeddings = self.embedder.embed(missing_texts)

            # Cache new embeddings
            self.cache.set_batch(
                missing_texts,
                self.embedder.model_name,
                new_embeddings,
            )

            # Insert into results
            for idx, emb_idx in enumerate(missing_indices):
                cached_embeddings[emb_idx] = new_embeddings[idx]

        return np.array(cached_embeddings)

    def get_stats(self) -> dict:
        """Get cache statistics.

        Returns:
            Cache statistics dictionary
        """
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total,
            "hit_rate": hit_rate,
            "cache_size": self.cache.size(),
        }

    def reset_stats(self) -> None:
        """Reset cache statistics."""
        self.hits = 0
        self.misses = 0
