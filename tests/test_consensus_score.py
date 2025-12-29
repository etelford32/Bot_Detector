"""Tests for consensus score calculation."""

import pytest

from analysis.consensus_score import (
    calculate_consensus_score,
    calculate_confidence,
    interpret_score,
)


def create_mock_thread_data(n_comments=20):
    """Create mock thread data for testing."""
    return {
        "thread_id": "test123",
        "title": "Test Thread",
        "subreddit": "test",
        "author": "testuser",
        "created_utc": 1000000,
        "score": 100,
        "num_comments": n_comments,
        "url": "https://reddit.com/test",
        "selftext": "Test post",
        "comments": [
            {
                "id": f"comment{i}",
                "author": f"user{i % 5}",
                "text": f"This is test comment number {i}",
                "text_normalized": f"this is test comment number {i}",
                "created_utc": 1000000 + i * 100,
                "score": 10,
                "parent_id": "t3_test123",
                "is_submitter": False,
                "edited": False,
            }
            for i in range(n_comments)
        ],
        "comments_analyzed": n_comments,
    }


def test_calculate_consensus_score():
    """Test consensus score calculation."""
    thread_data = create_mock_thread_data(20)

    score, metrics = calculate_consensus_score(thread_data)

    assert 0 <= score <= 100
    assert "final_score" in metrics
    assert "confidence" in metrics
    assert "semantic" in metrics
    assert "temporal" in metrics
    assert "network" in metrics


def test_calculate_consensus_score_insufficient_comments():
    """Test with insufficient comments."""
    thread_data = create_mock_thread_data(3)

    score, metrics = calculate_consensus_score(thread_data)

    assert score == 0.0
    assert "error" in metrics


def test_calculate_confidence():
    """Test confidence calculation."""
    metrics = {
        "semantic_score": 50.0,
        "temporal_score": 60.0,
        "network_score": 55.0,
    }

    confidence = calculate_confidence(
        {"semantic_score": 50.0},
        {"temporal_score": 60.0},
        {"network_score": 55.0},
        50,
    )

    assert confidence in ["Low", "Medium", "High", "Very High"]


def test_interpret_score():
    """Test score interpretation."""
    # Low score
    interp = interpret_score(15.0)
    assert interp["level"] == "Likely Organic"

    # Medium score
    interp = interpret_score(40.0)
    assert interp["level"] == "Possible Coordination"

    # High score
    interp = interpret_score(65.0)
    assert interp["level"] == "Likely Coordinated"

    # Very high score
    interp = interpret_score(85.0)
    assert interp["level"] == "Highly Coordinated"
