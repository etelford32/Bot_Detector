# 🤖 ConsensusWatch (Bot Detector MVP)

**Detects synthetic consensus and coordinated narrative steering in Reddit threads.**

## 🎯 What It Does

Given a Reddit thread or subreddit over a time window, ConsensusWatch outputs a **Synthetic Consensus Score** and human-readable explanation indicating whether the apparent consensus is organic or potentially coordinated.

## 🚀 Features

- **Real-time Reddit Analysis**: Fetch and analyze threads using PRAW
- **Semantic Similarity Detection**: Uses sentence transformers to identify coordinated messaging
- **Temporal Pattern Analysis**: Detects suspicious timing and burst patterns
- **Graph-based Coordination Detection**: Identifies clusters of accounts with coordinated behavior
- **Explainable Results**: Human-readable rationales for detection decisions
- **Multiple Interfaces**: CLI, REST API, and comprehensive web dashboard
- **Interactive Visualizations**: Rich graphs and charts for analysis results
- **Batch Analysis**: Analyze multiple threads across subreddits

## 📊 Synthetic Consensus Index

The system calculates a **Synthetic Consensus Score (0-100)** based on:

1. **Semantic Similarity**: Unusually high similarity between comments
2. **Temporal Clustering**: Coordinated posting patterns and timing bursts
3. **User-Comment Graphs**: Network analysis of user interactions
4. **Language Patterns**: Repetitive phrasing and template usage

See [docs/synthetic_consensus_index.md](docs/synthetic_consensus_index.md) for methodology.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/consensuswatch.git
cd consensuswatch

# Install dependencies
pip install -r requirements.txt

# Or install with pip
pip install -e .
```

## ⚙️ Configuration

Create a `.env` file with your Reddit API credentials:

```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=ConsensusWatch/0.1.0
```

[Get Reddit API credentials here](https://www.reddit.com/prefs/apps)

## 🎮 Usage

### CLI

```bash
# Analyze a specific thread
consensuswatch analyze --url "https://www.reddit.com/r/worldnews/comments/..."

# Analyze a subreddit over time
consensuswatch analyze --subreddit worldnews --hours 24

# With detailed output
consensuswatch analyze --url "..." --verbose --output report.json
```

### Python API

```python
from ingestion.thread_fetcher import fetch_thread
from analysis.consensus_score import calculate_consensus_score
from explainability.rationale import generate_rationale

# Fetch thread data
thread_data = fetch_thread("https://www.reddit.com/r/...")

# Calculate consensus score
score, metrics = calculate_consensus_score(thread_data)

# Get explanation
explanation = generate_rationale(score, metrics)

print(f"Synthetic Consensus Score: {score}/100")
print(f"Analysis: {explanation}")
```

### REST API

```bash
# Start the API server
uvicorn api.main:app --reload

# Analyze a thread
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.reddit.com/r/..."}'
```

### Web Dashboard

```bash
# Launch comprehensive web interface
streamlit run dashboard/app_new.py

# Or use the original simple dashboard
streamlit run dashboard/app.py
```

**Features:**
- 🏠 **Home**: Interactive introduction and feature showcase
- 🔍 **Analyze Thread**: Single thread analysis with comprehensive visualizations
- 📊 **Batch Analysis**: Analyze multiple threads from a subreddit
- 📚 **Documentation**: Complete methodology and usage guide
- ℹ️ **About**: Project information and ethics

**Visualizations Include:**
- Score gauge with risk levels
- Component score breakdowns (bar & radar charts)
- Similarity heatmaps
- Temporal burst detection graphs
- Network interaction graphs
- Cluster visualizations (2D projections)
- Metrics comparison tables

## 📁 Project Structure

```
consensuswatch/
├── ingestion/          # Reddit data fetching & normalization
├── embeddings/         # Text embedding & caching
├── analysis/           # Core detection algorithms
├── explainability/     # Human-readable explanations
├── api/                # FastAPI REST endpoints
├── dashboard/          # Streamlit web interface
├── cli/                # Command-line tool
├── tests/              # Unit tests
└── docs/               # Documentation
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_consensus_score.py
```

## 📖 Documentation

- [Vision & Motivation](docs/vision.md)
- [Methodology](docs/methodology.md)
- [Synthetic Consensus Index](docs/synthetic_consensus_index.md)
- [Limitations & Ethics](docs/limitations.md)

## 🔬 Example Case Studies

- [r/worldnews Analysis](examples/worldnews_case_study.md)
- [r/politics Analysis](examples/politics_case_study.md)

## ⚠️ Limitations

- **False positives**: Genuine grassroots movements may appear coordinated
- **Language support**: Currently optimized for English
- **API limits**: Reddit API rate limiting applies
- **Not definitive proof**: Results are probabilistic indicators, not proof

See [docs/limitations.md](docs/limitations.md) for full discussion.

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines and submit PRs.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [PRAW](https://praw.readthedocs.io/) - Reddit API wrapper
- [Sentence Transformers](https://www.sbert.net/) - Semantic embeddings
- [HDBSCAN](https://hdbscan.readthedocs.io/) - Clustering
- [FastAPI](https://fastapi.tiangolo.com/) - REST API
- [Streamlit](https://streamlit.io/) - Dashboard

## ⚖️ Ethics & Responsible Use

This tool is designed for research and transparency. Users should:
- Respect Reddit's Terms of Service
- Not harass or dox suspected bot accounts
- Consider context and avoid false accusations
- Use findings to improve platform health, not witch hunts

---

**Status**: MVP - Active Development

**Version**: 0.1.0
