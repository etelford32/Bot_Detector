"""Generate human-readable explanations for consensus scores."""

from typing import Dict, Any, List


def generate_rationale(
    score: float,
    metrics: Dict[str, Any],
) -> str:
    """Generate human-readable rationale for consensus score.

    Args:
        score: Consensus score (0-100)
        metrics: Detailed metrics from calculate_consensus_score

    Returns:
        Human-readable explanation
    """
    interpretation = metrics["interpretation"]
    confidence = metrics["confidence"]

    # Build rationale sections
    sections = []

    # Header
    sections.append(f"Score: {score:.1f}/100 ({interpretation['level']})")
    sections.append(f"Confidence: {confidence}")
    sections.append("")

    # Primary signals
    primary_signals = identify_primary_signals(metrics)
    if primary_signals:
        sections.append("Primary Signals:")
        for signal in primary_signals:
            sections.append(f"• {signal}")
        sections.append("")

    # Evidence
    evidence = collect_evidence(metrics)
    if evidence:
        sections.append("Evidence:")
        for item in evidence:
            sections.append(f"• {item}")
        sections.append("")

    # Interpretation
    sections.append(f"Interpretation: {interpretation['description']}")
    sections.append("")

    # Recommendation
    sections.append(f"Recommendation: {interpretation['recommendation']}")
    sections.append("")

    # Caveats
    caveats = generate_caveats(score, metrics)
    if caveats:
        sections.append("Caveats:")
        for caveat in caveats:
            sections.append(f"• {caveat}")

    return "\n".join(sections)


def identify_primary_signals(metrics: Dict[str, Any]) -> List[str]:
    """Identify the primary signals driving the score.

    Args:
        metrics: Detailed metrics

    Returns:
        List of signal descriptions
    """
    signals = []

    semantic = metrics.get("semantic", {})
    temporal = metrics.get("temporal", {})
    network = metrics.get("network", {})
    clustering = metrics.get("clustering", {})
    templates = metrics.get("templates", [])

    # Semantic signals
    if semantic.get("semantic_score", 0) > 60:
        high_sim_ratio = semantic.get("high_similarity_ratio", 0)
        signals.append(
            f"High semantic similarity: {high_sim_ratio:.1%} of comment pairs "
            f"are highly similar"
        )

    # Template usage
    if templates:
        top_template = templates[0]
        count = top_template["count"]
        total = metrics["n_analyzed"]
        ratio = count / total if total > 0 else 0
        signals.append(
            f"Template usage detected: {count} comments ({ratio:.1%} of thread) "
            f"match similar pattern"
        )

    # Temporal signals
    if temporal.get("temporal_score", 0) > 60:
        burst_coef = temporal.get("burst_coefficient", 0)
        n_bursts = temporal.get("n_bursts", 0)

        if burst_coef > 3:
            signals.append(
                f"Temporal burst detected: posting rate {burst_coef:.1f}x above baseline"
            )

        if n_bursts > 1:
            signals.append(f"Multiple coordinated bursts: {n_bursts} bursts detected")

    # Network signals
    if network.get("network_score", 0) > 60:
        isolation_ratio = network.get("isolation_ratio", 0)
        clustering_coef = network.get("clustering_coefficient", 0)

        if isolation_ratio > 0.3:
            largest = network.get("largest_isolated_group", 0)
            signals.append(
                f"Isolated user group: {largest} users form isolated cluster"
            )

        if clustering_coef > 0.5:
            signals.append(
                f"High user clustering: {clustering_coef:.2f} clustering coefficient"
            )

    # Clustering signals
    if clustering.get("clustering_score", 0) > 60:
        n_clusters = clustering.get("n_clusters", 0)
        largest_ratio = clustering.get("largest_cluster_ratio", 0)

        if largest_ratio > 0.2:
            signals.append(
                f"Large semantic cluster: {largest_ratio:.1%} of comments in single cluster"
            )

    return signals


def collect_evidence(metrics: Dict[str, Any]) -> List[str]:
    """Collect specific evidence examples.

    Args:
        metrics: Detailed metrics

    Returns:
        List of evidence items
    """
    evidence = []

    templates = metrics.get("templates", [])
    temporal = metrics.get("temporal", {})
    clustering = metrics.get("clustering", {})

    # Template examples
    if templates:
        top_template = templates[0]
        representative = top_template["representative"]
        count = top_template["count"]

        # Truncate if too long
        if len(representative) > 100:
            representative = representative[:97] + "..."

        evidence.append(
            f"Template example: \"{representative}\" "
            f"(appears {count} times with variations)"
        )

    # Temporal burst examples
    if temporal.get("temporal_score", 0) > 50:
        max_coordinated = temporal.get("max_coordinated_group", 0)
        if max_coordinated >= 3:
            evidence.append(
                f"Coordinated timing: {max_coordinated} comments posted "
                f"within 60 seconds"
            )

    # Clustering examples
    if clustering.get("n_clusters", 0) > 0:
        cluster_sizes = clustering.get("cluster_sizes", [])
        if cluster_sizes:
            evidence.append(
                f"Semantic clusters: {len(cluster_sizes)} distinct clusters "
                f"(largest: {max(cluster_sizes)} comments)"
            )

    return evidence


def generate_caveats(score: float, metrics: Dict[str, Any]) -> List[str]:
    """Generate caveats and alternative explanations.

    Args:
        score: Consensus score
        metrics: Detailed metrics

    Returns:
        List of caveats
    """
    caveats = []

    # Always include base caveat
    caveats.append("This is a probabilistic indicator, not definitive proof")

    # Low sample size
    n_comments = metrics.get("n_analyzed", 0)
    if n_comments < 30:
        caveats.append(
            f"Small sample size ({n_comments} comments) may reduce accuracy"
        )

    # High score caveats
    if score >= 50:
        temporal = metrics.get("temporal", {})

        # Breaking news could cause natural coordination
        if temporal.get("burst_coefficient", 0) > 3:
            caveats.append(
                "High posting rate could be organic response to breaking news"
            )

        # Grassroots movements
        caveats.append(
            "Genuine grassroots movements may exhibit similar patterns"
        )

    # Medium score caveats
    if 25 <= score < 50:
        caveats.append(
            "Ambiguous signals - could be organic or coordinated"
        )

    # Context-dependent
    caveats.append(
        "Consider thread topic and context when interpreting results"
    )

    return caveats


def generate_short_summary(score: float, metrics: Dict[str, Any]) -> str:
    """Generate a short one-line summary.

    Args:
        score: Consensus score
        metrics: Detailed metrics

    Returns:
        One-line summary
    """
    interpretation = metrics["interpretation"]
    confidence = metrics["confidence"]

    primary_signals = identify_primary_signals(metrics)
    top_signal = primary_signals[0] if primary_signals else "No strong signals"

    return (
        f"{interpretation['level']} (Score: {score:.1f}, "
        f"Confidence: {confidence}) - {top_signal}"
    )


def format_detailed_report(
    score: float,
    metrics: Dict[str, Any],
    include_raw_metrics: bool = False,
) -> str:
    """Format a detailed analysis report.

    Args:
        score: Consensus score
        metrics: Detailed metrics
        include_raw_metrics: Include raw metric values

    Returns:
        Formatted detailed report
    """
    sections = []

    # Header
    sections.append("=" * 80)
    sections.append("SYNTHETIC CONSENSUS ANALYSIS REPORT")
    sections.append("=" * 80)
    sections.append("")

    # Summary
    sections.append(generate_rationale(score, metrics))
    sections.append("")

    # Component scores
    if include_raw_metrics:
        sections.append("-" * 80)
        sections.append("Component Scores:")
        sections.append("")

        semantic = metrics.get("semantic", {})
        temporal = metrics.get("temporal", {})
        network = metrics.get("network", {})

        sections.append(f"Semantic Score:  {semantic.get('semantic_score', 0):.1f}/100")
        sections.append(f"Temporal Score:  {temporal.get('temporal_score', 0):.1f}/100")
        sections.append(f"Network Score:   {network.get('network_score', 0):.1f}/100")
        sections.append("")

        # Detailed metrics
        sections.append("Detailed Metrics:")
        sections.append(f"  Average Similarity: {semantic.get('avg_similarity', 0):.3f}")
        sections.append(f"  Burst Coefficient: {temporal.get('burst_coefficient', 0):.2f}x")
        sections.append(f"  Timing Entropy: {temporal.get('timing_entropy', 0):.2f}")
        sections.append(f"  Clustering Coefficient: {network.get('clustering_coefficient', 0):.3f}")
        sections.append("")

    # Footer
    sections.append("=" * 80)
    sections.append(f"Analyzed {metrics.get('n_analyzed', 0)} comments")
    sections.append("=" * 80)

    return "\n".join(sections)
