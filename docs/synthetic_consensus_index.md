# Synthetic Consensus Index

## Definition

The **Synthetic Consensus Index (SCI)** is a 0-100 score indicating the likelihood that apparent consensus in a Reddit thread is artificially coordinated rather than organic.

**Score = 0**: Consensus appears entirely organic
**Score = 100**: Consensus appears entirely synthetic/coordinated

---

## Score Components

### 1. Semantic Similarity Score (35% weight)

Measures how similar comments are in meaning, even if worded differently.

#### Calculation
```python
# Compute pairwise cosine similarity of embeddings
similarity_matrix = cosine_similarity(embeddings)

# Find high-similarity pairs (> threshold)
high_sim_pairs = similarity_matrix > 0.85

# Calculate metrics
cluster_sizes = hdbscan_clustering(embeddings)
template_matches = detect_template_usage(comments)

semantic_score = weighted_average([
    cluster_homogeneity,      # 40%
    avg_intra_cluster_sim,    # 30%
    template_usage_rate,      # 20%
    vocabulary_diversity,     # 10%
])
```

#### Red Flags (increases score)
- Large clusters (>10% of comments) with >85% similarity
- Template matching (multiple comments fit same pattern)
- Low vocabulary diversity (everyone uses same phrases)
- Unnatural uniformity (no dissent or variation)

#### Green Flags (decreases score)
- High diversity of opinions and phrasings
- Natural disagreement and debate
- Rich vocabulary variation
- Independent reasoning patterns

#### Example
**Organic (Score: 15)**
```
"I think this policy is misguided"
"Strongly disagree - it's necessary"
"Mixed feelings, but leaning against it"
"Here's why I support it: [detailed reasoning]"
```

**Coordinated (Score: 92)**
```
"This policy will destroy small businesses"
"The proposed policy would devastate small businesses"
"Small businesses will be destroyed by this policy"
"This will completely destroy our small business owners"
```

---

### 2. Temporal Clustering Score (25% weight)

Measures whether comments arrive in suspicious timing patterns.

#### Calculation
```python
# Analyze posting rate over time
time_windows = sliding_window(timestamps, window_size=15_min)
posting_rates = [len(window) for window in time_windows]

# Detect bursts
baseline_rate = median(posting_rates)
peak_rate = max(posting_rates)
burst_coefficient = peak_rate / baseline_rate

# Timing entropy
intervals = diff(sorted(timestamps))
timing_entropy = shannon_entropy(intervals)

temporal_score = weighted_average([
    burst_coefficient,        # 50%
    timing_entropy_inverse,   # 30%
    wave_detection,           # 20%
])
```

#### Red Flags
- Sudden bursts (10x normal rate)
- Regular intervals (automated posting)
- Multiple coordinated waves
- Suspicious synchronization (many comments within seconds)

#### Green Flags
- Steady, organic rate
- High timing entropy (random intervals)
- No unusual bursts
- Natural conversation flow

#### Example
**Organic (Score: 10)**
```
00:00 - comment
00:03 - comment
00:07 - comment
00:08 - comment
00:15 - comment
... irregular, natural timing
```

**Coordinated (Score: 88)**
```
14:00 - 0 comments
14:30 - 0 comments
15:00 - 28 comments (within 3 minutes!)
15:03 - 0 comments
15:30 - 0 comments
... obvious burst pattern
```

---

### 3. Network Coordination Score (25% weight)

Analyzes graph structure of user interactions.

#### Calculation
```python
# Build graph
G = networkx.Graph()
G.add_nodes_from(users)
G.add_nodes_from(comments)
G.add_edges_from(user_posts_comment)
G.add_edges_from(comment_replies_to_comment)

# Analyze structure
components = connected_components(G)
clustering_coef = clustering_coefficient(G)
modularity = community_modularity(G)

network_score = weighted_average([
    isolated_component_size,  # 40%
    clustering_coefficient,   # 30%
    modularity_inverse,       # 20%
    centrality_concentration, # 10%
])
```

#### Red Flags
- Isolated subgraphs (coordinated group doesn't interact with others)
- High clustering (users only interact within group)
- Low modularity (unnatural community structure)
- Centralized control (few accounts dominate)

#### Green Flags
- Integrated community structure
- Natural interaction patterns
- Healthy debate across groups
- Distributed participation

#### Example
**Organic**: Users interact across opinion lines, reply to each other, debate
**Coordinated**: Cluster of accounts only reply to each other, ignore dissent

---

### 4. Behavioral Anomaly Score (15% weight)

Examines account-level patterns.

#### Calculation
```python
# Analyze accounts
account_ages = [user.created_utc for user in users]
karma_scores = [user.karma for user in users]
posting_patterns = analyze_history(users)

behavioral_score = weighted_average([
    new_account_ratio,        # 35%
    low_karma_ratio,          # 25%
    single_issue_accounts,    # 25%
    suspicious_names,         # 15%
])
```

#### Red Flags
- High % of new accounts (created recently)
- Low karma (minimal history)
- Single-issue accounts (only post on one topic)
- Suspicious naming patterns (e.g., Word-Word-1234)

#### Green Flags
- Established accounts with history
- Diverse posting patterns
- Natural karma distribution
- Organic usernames

---

## Final Score Calculation

```python
WEIGHTS = {
    'semantic': 0.35,
    'temporal': 0.25,
    'network': 0.25,
    'behavioral': 0.15,
}

final_score = (
    WEIGHTS['semantic'] * semantic_score +
    WEIGHTS['temporal'] * temporal_score +
    WEIGHTS['network'] * network_score +
    WEIGHTS['behavioral'] * behavioral_score
)
```

---

## Score Interpretation

### 0-25: Likely Organic
**Interpretation**: Consensus appears genuine and grassroots.

**Confidence**: High if score < 15, Medium if 15-25

**Action**: No concerns, typical thread

**Example**: Popular post with diverse opinions and natural discussion

---

### 25-50: Possible Coordination
**Interpretation**: Some signals of coordination, but could be organic.

**Confidence**: Low to Medium

**Action**: Investigate further, monitor for escalation

**Example**: Breaking news causing natural coordinated response, OR small-scale manipulation

---

### 50-75: Likely Coordinated
**Interpretation**: Multiple strong signals of artificial coordination.

**Confidence**: Medium to High

**Action**: Likely manipulation, recommend further investigation

**Example**: Organized brigade, coordinated campaign, or bot network

---

### 75-100: Highly Coordinated
**Interpretation**: Overwhelming evidence of synthetic consensus.

**Confidence**: Very High

**Action**: Almost certainly manipulation, flag for removal/investigation

**Example**: Large-scale bot campaign, state-sponsored manipulation, professional astroturfing

---

## Confidence Levels

The system also outputs a **Confidence Score** based on:

- **Signal strength**: How strong are the indicators?
- **Signal agreement**: Do multiple indicators point the same direction?
- **Sample size**: Enough comments for statistical significance?
- **Edge cases**: Any mitigating factors?

**High Confidence**: Multiple strong signals, clear pattern
**Medium Confidence**: Mixed signals or limited data
**Low Confidence**: Ambiguous or insufficient evidence

---

## Calibration & Validation

### Known Coordinated Campaigns
Tested against confirmed manipulation:
- Russian IRA accounts (2016-2018)
- Commercial astroturfing campaigns
- Political brigades

**Target**: 90%+ detection rate (recall) on known cases

### Known Organic Threads
Tested against verified authentic discussions:
- r/AskHistorians high-quality threads
- Small community discussions
- Live event threads (sports, breaking news)

**Target**: <10% false positive rate (precision)

### Adversarial Testing
Can we fool the system?
- Paraphrasing attacks
- Slow-drip campaigns
- Mixed organic/synthetic

**Goal**: Continuously improve against adversarial tactics

---

## Limitations

1. **Not definitive proof**: Probabilistic indicator only
2. **False positives**: Genuine grassroots movements may score high
3. **Sophistication matters**: Advanced campaigns may evade detection
4. **Context-dependent**: Breaking news may naturally create coordination patterns
5. **Language-specific**: Optimized for English
6. **Volume-dependent**: Requires sufficient comments (n>20)

See [limitations.md](limitations.md) for full discussion.

---

## Updates & Evolution

This scoring system will evolve based on:
- Community feedback
- New manipulation tactics
- Academic research
- Platform changes
- Adversarial testing

**Current Version**: 0.1.0 (MVP)
**Last Updated**: 2025
