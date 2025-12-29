"""Tests for similarity analysis."""

import pytest
import numpy as np

from analysis.similarity import (
    compute_similarity_matrix,
    find_high_similarity_pairs,
    calculate_semantic_score,
)


def test_compute_similarity_matrix():
    """Test similarity matrix computation."""
    # Create simple embeddings
    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],  # Identical to first
        [0.0, 1.0, 0.0],  # Different
    ])

    sim_matrix = compute_similarity_matrix(embeddings)

    assert sim_matrix.shape == (3, 3)
    assert sim_matrix[0, 1] > 0.99  # Nearly identical
    assert sim_matrix[0, 2] < 0.1   # Very different


def test_find_high_similarity_pairs():
    """Test finding high similarity pairs."""
    sim_matrix = np.array([
        [1.0, 0.95, 0.3],
        [0.95, 1.0, 0.4],
        [0.3, 0.4, 1.0],
    ])

    pairs = find_high_similarity_pairs(sim_matrix, threshold=0.9)

    assert len(pairs) == 1
    assert pairs[0][2] >= 0.9  # Similarity score


def test_calculate_semantic_score():
    """Test semantic score calculation."""
    # Create embeddings with high similarity
    embeddings = np.array([
        [1.0, 0.0],
        [0.99, 0.1],
        [0.98, 0.2],
        [0.0, 1.0],
    ])

    metrics = calculate_semantic_score(embeddings)

    assert 0 <= metrics["semantic_score"] <= 100
    assert 0 <= metrics["avg_similarity"] <= 1
    assert 0 <= metrics["high_similarity_ratio"] <= 1


def test_calculate_semantic_score_insufficient_data():
    """Test semantic score with insufficient data."""
    embeddings = np.array([[1.0, 0.0]])

    metrics = calculate_semantic_score(embeddings)

    assert metrics["semantic_score"] == 0.0
