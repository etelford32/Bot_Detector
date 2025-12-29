"""Main application with navigation and page routing."""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="ConsensusWatch - Bot Detector",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
def load_css():
    """Load custom CSS styling."""
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #FF4B4B;
            --secondary-color: #0E1117;
            --background-color: #FFFFFF;
            --text-color: #262730;
        }

        /* Header styling */
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 1rem;
            padding: 1rem;
        }

        .sub-header {
            font-size: 1.5rem;
            color: var(--text-color);
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Card styling */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
        }

        .warning-card {
            background: #FFF3CD;
            border-left: 5px solid #FFC107;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }

        .success-card {
            background: #D4EDDA;
            border-left: 5px solid #28A745;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }

        .danger-card {
            background: #F8D7DA;
            border-left: 5px solid #DC3545;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }

        /* Navigation styling */
        .nav-link {
            font-size: 1.1rem;
            padding: 0.5rem 1rem;
            margin: 0.25rem 0;
            border-radius: 5px;
            cursor: pointer;
        }

        /* Score badge */
        .score-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.2rem;
        }

        .score-low {
            background: #28A745;
            color: white;
        }

        .score-medium {
            background: #FFC107;
            color: black;
        }

        .score-high {
            background: #DC3545;
            color: white;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            border-top: 1px solid #ddd;
            margin-top: 3rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def show_navigation():
    """Show sidebar navigation."""
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/FF4B4B/FFFFFF?text=ConsensusWatch",
                 use_container_width=True)

        st.markdown("## 🧭 Navigation")

        # Navigation menu
        page = st.radio(
            "Go to:",
            ["🏠 Home", "🔍 Analyze Thread", "📊 Batch Analysis", "📚 Documentation", "ℹ️ About"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Quick stats
        st.markdown("### 📈 Quick Info")
        st.metric("Version", "0.1.0")
        st.metric("Status", "Active")

        st.markdown("---")

        # Resources
        st.markdown("### 🔗 Resources")
        st.markdown("[📖 Methodology]()")
        st.markdown("[🔬 Research]()")
        st.markdown("[💻 GitHub]()")
        st.markdown("[📧 Contact]()")

        st.markdown("---")

        # Settings
        with st.expander("⚙️ Settings"):
            st.checkbox("Use embedding cache", value=True, key="use_cache")
            st.checkbox("Show raw metrics", value=False, key="show_raw")
            st.selectbox("Theme", ["Light", "Dark"], key="theme")

    return page


def main():
    """Main application entry point."""
    # Load custom CSS
    load_css()

    # Show navigation and get selected page
    page = show_navigation()

    # Route to appropriate page
    if page == "🏠 Home":
        from dashboard.pages import home
        home.show()
    elif page == "🔍 Analyze Thread":
        from dashboard.pages import analyze
        analyze.show()
    elif page == "📊 Batch Analysis":
        from dashboard.pages import batch_analyze
        batch_analyze.show()
    elif page == "📚 Documentation":
        from dashboard.pages import documentation
        documentation.show()
    elif page == "ℹ️ About":
        from dashboard.pages import about
        about.show()

    # Footer
    st.markdown("---")
    st.markdown("""
        <div class="footer">
            <p>🤖 <strong>ConsensusWatch v0.1.0</strong> - Detect synthetic consensus in Reddit threads</p>
            <p>Built with ❤️ using Streamlit | <a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
