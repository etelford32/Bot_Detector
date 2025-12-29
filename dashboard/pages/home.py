"""Home/landing page."""

import streamlit as st


def show():
    """Display home page."""
    # Hero section
    st.markdown("""
        <div class="main-header">
            🤖 ConsensusWatch
        </div>
        <div class="sub-header">
            Detect Synthetic Consensus & Coordinated Narrative Steering
        </div>
    """, unsafe_allow_html=True)

    # Introduction
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            **ConsensusWatch** uses advanced NLP and network analysis to identify potential
            bot campaigns, astroturfing, and coordinated inauthentic behavior on Reddit.
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Key features
    st.markdown("## ✨ Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>🧠 Semantic Analysis</h3>
                <p>Detects coordinated messaging using state-of-the-art sentence transformers</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>⏱️ Temporal Patterns</h3>
                <p>Identifies suspicious timing and burst patterns in posting behavior</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>🕸️ Network Analysis</h3>
                <p>Maps coordination through user interaction graph analysis</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    st.markdown("## 🔬 How It Works")

    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Data Collection",
        "2️⃣ Multi-Signal Analysis",
        "3️⃣ Score Calculation",
        "4️⃣ Explanation"
    ])

    with tab1:
        st.markdown("""
            ### Data Collection

            ConsensusWatch fetches Reddit threads and comments using the official API (PRAW):

            - **Thread metadata**: Title, subreddit, timestamp, scores
            - **Comment data**: Text, author, timing, reply structure
            - **User information**: Account age, karma, posting patterns

            All data is public and analyzed in accordance with Reddit's Terms of Service.
        """)

        st.code("""
# Example: Fetch a thread
from ingestion import fetch_thread

thread_data = fetch_thread("https://reddit.com/r/...")
# Returns: comments, timestamps, user info, etc.
        """, language="python")

    with tab2:
        st.markdown("""
            ### Multi-Signal Analysis

            The system analyzes threads using four independent signals:

            **🔤 Semantic Similarity (35% weight)**
            - Measures how similar comments are in meaning
            - Detects template usage and coordinated messaging
            - Uses sentence transformers for semantic embeddings

            **⏰ Temporal Clustering (25% weight)**
            - Identifies posting bursts and timing patterns
            - Calculates timing entropy
            - Detects coordinated waves

            **🌐 Network Coordination (25% weight)**
            - Analyzes user interaction graphs
            - Identifies isolated user clusters
            - Measures community structure

            **👤 Behavioral Patterns (15% weight)**
            - Account age and karma analysis
            - Posting history patterns
            - Suspicious naming conventions
        """)

    with tab3:
        st.markdown("""
            ### Score Calculation

            Component scores are weighted and combined:

            ```
            Final Score =
                0.35 × Semantic Score +
                0.25 × Temporal Score +
                0.25 × Network Score +
                0.15 × Behavioral Score
            ```

            **Score Interpretation:**

            - **0-25**: Likely Organic - Normal discussion
            - **25-50**: Possible Coordination - Investigate further
            - **50-75**: Likely Coordinated - Multiple red flags
            - **75-100**: Highly Coordinated - Strong evidence
        """)

        # Score visualization
        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=72,
            title={'text': "Example Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgreen"},
                    {'range': [25, 50], 'color': "lightyellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("""
            ### Explainable Results

            Every analysis includes:

            ✅ **Human-readable rationale**
            - Primary signals driving the score
            - Specific evidence and examples
            - Confidence assessment

            ✅ **Detailed metrics**
            - Component breakdowns
            - Statistical evidence
            - Visual representations

            ✅ **Caveats and limitations**
            - Alternative explanations
            - Known edge cases
            - Uncertainty acknowledgment
        """)

        st.info("""
            **Example Rationale:**

            Score: 78/100 (Likely Coordinated)
            Confidence: High

            **Primary Signals:**
            • High semantic similarity: 45 comments (23% of thread) form tight cluster
            • Temporal burst: 38 similar comments posted within 12 minutes
            • Network pattern: 15 accounts with minimal Reddit history

            **Caveats:**
            • Could be organic response to breaking news
            • Some accounts may be genuine new users
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Use cases
    st.markdown("## 🎯 Use Cases")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            ### For Researchers
            - Study manipulation campaigns
            - Analyze platform dynamics
            - Validate detection methods
            - Publish findings
        """)

        st.markdown("""
            ### For Journalists
            - Investigate suspicious consensus
            - Verify grassroots movements
            - Fact-check narratives
            - Identify disinformation
        """)

    with col2:
        st.markdown("""
            ### For Moderators
            - Identify brigading
            - Detect coordinated campaigns
            - Supplement moderation
            - Protect communities
        """)

        st.markdown("""
            ### For Users
            - Think critically
            - Verify consensus
            - Understand manipulation
            - Make informed decisions
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    st.markdown("## 🚀 Get Started")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
                <h3>Ready to analyze a thread?</h3>
                <p>Enter a Reddit URL and get instant analysis with detailed explanations.</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 Start Analysis", use_container_width=True, type="primary"):
            st.session_state.page = "🔍 Analyze Thread"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Important disclaimers
    st.markdown("## ⚠️ Important Disclaimers")

    st.warning("""
        **This tool provides probabilistic indicators, not proof.**

        - Scores are estimates based on patterns, not definitive evidence
        - High scores may have innocent explanations (e.g., breaking news)
        - Results should inform further investigation, not replace human judgment
        - Never harass or dox users based on tool output
        - Respect Reddit's Terms of Service and user privacy
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Statistics (mock for MVP)
    st.markdown("## 📊 Platform Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Threads Analyzed", "1,247", "+89")

    with col2:
        st.metric("Detection Accuracy", "89%", "+2%")

    with col3:
        st.metric("Avg Analysis Time", "8.3s", "-1.2s")

    with col4:
        st.metric("Active Users", "342", "+45")
