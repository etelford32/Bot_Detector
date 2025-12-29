"""Documentation page."""

import streamlit as st
from pathlib import Path


def show():
    """Display documentation page."""
    st.markdown("# 📚 Documentation")

    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Getting Started",
        "🔬 Methodology",
        "📊 Synthetic Consensus Index",
        "⚠️ Limitations",
        "💡 Use Cases"
    ])

    with tab1:
        show_getting_started()

    with tab2:
        show_methodology()

    with tab3:
        show_sci_explanation()

    with tab4:
        show_limitations()

    with tab5:
        show_use_cases()


def show_getting_started():
    """Getting started guide."""
    st.markdown("## Getting Started with ConsensusWatch")

    st.markdown("""
### Quick Start

1. **Analyze a Single Thread**
   - Go to the "Analyze Thread" page
   - Paste a Reddit thread URL
   - Click "Analyze"
   - Review the score and detailed breakdown

2. **Batch Analysis**
   - Go to "Batch Analysis" page
   - Enter a subreddit name
   - Set time window and filters
   - Click "Analyze Subreddit"
   - Compare results across threads

3. **Interpret Results**
   - **Score 0-25**: Likely organic discussion
   - **Score 25-50**: Some coordination signals
   - **Score 50-75**: Likely coordinated behavior
   - **Score 75-100**: Highly coordinated/synthetic

### Understanding the Score

The Synthetic Consensus Score combines four independent signals:

**🔤 Semantic Analysis (35%)**: Detects similar messaging patterns
- Template usage
- Coordinated talking points
- Unusual similarity

**⏰ Temporal Analysis (25%)**: Identifies timing patterns
- Posting bursts
- Coordinated waves
- Automated timing

**🌐 Network Analysis (25%)**: Maps user coordination
- Isolated clusters
- Interaction patterns
- Community structure

**👤 Behavioral Analysis (15%)**: Evaluates account patterns
- Account age
- Posting history
- Suspicious characteristics
    """)

    st.info("""
**Pro Tip**: Always read the full rationale! The score is just a starting point.
Context, caveats, and evidence are crucial for proper interpretation.
    """)

    st.markdown("""
### Best Practices

✅ **Do:**
- Consider thread context (breaking news, controversy)
- Read the detailed explanation
- Look for multiple corroborating signals
- Treat scores as probabilistic indicators
- Report findings responsibly

❌ **Don't:**
- Treat scores as definitive proof
- Harass suspected accounts
- Ignore alternative explanations
- Skip the confidence rating
- Share results without context
    """)


def show_methodology():
    """Methodology explanation."""
    st.markdown("## Methodology")

    st.markdown("""
ConsensusWatch uses a multi-layered analysis approach to detect coordinated behavior:

### 1. Data Collection

Fetches public Reddit data via PRAW API:
- Thread metadata
- Comment text and timing
- User information
- Reply structure
    """)

    st.code("""
# Example data collection
from ingestion import fetch_thread

thread_data = fetch_thread(url)
# Returns: comments, timestamps, users, etc.
    """, language="python")

    st.markdown("""
### 2. Semantic Analysis

Uses sentence transformers to generate embeddings:
- Model: `all-MiniLM-L6-v2`
- Embedding dimension: 384
- Similarity metric: Cosine similarity

**Detects:**
- Template-based commenting
- Coordinated messaging
- Unusual uniformity
- Paraphrasing patterns
    """)

    st.markdown("""
### 3. Clustering Analysis

HDBSCAN + UMAP for pattern detection:
- Identifies comment clusters
- Measures cluster density
- Detects coordination groups

**Parameters:**
- Min cluster size: 5
- Min samples: 3
- Metric: Cosine distance
    """)

    st.markdown("""
### 4. Temporal Analysis

Analyzes posting timing:
- Burst detection (sliding window)
- Timing entropy calculation
- Coordinated wave identification

**Metrics:**
- Burst coefficient: Peak/baseline rate
- Timing entropy: Shannon entropy
- Coordination window: 60 seconds
    """)

    st.markdown("""
### 5. Network Analysis

Graph-based coordination detection:
- User-comment interaction graph
- Community structure analysis
- Isolation detection

**Uses NetworkX for:**
- Clustering coefficient
- Connected components
- Centrality measures
    """)

    st.markdown("""
### 6. Score Calculation

Weighted combination:
```
Score = 0.35×Semantic + 0.25×Temporal + 0.25×Network + 0.15×Behavioral
```

Confidence based on:
- Signal strength
- Signal agreement
- Sample size
    """)


def show_sci_explanation():
    """Explain Synthetic Consensus Index."""
    st.markdown("## Synthetic Consensus Index (SCI)")

    st.markdown("""
The SCI is a 0-100 score indicating likelihood of artificial coordination.

### Score Components

#### 🔤 Semantic Score (35% weight)

Measures comment similarity:

**Metrics:**
- Average pairwise similarity
- High similarity ratio (>0.85)
- Template usage frequency
- Cluster homogeneity

**Red Flags:**
- >20% of comments in tight cluster
- Template matching detected
- Low vocabulary diversity
    """)

    st.latex(r"""
    \text{Semantic} = 0.4 \times \overline{\text{sim}} + 0.3 \times \text{high\_sim\_ratio} + 0.3 \times \text{cluster\_homog}
    """)

    st.markdown("""
#### ⏰ Temporal Score (25% weight)

Analyzes timing patterns:

**Metrics:**
- Burst coefficient (peak/baseline)
- Timing entropy
- Number of bursts
- Coordinated groups

**Red Flags:**
- Burst >3x baseline
- Low timing entropy (<2.0)
- Multiple coordinated waves
    """)

    st.latex(r"""
    \text{Temporal} = 0.4 \times \text{burst\_coef} + 0.3 \times (1 - \text{entropy}) + 0.3 \times \text{coord\_ratio}
    """)

    st.markdown("""
#### 🌐 Network Score (25% weight)

Evaluates user coordination:

**Metrics:**
- Clustering coefficient
- Isolation ratio
- Repeat posting
- Community structure

**Red Flags:**
- Isolated user clusters
- High clustering (>0.5)
- Limited cross-group interaction
    """)

    st.markdown("""
### Interpretation Thresholds

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 0-25 | Likely Organic | No concerns |
| 25-50 | Possible Coordination | Investigate |
| 50-75 | Likely Coordinated | Multiple red flags |
| 75-100 | Highly Coordinated | Strong evidence |

### Confidence Levels

**Very High**: Multiple strong signals, large sample
**High**: Strong signals, adequate sample
**Medium**: Mixed signals or moderate sample
**Low**: Weak signals or small sample
    """)


def show_limitations():
    """Show limitations and ethical considerations."""
    st.markdown("## Limitations & Ethics")

    st.warning("""
### ⚠️ Important Limitations

**This tool provides indicators, not proof.**
    """)

    st.markdown("""
### Technical Limitations

**1. False Positives**
- Breaking news creates natural bursts
- Grassroots movements show coordination
- Memes and copypasta trigger alerts
- Cultural references appear similar

**2. False Negatives**
- Sophisticated campaigns evade detection
- Slow-drip tactics avoid temporal flags
- Aged accounts bypass behavioral checks
- Paraphrasing evades semantic detection

**3. Sample Size Dependency**
- Requires 20+ comments minimum
- Small threads less reliable
- Need time span for temporal analysis

**4. Language Limitations**
- Optimized for English
- May misread cultural nuances
- Slang and dialects challenging

### Ethical Considerations

**Privacy**
- Only public data analyzed
- No personal information stored
- Respect user privacy

**Responsible Use**
- Don't harass users
- No doxxing based on scores
- Provide full context when sharing
- Acknowledge uncertainty

**Bias Awareness**
- Training data biases
- Cultural assumptions
- Validation dataset selection

### What This Tool Cannot Do

❌ Prove individual accounts are bots
❌ Distinguish all sophisticated campaigns
❌ Account for all cultural context
❌ Replace human judgment
❌ Provide 100% accuracy

### Recommended Approach

1. Use tool as screening mechanism
2. Manually review high scores
3. Consider context and timing
4. Look for corroborating evidence
5. Acknowledge uncertainty
6. Report responsibly
    """)

    st.info("""
**Remember**: This is a research tool, not a verdict system.
Scores should inform investigation, not replace critical thinking.
    """)


def show_use_cases():
    """Show use cases and examples."""
    st.markdown("## Use Cases & Examples")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
### 👨‍🔬 Researchers

**Applications:**
- Study manipulation campaigns
- Validate detection methods
- Analyze platform dynamics
- Publish findings

**Best Practices:**
- Document methodology
- Validate against known cases
- Acknowledge limitations
- Share responsibly

**Example Research Questions:**
- How do coordination tactics vary by topic?
- What temporal patterns indicate bots?
- How effective is platform moderation?
        """)

    with col2:
        st.markdown("""
### 📰 Journalists

**Applications:**
- Investigate suspicious consensus
- Verify grassroots claims
- Fact-check narratives
- Identify disinformation

**Best Practices:**
- Cross-verify with sources
- Provide full context
- Quote scores accurately
- Don't doxx accounts

**Story Ideas:**
- "Is this viral thread organic?"
- "Investigating astroturfing campaigns"
- "How bots shape political discourse"
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
### 🛡️ Moderators

**Applications:**
- Identify brigading
- Detect campaigns
- Supplement moderation
- Protect communities

**Best Practices:**
- Use as one signal
- Don't auto-remove
- Consider appeals
- Document decisions

**Moderation Workflow:**
1. Tool flags high-score thread
2. Manual review of context
3. Check user histories
4. Make informed decision
        """)

    with col2:
        st.markdown("""
### 👥 General Users

**Applications:**
- Think critically
- Verify consensus
- Understand manipulation
- Make informed decisions

**Best Practices:**
- Don't assume all bots
- Consider alternatives
- Read full rationale
- Stay skeptical

**Mental Model:**
- High score = "worth investigating"
- Not "definitely fake"
- Context always matters
        """)

    st.markdown("---")
    st.markdown("### 📊 Case Study Examples")

    with st.expander("Example 1: Breaking News (False Positive)"):
        st.markdown("""
**Thread**: Major political announcement
**Score**: 58/100 (Likely Coordinated)
**Reality**: Organic response

**Why high score?**
- Natural burst as users react
- Similar emotional responses
- Shared factual information

**Distinguishing features:**
- Genuine emotion in comments
- Diverse user histories
- Discussion evolves over time

**Lesson**: Breaking news creates coordination patterns
        """)

    with st.expander("Example 2: Astroturfing Campaign (True Positive)"):
        st.markdown("""
**Thread**: Product/policy endorsement
**Score**: 81/100 (Highly Coordinated)
**Reality**: Confirmed astroturfing

**Signals:**
- 58% of comments in tight cluster
- Template: "As a [identity], I support [thing]"
- 4 posting bursts within hour
- 22/34 accounts created same month

**Outcome**: Campaign verified through external investigation

**Lesson**: Multiple strong signals = high confidence
        """)

    with st.expander("Example 3: Legitimate Activism (Nuanced Case)"):
        st.markdown("""
**Thread**: Call to action for policy
**Score**: 56/100 (Likely Coordinated)
**Reality**: Genuine activism

**Why high score?**
- Organized messaging (by design)
- Shared talking points
- Coordinated timing

**Why legitimate?**
- Transparent about organization
- Links to real advocacy group
- Established accounts
- Diverse engagement history

**Lesson**: High scores can flag legitimate organization
        """)
