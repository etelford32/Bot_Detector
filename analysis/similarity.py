"""Semantic similarity analysis for comments."""

from typing import List, Dict, Tuple, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute pairwise cosine similarity matrix.

    Args:
        embeddings: Array of embeddings (shape: [n, embedding_dim])

    Returns:
        Similarity matrix (shape: [n, n])
    """
    return cosine_similarity(embeddings)


def find_high_similarity_pairs(
    similarity_matrix: np.ndarray,
    threshold: float = 0.85,
) -> List[Tuple[int, int, float]]:
    """Find pairs of comments with high similarity.

    Args:
        similarity_matrix: Pairwise similarity matrix
        threshold: Minimum similarity threshold

    Returns:
        List of (idx1, idx2, similarity) tuples
    """
    pairs = []
    n = similarity_matrix.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_matrix[i, j]
            if sim >= threshold:
                pairs.append((i, j, float(sim)))

    # Sort by similarity (descending)
    pairs.sort(key=lambda x: x[2], reverse=True)

    return pairs


def find_similar_groups(
    similarity_matrix: np.ndarray,
    threshold: float = 0.85,
    min_group_size: int = 3,
) -> List[List[int]]:
    """Find groups of mutually similar comments.

    Args:
        similarity_matrix: Pairwise similarity matrix
        threshold: Minimum similarity threshold
        min_group_size: Minimum group size to return

    Returns:
        List of groups (each group is a list of indices)
    """
    n = similarity_matrix.shape[0]
    visited = set()
    groups = []

    for i in range(n):
        if i in visited:
            continue

        # Find all comments similar to this one
        similar = [i]
        for j in range(n):
            if i != j and similarity_matrix[i, j] >= threshold:
                similar.append(j)

        if len(similar) >= min_group_size:
            # Check if this is a new group
            similar_set = set(similar)
            is_new = True
            for existing_group in groups:
                if similar_set == set(existing_group):
                    is_new = False
                    break

            if is_new:
                groups.append(similar)
                visited.update(similar)

    return groups


def detect_template_usage(
    comments: List[str],
    embeddings: np.ndarray,
    threshold: float = 0.90,
    min_instances: int = 3,
) -> List[Dict[str, Any]]:
    """Detect template-based commenting patterns.

    Args:
        comments: List of comment texts
        embeddings: Comment embeddings
        threshold: Similarity threshold for template matching
        min_instances: Minimum instances to count as template

    Returns:
        List of detected templates with metadata
    """
    similarity_matrix = compute_similarity_matrix(embeddings)
    groups = find_similar_groups(similarity_matrix, threshold, min_instances)

    templates = []
    for group in groups:
        # Get representative comment (most central)
        group_sims = similarity_matrix[group][:, group]
        avg_sims = group_sims.mean(axis=1)
        representative_idx = group[np.argmax(avg_sims)]

        template = {
            "representative": comments[representative_idx],
            "instances": [comments[i] for i in group],
            "indices": group,
            "count": len(group),
            "avg_similarity": float(avg_sims.mean()),
        }
        templates.append(template)

    # Sort by count (most common first)
    templates.sort(key=lambda x: x["count"], reverse=True)

    return templates


def calculate_semantic_score(
    embeddings: np.ndarray,
    similarity_threshold: float = 0.85,
) -> Dict[str, float]:
    """Calculate semantic similarity score metrics.

    Args:
        embeddings: Comment embeddings
        similarity_threshold: Threshold for high similarity

    Returns:
        Dictionary of semantic metrics
    """
    if len(embeddings) < 2:
        return {
            "semantic_score": 0.0,
            "avg_similarity": 0.0,
            "max_similarity": 0.0,
            "high_similarity_ratio": 0.0,
            "cluster_homogeneity": 0.0,
        }

    similarity_matrix = compute_similarity_matrix(embeddings)

    # Get upper triangle (exclude diagonal)
    upper_triangle = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]

    avg_similarity = float(upper_triangle.mean())
    max_similarity = float(upper_triangle.max())

    # Ratio of high similarity pairs
    high_sim_count = (upper_triangle >= similarity_threshold).sum()
    total_pairs = len(upper_triangle)
    high_similarity_ratio = high_sim_count / total_pairs if total_pairs > 0 else 0.0

    # Cluster homogeneity (how tight are the groups?)
    groups = find_similar_groups(similarity_matrix, similarity_threshold)
    if groups:
        group_sizes = [len(g) for g in groups]
        largest_group_ratio = max(group_sizes) / len(embeddings)
        cluster_homogeneity = largest_group_ratio
    else:
        cluster_homogeneity = 0.0

    # Calculate overall semantic score (0-100)
    # Higher score = more coordinated/similar
    semantic_score = (
        0.4 * (avg_similarity * 100) +
        0.3 * (high_similarity_ratio * 100) +
        0.3 * (cluster_homogeneity * 100)
    )

    return {
        "semantic_score": float(semantic_score),
        "avg_similarity": avg_similarity,
        "max_similarity": max_similarity,
        "high_similarity_ratio": high_similarity_ratio,
        "cluster_homogeneity": cluster_homogeneity,
    }


def calculate_diversity_metrics(
    embeddings: np.ndarray,
) -> Dict[str, float]:
    """Calculate diversity metrics for embeddings.

    Args:
        embeddings: Comment embeddings

    Returns:
        Dictionary of diversity metrics
    """
    if len(embeddings) < 2:
        return {
            "std_similarity": 0.0,
            "diversity_index": 0.0,
        }

    similarity_matrix = compute_similarity_matrix(embeddings)
    upper_triangle = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]

    # Standard deviation of similarities (higher = more diverse)
    std_similarity = float(upper_triangle.std())

    # Diversity index (inverse of average similarity)
    avg_similarity = float(upper_triangle.mean())
    diversity_index = 1.0 - avg_similarity

    return {
        "std_similarity": std_similarity,
        "diversity_index": diversity_index,
    }
