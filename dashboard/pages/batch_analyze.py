"""Batch analysis page for analyzing multiple threads."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ingestion.thread_fetcher import fetch_subreddit_window, fetch_subreddit_threads
from analysis.consensus_score import calculate_consensus_score
from dashboard.components import visualizations as viz


def show():
    """Display batch analysis page."""
    st.markdown("# 📊 Batch Thread Analysis")
    st.markdown("Analyze multiple threads from a subreddit to identify patterns across discussions.")

    # Input section
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        subreddit = st.text_input(
            "Subreddit Name",
            placeholder="worldnews",
            help="Enter subreddit name without 'r/'"
        )

    with col2:
        time_window = st.selectbox(
            "Time Window",
            options=[1, 6, 12, 24, 48, 72],
            index=3,
            format_func=lambda x: f"{x} hours"
        )

    with col3:
        min_comments = st.number_input(
            "Min Comments",
            min_value=10,
            max_value=500,
            value=50,
            step=10
        )

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            max_threads = st.slider("Max threads to analyze", 5, 50, 20)
            use_cache = st.checkbox("Use embedding cache", value=True)
        with col2:
            sort_by = st.selectbox("Sort by", ["hot", "new", "top", "rising"])
            filter_score = st.slider("Filter by score threshold", 0, 100, 0)

    # Analyze button
    analyze_button = st.button("📊 Analyze Subreddit", type="primary", use_container_width=True)

    if analyze_button and subreddit:
        with st.spinner(f"🔄 Analyzing r/{subreddit}... This may take several minutes."):
            try:
                # Fetch threads
                st.info(f"📥 Fetching threads from r/{subreddit}...")

                threads = fetch_subreddit_window(
                    subreddit,
                    hours=time_window,
                    comment_threshold=min_comments
                )

                if not threads:
                    st.warning("No threads found matching your criteria. Try adjusting the filters.")
                    return

                # Limit threads
                threads = threads[:max_threads]

                st.success(f"Found {len(threads)} threads to analyze")

                # Analyze each thread
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i, thread_data in enumerate(threads):
                    status_text.text(f"Analyzing thread {i+1}/{len(threads)}: {thread_data['title'][:50]}...")

                    try:
                        score, metrics = calculate_consensus_score(thread_data, use_cache)

                        results.append({
                            'thread_id': thread_data['thread_id'],
                            'title': thread_data['title'],
                            'url': thread_data['url'],
                            'score': score,
                            'n_comments': thread_data['num_comments'],
                            'thread_score': thread_data['score'],
                            'interpretation': metrics['interpretation']['level'],
                            'confidence': metrics['confidence'],
                            'semantic_score': metrics.get('semantic', {}).get('semantic_score', 0),
                            'temporal_score': metrics.get('temporal', {}).get('temporal_score', 0),
                            'network_score': metrics.get('network', {}).get('network_score', 0),
                        })

                    except Exception as e:
                        st.warning(f"Failed to analyze: {thread_data['title'][:50]}... - {str(e)}")
                        continue

                    progress_bar.progress((i + 1) / len(threads))

                progress_bar.empty()
                status_text.empty()

                if not results:
                    st.error("Failed to analyze any threads. Please try again.")
                    return

                # Filter by score if needed
                if filter_score > 0:
                    results = [r for r in results if r['score'] >= filter_score]

                # Display results
                display_batch_results(subreddit, results, time_window)

            except Exception as e:
                st.error(f"❌ Error during batch analysis: {str(e)}")
                st.exception(e)

    # Information section
    if not subreddit:
        st.markdown("---")
        st.markdown("### 📌 How Batch Analysis Works")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                **Use Cases:**
                - Monitor subreddit for coordinated campaigns
                - Identify trends in manipulation tactics
                - Compare threads on similar topics
                - Generate research datasets
            """)

        with col2:
            st.markdown("""
                **What You'll Get:**
                - Score distribution across threads
                - High-risk thread identification
                - Comparative visualizations
                - Downloadable results
            """)


def display_batch_results(subreddit, results, time_window):
    """Display batch analysis results."""
    st.markdown("---")
    st.markdown(f"## 📊 Analysis Results: r/{subreddit}")

    # Summary statistics
    scores = [r['score'] for r in results]
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)

    high_risk = sum(1 for s in scores if s >= 75)
    medium_risk = sum(1 for s in scores if 50 <= s < 75)
    low_risk = sum(1 for s in scores if s < 50)

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Threads Analyzed", len(results))

    with col2:
        st.metric("Average Score", f"{avg_score:.1f}")

    with col3:
        st.metric("Highest Score", f"{max_score:.1f}")

    with col4:
        st.metric("High Risk Threads", high_risk, delta=f"{high_risk/len(results)*100:.0f}%")

    # Risk distribution
    st.markdown("### 🎯 Risk Distribution")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Distribution chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=['High Risk\n(≥75)', 'Medium Risk\n(50-74)', 'Low Risk\n(<50)'],
            y=[high_risk, medium_risk, low_risk],
            marker_color=['#DC3545', '#FFC107', '#28A745'],
            text=[high_risk, medium_risk, low_risk],
            textposition='auto',
        ))

        fig.update_layout(
            title="Thread Risk Categories",
            yaxis_title="Number of Threads",
            height=300,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.metric("🔴 High Risk", f"{high_risk} ({high_risk/len(results)*100:.0f}%)")
        st.metric("🟡 Medium Risk", f"{medium_risk} ({medium_risk/len(results)*100:.0f}%)")
        st.metric("🟢 Low Risk", f"{low_risk} ({low_risk/len(results)*100:.0f}%)")

    # Score distribution histogram
    st.markdown("### 📈 Score Distribution")

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=scores,
        nbinsx=20,
        marker_color='#667eea',
        hovertemplate='Score: %{x:.1f}<br>Count: %{y}<extra></extra>'
    ))

    fig.add_vline(x=avg_score, line_dash="dash", line_color="red",
                  annotation_text=f"Average: {avg_score:.1f}")

    fig.update_layout(
        title="Distribution of Consensus Scores",
        xaxis_title="Consensus Score",
        yaxis_title="Number of Threads",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

    # Component score comparison
    st.markdown("### 🔍 Component Score Comparison")

    df = pd.DataFrame(results)

    fig = go.Figure()

    fig.add_trace(go.Box(y=df['semantic_score'], name='Semantic', marker_color='#667eea'))
    fig.add_trace(go.Box(y=df['temporal_score'], name='Temporal', marker_color='#f093fb'))
    fig.add_trace(go.Box(y=df['network_score'], name='Network', marker_color='#4facfe'))

    fig.update_layout(
        title="Component Score Distribution",
        yaxis_title="Score (0-100)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Thread list
    st.markdown("### 📋 Analyzed Threads")

    # Sort options
    sort_by = st.selectbox(
        "Sort by:",
        ['Consensus Score (High to Low)', 'Consensus Score (Low to High)',
         'Thread Score', 'Number of Comments', 'Title']
    )

    if sort_by == 'Consensus Score (High to Low)':
        results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)
    elif sort_by == 'Consensus Score (Low to High)':
        results_sorted = sorted(results, key=lambda x: x['score'])
    elif sort_by == 'Thread Score':
        results_sorted = sorted(results, key=lambda x: x['thread_score'], reverse=True)
    elif sort_by == 'Number of Comments':
        results_sorted = sorted(results, key=lambda x: x['n_comments'], reverse=True)
    else:
        results_sorted = sorted(results, key=lambda x: x['title'])

    # Display threads
    for i, result in enumerate(results_sorted, 1):
        score = result['score']

        # Color-code based on risk
        if score >= 75:
            badge_color = "#DC3545"
            risk_level = "High Risk"
        elif score >= 50:
            badge_color = "#FFC107"
            risk_level = "Medium Risk"
        else:
            badge_color = "#28A745"
            risk_level = "Low Risk"

        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**{i}. {result['title']}**")
                st.markdown(f"[View Thread]({result['url']})")

            with col2:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="background: {badge_color}; color: white; padding: 0.5rem; border-radius: 5px; font-weight: bold;">
                            {score:.1f}/100
                        </div>
                        <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">
                            {risk_level}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.metric("Comments", result['n_comments'], label_visibility="visible")

            st.markdown(f"*{result['interpretation']} (Confidence: {result['confidence']})*")

        st.markdown("---")

    # Export options
    st.markdown("### 💾 Export Results")

    col1, col2 = st.columns(2)

    with col1:
        # CSV export
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"consensuswatch_{subreddit}_{time_window}h.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # JSON export
        import json
        json_data = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name=f"consensuswatch_{subreddit}_{time_window}h.json",
            mime="application/json",
            use_container_width=True
        )
