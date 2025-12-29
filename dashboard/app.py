"""Streamlit dashboard for ConsensusWatch."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from ingestion.thread_fetcher import fetch_thread
from analysis.consensus_score import calculate_consensus_score
from analysis.clustering import reduce_dimensions
from explainability.rationale import generate_rationale, format_detailed_report
from explainability.summaries import generate_narrative_summary


st.set_page_config(
    page_title="ConsensusWatch - Bot Detector",
    page_icon="🤖",
    layout="wide",
)


def main():
    """Main dashboard application."""
    st.title("🤖 ConsensusWatch - Reddit Bot Detector")
    st.markdown(
        "Detect synthetic consensus and coordinated narrative steering in Reddit threads"
    )

    # Sidebar
    st.sidebar.title("Settings")
    use_cache = st.sidebar.checkbox("Use embedding cache", value=True)
    show_raw_metrics = st.sidebar.checkbox("Show raw metrics", value=False)

    # Main input
    st.header("Analyze a Reddit Thread")

    thread_url = st.text_input(
        "Enter Reddit thread URL:",
        placeholder="https://www.reddit.com/r/worldnews/comments/...",
    )

    analyze_button = st.button("Analyze Thread", type="primary")

    if analyze_button and thread_url:
        with st.spinner("Fetching and analyzing thread..."):
            try:
                # Fetch thread
                thread_data = fetch_thread(thread_url)

                # Calculate score
                score, metrics = calculate_consensus_score(thread_data, use_cache)

                # Display results
                display_results(thread_data, score, metrics, show_raw_metrics)

            except Exception as e:
                st.error(f"Error analyzing thread: {str(e)}")


def display_results(thread_data, score, metrics, show_raw_metrics):
    """Display analysis results."""
    # Thread info
    st.subheader("Thread Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Subreddit", f"r/{thread_data['subreddit']}")

    with col2:
        st.metric("Comments Analyzed", metrics['n_analyzed'])

    with col3:
        st.metric("Thread Score", thread_data['score'])

    st.markdown(f"**Title:** {thread_data['title']}")

    # Main score display
    st.divider()
    display_score_gauge(score, metrics)

    # Component scores
    st.divider()
    st.subheader("Component Analysis")
    display_component_scores(metrics)

    # Rationale
    st.divider()
    st.subheader("Detailed Analysis")
    rationale = generate_rationale(score, metrics)
    st.text(rationale)

    # Visualizations
    if show_raw_metrics:
        st.divider()
        st.subheader("Advanced Metrics")
        display_advanced_metrics(metrics)


def display_score_gauge(score, metrics):
    """Display score as a gauge chart."""
    interpretation = metrics['interpretation']
    confidence = metrics['confidence']

    col1, col2 = st.columns([2, 1])

    with col1:
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title={'text': "Synthetic Consensus Score"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': get_score_color(score)},
                'steps': [
                    {'range': [0, 25], 'color': "lightgreen"},
                    {'range': [25, 50], 'color': "lightyellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric("Interpretation", interpretation['level'])
        st.metric("Confidence", confidence)

        # Color-coded interpretation
        level = interpretation['level']
        if "Organic" in level:
            st.success(interpretation['description'])
        elif "Possible" in level:
            st.warning(interpretation['description'])
        elif "Likely" in level:
            st.warning(interpretation['description'])
        else:
            st.error(interpretation['description'])


def display_component_scores(metrics):
    """Display component scores as bar chart."""
    semantic = metrics.get('semantic', {})
    temporal = metrics.get('temporal', {})
    network = metrics.get('network', {})

    components = {
        'Semantic': semantic.get('semantic_score', 0),
        'Temporal': temporal.get('temporal_score', 0),
        'Network': network.get('network_score', 0),
    }

    # Bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(components.keys()),
            y=list(components.values()),
            marker_color=[get_score_color(v) for v in components.values()],
            text=[f"{v:.1f}" for v in components.values()],
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Component Scores",
        yaxis_title="Score (0-100)",
        yaxis_range=[0, 100],
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Semantic Score",
            f"{components['Semantic']:.1f}/100",
            help="Measures semantic similarity and template usage"
        )

    with col2:
        st.metric(
            "Temporal Score",
            f"{components['Temporal']:.1f}/100",
            help="Measures timing patterns and bursts"
        )

    with col3:
        st.metric(
            "Network Score",
            f"{components['Network']:.1f}/100",
            help="Measures user interaction patterns"
        )


def display_advanced_metrics(metrics):
    """Display advanced metrics and visualizations."""
    # Tabs for different metric categories
    tab1, tab2, tab3 = st.tabs(["Semantic", "Temporal", "Network"])

    with tab1:
        semantic = metrics.get('semantic', {})
        st.json({
            "Average Similarity": f"{semantic.get('avg_similarity', 0):.3f}",
            "Max Similarity": f"{semantic.get('max_similarity', 0):.3f}",
            "High Similarity Ratio": f"{semantic.get('high_similarity_ratio', 0):.3f}",
            "Cluster Homogeneity": f"{semantic.get('cluster_homogeneity', 0):.3f}",
        })

        # Templates
        templates = metrics.get('templates', [])
        if templates:
            st.subheader("Detected Templates")
            for i, template in enumerate(templates[:3]):
                with st.expander(f"Template {i+1} ({template['count']} instances)"):
                    st.write(f"**Representative:** {template['representative']}")
                    st.write(f"**Similarity:** {template['avg_similarity']:.3f}")

    with tab2:
        temporal = metrics.get('temporal', {})
        st.json({
            "Burst Coefficient": f"{temporal.get('burst_coefficient', 0):.2f}x",
            "Timing Entropy": f"{temporal.get('timing_entropy', 0):.2f}",
            "Number of Bursts": temporal.get('n_bursts', 0),
            "Max Coordinated Group": temporal.get('max_coordinated_group', 0),
        })

    with tab3:
        network = metrics.get('network', {})
        st.json({
            "Clustering Coefficient": f"{network.get('clustering_coefficient', 0):.3f}",
            "Isolation Ratio": f"{network.get('isolation_ratio', 0):.3f}",
            "Largest Isolated Group": network.get('largest_isolated_group', 0),
            "Comments per User": f"{network.get('comments_per_user', 0):.2f}",
        })


def get_score_color(score):
    """Get color for score."""
    if score < 25:
        return "green"
    elif score < 50:
        return "yellow"
    elif score < 75:
        return "orange"
    else:
        return "red"


if __name__ == "__main__":
    main()
