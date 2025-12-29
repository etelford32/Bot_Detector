"""Tests for clustering analysis."""

import pytest
import numpy as np

from analysis.clustering import (
    perform_clustering,
    calculate_clustering_score,
    reduce_dimensions,
)


def test_perform_clustering():
    """Test HDBSCAN clustering."""
    # Create clustered data
    cluster1 = np.random.randn(10, 3) + np.array([0, 0, 0])
    cluster2 = np.random.randn(10, 3) + np.array([5, 5, 5])
    embeddings = np.vstack([cluster1, cluster2])

    result = perform_clustering(embeddings, min_cluster_size=5)

    assert "labels" in result
    assert "n_clusters" in result
    assert len(result["labels"]) == len(embeddings)


def test_perform_clustering_insufficient_data():
    """Test clustering with insufficient data."""
    embeddings = np.random.randn(3, 3)

    result = perform_clustering(embeddings, min_cluster_size=5)

    assert result["n_clusters"] == 0
    assert result["noise_ratio"] == 1.0


def test_reduce_dimensions():
    """Test UMAP dimensionality reduction."""
    embeddings = np.random.randn(20, 10)

    reduced = reduce_dimensions(embeddings, n_components=2)

    assert reduced.shape == (20, 2)


def test_calculate_clustering_score():
    """Test clustering score calculation."""
    # Create well-separated clusters
    cluster1 = np.random.randn(15, 3) + np.array([0, 0, 0])
    cluster2 = np.random.randn(10, 3) + np.array([10, 10, 10])
    embeddings = np.vstack([cluster1, cluster2])

    metrics = calculate_clustering_score(embeddings, min_cluster_size=5)

    assert 0 <= metrics["clustering_score"] <= 100
    assert metrics["n_clusters"] >= 0
