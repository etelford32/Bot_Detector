"""Thread analysis page with comprehensive visualizations."""

import streamlit as st
import numpy as np

from ingestion.thread_fetcher import fetch_thread
from analysis.consensus_score import calculate_consensus_score
from analysis.similarity import compute_similarity_matrix
from analysis.clustering import perform_clustering
from explainability.rationale import generate_rationale
from dashboard.components import visualizations as viz


def show():
    """Display thread analysis page."""
    st.markdown("# 🔍 Analyze Reddit Thread")
    st.markdown("Enter a Reddit thread URL to analyze for synthetic consensus patterns.")

    # Input section
    col1, col2 = st.columns([3, 1])

    with col1:
        thread_url = st.text_input(
            "Reddit Thread URL",
            placeholder="https://www.reddit.com/r/worldnews/comments/...",
            help="Paste the full URL of a Reddit thread"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            use_cache = st.checkbox("Use embedding cache", value=True)
        with col2:
            show_visualizations = st.checkbox("Show all visualizations", value=True)
        with col3:
            show_raw_data = st.checkbox("Show raw data", value=False)

    # Analysis
    if analyze_button and thread_url:
        with st.spinner("🔄 Fetching and analyzing thread... This may take a minute."):
            try:
                # Fetch thread
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("📥 Fetching thread data...")
                thread_data = fetch_thread(thread_url)
                progress_bar.progress(25)

                status_text.text("🧠 Generating embeddings...")
                # The calculate_consensus_score will handle embeddings
                progress_bar.progress(50)

                status_text.text("📊 Analyzing patterns...")
                score, metrics = calculate_consensus_score(thread_data, use_cache)
                progress_bar.progress(75)

                status_text.text("✅ Generating report...")
                progress_bar.progress(100)

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                # Display results
                display_results(thread_data, score, metrics, show_visualizations, show_raw_data)

                # Success message
                st.success("✅ Analysis complete!")

            except Exception as e:
                st.error(f"❌ Error analyzing thread: {str(e)}")
                st.exception(e)

    # Example links
    if not thread_url:
        st.markdown("---")
        st.markdown("### 📌 Example Threads (for testing)")
        st.markdown("""
            Try analyzing these example patterns:
            - **High engagement thread**: Popular discussion with many comments
            - **Breaking news**: Fast-moving conversation
            - **Controversial topic**: Divided opinions

            *Note: Use real Reddit URLs for actual analysis*
        """)


def display_results(thread_data, score, metrics, show_visualizations, show_raw_data):
    """Display comprehensive analysis results."""

    # Thread header
    st.markdown("---")
    st.markdown("## 📋 Thread Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Subreddit", f"r/{thread_data['subreddit']}")
    with col2:
        st.metric("Total Comments", thread_data['num_comments'])
    with col3:
        st.metric("Analyzed", metrics['n_analyzed'])
    with col4:
        st.metric("Thread Score", f"↑ {thread_data['score']}")

    st.markdown(f"**Title:** {thread_data['title']}")
    st.markdown(f"**URL:** {thread_data['url']}")

    # Main score display
    st.markdown("---")
    st.markdown("## 🎯 Synthetic Consensus Score")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Gauge chart
        fig_gauge = viz.score_gauge(score)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Interpretation card
        interpretation = metrics['interpretation']
        confidence = metrics['confidence']

        st.markdown(f"""
            <div style="padding: 2rem; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h2 style="color: white; margin-top: 0;">Score: {score:.1f}/100</h2>
                <h3 style="color: white;">{interpretation['level']}</h3>
                <p><strong>Confidence:</strong> {confidence}</p>
                <p>{interpretation['description']}</p>
                <hr style="border-color: rgba(255,255,255,0.3);">
                <p><strong>Recommendation:</strong><br>{interpretation['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)

    # Component scores
    st.markdown("---")
    st.markdown("## 📊 Component Analysis")

    tab1, tab2 = st.tabs(["📊 Bar Chart", "🕸️ Radar Chart"])

    with tab1:
        fig_bar = viz.component_scores_bar(metrics)
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        fig_radar = viz.component_scores_radar(metrics)
        st.plotly_chart(fig_radar, use_container_width=True)

    # Component breakdown
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        semantic_score = metrics.get('semantic', {}).get('semantic_score', 0)
        st.metric(
            "Semantic Score",
            f"{semantic_score:.1f}",
            help="Measures similarity in comment content and messaging"
        )

    with col2:
        temporal_score = metrics.get('temporal', {}).get('temporal_score', 0)
        st.metric(
            "Temporal Score",
            f"{temporal_score:.1f}",
            help="Detects suspicious timing patterns and bursts"
        )

    with col3:
        network_score = metrics.get('network', {}).get('network_score', 0)
        st.metric(
            "Network Score",
            f"{network_score:.1f}",
            help="Analyzes user interaction and coordination patterns"
        )

    with col4:
        behavioral_score = metrics.get('behavioral', {}).get('behavioral_score', 0)
        st.metric(
            "Behavioral Score",
            f"{behavioral_score:.1f}",
            help="Evaluates account characteristics and posting behavior"
        )

    # Detailed analysis
    if show_visualizations:
        st.markdown("---")
        st.markdown("## 📈 Detailed Visualizations")

        # Create tabs for different analysis types
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔤 Semantic Analysis",
            "⏰ Temporal Patterns",
            "🌐 Network Structure",
            "📏 Metrics Comparison"
        ])

        with tab1:
            display_semantic_analysis(thread_data, metrics)

        with tab2:
            display_temporal_analysis(thread_data, metrics)

        with tab3:
            display_network_analysis(thread_data, metrics)

        with tab4:
            display_metrics_comparison(metrics)

    # Rationale
    st.markdown("---")
    st.markdown("## 📝 Detailed Explanation")

    rationale = generate_rationale(score, metrics)

    with st.expander("📄 View Full Rationale", expanded=True):
        st.text(rationale)

    # Templates detected
    templates = metrics.get('templates', [])
    if templates:
        st.markdown("---")
        st.markdown("## 🔖 Template Detection")

        st.markdown(f"**{len(templates)} template patterns detected**")

        for i, template in enumerate(templates[:5], 1):
            with st.expander(f"Template {i}: {template['count']} instances (avg similarity: {template['avg_similarity']:.3f})"):
                st.markdown(f"**Representative text:**")
                st.info(template['representative'])

                st.markdown("**Example variations:**")
                for j, instance in enumerate(template['instances'][:3], 1):
                    st.markdown(f"{j}. _{instance}_")

    # Raw data
    if show_raw_data:
        st.markdown("---")
        st.markdown("## 🔍 Raw Data")

        with st.expander("View Raw Metrics"):
            st.json(metrics)

        with st.expander("View Thread Data"):
            st.json(thread_data)


def display_semantic_analysis(thread_data, metrics):
    """Display semantic analysis visualizations."""
    st.markdown("### Semantic Similarity Analysis")

    # Get embeddings if available in session state
    if 'last_embeddings' in st.session_state:
        embeddings = st.session_state.last_embeddings

        col1, col2 = st.columns(2)

        with col1:
            # Similarity heatmap
            sim_matrix = compute_similarity_matrix(embeddings)
            fig_heatmap = viz.similarity_heatmap(sim_matrix)
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with col2:
            # Cluster visualization
            clustering = metrics.get('clustering', {})
            if clustering.get('n_clusters', 0) > 0:
                # Perform clustering for visualization
                from analysis.clustering import perform_clustering
                clustering_result = perform_clustering(embeddings)
                labels = clustering_result['labels']

                fig_clusters = viz.cluster_visualization_2d(embeddings, labels)
                st.plotly_chart(fig_clusters, use_container_width=True)
            else:
                st.info("No distinct clusters detected")

    # Semantic metrics
    semantic = metrics.get('semantic', {})

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Similarity",
            f"{semantic.get('avg_similarity', 0):.3f}",
            help="Mean cosine similarity between all comment pairs"
        )

    with col2:
        st.metric(
            "Max Similarity",
            f"{semantic.get('max_similarity', 0):.3f}",
            help="Highest similarity found between any two comments"
        )

    with col3:
        st.metric(
            "High Similarity Ratio",
            f"{semantic.get('high_similarity_ratio', 0):.1%}",
            help="Percentage of comment pairs with similarity > 0.85"
        )


def display_temporal_analysis(thread_data, metrics):
    """Display temporal analysis visualizations."""
    st.markdown("### Temporal Pattern Analysis")

    timestamps = [c['created_utc'] for c in thread_data['comments']]

    # Timeline
    fig_timeline = viz.temporal_timeline(timestamps)
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Burst chart
    fig_burst = viz.temporal_burst_chart(timestamps)
    st.plotly_chart(fig_burst, use_container_width=True)

    # Temporal metrics
    temporal = metrics.get('temporal', {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Burst Coefficient",
            f"{temporal.get('burst_coefficient', 0):.2f}x",
            help="Peak rate compared to baseline (>3.0 is suspicious)"
        )

    with col2:
        st.metric(
            "Timing Entropy",
            f"{temporal.get('timing_entropy', 0):.2f}",
            help="Randomness of posting intervals (lower = more coordinated)"
        )

    with col3:
        st.metric(
            "Bursts Detected",
            temporal.get('n_bursts', 0),
            help="Number of posting bursts identified"
        )

    with col4:
        st.metric(
            "Max Coordinated",
            temporal.get('max_coordinated_group', 0),
            help="Largest group posting within 60 seconds"
        )


def display_network_analysis(thread_data, metrics):
    """Display network analysis visualizations."""
    st.markdown("### Network Structure Analysis")

    # Network graph
    try:
        fig_network = viz.network_graph(thread_data, max_nodes=75)
        st.plotly_chart(fig_network, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not generate network graph: {str(e)}")

    # Network metrics
    network = metrics.get('network', {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Clustering Coef.",
            f"{network.get('clustering_coefficient', 0):.3f}",
            help="How interconnected users are (higher = more coordinated)"
        )

    with col2:
        st.metric(
            "Isolation Ratio",
            f"{network.get('isolation_ratio', 0):.1%}",
            help="Percentage of users in isolated clusters"
        )

    with col3:
        st.metric(
            "Largest Cluster",
            network.get('largest_isolated_group', 0),
            help="Size of largest isolated user group"
        )

    with col4:
        st.metric(
            "Comments/User",
            f"{network.get('comments_per_user', 0):.2f}",
            help="Average comments per unique user"
        )


def display_metrics_comparison(metrics):
    """Display detailed metrics comparison table."""
    st.markdown("### Metrics vs. Thresholds")

    st.markdown("""
        This table compares key metrics against detection thresholds.
        🔴 **Alert** indicates the metric exceeds the suspicious threshold.
    """)

    df = viz.metric_comparison_table(metrics)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Additional metric details
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Clustering Metrics")
        clustering = metrics.get('clustering', {})

        st.metric("Number of Clusters", clustering.get('n_clusters', 0))
        st.metric("Largest Cluster Ratio", f"{clustering.get('largest_cluster_ratio', 0):.1%}")
        st.metric("Noise Ratio", f"{clustering.get('noise_ratio', 0):.1%}")

    with col2:
        st.markdown("#### Distribution Metrics")
        semantic = metrics.get('semantic', {})

        if 'std_similarity' in semantic:
            st.metric("Similarity Std Dev", f"{semantic.get('std_similarity', 0):.3f}")
        if 'diversity_index' in semantic:
            st.metric("Diversity Index", f"{semantic.get('diversity_index', 0):.3f}")
