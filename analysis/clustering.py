"""Clustering analysis for comment embeddings."""

from typing import Dict, List, Any, Optional
import numpy as np
import hdbscan
import umap


def perform_clustering(
    embeddings: np.ndarray,
    min_cluster_size: int = 5,
    min_samples: int = 3,
    metric: str = "euclidean",
) -> Dict[str, Any]:
    """Perform HDBSCAN clustering on embeddings.

    Args:
        embeddings: Comment embeddings
        min_cluster_size: Minimum cluster size
        min_samples: Minimum samples for core points
        metric: Distance metric

    Returns:
        Dictionary with cluster labels and metrics
    """
    if len(embeddings) < min_cluster_size:
        return {
            "labels": np.array([-1] * len(embeddings)),
            "n_clusters": 0,
            "noise_ratio": 1.0,
            "cluster_sizes": [],
            "probabilities": np.array([0.0] * len(embeddings)),
        }

    # Perform clustering
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric=metric,
    )

    labels = clusterer.fit_predict(embeddings)
    probabilities = clusterer.probabilities_

    # Calculate metrics
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    noise_count = (labels == -1).sum()
    noise_ratio = noise_count / len(labels)

    # Cluster sizes
    cluster_sizes = []
    for cluster_id in range(n_clusters):
        size = (labels == cluster_id).sum()
        cluster_sizes.append(int(size))

    return {
        "labels": labels,
        "n_clusters": int(n_clusters),
        "noise_ratio": float(noise_ratio),
        "cluster_sizes": cluster_sizes,
        "probabilities": probabilities,
        "clusterer": clusterer,
    }


def reduce_dimensions(
    embeddings: np.ndarray,
    n_components: int = 2,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    metric: str = "cosine",
) -> np.ndarray:
    """Reduce dimensionality using UMAP.

    Args:
        embeddings: High-dimensional embeddings
        n_components: Target dimensions
        n_neighbors: Number of neighbors for UMAP
        min_dist: Minimum distance for UMAP
        metric: Distance metric

    Returns:
        Low-dimensional embeddings
    """
    if len(embeddings) < n_neighbors:
        n_neighbors = max(2, len(embeddings) - 1)

    reducer = umap.UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metric,
    )

    reduced = reducer.fit_transform(embeddings)

    return reduced


def analyze_clusters(
    embeddings: np.ndarray,
    labels: np.ndarray,
    comments: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Analyze individual clusters.

    Args:
        embeddings: Comment embeddings
        labels: Cluster labels
        comments: Optional comment texts

    Returns:
        List of cluster analysis dictionaries
    """
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    clusters = []
    for cluster_id in range(n_clusters):
        mask = labels == cluster_id
        cluster_embeddings = embeddings[mask]
        cluster_indices = np.where(mask)[0]

        # Calculate cluster metrics
        centroid = cluster_embeddings.mean(axis=0)

        # Distances from centroid
        distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
        avg_distance = float(distances.mean())
        std_distance = float(distances.std())

        # Cluster density (inverse of average distance)
        density = 1.0 / (avg_distance + 1e-10)

        cluster_info = {
            "cluster_id": int(cluster_id),
            "size": int(mask.sum()),
            "centroid": centroid,
            "avg_distance_to_centroid": avg_distance,
            "std_distance_to_centroid": std_distance,
            "density": float(density),
            "indices": cluster_indices.tolist(),
        }

        # Add comments if provided
        if comments:
            cluster_comments = [comments[i] for i in cluster_indices]
            cluster_info["comments"] = cluster_comments

            # Find most representative comment (closest to centroid)
            closest_idx = np.argmin(distances)
            cluster_info["representative_comment"] = cluster_comments[closest_idx]
            cluster_info["representative_index"] = int(cluster_indices[closest_idx])

        clusters.append(cluster_info)

    # Sort by size (largest first)
    clusters.sort(key=lambda x: x["size"], reverse=True)

    return clusters


def calculate_clustering_score(
    embeddings: np.ndarray,
    min_cluster_size: int = 5,
) -> Dict[str, float]:
    """Calculate clustering-based coordination score.

    Args:
        embeddings: Comment embeddings
        min_cluster_size: Minimum cluster size

    Returns:
        Dictionary of clustering metrics
    """
    clustering_result = perform_clustering(embeddings, min_cluster_size)

    n_clusters = clustering_result["n_clusters"]
    noise_ratio = clustering_result["noise_ratio"]
    cluster_sizes = clustering_result["cluster_sizes"]

    if n_clusters == 0:
        return {
            "clustering_score": 0.0,
            "n_clusters": 0,
            "largest_cluster_ratio": 0.0,
            "noise_ratio": noise_ratio,
        }

    # Largest cluster ratio
    largest_cluster_size = max(cluster_sizes)
    largest_cluster_ratio = largest_cluster_size / len(embeddings)

    # Clustering score (0-100)
    # Higher score = more suspicious clustering
    clustering_score = (
        0.5 * (largest_cluster_ratio * 100) +
        0.3 * ((1.0 - noise_ratio) * 100) +
        0.2 * min(n_clusters * 10, 100)  # More clusters = more coordination
    )

    return {
        "clustering_score": float(clustering_score),
        "n_clusters": n_clusters,
        "largest_cluster_ratio": largest_cluster_ratio,
        "noise_ratio": noise_ratio,
        "cluster_sizes": cluster_sizes,
    }


def get_cluster_visualization_data(
    embeddings: np.ndarray,
    labels: np.ndarray,
) -> Dict[str, Any]:
    """Prepare data for cluster visualization.

    Args:
        embeddings: Comment embeddings
        labels: Cluster labels

    Returns:
        Visualization data dictionary
    """
    # Reduce to 2D for visualization
    reduced = reduce_dimensions(embeddings, n_components=2)

    return {
        "x": reduced[:, 0].tolist(),
        "y": reduced[:, 1].tolist(),
        "labels": labels.tolist(),
        "n_clusters": int(len(set(labels)) - (1 if -1 in labels else 0)),
    }
