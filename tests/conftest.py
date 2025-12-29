"""Pytest configuration and fixtures."""

import pytest
import numpy as np


@pytest.fixture
def sample_embeddings():
    """Sample embeddings for testing."""
    return np.random.randn(20, 10)


@pytest.fixture
def sample_timestamps():
    """Sample timestamps for testing."""
    return [1000000 + i * 100 for i in range(20)]


@pytest.fixture
def sample_comments():
    """Sample comment texts for testing."""
    return [
        "This is a test comment",
        "Another test comment here",
        "Yet another comment for testing",
        "Different comment with different words",
        "Unique comment text here",
    ]
