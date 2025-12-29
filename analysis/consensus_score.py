"""Calculate Synthetic Consensus Score."""

from typing import Dict, Any, List
import numpy as np

from embeddings.embedder import TextEmbedder
from embeddings.cache import CachedEmbedder, EmbeddingCache
from analysis.similarity import calculate_semantic_score, detect_template_usage
from analysis.clustering import calculate_clustering_score
from analysis.temporal import calculate_temporal_score
from analysis.graph import calculate_network_score


def calculate_consensus_score(
    thread_data: Dict[str, Any],
    use_cache: bool = True,
) -> tuple[float, Dict[str, Any]]:
    """Calculate Synthetic Consensus Score for a thread.

    Args:
        thread_data: Thread data from fetch_thread
        use_cache: Use embedding cache

    Returns:
        Tuple of (score, detailed_metrics)
    """
    comments = thread_data["comments"]

    if len(comments) < 5:
        return 0.0, {
            "error": "Insufficient comments for analysis (minimum 5 required)",
            "n_comments": len(comments),
        }

    # Extract comment texts (normalized)
    comment_texts = [c["text_normalized"] for c in comments if c["text_normalized"]]

    if len(comment_texts) < 5:
        return 0.0, {
            "error": "Insufficient valid comments after normalization",
            "n_comments": len(comment_texts),
        }

    # Generate embeddings
    embedder = TextEmbedder()

    if use_cache:
        cache = EmbeddingCache(cache_type="memory")
        cached_embedder = CachedEmbedder(embedder, cache)
        embeddings = cached_embedder.embed(comment_texts)
    else:
        embeddings = embedder.embed(comment_texts)

    # Extract timestamps
    timestamps = [c["created_utc"] for c in comments]

    # Calculate component scores
    semantic_metrics = calculate_semantic_score(embeddings)
    clustering_metrics = calculate_clustering_score(embeddings)
    temporal_metrics = calculate_temporal_score(timestamps)
    network_metrics = calculate_network_score(thread_data)

    # Detect templates
    templates = detect_template_usage(comment_texts, embeddings)

    # Calculate behavioral score (simplified for MVP)
    behavioral_score = calculate_behavioral_score(thread_data)

    # Calculate final score (weighted average)
    WEIGHTS = {
        "semantic": 0.35,
        "temporal": 0.25,
        "network": 0.25,
        "behavioral": 0.15,
    }

    final_score = (
        WEIGHTS["semantic"] * semantic_metrics["semantic_score"] +
        WEIGHTS["temporal"] * temporal_metrics["temporal_score"] +
        WEIGHTS["network"] * network_metrics["network_score"] +
        WEIGHTS["behavioral"] * behavioral_score
    )

    # Calculate confidence
    confidence = calculate_confidence(
        semantic_metrics,
        temporal_metrics,
        network_metrics,
        len(comments),
    )

    # Compile detailed metrics
    detailed_metrics = {
        "final_score": float(final_score),
        "confidence": confidence,
        "n_comments": len(comments),
        "n_analyzed": len(comment_texts),
        "weights": WEIGHTS,
        "semantic": semantic_metrics,
        "clustering": clustering_metrics,
        "temporal": temporal_metrics,
        "network": network_metrics,
        "behavioral": {
            "behavioral_score": behavioral_score,
        },
        "templates": templates[:5] if templates else [],  # Top 5 templates
        "interpretation": interpret_score(final_score),
    }

    return float(final_score), detailed_metrics


def calculate_behavioral_score(thread_data: Dict[str, Any]) -> float:
    """Calculate behavioral anomaly score (simplified for MVP).

    Args:
        thread_data: Thread data with comments

    Returns:
        Behavioral score (0-100)
    """
    comments = thread_data["comments"]

    if not comments:
        return 0.0

    # Analyze user accounts
    authors = [c["author"] for c in comments]
    unique_authors = set(authors)

    # Deleted/removed accounts ratio
    deleted_ratio = sum(1 for a in authors if a == "[deleted]") / len(authors)

    # Submitter participation (OP dominance)
    submitter_comments = sum(1 for c in comments if c.get("is_submitter", False))
    submitter_ratio = submitter_comments / len(comments) if comments else 0.0

    # Comments per user
    from collections import Counter
    author_counts = Counter(authors)
    avg_comments_per_user = len(comments) / len(unique_authors) if unique_authors else 0.0
    repeat_poster_score = min(avg_comments_per_user / 5.0, 1.0)

    # Calculate behavioral score
    behavioral_score = (
        0.3 * (deleted_ratio * 100) +
        0.3 * (repeat_poster_score * 100) +
        0.2 * (submitter_ratio * 100) +
        0.2 * 0  # Reserved for account age/karma (requires API enhancement)
    )

    return float(behavioral_score)


def calculate_confidence(
    semantic_metrics: Dict[str, float],
    temporal_metrics: Dict[str, float],
    network_metrics: Dict[str, float],
    n_comments: int,
) -> str:
    """Calculate confidence level for the analysis.

    Args:
        semantic_metrics: Semantic analysis metrics
        temporal_metrics: Temporal analysis metrics
        network_metrics: Network analysis metrics
        n_comments: Number of comments analyzed

    Returns:
        Confidence level (Low, Medium, High, Very High)
    """
    # Signal strength (how extreme are the scores?)
    scores = [
        semantic_metrics["semantic_score"],
        temporal_metrics["temporal_score"],
        network_metrics["network_score"],
    ]

    avg_score = np.mean(scores)
    score_std = np.std(scores)

    # Strong signal = high average and low variance
    signal_strength = avg_score * (1 - score_std / 50)  # Normalize std

    # Sample size adequacy
    if n_comments < 20:
        sample_adequacy = 0.5
    elif n_comments < 50:
        sample_adequacy = 0.75
    else:
        sample_adequacy = 1.0

    # Signal agreement (do all metrics agree?)
    # All high or all low = high agreement
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score

    if score_range < 20:
        signal_agreement = 1.0
    elif score_range < 40:
        signal_agreement = 0.75
    else:
        signal_agreement = 0.5

    # Overall confidence
    confidence_score = (
        0.4 * (signal_strength / 100) +
        0.3 * sample_adequacy +
        0.3 * signal_agreement
    )

    # Map to levels
    if confidence_score >= 0.8:
        return "Very High"
    elif confidence_score >= 0.6:
        return "High"
    elif confidence_score >= 0.4:
        return "Medium"
    else:
        return "Low"


def interpret_score(score: float) -> Dict[str, str]:
    """Interpret the consensus score.

    Args:
        score: Consensus score (0-100)

    Returns:
        Interpretation dictionary
    """
    if score < 25:
        return {
            "level": "Likely Organic",
            "description": "Consensus appears genuine and grassroots",
            "recommendation": "No concerns, typical organic discussion",
        }
    elif score < 50:
        return {
            "level": "Possible Coordination",
            "description": "Some signals of coordination, but could be organic",
            "recommendation": "Investigate further, monitor for escalation",
        }
    elif score < 75:
        return {
            "level": "Likely Coordinated",
            "description": "Multiple strong signals of artificial coordination",
            "recommendation": "Likely manipulation, recommend further investigation",
        }
    else:
        return {
            "level": "Highly Coordinated",
            "description": "Overwhelming evidence of synthetic consensus",
            "recommendation": "Almost certainly manipulation, flag for review",
        }


def analyze_thread_batch(
    thread_urls: List[str],
    use_cache: bool = True,
) -> List[tuple[str, float, Dict[str, Any]]]:
    """Analyze multiple threads.

    Args:
        thread_urls: List of Reddit thread URLs
        use_cache: Use embedding cache

    Returns:
        List of (url, score, metrics) tuples
    """
    from ingestion.thread_fetcher import fetch_thread

    results = []

    for url in thread_urls:
        try:
            thread_data = fetch_thread(url)
            score, metrics = calculate_consensus_score(thread_data, use_cache)
            results.append((url, score, metrics))
        except Exception as e:
            results.append((url, 0.0, {"error": str(e)}))

    return results
