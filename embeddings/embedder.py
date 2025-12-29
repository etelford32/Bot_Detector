"""Text embedding using sentence transformers."""

import os
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class TextEmbedder:
    """Wrapper for sentence transformer embeddings."""

    def __init__(self, model_name: str = None):
        """Initialize embedder.

        Args:
            model_name: Sentence transformer model name
                       (defaults to all-MiniLM-L6-v2)
        """
        self.model_name = model_name or os.getenv(
            "EMBEDDING_MODEL", "all-MiniLM-L6-v2"
        )
        self.model = SentenceTransformer(self.model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings for text(s).

        Args:
            texts: Single text or list of texts

        Returns:
            Numpy array of embeddings (shape: [n_texts, embedding_dim])
        """
        # Handle single text
        if isinstance(texts, str):
            texts = [texts]

        # Filter empty texts
        valid_texts = [t if t else " " for t in texts]

        # Generate embeddings
        embeddings = self.model.encode(
            valid_texts,
            convert_to_numpy=True,
            show_progress_bar=len(valid_texts) > 100,
        )

        return embeddings

    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
    ) -> np.ndarray:
        """Generate embeddings in batches.

        Args:
            texts: List of texts
            batch_size: Batch size for encoding

        Returns:
            Numpy array of embeddings
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return embeddings

    def similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity score (0-1)
        """
        emb1, emb2 = self.embed([text1, text2])

        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

        return float(similarity)

    def batch_similarity(self, embeddings: np.ndarray) -> np.ndarray:
        """Compute pairwise cosine similarity matrix.

        Args:
            embeddings: Array of embeddings (shape: [n, embedding_dim])

        Returns:
            Similarity matrix (shape: [n, n])
        """
        # Normalize embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized = embeddings / norms

        # Compute similarity matrix
        similarity_matrix = np.dot(normalized, normalized.T)

        return similarity_matrix

    def find_similar(
        self,
        query: str,
        candidates: List[str],
        top_k: int = 5,
        threshold: float = 0.5,
    ) -> List[tuple]:
        """Find most similar texts to query.

        Args:
            query: Query text
            candidates: List of candidate texts
            top_k: Number of top results to return
            threshold: Minimum similarity threshold

        Returns:
            List of (index, text, similarity) tuples
        """
        # Embed query and candidates
        all_texts = [query] + candidates
        embeddings = self.embed(all_texts)

        query_emb = embeddings[0]
        candidate_embs = embeddings[1:]

        # Compute similarities
        similarities = []
        for idx, emb in enumerate(candidate_embs):
            sim = np.dot(query_emb, emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(emb)
            )
            if sim >= threshold:
                similarities.append((idx, candidates[idx], float(sim)))

        # Sort by similarity
        similarities.sort(key=lambda x: x[2], reverse=True)

        return similarities[:top_k]

    def get_model_info(self) -> dict:
        """Get information about the current model.

        Returns:
            Model information dictionary
        """
        return {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "max_seq_length": self.model.max_seq_length,
        }


def cosine_distance(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Compute cosine distance (1 - similarity).

    Args:
        emb1: First embedding
        emb2: Second embedding

    Returns:
        Cosine distance (0-2, where 0 = identical)
    """
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return 1.0 - similarity


def euclidean_distance(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Compute Euclidean distance between embeddings.

    Args:
        emb1: First embedding
        emb2: Second embedding

    Returns:
        Euclidean distance
    """
    return float(np.linalg.norm(emb1 - emb2))
