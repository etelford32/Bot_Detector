"""Network graph analysis for user-comment coordination."""

from typing import Dict, List, Any, Set, Tuple
import networkx as nx
from collections import defaultdict, Counter


def build_comment_graph(thread_data: Dict[str, Any]) -> nx.Graph:
    """Build a graph of user-comment interactions.

    Args:
        thread_data: Thread data with comments

    Returns:
        NetworkX graph
    """
    G = nx.Graph()

    comments = thread_data["comments"]

    # Add nodes for users and comments
    for comment in comments:
        comment_id = comment["id"]
        author = comment["author"]

        # Add nodes
        G.add_node(f"user:{author}", node_type="user", name=author)
        G.add_node(f"comment:{comment_id}", node_type="comment", **comment)

        # Add edge: user posts comment
        G.add_edge(f"user:{author}", f"comment:{comment_id}", edge_type="posts")

    # Add reply edges
    for comment in comments:
        comment_id = comment["id"]
        parent_id = comment.get("parent_id", "")

        if parent_id and parent_id.startswith("t1_"):
            # This is a comment reply
            parent_comment_id = parent_id[3:]  # Remove "t1_" prefix

            if G.has_node(f"comment:{parent_comment_id}"):
                G.add_edge(
                    f"comment:{comment_id}",
                    f"comment:{parent_comment_id}",
                    edge_type="replies_to",
                )

    return G


def analyze_user_network(thread_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze user interaction network.

    Args:
        thread_data: Thread data with comments

    Returns:
        Network analysis metrics
    """
    G = build_comment_graph(thread_data)

    # Extract user subgraph
    user_nodes = [n for n, attr in G.nodes(data=True) if attr.get("node_type") == "user"]
    comments = thread_data["comments"]

    # Build user-to-user graph (users connected if they interact)
    user_graph = nx.Graph()
    user_graph.add_nodes_from(user_nodes)

    # Connect users who reply to each other
    for comment in comments:
        author = comment["author"]
        parent_id = comment.get("parent_id", "")

        if parent_id.startswith("t1_"):
            parent_comment_id = parent_id[3:]

            # Find parent author
            parent_comment = next(
                (c for c in comments if c["id"] == parent_comment_id),
                None
            )

            if parent_comment:
                parent_author = parent_comment["author"]
                if author != parent_author:
                    user_graph.add_edge(f"user:{author}", f"user:{parent_author}")

    # Calculate metrics
    n_users = len(user_nodes)

    if n_users == 0:
        return {
            "n_users": 0,
            "n_edges": 0,
            "density": 0.0,
            "avg_degree": 0.0,
            "clustering_coefficient": 0.0,
            "n_components": 0,
            "largest_component_size": 0,
        }

    n_edges = user_graph.number_of_edges()
    density = nx.density(user_graph)

    degrees = [d for _, d in user_graph.degree()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0.0

    # Clustering coefficient
    try:
        clustering_coefficient = nx.average_clustering(user_graph)
    except:
        clustering_coefficient = 0.0

    # Connected components
    components = list(nx.connected_components(user_graph))
    n_components = len(components)
    largest_component_size = max([len(c) for c in components], default=0)

    return {
        "n_users": n_users,
        "n_edges": n_edges,
        "density": float(density),
        "avg_degree": float(avg_degree),
        "clustering_coefficient": float(clustering_coefficient),
        "n_components": n_components,
        "largest_component_size": largest_component_size,
        "components": [list(c) for c in components],
    }


def detect_coordination_patterns(thread_data: Dict[str, Any]) -> Dict[str, Any]:
    """Detect coordination patterns in user behavior.

    Args:
        thread_data: Thread data with comments

    Returns:
        Coordination pattern metrics
    """
    comments = thread_data["comments"]

    # Track user posting patterns
    user_comments = defaultdict(list)
    for comment in comments:
        author = comment["author"]
        user_comments[author].append(comment)

    # Detect patterns
    patterns = {
        "single_issue_users": 0,
        "burst_posters": 0,
        "non_interactive_users": 0,
        "coordinated_groups": [],
    }

    # Single-issue users (only post in this thread)
    # Note: Would need user history for full detection
    patterns["single_issue_users"] = len(user_comments)

    # Burst posters (multiple comments in short time)
    for author, user_comment_list in user_comments.items():
        if len(user_comment_list) >= 3:
            timestamps = [c["created_utc"] for c in user_comment_list]
            time_span = max(timestamps) - min(timestamps)

            # Posted 3+ times in < 5 minutes
            if time_span < 300:
                patterns["burst_posters"] += 1

    # Non-interactive users (don't reply to others)
    for author, user_comment_list in user_comments.items():
        has_reply = any(
            c.get("parent_id", "").startswith("t1_")
            for c in user_comment_list
        )
        if not has_reply and len(user_comment_list) > 1:
            patterns["non_interactive_users"] += 1

    return patterns


def find_isolated_subgraphs(thread_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find isolated subgraphs (potential coordination clusters).

    Args:
        thread_data: Thread data with comments

    Returns:
        List of isolated subgraph info
    """
    network_analysis = analyze_user_network(thread_data)
    components = network_analysis["components"]

    # Filter for components with multiple users
    isolated_groups = []

    for component in components:
        if len(component) >= 3:  # At least 3 users
            # Extract user names
            users = [node.replace("user:", "") for node in component]

            isolated_groups.append({
                "users": users,
                "size": len(users),
            })

    # Sort by size
    isolated_groups.sort(key=lambda x: x["size"], reverse=True)

    return isolated_groups


def calculate_network_score(thread_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate network-based coordination score.

    Args:
        thread_data: Thread data with comments

    Returns:
        Dictionary of network metrics
    """
    network_metrics = analyze_user_network(thread_data)
    coordination_patterns = detect_coordination_patterns(thread_data)
    isolated_groups = find_isolated_subgraphs(thread_data)

    n_users = network_metrics["n_users"]
    n_comments = len(thread_data["comments"])

    if n_users == 0:
        return {
            "network_score": 0.0,
            "clustering_coefficient": 0.0,
            "isolation_ratio": 0.0,
        }

    # Clustering coefficient (higher = more coordinated)
    clustering_coefficient = network_metrics["clustering_coefficient"]

    # Isolation ratio (large isolated group vs total)
    largest_isolated = max([g["size"] for g in isolated_groups], default=0)
    isolation_ratio = largest_isolated / n_users if n_users > 0 else 0.0

    # Comments per user ratio (higher = fewer unique users)
    comments_per_user = n_comments / n_users if n_users > 0 else 0.0
    repeat_poster_score = min(comments_per_user / 5.0, 1.0)  # Normalize

    # Calculate network score (0-100)
    network_score = (
        0.4 * (clustering_coefficient * 100) +
        0.4 * (isolation_ratio * 100) +
        0.2 * (repeat_poster_score * 100)
    )

    return {
        "network_score": float(network_score),
        "clustering_coefficient": clustering_coefficient,
        "isolation_ratio": isolation_ratio,
        "largest_isolated_group": largest_isolated,
        "comments_per_user": float(comments_per_user),
    }


def get_user_statistics(thread_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get statistics about users in the thread.

    Args:
        thread_data: Thread data with comments

    Returns:
        User statistics dictionary
    """
    comments = thread_data["comments"]

    # Count comments per user
    user_comment_counts = Counter(c["author"] for c in comments)

    # Calculate statistics
    comment_counts = list(user_comment_counts.values())

    return {
        "n_unique_users": len(user_comment_counts),
        "total_comments": len(comments),
        "avg_comments_per_user": sum(comment_counts) / len(comment_counts) if comment_counts else 0,
        "max_comments_per_user": max(comment_counts, default=0),
        "top_posters": user_comment_counts.most_common(10),
    }
