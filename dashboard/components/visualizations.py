"""Reusable visualization components."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime


def score_gauge(score, title="Synthetic Consensus Score"):
    """Create a gauge chart for the consensus score."""
    # Determine color based on score
    if score < 25:
        color = "green"
    elif score < 50:
        color = "yellow"
    elif score < 75:
        color = "orange"
    else:
        color = "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': title, 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': '#D4EDDA'},
                {'range': [25, 50], 'color': '#FFF3CD'},
                {'range': [50, 75], 'color': '#FFE5CC'},
                {'range': [75, 100], 'color': '#F8D7DA'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        },
        number={'font': {'size': 48}}
    ))

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=80, b=20),
        font={'color': "darkblue", 'family': "Arial"}
    )

    return fig


def component_scores_bar(metrics):
    """Create bar chart for component scores."""
    semantic = metrics.get('semantic', {}).get('semantic_score', 0)
    temporal = metrics.get('temporal', {}).get('temporal_score', 0)
    network = metrics.get('network', {}).get('network_score', 0)
    behavioral = metrics.get('behavioral', {}).get('behavioral_score', 0)

    components = ['Semantic', 'Temporal', 'Network', 'Behavioral']
    scores = [semantic, temporal, network, behavioral]
    colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b']

    fig = go.Figure(data=[
        go.Bar(
            x=components,
            y=scores,
            marker_color=colors,
            text=[f"{s:.1f}" for s in scores],
            textposition='auto',
            textfont=dict(size=16, color='white'),
            hovertemplate='%{x}<br>Score: %{y:.1f}/100<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Component Score Breakdown",
        yaxis_title="Score (0-100)",
        yaxis_range=[0, 100],
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxis(tickfont=dict(size=14))
    fig.update_yaxis(gridcolor='lightgray')

    return fig


def component_scores_radar(metrics):
    """Create radar chart for component scores."""
    semantic = metrics.get('semantic', {}).get('semantic_score', 0)
    temporal = metrics.get('temporal', {}).get('temporal_score', 0)
    network = metrics.get('network', {}).get('network_score', 0)
    behavioral = metrics.get('behavioral', {}).get('behavioral_score', 0)

    categories = ['Semantic', 'Temporal', 'Network', 'Behavioral']
    values = [semantic, temporal, network, behavioral]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Close the polygon
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.5)',
        line=dict(color='rgb(102, 126, 234)', width=3),
        name='Scores'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=12)
            )
        ),
        showlegend=False,
        height=400,
        title="Component Scores (Radar View)"
    )

    return fig


def similarity_heatmap(similarity_matrix, max_display=50):
    """Create heatmap of comment similarity matrix."""
    # Limit size for display
    if len(similarity_matrix) > max_display:
        similarity_matrix = similarity_matrix[:max_display, :max_display]

    fig = go.Figure(data=go.Heatmap(
        z=similarity_matrix,
        colorscale='RdYlGn_r',
        zmin=0,
        zmax=1,
        colorbar=dict(title="Similarity"),
        hovertemplate='Comment %{x} vs %{y}<br>Similarity: %{z:.3f}<extra></extra>'
    ))

    fig.update_layout(
        title=f"Comment Similarity Heatmap (first {min(len(similarity_matrix), max_display)} comments)",
        xaxis_title="Comment Index",
        yaxis_title="Comment Index",
        height=500,
        width=500,
    )

    return fig


def temporal_timeline(timestamps, comments=None):
    """Create timeline of comment posting."""
    # Convert timestamps to datetime
    dates = [datetime.fromtimestamp(ts) for ts in timestamps]

    # Create histogram
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=dates,
        nbinsx=30,
        marker_color='#667eea',
        hovertemplate='Time: %{x}<br>Comments: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title="Comment Posting Timeline",
        xaxis_title="Time",
        yaxis_title="Number of Comments",
        height=350,
        showlegend=False,
        hovermode='x'
    )

    return fig


def temporal_burst_chart(timestamps, bursts=None):
    """Create chart showing posting rate over time with burst detection."""
    from collections import Counter

    # Convert to datetime
    dates = [datetime.fromtimestamp(ts) for ts in timestamps]

    # Count by minute
    minute_counts = Counter([d.replace(second=0, microsecond=0) for d in dates])
    sorted_times = sorted(minute_counts.keys())
    counts = [minute_counts[t] for t in sorted_times]

    fig = go.Figure()

    # Baseline rate
    baseline = np.median(counts) if counts else 0

    fig.add_trace(go.Scatter(
        x=sorted_times,
        y=counts,
        mode='lines+markers',
        name='Posting Rate',
        line=dict(color='#667eea', width=2),
        marker=dict(size=6),
        hovertemplate='Time: %{x}<br>Comments/min: %{y}<extra></extra>'
    ))

    # Baseline line
    fig.add_hline(
        y=baseline,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Baseline ({baseline:.1f})",
        annotation_position="right"
    )

    # Burst threshold (3x baseline)
    if baseline > 0:
        fig.add_hline(
            y=baseline * 3,
            line_dash="dot",
            line_color="red",
            annotation_text="Burst Threshold",
            annotation_position="right"
        )

    fig.update_layout(
        title="Posting Rate Over Time",
        xaxis_title="Time",
        yaxis_title="Comments per Minute",
        height=400,
        hovermode='x unified'
    )

    return fig


def cluster_visualization_2d(embeddings, labels):
    """Create 2D visualization of comment clusters."""
    from analysis.clustering import reduce_dimensions

    # Reduce to 2D
    reduced = reduce_dimensions(embeddings, n_components=2)

    # Create DataFrame
    df = pd.DataFrame({
        'x': reduced[:, 0],
        'y': reduced[:, 1],
        'cluster': [f"Cluster {l}" if l >= 0 else "Noise" for l in labels],
        'comment_id': range(len(labels))
    })

    # Create scatter plot
    fig = px.scatter(
        df,
        x='x',
        y='y',
        color='cluster',
        hover_data=['comment_id'],
        title='Comment Clusters (2D Projection)',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(
        height=500,
        xaxis_title="Dimension 1",
        yaxis_title="Dimension 2",
        showlegend=True
    )

    fig.update_traces(marker=dict(size=10))

    return fig


def network_graph(thread_data, max_nodes=100):
    """Create network graph of user interactions."""
    from analysis.graph import build_comment_graph
    import networkx as nx

    # Build graph
    G = build_comment_graph(thread_data)

    # Limit nodes for visualization
    if len(G.nodes()) > max_nodes:
        # Get most connected nodes
        degrees = dict(G.degree())
        top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:max_nodes]
        G = G.subgraph(top_nodes)

    # Get positions using spring layout
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # Extract node positions
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_type = G.nodes[node].get('node_type', 'unknown')
        node_text.append(f"{node}<br>Type: {node_type}")
        node_color.append('#667eea' if node_type == 'user' else '#f093fb')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=node_color,
            size=10,
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'User-Comment Network (showing {len(G.nodes())} nodes)',
                        showlegend=False,
                        hovermode='closest',
                        height=500,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig


def score_distribution(scores, current_score):
    """Show distribution of scores with current score highlighted."""
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=scores,
        nbinsx=20,
        marker_color='lightblue',
        name='All Threads'
    ))

    # Add vertical line for current score
    fig.add_vline(
        x=current_score,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Current: {current_score:.1f}",
        annotation_position="top"
    )

    fig.update_layout(
        title="Score Distribution Comparison",
        xaxis_title="Consensus Score",
        yaxis_title="Number of Threads",
        height=350,
        showlegend=False
    )

    return fig


def metric_comparison_table(metrics):
    """Create table comparing metrics to thresholds."""
    data = {
        'Metric': [
            'Average Similarity',
            'High Similarity Ratio',
            'Burst Coefficient',
            'Timing Entropy',
            'Clustering Coefficient',
            'Largest Cluster Ratio'
        ],
        'Value': [
            f"{metrics.get('semantic', {}).get('avg_similarity', 0):.3f}",
            f"{metrics.get('semantic', {}).get('high_similarity_ratio', 0):.3f}",
            f"{metrics.get('temporal', {}).get('burst_coefficient', 0):.2f}x",
            f"{metrics.get('temporal', {}).get('timing_entropy', 0):.2f}",
            f"{metrics.get('network', {}).get('clustering_coefficient', 0):.3f}",
            f"{metrics.get('clustering', {}).get('largest_cluster_ratio', 0):.3f}",
        ],
        'Threshold': [
            '> 0.600',
            '> 0.300',
            '> 3.0x',
            '< 2.0',
            '> 0.400',
            '> 0.200'
        ],
        'Status': []
    }

    # Determine status
    values = [
        metrics.get('semantic', {}).get('avg_similarity', 0),
        metrics.get('semantic', {}).get('high_similarity_ratio', 0),
        metrics.get('temporal', {}).get('burst_coefficient', 0),
        metrics.get('temporal', {}).get('timing_entropy', 0),
        metrics.get('network', {}).get('clustering_coefficient', 0),
        metrics.get('clustering', {}).get('largest_cluster_ratio', 0),
    ]

    thresholds = [0.600, 0.300, 3.0, 2.0, 0.400, 0.200]
    comparisons = ['>', '>', '>', '<', '>', '>']

    for v, t, c in zip(values, thresholds, comparisons):
        if c == '>':
            status = '🔴 Alert' if v > t else '🟢 Normal'
        else:
            status = '🔴 Alert' if v < t else '🟢 Normal'
        data['Status'].append(status)

    df = pd.DataFrame(data)

    return df
