# Methodology

## Overview

ConsensusWatch detects synthetic consensus through a multi-layered analysis combining:

1. **Semantic Analysis**: Detecting coordinated messaging via text embeddings
2. **Temporal Analysis**: Identifying suspicious timing patterns
3. **Network Analysis**: Mapping user-comment coordination graphs
4. **Behavioral Analysis**: Finding anomalous patterns in posting behavior

These signals combine to produce a **Synthetic Consensus Score** (0-100) and human-readable explanation.

---

## 1. Data Ingestion

### Reddit API Collection
- Uses PRAW (Python Reddit API Wrapper) to fetch thread/subreddit data
- Collects: comment text, author, timestamp, score, parent/child relationships
- Normalizes text: lowercasing, removing URLs, handling markdown

### Data Structure
```python
{
  "thread_id": "abc123",
  "comments": [
    {
      "id": "def456",
      "author": "user1",
      "text": "normalized comment text...",
      "created_utc": 1234567890,
      "score": 42,
      "parent_id": None
    },
    ...
  ]
}
```

---

## 2. Semantic Similarity Analysis

### Text Embeddings
- Uses sentence transformers (default: `all-MiniLM-L6-v2`)
- Converts each comment to a 384-dimensional vector
- Embeddings cached to avoid recomputation

### Similarity Matrix
- Computes pairwise cosine similarity between all comments
- Identifies unusually high similarity clusters
- Filters out trivial agreement (e.g., "yes", "agreed")

### Red Flags
- **High similarity**: Large groups with >85% similarity
- **Template usage**: Many comments matching a single template
- **Paraphrasing**: Semantically identical but superficially different

**Example:**
```
Comment A: "This policy will destroy the economy and hurt families"
Comment B: "The proposed policy would devastate our economy and harm families"
Similarity: 0.92 (suspicious)
```

---

## 3. Clustering Analysis

### HDBSCAN Clustering
- Groups semantically similar comments into clusters
- Identifies coordination based on cluster density and size
- Parameters: `min_cluster_size=5`, `min_samples=3`

### UMAP Dimensionality Reduction
- Reduces embeddings to 2D for visualization
- Helps identify distinct narrative clusters
- Reveals coordination patterns invisible in high-dimensional space

### Metrics
- **Cluster homogeneity**: How tight are clusters?
- **Cluster separation**: Are clusters distinct?
- **Outliers**: How many comments don't fit any cluster?

---

## 4. Temporal Analysis

### Burst Detection
- Identifies abnormal posting rate spikes
- Sliding window analysis (default: 15-minute windows)
- Flags coordinated "bursts" of similar content

### Timing Patterns
- Analyzes inter-comment intervals
- Detects automated/scripted patterns (e.g., exactly 60-second gaps)
- Identifies coordinated posting waves

### Metrics
- **Burst coefficient**: Ratio of peak rate to baseline
- **Timing entropy**: Randomness of posting times
- **Wave detection**: Multiple coordinated bursts

**Example:**
```
Normal: Comments arrive at irregular intervals (high entropy)
Suspicious: 20 similar comments posted within 3 minutes (low entropy, high burst)
```

---

## 5. Network Graph Analysis

### User-Comment Graph
- Nodes: Users and comments
- Edges: User posts comment, comment replies to comment
- Analyzes community structure and coordination

### Metrics
- **Clustering coefficient**: How interconnected are users?
- **Component analysis**: Isolated subgraphs of coordinated users
- **Centrality**: Key accounts driving coordination

### Pattern Detection
- **Sockpuppet networks**: Single user with multiple accounts
- **Coordinated brigading**: External group targeting thread
- **Astroturfing**: Fake grassroots consensus

---

## 6. Synthetic Consensus Score

### Components (weighted average)

1. **Semantic Score (35%)**
   - Based on similarity clustering and template usage
   - 0 = diverse opinions, 100 = identical messaging

2. **Temporal Score (25%)**
   - Based on burst detection and timing patterns
   - 0 = organic timing, 100 = synchronized posting

3. **Network Score (25%)**
   - Based on graph analysis and community structure
   - 0 = organic interactions, 100 = coordinated network

4. **Behavioral Score (15%)**
   - Account age, karma, posting history patterns
   - 0 = established users, 100 = suspicious accounts

### Final Score Calculation
```python
final_score = (
    0.35 * semantic_score +
    0.25 * temporal_score +
    0.25 * network_score +
    0.15 * behavioral_score
)
```

### Score Interpretation
- **0-25**: Likely organic consensus
- **25-50**: Some coordination signals, investigate further
- **50-75**: Likely coordinated behavior
- **75-100**: Highly coordinated / synthetic consensus

---

## 7. Explainability

### Human-Readable Rationale
Every score includes:
- **Primary signals**: Top reasons for the score
- **Evidence**: Specific examples (clusters, timing patterns)
- **Confidence**: How certain is the assessment?
- **Caveats**: Alternative explanations

### Example Output
```
Score: 72/100 (Likely Coordinated)

Primary Signals:
• High semantic similarity: 45 comments (23% of thread) form tight cluster
• Temporal burst: 38 similar comments posted within 12 minutes
• Network pattern: 15 accounts with minimal Reddit history, all joined this month

Evidence:
• Cluster example: "This is terrible for small businesses" (repeated 12x with minor variations)
• Posting burst: 3:45 PM - 3:57 PM (31 comments, 2.6/min vs. baseline 0.4/min)

Confidence: High (multiple strong signals)

Caveats:
• Could be organic response to breaking news
• Some accounts may be genuine new users
```

---

## 8. Validation

### Ground Truth Datasets
- Known bot campaigns (e.g., Russian IRA accounts)
- Confirmed organic threads (from trusted communities)
- Adversarial testing (can we fool the system?)

### Metrics
- **Precision**: What % of flagged threads are actually coordinated?
- **Recall**: What % of coordinated threads do we catch?
- **F1 Score**: Harmonic mean of precision and recall

### Continuous Improvement
- Community feedback on false positives/negatives
- Regular model retraining
- A/B testing of detection parameters

---

## Limitations

See [limitations.md](limitations.md) for full discussion.

Key constraints:
- Probabilistic, not definitive
- May miss sophisticated campaigns
- Language-dependent (optimized for English)
- Requires sufficient comment volume (n>20)

---

## References

- [Sentence Transformers](https://arxiv.org/abs/1908.10084)
- [HDBSCAN Clustering](https://arxiv.org/abs/1911.02282)
- [Graph-based Bot Detection](https://arxiv.org/abs/2006.08808)
- [Coordinated Inauthentic Behavior](https://carnegieendowment.org/research/2020/09/coordinated-inauthentic-behavior-explained)
