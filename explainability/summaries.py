"""Generate narrative summaries of detected patterns."""

from typing import Dict, Any, List


def generate_narrative_summary(
    thread_data: Dict[str, Any],
    score: float,
    metrics: Dict[str, Any],
) -> str:
    """Generate a narrative summary of the analysis.

    Args:
        thread_data: Thread data
        score: Consensus score
        metrics: Detailed metrics

    Returns:
        Narrative summary
    """
    sections = []

    # Thread overview
    overview = generate_thread_overview(thread_data)
    sections.append(overview)
    sections.append("")

    # Pattern description
    patterns = describe_patterns(metrics)
    sections.append(patterns)
    sections.append("")

    # Assessment
    assessment = generate_assessment(score, metrics)
    sections.append(assessment)

    return "\n".join(sections)


def generate_thread_overview(thread_data: Dict[str, Any]) -> str:
    """Generate thread overview.

    Args:
        thread_data: Thread data

    Returns:
        Overview text
    """
    title = thread_data.get("title", "Unknown")
    subreddit = thread_data.get("subreddit", "Unknown")
    n_comments = thread_data.get("comments_analyzed", 0)
    score = thread_data.get("score", 0)

    return (
        f"Thread: \"{title}\"\n"
        f"Subreddit: r/{subreddit}\n"
        f"Comments analyzed: {n_comments}\n"
        f"Thread score: {score}"
    )


def describe_patterns(metrics: Dict[str, Any]) -> str:
    """Describe detected patterns in narrative form.

    Args:
        metrics: Detailed metrics

    Returns:
        Pattern description
    """
    patterns = []

    semantic = metrics.get("semantic", {})
    temporal = metrics.get("temporal", {})
    network = metrics.get("network", {})
    templates = metrics.get("templates", [])

    # Semantic patterns
    avg_sim = semantic.get("avg_similarity", 0)
    if avg_sim > 0.5:
        patterns.append(
            f"The comments show elevated semantic similarity "
            f"(average {avg_sim:.2f}), suggesting coordinated messaging."
        )
    else:
        patterns.append(
            "The comments show diverse semantic content, "
            "consistent with organic discussion."
        )

    # Template usage
    if templates:
        top_template = templates[0]
        count = top_template["count"]
        patterns.append(
            f"Template usage detected: {count} comments follow a similar pattern, "
            f"which may indicate scripted or coordinated posting."
        )

    # Temporal patterns
    burst_coef = temporal.get("burst_coefficient", 0)
    if burst_coef > 3:
        patterns.append(
            f"A significant posting burst was detected, with peak activity "
            f"{burst_coef:.1f}x higher than baseline. This could indicate "
            f"coordinated action or organic response to breaking news."
        )
    else:
        patterns.append(
            "Comment timing appears organic, with no significant bursts detected."
        )

    # Network patterns
    isolation_ratio = network.get("isolation_ratio", 0)
    if isolation_ratio > 0.3:
        largest = network.get("largest_isolated_group", 0)
        patterns.append(
            f"A cluster of {largest} users appears isolated from the broader "
            f"discussion, potentially indicating a coordinated group."
        )

    if not patterns:
        patterns.append("No significant coordination patterns detected.")

    return "Patterns Detected:\n" + "\n".join(f"• {p}" for p in patterns)


def generate_assessment(score: float, metrics: Dict[str, Any]) -> str:
    """Generate overall assessment.

    Args:
        score: Consensus score
        metrics: Detailed metrics

    Returns:
        Assessment text
    """
    interpretation = metrics["interpretation"]
    confidence = metrics["confidence"]

    assessment = f"Assessment:\n"
    assessment += f"The analysis indicates {interpretation['level'].lower()} "
    assessment += f"with {confidence.lower()} confidence (score: {score:.1f}/100).\n\n"
    assessment += f"{interpretation['description']}\n\n"
    assessment += f"Recommendation: {interpretation['recommendation']}"

    return assessment


def generate_json_summary(
    thread_data: Dict[str, Any],
    score: float,
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate JSON-formatted summary.

    Args:
        thread_data: Thread data
        score: Consensus score
        metrics: Detailed metrics

    Returns:
        JSON-serializable summary dictionary
    """
    return {
        "thread": {
            "id": thread_data.get("thread_id"),
            "title": thread_data.get("title"),
            "subreddit": thread_data.get("subreddit"),
            "url": thread_data.get("url"),
            "score": thread_data.get("score"),
            "num_comments": thread_data.get("num_comments"),
        },
        "analysis": {
            "score": round(score, 2),
            "interpretation": metrics["interpretation"]["level"],
            "confidence": metrics["confidence"],
            "n_analyzed": metrics["n_analyzed"],
        },
        "signals": {
            "semantic_score": round(metrics.get("semantic", {}).get("semantic_score", 0), 2),
            "temporal_score": round(metrics.get("temporal", {}).get("temporal_score", 0), 2),
            "network_score": round(metrics.get("network", {}).get("network_score", 0), 2),
        },
        "key_findings": extract_key_findings(metrics),
    }


def extract_key_findings(metrics: Dict[str, Any]) -> List[str]:
    """Extract key findings from metrics.

    Args:
        metrics: Detailed metrics

    Returns:
        List of key finding strings
    """
    findings = []

    semantic = metrics.get("semantic", {})
    temporal = metrics.get("temporal", {})
    network = metrics.get("network", {})
    templates = metrics.get("templates", [])

    # High similarity
    if semantic.get("semantic_score", 0) > 60:
        findings.append("High semantic similarity detected")

    # Template usage
    if templates:
        findings.append(f"Template usage: {templates[0]['count']} matching comments")

    # Temporal bursts
    if temporal.get("burst_coefficient", 0) > 3:
        findings.append("Significant posting burst detected")

    # Network clustering
    if network.get("isolation_ratio", 0) > 0.3:
        findings.append("Isolated user cluster detected")

    if not findings:
        findings.append("No significant coordination signals")

    return findings


def format_markdown_report(
    thread_data: Dict[str, Any],
    score: float,
    metrics: Dict[str, Any],
) -> str:
    """Format analysis as markdown report.

    Args:
        thread_data: Thread data
        score: Consensus score
        metrics: Detailed metrics

    Returns:
        Markdown-formatted report
    """
    md = []

    # Header
    md.append("# Bot Detection Analysis Report")
    md.append("")

    # Thread info
    md.append("## Thread Information")
    md.append("")
    md.append(f"- **Title**: {thread_data.get('title')}")
    md.append(f"- **Subreddit**: r/{thread_data.get('subreddit')}")
    md.append(f"- **URL**: {thread_data.get('url')}")
    md.append(f"- **Comments**: {thread_data.get('num_comments')}")
    md.append(f"- **Score**: {thread_data.get('score')}")
    md.append("")

    # Results
    interpretation = metrics["interpretation"]
    md.append("## Analysis Results")
    md.append("")
    md.append(f"**Score**: {score:.1f}/100")
    md.append("")
    md.append(f"**Interpretation**: {interpretation['level']}")
    md.append("")
    md.append(f"**Confidence**: {metrics['confidence']}")
    md.append("")

    # Component scores
    md.append("## Component Scores")
    md.append("")
    md.append("| Component | Score |")
    md.append("|-----------|-------|")

    semantic = metrics.get("semantic", {})
    temporal = metrics.get("temporal", {})
    network = metrics.get("network", {})

    md.append(f"| Semantic | {semantic.get('semantic_score', 0):.1f}/100 |")
    md.append(f"| Temporal | {temporal.get('temporal_score', 0):.1f}/100 |")
    md.append(f"| Network | {network.get('network_score', 0):.1f}/100 |")
    md.append("")

    # Key findings
    findings = extract_key_findings(metrics)
    md.append("## Key Findings")
    md.append("")
    for finding in findings:
        md.append(f"- {finding}")
    md.append("")

    # Recommendation
    md.append("## Recommendation")
    md.append("")
    md.append(interpretation['recommendation'])
    md.append("")

    return "\n".join(md)
