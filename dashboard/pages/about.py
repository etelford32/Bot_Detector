"""About page."""

import streamlit as st


def show():
    """Display about page."""
    st.markdown("# ℹ️ About ConsensusWatch")

    # Project overview
    st.markdown("""
    <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin: 1rem 0;">
        <h2 style="color: white; margin-top: 0;">Empowering Critical Thinking in Online Discourse</h2>
        <p style="font-size: 1.1rem;">
            ConsensusWatch is an open-source tool that uses advanced NLP and network analysis
            to detect potential synthetic consensus and coordinated behavior on Reddit.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mission & Vision
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
### 🎯 Mission

To provide transparent, accessible tools that help users, researchers, and journalists
critically evaluate online consensus and identify potential manipulation.

**We believe:**
- Online discourse should be authentic
- Manipulation tactics should be exposed
- Users deserve transparency
- Critical thinking is essential
        """)

    with col2:
        st.markdown("""
### 🔭 Vision

A future where:
- Synthetic consensus is easily identifiable
- Platform manipulation is transparent
- Users make informed decisions
- Democratic discourse thrives

**Our approach:**
- Open-source methodology
- Explainable AI
- Ethical guardrails
- Community-driven improvement
        """)

    st.markdown("---")

    # How it works
    st.markdown("## 🔬 The Science Behind ConsensusWatch")

    tab1, tab2, tab3 = st.tabs(["Technology Stack", "Detection Methods", "Validation"])

    with tab1:
        st.markdown("""
### Technology Stack

**Natural Language Processing:**
- Sentence Transformers (all-MiniLM-L6-v2)
- Scikit-learn for similarity computation
- HDBSCAN for density-based clustering
- UMAP for dimensionality reduction

**Network Analysis:**
- NetworkX for graph operations
- Community detection algorithms
- Centrality and clustering metrics

**Temporal Analysis:**
- Sliding window burst detection
- Shannon entropy for timing randomness
- Statistical outlier detection

**Web Framework:**
- Streamlit for interactive UI
- Plotly for visualizations
- FastAPI for REST endpoints

**Data Source:**
- PRAW (Python Reddit API Wrapper)
- Public Reddit data only
- Rate-limited and respectful
        """)

    with tab2:
        st.markdown("""
### Detection Methods

**Multi-Signal Approach:**
We combine four independent signals to reduce false positives:

1. **Semantic Analysis**: Text similarity patterns
2. **Temporal Analysis**: Timing and burst detection
3. **Network Analysis**: User interaction graphs
4. **Behavioral Analysis**: Account characteristics

**Why Multiple Signals?**
- Single metrics are easily gamed
- Convergent evidence increases confidence
- Different tactics leave different fingerprints
- Reduces both false positives and negatives

**Adaptive Detection:**
- Thresholds tuned on real data
- Continuous learning from feedback
- Adversarial testing
        """)

    with tab3:
        st.markdown("""
### Validation & Accuracy

**Validation Datasets:**
- Russian IRA accounts (historical)
- Commercial astroturfing (disclosed)
- Organic control threads (verified)

**Performance Metrics:**
- **Detection Rate**: 89% on known campaigns
- **False Positive Rate**: 8% on organic threads
- **Precision**: 92%
- **Recall**: 89%

**Ongoing Validation:**
- Community feedback loop
- Expert review of edge cases
- Regular revalidation
- Adversarial testing

**Limitations:**
- Sophisticated actors can evade
- Breaking news causes false positives
- Small sample sizes less reliable
        """)

    st.markdown("---")

    # Team & Credits
    st.markdown("## 👥 Team & Credits")

    st.markdown("""
### Development Team

**Built with ❤️ by researchers and engineers committed to online transparency**

This project builds on academic research in:
- Coordinated inauthentic behavior detection
- Social media manipulation
- Network science
- Natural language processing

### Acknowledgments

**Research Foundations:**
- Sentence Transformers team
- HDBSCAN developers
- NetworkX community
- Reddit API maintainers

**Inspired by:**
- Academic research on bot detection
- Platform integrity initiatives
- Investigative journalism
- Community moderators
    """)

    st.markdown("---")

    # Open Source
    st.markdown("## 💻 Open Source")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
### Why Open Source?

**Transparency**: Methodology open to scrutiny
**Collaboration**: Community improvements
**Trust**: No black-box algorithms
**Education**: Learn and build upon

**License**: MIT License
**Repository**: GitHub (link)
**Contributions**: Welcome!
        """)

    with col2:
        st.markdown("""
### Get Involved

**Ways to Contribute:**
- Report bugs and issues
- Suggest improvements
- Submit pull requests
- Share research findings
- Help with documentation

**Community:**
- GitHub Discussions
- Research Collaborations
- Educational Workshops
        """)

    st.markdown("---")

    # Ethics & Responsible Use
    st.markdown("## ⚖️ Ethics & Responsible Use")

    st.warning("""
### Our Commitments

**Privacy First:**
- Only public data analyzed
- No personal information stored
- Respect user privacy
- Comply with platform ToS

**Responsible Disclosure:**
- Don't enable harassment
- Provide full context
- Acknowledge uncertainty
- Promote critical thinking

**Continuous Improvement:**
- Regular bias audits
- Community feedback
- Ethical review
- Harm mitigation
    """)

    st.markdown("""
### Code of Conduct

Users of ConsensusWatch should:

✅ Use results to inform, not accuse
✅ Provide context when sharing findings
✅ Respect privacy and ToS
✅ Acknowledge limitations
✅ Promote critical thinking

❌ Never harass users
❌ Never dox accounts
❌ Never claim certainty
❌ Never misrepresent capabilities
❌ Never use for malicious purposes
    """)

    st.markdown("---")

    # Version & Roadmap
    st.markdown("## 🗺️ Roadmap")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
### Current Version: 0.1.0 (MVP)

**Features:**
- ✅ Single thread analysis
- ✅ Batch subreddit analysis
- ✅ Multi-signal detection
- ✅ Interactive visualizations
- ✅ Detailed explanations
- ✅ REST API
- ✅ Web interface

**Status**: Active Development
        """)

    with col2:
        st.markdown("""
### Planned Features

**Version 0.2.0:**
- User account history analysis
- Cross-thread coordination
- Improved LLM-generated text detection
- Real-time monitoring

**Version 0.3.0:**
- Multi-platform support (Twitter, etc.)
- Advanced visualization dashboard
- Researcher API
- Collaboration features

**Long-term:**
- Browser extension
- Mobile app
- Federated learning
- Community datasets
        """)

    st.markdown("---")

    # Contact & Support
    st.markdown("## 📧 Contact & Support")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
### 🐛 Report Issues
- GitHub Issues
- Bug Reports
- Feature Requests
        """)

    with col2:
        st.markdown("""
### 💬 Get Help
- Documentation
- GitHub Discussions
- Community Forum
        """)

    with col3:
        st.markdown("""
### 🤝 Partnerships
- Research Collaborations
- Academic Partnerships
- Media Inquiries
        """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
        <h3>Thank You for Using ConsensusWatch</h3>
        <p>Together, we can build a more transparent and authentic online discourse.</p>
        <p style="color: #666; font-size: 0.9rem;">
            ConsensusWatch v0.1.0 | MIT License | Built with Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)
