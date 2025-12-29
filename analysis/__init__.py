"""Analysis module for bot detection."""

from analysis.similarity import (
    compute_similarity_matrix,
    find_high_similarity_pairs,
    detect_template_usage,
    calculate_semantic_score,
)
from analysis.clustering import (
    perform_clustering,
    reduce_dimensions,
    calculate_clustering_score,
)
from analysis.temporal import (
    calculate_posting_rate,
    detect_bursts,
    calculate_temporal_score,
)
from analysis.graph import (
    build_comment_graph,
    analyze_user_network,
    calculate_network_score,
)
from analysis.consensus_score import (
    calculate_consensus_score,
    analyze_thread_batch,
)

__all__ = [
    "compute_similarity_matrix",
    "find_high_similarity_pairs",
    "detect_template_usage",
    "calculate_semantic_score",
    "perform_clustering",
    "reduce_dimensions",
    "calculate_clustering_score",
    "calculate_posting_rate",
    "detect_bursts",
    "calculate_temporal_score",
    "build_comment_graph",
    "analyze_user_network",
    "calculate_network_score",
    "calculate_consensus_score",
    "analyze_thread_batch",
]
