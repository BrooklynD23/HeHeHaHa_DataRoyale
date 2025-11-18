# Winning Team Analysis & Reverse Engineering Plan

**Date**: November 18, 2025
**Purpose**: Comprehensive audit of current work vs winning team's approach
**Competition**: Cal Poly Pomona DataRoyale (Post-competition analysis for learning)

---

## Executive Summary

The winning team achieved 1st place by **fundamentally reframing the problem** from a game-centric analysis to a **player behavioral and retention strategy**. While your team focused on deck composition and battle outcomes (achieving solid technical work), the winners focused on player psychology, churn prediction, and business metrics.

**Key Paradigm Shift**:
- **Your Approach**: "What deck composition wins battles?"
- **Winning Approach**: "What player behaviors predict retention and churn?"

---

## Part 1: Repository Audit - Current State

### ✅ What You Built (Strengths)

#### 1. **Solid Technical Infrastructure**
- ✅ DuckDB integration for handling 9.2GB CSV without memory issues
- ✅ Modular code structure (`src/` utilities, reusable functions)
- ✅ 8 Jupyter notebooks with clear workflow progression
- ✅ Google Colab compatibility
- ✅ Comprehensive documentation (CLAUDE.md, README.md, implementation guides)

#### 2. **Complete Game-Centric Analysis**

**Notebook 01: Data Profiling**
- Data quality assessment
- Missing value analysis
- Outlier detection

**Notebook 02: Battle Metadata Analysis**
- Arena distribution
- Trophy range patterns
- Game mode analysis

**Notebook 03: Card Analysis** (Most complete)
- ✅ Global card win rates (100+ cards analyzed)
- ✅ 2-card synergy analysis with lift metrics
- ✅ Trophy-bracket card win rates (8 brackets)
- ✅ Deck archetype clustering (Beatdown, Cycle, Control, etc.)
- ✅ Elixir cost optimization
- 🔄 Trophy-bracket synergy (partially done)

**Notebook 04: Player Progression**
- ✅ Trophy distribution and wall detection (4k, 5k, 6k, 7k)
- ✅ Trophy change patterns by bracket
- ✅ Deck evolution analysis
- ✅ Matchup fairness (underdog wins)

**Notebook 04.5: Advanced Meta Analysis** (25% complete)
- ✅ Data-driven trophy wall detection algorithm
- ✅ Optimal elixir cost with Wilson confidence intervals
- ⏳ 8+ pending advanced analyses

**Notebook 05: Feature Engineering**
- ✅ Matchup features (trophy_diff, elixir_diff, card_level_diff)
- ✅ Archetype indicators (spell-heavy, beatdown, cycle)
- ✅ Trophy bracket categorization
- ✅ Tower damage features (crown_diff, close_game)

**Notebook 06: Modeling**
- ✅ 3 ML models (Logistic Regression, Random Forest, XGBoost)
- ✅ Proper train/test split with stratification
- ✅ Feature importance analysis
- ✅ Model comparison against 56.94% benchmark
- ✅ Expected accuracy: 52-60%

**Notebook 07: Visualization Library**
- ✅ Presentation-ready charts (300 DPI, colorblind-friendly)
- ✅ Top cards by win rate
- ✅ Trophy distribution
- ✅ Deck evolution
- ✅ Model comparison

#### 3. **Key Insights Generated**
1. **Card Balance**: ~10 cards exceed 52% win rate (potential balance issues)
2. **Trophy Walls**: Clear clustering at 4k, 5k, 6k, 7k milestones
3. **Meta Shift**: Top cards change significantly across trophy brackets
4. **Deck Evolution**: Higher skill = more elixir, legendaries, spells
5. **Synergy Patterns**: 5,151 card pairs with >500 usage show clear synergy

### ⚠️ What Was Missing (Gaps Identified)

#### 1. **Analytical Approach**
- ❌ **Game-centric vs Player-centric**: Analyzed battles, not players
- ❌ **No temporal analysis**: Didn't track individual player journeys over time
- ❌ **No behavioral metrics**: No engagement, return rate, or churn analysis
- ❌ **No retention focus**: Focused on "winning" not "staying engaged"

#### 2. **Feature Engineering**
- ❌ **No player-level aggregation**: Each battle treated independently
- ❌ **No temporal features**: No next_battleTime, return gaps, session analysis
- ❌ **No streak tracking**: No loss streaks, win streaks, momentum
- ❌ **No behavioral tilt**: No emotional response metrics
- ❌ **No engagement metrics**: No match frequency, play patterns

#### 3. **Data Structure**
- ❌ **Battle-centric format**: Didn't restructure to player-centric
- ❌ **No player timelines**: Didn't order battles chronologically per player
- ❌ **No player profiling**: Didn't segment players by engagement level

#### 4. **Modeling Approach**
- ❌ **Wrong prediction target**: Predicted battle outcomes (52-60% accuracy)
- ✅ **Should have predicted**: Player churn/retention (90% accuracy achievable!)
- ❌ **No stratified player sampling**: Random sampling, not player-based
- ❌ **No calibration analysis**: Missing from notebook 06

#### 5. **Deliverable Format**
- ❌ **Static presentation**: PowerPoint/Google Slides only
- ❌ **No interactive dashboard**: Missed the Streamlit opportunity
- ❌ **No player profiles**: No comparative case studies

#### 6. **Business Framing**
- ❌ **Competitive focus**: "What wins?" instead of "What retains?"
- ❌ **No business recommendations**: No monetization, retention strategies
- ❌ **Game balance focus**: Developer perspective, not business perspective

---

## Part 2: Winning Team Deep Dive

### 🏆 What Made Them Win

#### 1. **Paradigm Reframe: From Game to Business**

**Your Question**: "What deck composition wins battles?"
**Their Question**: "What player behaviors predict churn and retention?"

**Impact**:
- More relevant to real-world business decisions
- Higher predictive accuracy (90% vs 52-60%)
- More actionable recommendations
- Stronger storytelling (player psychology is engaging)

#### 2. **Player-Centric Data Transformation**

**Process**:
```
Raw Data (16.9M battles)
    ↓
Group by player tag
    ↓
Sort by battleTime (chronological)
    ↓
Calculate temporal features
    ↓
Player-level dataset (N players × engineered features)
```

**Key Features Engineered**:

| Feature | Description | Example Values |
|---------|-------------|----------------|
| `next_battleTime` | Timestamp of next battle | datetime |
| `return_gap` | Time between battles | 5 min, 2 hrs, 3 days |
| `fast_return_1hr` | Returned within 1 hour | True/False |
| `loss_streak` | Consecutive losses | 0, 1, 2, 3, ..., 10+ |
| `loss_streak_bucket` | Categorized streaks | "0", "1-2", "3-5", "6-10", "10+" |
| `win_rate` | Player's overall win % | 45%, 52%, 68% |
| `match_count` | Total battles played | 10, 28, 150 |
| `trophy_momentum` | Trophy change trend | +120, -45, +5 |
| `behavioral_tilt` | Fast return after loss | Binary or continuous |

#### 3. **Behavioral Tilt Metric (Their Secret Weapon)**

**Definition**: Measures whether players return quickly after losing (emotional/tilted) vs stopping play (discouraged)

**Calculation** (inferred):
```python
def calculate_behavioral_tilt(player_battles):
    """
    For each loss, check if player returned within 1 hour
    Aggregate to get tilt score per player
    """
    tilt_events = 0
    total_losses = 0

    for i, battle in enumerate(player_battles[:-1]):  # Exclude last battle
        if battle['outcome'] == 'loss':
            total_losses += 1
            next_battle = player_battles[i + 1]
            time_gap = next_battle['battleTime'] - battle['battleTime']

            if time_gap < timedelta(hours=1):
                tilt_events += 1  # Fast return = tilted

    return tilt_events / total_losses if total_losses > 0 else 0
```

**Insights They Found**:
1. **Early tilt spike**: 2-3 consecutive losses → players return quickly (emotional)
2. **Tilt collapse**: 7-10 losses → players stop returning (churn)
3. **Return time > trophy count**: Behavior patterns predict retention better than skill

#### 4. **Stratified Player Sampling**

**Your Approach**: Random 10% sample of battles
**Their Approach**:
1. Identify players with ≥10 matches (ensure meaningful history)
2. Sample players (not battles)
3. Take ALL battles for sampled players (preserve temporal sequences)
4. Stratify by engagement level (casual vs hardcore)

**Why It Matters**:
- Preserves player journey integrity
- Enables temporal feature engineering
- Reduces noise from one-time players
- Better train/test split (by player, not by battle)

#### 5. **Streamlit Dashboard (Interactive Storytelling)**

**Components** (inferred from LinkedIn post):

1. **Player Filter**: Select by match count (e.g., 10+ matches, 20+, 50+)
2. **Metrics Panel**:
   - Win rate
   - Trophy momentum (change over time)
   - Return behavior (avg gap, fast returns %)
3. **Behavioral Tilt Chart**:
   - X-axis: Loss streak length (0, 1, 2, ..., 10+)
   - Y-axis: % players returning within 1 hour
   - Shows spike at 2-3 losses, collapse at 7-10
4. **Player Comparison**:
   - Profile A: 14 matches, high churn risk
   - Profile B: 28 matches, highly engaged
   - Side-by-side metrics, behavior patterns
5. **Interactive Filters**:
   - Trophy range slider
   - Game mode selector
   - Time period selector

**Technical Stack** (inferred):
```python
import streamlit as st
import plotly.express as px
import pandas as pd

# Filters
min_matches = st.slider("Minimum Matches", 10, 100, 10)

# Load player data
players = load_player_data()
filtered = players[players['match_count'] >= min_matches]

# Display metrics
st.metric("Avg Win Rate", f"{filtered['win_rate'].mean():.1f}%")

# Tilt analysis
tilt_data = filtered.groupby('loss_streak_bucket')['fast_return_1hr'].mean()
fig = px.bar(tilt_data, title="Behavioral Tilt by Loss Streak")
st.plotly_chart(fig)

# Player comparison
col1, col2 = st.columns(2)
with col1:
    st.subheader("High-Risk Player")
    show_player_profile(player_id="...")
with col2:
    st.subheader("Engaged Player")
    show_player_profile(player_id="...")
```

#### 6. **Random Forest Model (90% Accuracy)**

**Prediction Target**: Churn (binary classification)
- `1` = Player stopped playing (no battles in next 7 days)
- `0` = Player returned (continued playing)

**Features Used** (inferred):
```python
features = [
    # Engagement
    'match_count',
    'avg_return_gap_hours',
    'fast_return_1hr_rate',
    'days_since_first_battle',

    # Performance
    'win_rate',
    'trophy_momentum_7d',  # Change over last 7 days
    'current_trophy_level',

    # Behavior
    'behavioral_tilt_score',
    'current_loss_streak',
    'max_loss_streak_ever',
    'avg_session_length_minutes',

    # Recent activity
    'battles_last_24h',
    'battles_last_7d',
    'trophy_change_last_5_battles',
]
```

**Why 90% Accuracy?**
- Churn is more predictable than battle outcomes
- Strong signal from behavioral patterns
- Return time is highly predictive
- Loss streaks have clear threshold effects

**Model Training** (inferred):
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define churn (no battle in next 7 days)
players['churned'] = players['days_until_next_battle'] > 7

# Train/test split by player (not by battle!)
X = players[features]
y = players['churned']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Random Forest
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=50,
    class_weight='balanced',  # Handle class imbalance
    random_state=42
)

rf.fit(X_train, y_train)
accuracy = rf.score(X_test, y_test)  # ~90%
```

**Feature Importance** (expected top features):
1. `avg_return_gap_hours` (~25% importance)
2. `current_loss_streak` (~18%)
3. `behavioral_tilt_score` (~15%)
4. `match_count` (~12%)
5. `win_rate` (~8%)
6. `trophy_momentum_7d` (~7%)
7. Others (~15%)

#### 7. **Business-Focused Recommendations**

**Your Approach**: Game balance insights (which cards are OP)
**Their Approach**: Retention strategies (how to keep players engaged)

**Their Recommendations** (from LinkedIn post):

| Insight | Recommendation | Business Impact |
|---------|----------------|-----------------|
| 2-3 loss spike causes tilt | Light loss-protection after 2 losses | Reduce early churn |
| Early losses drive emotional returns | Easier matchmaking for beginners | Improve new player experience |
| 7-10 loss streaks → churn | Cool-down prompts + small rewards | Retain frustrated players |
| Return time > trophies as signal | Use engagement metrics in matchmaking | Better player satisfaction |
| Tilt is measurable | Personalized difficulty adjustment | Dynamic balance system |

**Why Judges Loved This**:
- ✅ **Clarity & Storytelling**: Player psychology is relatable
- ✅ **Data Understanding**: Acknowledged behavioral patterns, not just stats
- ✅ **Technical Rigor**: 90% accuracy, proper validation
- ✅ **Insights & Recommendations**: Directly actionable for game developers
- ✅ **Visuals**: Interactive dashboard > static charts

---

## Part 3: Critical Differences Analysis

### Side-by-Side Comparison

| Dimension | Your Team | Winning Team |
|-----------|-----------|--------------|
| **Unit of Analysis** | Battle (16.9M rows) | Player (N players) |
| **Data Structure** | Each row = 1 battle | Each row = 1 player's aggregated history |
| **Temporal Ordering** | Not used | Critical (sorted by battleTime) |
| **Feature Engineering** | Battle-level (elixir_diff, trophy_diff) | Player-level (return_gap, loss_streaks, tilt) |
| **Sampling Strategy** | Random 10% of battles | Stratified by player engagement (10+ matches) |
| **Prediction Target** | Battle outcome (win/loss) | Player churn (stop playing) |
| **Model Accuracy** | 52-60% | 90% |
| **Feature Count** | ~30-40 | ~15-20 (simpler but more predictive) |
| **Top Feature** | Card composition | Return time behavior |
| **Visualization** | Static charts (PNG) | Interactive dashboard (Streamlit) |
| **Story Angle** | "What wins?" (competitive) | "What retains?" (business) |
| **Recommendations** | Card balance adjustments | Retention strategies |
| **Judging Appeal** | Technical depth | Business relevance + technical depth |

### Why Their Accuracy Was Higher

**Your 52-60% Accuracy (Battle Prediction)**:
- Battle outcomes are inherently noisy
- Player skill variance is high
- Luck/RNG factors (card draw, tower placement timing)
- Missing key features (player skill rating, card levels, exact matchup)

**Their 90% Accuracy (Churn Prediction)**:
- Behavioral patterns are stable and predictable
- Strong signal from return time (if gap > 7 days, likely churned)
- Loss streaks have clear threshold effects
- Engagement metrics are highly correlated

**Analogy**:
- Predicting a coin flip outcome = hard (~50%)
- Predicting if someone will come back to a casino = easier (behavioral patterns)

---

## Part 4: Reverse Engineering Plan

### Phase 1: Data Transformation (Foundation)

**Goal**: Convert battle-centric data to player-centric format

#### Step 1.1: Player Timeline Construction

**New Notebook**: `notebooks/09-player-timeline-construction.ipynb`

```python
import duckdb
import pandas as pd
from datetime import timedelta

# Connect to data
con = duckdb.connect()
con.execute("""
    CREATE VIEW battles AS
    SELECT * FROM read_csv_auto('battles.csv',
        SAMPLE_SIZE=-1, IGNORE_ERRORS=true
    )
""")

# Step 1: Extract player-battle pairs with outcomes
query = """
WITH player_battles AS (
    -- Winner's perspective
    SELECT
        "winner.tag" AS player_tag,
        battleTime,
        1 AS outcome,  -- Win
        "winner.startingTrophies" AS trophies_before,
        "winner.trophyChange" AS trophy_change,
        "winner.crowns" AS crowns,
        "loser.startingTrophies" AS opponent_trophies,
        "gameMode.id" AS game_mode,
        "arena.id" AS arena
    FROM battles
    WHERE "winner.tag" IS NOT NULL

    UNION ALL

    -- Loser's perspective
    SELECT
        "loser.tag" AS player_tag,
        battleTime,
        0 AS outcome,  -- Loss
        "loser.startingTrophies" AS trophies_before,
        "loser.trophyChange" AS trophy_change,
        "loser.crowns" AS crowns,
        "winner.startingTrophies" AS opponent_trophies,
        "gameMode.id" AS game_mode,
        "arena.id" AS arena
    FROM battles
    WHERE "loser.tag" IS NOT NULL
)
SELECT *
FROM player_battles
ORDER BY player_tag, battleTime
"""

# Execute query (will be large!)
# Use LIMIT for testing, then run on full dataset
player_timeline = con.sql(query + " LIMIT 1000000").df()

# Save as Parquet for fast reloading
player_timeline.to_parquet('artifacts/player_timeline.parquet')
print(f"Created player timeline: {len(player_timeline):,} rows")
```

#### Step 1.2: Temporal Feature Engineering

```python
# Load player timeline
player_timeline = pd.read_parquet('artifacts/player_timeline.parquet')

# Convert battleTime to datetime
player_timeline['battleTime'] = pd.to_datetime(player_timeline['battleTime'])

# Group by player
grouped = player_timeline.groupby('player_tag')

# Feature 1: Next battle time
player_timeline['next_battleTime'] = grouped['battleTime'].shift(-1)

# Feature 2: Return gap (in hours)
player_timeline['return_gap_hours'] = (
    (player_timeline['next_battleTime'] - player_timeline['battleTime'])
    .dt.total_seconds() / 3600
)

# Feature 3: Fast return (within 1 hour)
player_timeline['fast_return_1hr'] = (
    player_timeline['return_gap_hours'] < 1.0
).fillna(False)

# Feature 4: Loss streak calculation
def calculate_loss_streaks(group):
    """Calculate current loss streak at each battle"""
    streaks = []
    current_streak = 0

    for outcome in group['outcome']:
        if outcome == 0:  # Loss
            current_streak += 1
        else:  # Win
            current_streak = 0
        streaks.append(current_streak)

    return pd.Series(streaks, index=group.index)

player_timeline['loss_streak'] = grouped.apply(
    calculate_loss_streaks
).reset_index(level=0, drop=True)

# Feature 5: Win streak (same logic)
def calculate_win_streaks(group):
    streaks = []
    current_streak = 0

    for outcome in group['outcome']:
        if outcome == 1:  # Win
            current_streak += 1
        else:  # Loss
            current_streak = 0
        streaks.append(current_streak)

    return pd.Series(streaks, index=group.index)

player_timeline['win_streak'] = grouped.apply(
    calculate_win_streaks
).reset_index(level=0, drop=True)

# Feature 6: Loss streak bucket
def bucket_streak(streak):
    if streak == 0:
        return "0"
    elif streak <= 2:
        return "1-2"
    elif streak <= 5:
        return "3-5"
    elif streak <= 10:
        return "6-10"
    else:
        return "10+"

player_timeline['loss_streak_bucket'] = player_timeline['loss_streak'].apply(bucket_streak)

# Save enhanced timeline
player_timeline.to_parquet('artifacts/player_timeline_features.parquet')
print("Temporal features added!")
```

#### Step 1.3: Player-Level Aggregation

```python
# Load enhanced timeline
player_timeline = pd.read_parquet('artifacts/player_timeline_features.parquet')

# Filter: Players with 10+ matches (like winning team)
player_match_counts = player_timeline.groupby('player_tag').size()
eligible_players = player_match_counts[player_match_counts >= 10].index

player_timeline_filtered = player_timeline[
    player_timeline['player_tag'].isin(eligible_players)
]

print(f"Players with 10+ matches: {len(eligible_players):,}")

# Aggregate to player level
player_aggregated = player_timeline_filtered.groupby('player_tag').agg({
    # Match count
    'battleTime': 'count',  # Total matches

    # Performance
    'outcome': 'mean',  # Win rate
    'trophy_change': 'sum',  # Total trophy change (momentum)
    'trophies_before': ['first', 'last'],  # Starting and ending trophies

    # Behavioral
    'return_gap_hours': ['mean', 'median', 'std'],
    'fast_return_1hr': 'mean',  # % of fast returns
    'loss_streak': 'max',  # Worst loss streak ever

    # Time span
    'battleTime': ['min', 'max'],  # First and last battle dates
}).reset_index()

# Flatten column names
player_aggregated.columns = [
    'player_tag',
    'match_count',
    'win_rate',
    'total_trophy_change',
    'starting_trophies',
    'ending_trophies',
    'avg_return_gap_hours',
    'median_return_gap_hours',
    'std_return_gap_hours',
    'fast_return_rate',
    'max_loss_streak',
    'first_battle',
    'last_battle',
]

# Additional features
player_aggregated['days_active'] = (
    (player_aggregated['last_battle'] - player_aggregated['first_battle'])
    .dt.total_seconds() / 86400
)

player_aggregated['trophy_momentum'] = (
    player_aggregated['ending_trophies'] - player_aggregated['starting_trophies']
)

# Save player-level dataset
player_aggregated.to_parquet('artifacts/player_aggregated.parquet')
print(f"Player-level dataset created: {len(player_aggregated):,} players")
```

---

### Phase 2: Behavioral Tilt Metric

**New Notebook**: `notebooks/10-behavioral-tilt-analysis.ipynb`

#### Step 2.1: Calculate Behavioral Tilt

```python
import pandas as pd
import numpy as np

# Load player timeline
player_timeline = pd.read_parquet('artifacts/player_timeline_features.parquet')

# Filter to eligible players (10+ matches)
player_match_counts = player_timeline.groupby('player_tag').size()
eligible_players = player_match_counts[player_match_counts >= 10].index
player_timeline_filtered = player_timeline[
    player_timeline['player_tag'].isin(eligible_players)
]

# Calculate behavioral tilt per player
def calculate_player_tilt(group):
    """
    Tilt = % of losses followed by fast return (< 1 hour)
    High tilt = emotional, reactive behavior
    """
    losses = group[group['outcome'] == 0].copy()  # Filter to losses only

    if len(losses) == 0:
        return 0.0

    # Check fast returns after losses
    fast_returns_after_loss = losses['fast_return_1hr'].sum()

    # Exclude last battle (no next battle to measure)
    total_losses_with_next = (losses['next_battleTime'].notna()).sum()

    if total_losses_with_next == 0:
        return 0.0

    tilt_score = fast_returns_after_loss / total_losses_with_next
    return tilt_score

# Apply to each player
tilt_scores = player_timeline_filtered.groupby('player_tag').apply(
    calculate_player_tilt
).reset_index()
tilt_scores.columns = ['player_tag', 'behavioral_tilt_score']

# Merge with player aggregated data
player_aggregated = pd.read_parquet('artifacts/player_aggregated.parquet')
player_aggregated = player_aggregated.merge(tilt_scores, on='player_tag', how='left')

# Save updated dataset
player_aggregated.to_parquet('artifacts/player_aggregated.parquet')
print("Behavioral tilt added!")
```

#### Step 2.2: Tilt by Loss Streak Analysis

```python
# Analyze tilt behavior by loss streak length
tilt_by_streak = player_timeline_filtered.groupby('loss_streak_bucket').agg({
    'fast_return_1hr': 'mean',  # % fast returns
    'return_gap_hours': 'median',  # Typical return time
    'player_tag': 'count',  # Sample size
}).reset_index()

tilt_by_streak.columns = [
    'loss_streak_bucket',
    'fast_return_rate',
    'median_return_gap_hours',
    'battle_count'
]

# Sort by streak bucket
bucket_order = ["0", "1-2", "3-5", "6-10", "10+"]
tilt_by_streak['loss_streak_bucket'] = pd.Categorical(
    tilt_by_streak['loss_streak_bucket'],
    categories=bucket_order,
    ordered=True
)
tilt_by_streak = tilt_by_streak.sort_values('loss_streak_bucket')

print(tilt_by_streak)

# Save for visualization
tilt_by_streak.to_parquet('artifacts/tilt_by_loss_streak.parquet')
```

**Expected Output**:
```
loss_streak_bucket  fast_return_rate  median_return_gap_hours  battle_count
0                      0.35                     4.2            8,500,000
1-2                    0.48                     0.8            3,200,000
3-5                    0.52                     0.6            1,100,000
6-10                   0.28                     8.5              450,000
10+                    0.15                    24.0              120,000
```

**Key Insight** (mirroring winning team):
- **Spike at 1-2 losses**: Players return quickly (emotional, tilted)
- **Peak at 3-5 losses**: Maximum tilt
- **Collapse at 6-10+**: Players get discouraged, stop playing

---

### Phase 3: Churn Prediction Model

**New Notebook**: `notebooks/11-churn-prediction-model.ipynb`

#### Step 3.1: Define Churn Target

```python
import pandas as pd
from datetime import timedelta

# Load player aggregated data
player_aggregated = pd.read_parquet('artifacts/player_aggregated.parquet')

# Define churn: No battle in last 7 days of dataset
dataset_end = player_aggregated['last_battle'].max()
churn_threshold_days = 7

player_aggregated['days_since_last_battle'] = (
    (dataset_end - player_aggregated['last_battle']).dt.total_seconds() / 86400
)

player_aggregated['churned'] = (
    player_aggregated['days_since_last_battle'] > churn_threshold_days
).astype(int)

print(f"Churn rate: {player_aggregated['churned'].mean():.1%}")
# Expected: 30-50% (many players stop eventually)
```

#### Step 3.2: Feature Selection

```python
# Select features for modeling
feature_columns = [
    # Engagement
    'match_count',
    'days_active',
    'avg_return_gap_hours',
    'median_return_gap_hours',
    'fast_return_rate',

    # Performance
    'win_rate',
    'trophy_momentum',
    'starting_trophies',

    # Behavior
    'behavioral_tilt_score',
    'max_loss_streak',
]

X = player_aggregated[feature_columns].fillna(0)
y = player_aggregated['churned']

print(f"Features: {X.shape[1]}")
print(f"Players: {len(X):,}")
print(f"Churn rate: {y.mean():.1%}")
```

#### Step 3.3: Train Random Forest

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# Random Forest
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=100,
    min_samples_leaf=50,
    class_weight='balanced',  # Handle imbalanced classes
    n_jobs=-1,
    random_state=42
)

# Train
rf.fit(X_train, y_train)

# Predict
y_pred = rf.predict(X_test)
y_pred_proba = rf.predict_proba(X_test)[:, 1]

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\n{'='*50}")
print(f"CHURN PREDICTION MODEL RESULTS")
print(f"{'='*50}")
print(f"Accuracy: {accuracy:.1%}")
print(f"ROC-AUC: {roc_auc:.3f}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nTop 5 Features:")
print(feature_importance.head())

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Retained', 'Churned'])
disp.plot()
plt.title(f'Churn Prediction (Accuracy: {accuracy:.1%})')
plt.savefig('presentation/figures/fig_churn_confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Save model
import joblib
joblib.dump(rf, 'artifacts/churn_model_rf.pkl')
print("\nModel saved!")
```

**Expected Results**:
```
Accuracy: 88-92%  (similar to winning team's 90%)
ROC-AUC: 0.92-0.95

Top 5 Features:
1. avg_return_gap_hours     (28% importance)
2. fast_return_rate          (18%)
3. behavioral_tilt_score     (14%)
4. match_count               (12%)
5. max_loss_streak           (9%)
```

---

### Phase 4: Interactive Streamlit Dashboard

**New File**: `streamlit_dashboard.py`

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Clash Royale Player Retention Dashboard",
    page_icon="👑",
    layout="wide"
)

# Title
st.title("👑 Clash Royale: Player Retention & Behavioral Tilt Analysis")
st.markdown("**Reframing Clash Royale from game strategy to player retention strategy**")

# Load data
@st.cache_data
def load_data():
    players = pd.read_parquet('artifacts/player_aggregated.parquet')
    tilt_by_streak = pd.read_parquet('artifacts/tilt_by_loss_streak.parquet')
    return players, tilt_by_streak

players, tilt_by_streak = load_data()

# Sidebar filters
st.sidebar.header("Filters")
min_matches = st.sidebar.slider(
    "Minimum Matches Played",
    min_value=10,
    max_value=100,
    value=10,
    step=5
)

trophy_range = st.sidebar.slider(
    "Trophy Range",
    min_value=int(players['starting_trophies'].min()),
    max_value=int(players['starting_trophies'].max()),
    value=(
        int(players['starting_trophies'].min()),
        int(players['starting_trophies'].max())
    )
)

# Filter data
filtered_players = players[
    (players['match_count'] >= min_matches) &
    (players['starting_trophies'] >= trophy_range[0]) &
    (players['starting_trophies'] <= trophy_range[1])
]

st.sidebar.markdown(f"**Players shown**: {len(filtered_players):,}")

# Metrics row
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_winrate = filtered_players['win_rate'].mean()
    st.metric("Avg Win Rate", f"{avg_winrate:.1%}")

with col2:
    churn_rate = filtered_players['churned'].mean()
    st.metric("Churn Rate", f"{churn_rate:.1%}")

with col3:
    avg_return_gap = filtered_players['avg_return_gap_hours'].median()
    st.metric("Median Return Gap", f"{avg_return_gap:.1f} hrs")

with col4:
    avg_tilt = filtered_players['behavioral_tilt_score'].mean()
    st.metric("Avg Behavioral Tilt", f"{avg_tilt:.1%}")

# Behavioral Tilt Chart (KEY INSIGHT)
st.header("🔥 Behavioral Tilt Analysis")
st.markdown("""
**Behavioral Tilt**: Measures how quickly players return after losing.
**Key Finding**: Tilt spikes after 2-3 losses (emotional returns), then collapses at 7-10 losses (churn).
""")

fig_tilt = px.bar(
    tilt_by_streak,
    x='loss_streak_bucket',
    y='fast_return_rate',
    title='Fast Return Rate by Loss Streak (Behavioral Tilt)',
    labels={
        'loss_streak_bucket': 'Consecutive Losses',
        'fast_return_rate': '% Returning Within 1 Hour'
    },
    text='fast_return_rate',
    color='fast_return_rate',
    color_continuous_scale='RdYlGn_r'
)
fig_tilt.update_traces(texttemplate='%{text:.1%}', textposition='outside')
fig_tilt.update_layout(height=400)
st.plotly_chart(fig_tilt, use_container_width=True)

# Player Comparison
st.header("👥 Player Profile Comparison")
st.markdown("Compare a **high-risk churn player** vs **highly engaged player**")

col1, col2 = st.columns(2)

# Find example players
high_risk = filtered_players[
    (filtered_players['churned'] == 1) &
    (filtered_players['match_count'] <= 20)
].iloc[0] if len(filtered_players[filtered_players['churned'] == 1]) > 0 else None

engaged = filtered_players[
    (filtered_players['churned'] == 0) &
    (filtered_players['match_count'] >= 30)
].iloc[0] if len(filtered_players[filtered_players['churned'] == 0]) > 0 else None

with col1:
    st.subheader("⚠️ High-Risk Player")
    if high_risk is not None:
        st.metric("Match Count", int(high_risk['match_count']))
        st.metric("Win Rate", f"{high_risk['win_rate']:.1%}")
        st.metric("Avg Return Gap", f"{high_risk['avg_return_gap_hours']:.1f} hrs")
        st.metric("Behavioral Tilt", f"{high_risk['behavioral_tilt_score']:.1%}")
        st.metric("Max Loss Streak", int(high_risk['max_loss_streak']))
        st.metric("Trophy Momentum", int(high_risk['trophy_momentum']))

with col2:
    st.subheader("✅ Engaged Player")
    if engaged is not None:
        st.metric("Match Count", int(engaged['match_count']))
        st.metric("Win Rate", f"{engaged['win_rate']:.1%}")
        st.metric("Avg Return Gap", f"{engaged['avg_return_gap_hours']:.1f} hrs")
        st.metric("Behavioral Tilt", f"{engaged['behavioral_tilt_score']:.1%}")
        st.metric("Max Loss Streak", int(engaged['max_loss_streak']))
        st.metric("Trophy Momentum", int(engaged['trophy_momentum']))

# Retention vs Engagement Scatter
st.header("📈 Retention Signals")

fig_scatter = px.scatter(
    filtered_players.sample(min(5000, len(filtered_players))),  # Sample for performance
    x='avg_return_gap_hours',
    y='win_rate',
    color='churned',
    size='match_count',
    hover_data=['behavioral_tilt_score', 'max_loss_streak'],
    title='Return Time vs Win Rate (Color = Churn Status)',
    labels={
        'avg_return_gap_hours': 'Avg Return Gap (hours)',
        'win_rate': 'Win Rate',
        'churned': 'Churned'
    },
    color_discrete_map={0: 'green', 1: 'red'}
)
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter, use_container_width=True)

# Business Recommendations
st.header("💡 Business Recommendations")
st.markdown("""
### Targeted Retention Strategies

**Early-Stage Players (2-3 Loss Streaks)**:
- ✅ Introduce light loss protection (e.g., reduced trophy loss for first 2 losses)
- ✅ Slightly easier matchmaking after consecutive losses
- ✅ Positive reinforcement messages ("You're improving!")

**Mid-Stage Frustration (3-5 Loss Streaks)**:
- ✅ Offer skill-building tips or deck suggestions
- ✅ Recommend game mode changes (switch from ladder to 2v2)
- ✅ Small rewards for persistence (coins, common cards)

**High-Risk Churn (7-10+ Loss Streaks)**:
- ✅ Cool-down prompts ("Take a break, come back refreshed!")
- ✅ Guaranteed win mechanics (tutorial mode, practice battles)
- ✅ Special comeback bonuses (2x trophy gains on next win)

**Key Insight**: Return time behavior is a stronger retention signal than win rate or trophy count.
**Recommendation**: Use engagement metrics (not just skill metrics) in matchmaking algorithms.
""")

# Footer
st.markdown("---")
st.markdown("**Data**: 16.9M battles | **Players Analyzed**: {:,} (10+ matches)".format(
    len(players)
))
```

**To Run**:
```bash
pip install streamlit plotly
streamlit run streamlit_dashboard.py
```

---

### Phase 5: Presentation Strategy

**New Notebook**: `notebooks/12-winning-presentation-synthesis.ipynb`

#### Updated Story Structure (8 minutes)

**Slide 1: Title** (30 sec)
- "Clash Royale: From Game Strategy to Player Retention Strategy"
- Team names

**Slide 2: The Reframe** (1 min)
- Traditional approach: "What deck wins?"
- Our approach: "What player behaviors predict retention?"
- Why it matters: Retention = revenue for game companies

**Slide 3: Data Transformation** (1.5 min)
- Started with 16.9M battles
- Grouped by player tag → Created player timelines
- Engineered temporal features:
  - return_gap, fast_return_1hr, loss_streaks, behavioral_tilt
- Final dataset: N players with 10+ matches

**Slide 4: Behavioral Tilt Discovery** (2 min)
- **Show dashboard screenshot or chart**
- Definition: Fast returns after losses (emotional behavior)
- Key finding 1: Tilt spikes at 2-3 losses (48-52% fast return rate)
- Key finding 2: Tilt collapses at 7-10 losses (15-28% fast return rate)
- Insight: Loss streak thresholds predict churn

**Slide 5: Predictive Model** (1.5 min)
- Random Forest classifier
- **90% accuracy** predicting player churn
- Top features:
  1. Return time behavior (28% importance)
  2. Fast return rate (18%)
  3. Behavioral tilt (14%)
  4. Match count (12%)
- Insight: Engagement > Skill for retention

**Slide 6: Player Profiles** (1 min)
- **Show dashboard comparison or table**
- High-risk player: 14 matches, high tilt, long return gaps → Churned
- Engaged player: 28 matches, moderate tilt, short return gaps → Retained
- Demonstrates actionable player segmentation

**Slide 7: Business Recommendations** (1.5 min)
- Early losses (2-3): Loss protection, easier matchmaking
- Mid-stage (3-5): Skill tips, rewards
- High-risk (7-10+): Cool-down prompts, comeback bonuses
- Use return time in matchmaking (not just trophies)

**Slide 8: Impact & Takeaways** (30 sec)
- Reframed problem → Higher accuracy (90% vs 52-60%)
- Player-centric analysis → Actionable business insights
- Interactive dashboard → Ongoing monitoring tool
- Thank you + Q&A

**Timing**: Aim for 7:30 to leave 30s buffer

---

## Part 5: Implementation Roadmap

### Timeline Estimate

| Phase | Tasks | Estimated Time | Dependencies |
|-------|-------|----------------|--------------|
| **Phase 1** | Data transformation to player-centric | 4-6 hours | Access to battles.csv |
| **Phase 2** | Behavioral tilt calculation | 2-3 hours | Phase 1 complete |
| **Phase 3** | Churn prediction model | 3-4 hours | Phases 1-2 complete |
| **Phase 4** | Streamlit dashboard | 4-6 hours | Phase 3 complete |
| **Phase 5** | Presentation creation | 2-3 hours | All analyses done |
| **Testing** | End-to-end testing, debugging | 2-3 hours | - |
| **Total** | | **17-25 hours** | |

### Prioritization for Learning

**Must-Do (Core Learning)**:
1. ✅ Phase 1: Player timeline construction (fundamental shift)
2. ✅ Phase 2: Behavioral tilt analysis (key differentiator)
3. ✅ Phase 3: Churn model (demonstrates accuracy improvement)

**Should-Do (Good Learning)**:
4. ✅ Phase 4: Streamlit dashboard (modern deliverable format)
5. ✅ Compare accuracy: Your 52-60% vs their 90%

**Nice-to-Have (Time Permitting)**:
6. ⏳ Advanced tilt metrics (session analysis, tilt decay over time)
7. ⏳ Player clustering (casual vs hardcore vs at-risk)
8. ⏳ Time-series forecasting (predict when players will return)

---

## Part 6: Key Learnings & Takeaways

### What You Did Well

1. **Technical Infrastructure**: DuckDB, modular code, documentation
2. **Domain Expertise**: Deep card analysis, meta understanding
3. **Analytical Rigor**: Proper train/test splits, multiple models
4. **Presentation Prep**: Professional charts, clear structure

### What the Winners Did Differently

1. **Problem Reframing**: Game → Business perspective
2. **Unit of Analysis**: Battle → Player
3. **Feature Engineering**: Temporal and behavioral vs compositional
4. **Prediction Target**: Churn (90% achievable) vs Battle outcome (52-60% ceiling)
5. **Deliverable**: Interactive dashboard vs Static slides
6. **Storytelling**: Player psychology (relatable) vs Card balance (technical)

### Universal Competition Lessons

#### 1. **Reframe > Execute**
- Spending time on the "right problem" matters more than perfect execution
- Ask: "What question would judges find most valuable?"

#### 2. **Know Your Audience**
- Judges value: Business relevance > Technical complexity
- 90% accuracy on meaningful problem > 99% on trivial problem

#### 3. **Deliverable Format Matters**
- Interactive dashboard > Static charts (engagement factor)
- Live demo > Screenshot (wow factor)
- Streamlit is quick to learn, high impact

#### 4. **Feature Engineering > Model Selection**
- Their 10 features > Your 40 features (quality > quantity)
- Temporal features are powerful but underused
- Behavioral >> Compositional for predicting human actions

#### 5. **Tell a Story, Not Just Results**
- "Player psychology" is inherently engaging
- Use case studies (Player A vs Player B)
- Connect to real-world impact (retention = revenue)

#### 6. **Accuracy Isn't Everything**
- Context matters: 90% churn prediction > 60% battle prediction
- Judges appreciated actionable insights over raw accuracy

---

## Part 7: Next Steps for Your Team

### Immediate Actions (Next Session)

1. **Run Phase 1**: Player timeline construction
   - Start with 10% sample to validate approach
   - Verify temporal feature calculation logic
   - Inspect output: Does it make sense?

2. **Calculate Behavioral Tilt**:
   - Implement tilt metric
   - Plot tilt by loss streak
   - Compare to winning team's findings

3. **Build Churn Model**:
   - Define churn (7-day threshold)
   - Train Random Forest
   - Measure accuracy (target: 85-90%)

### Medium-Term (Next Week)

4. **Learn Streamlit**:
   - Complete Streamlit tutorial (2 hours)
   - Build basic dashboard with your data
   - Add filters and interactivity

5. **Compare Results**:
   - Document accuracy differences
   - Analyze feature importance differences
   - Write up learnings

### Long-Term (Future Competitions)

6. **Checklist Before Starting**:
   - [ ] What's the "business question" here?
   - [ ] What's the right unit of analysis?
   - [ ] What temporal patterns exist?
   - [ ] What's the most valuable prediction target?
   - [ ] How can I make this interactive?

7. **Build a Template**:
   - Player-centric transformation script
   - Temporal feature engineering functions
   - Streamlit dashboard boilerplate
   - Reuse for future competitions

---

## Part 8: Technical Resources

### Code Templates

**Temporal Feature Engineering Template**:
```python
def engineer_temporal_features(df, player_col, time_col, outcome_col):
    """
    Universal temporal feature engineering for player-centric analysis

    Args:
        df: DataFrame with player timelines
        player_col: Column name for player ID
        time_col: Column name for timestamps
        outcome_col: Column name for win/loss (1/0)

    Returns:
        DataFrame with added temporal features
    """
    df = df.sort_values([player_col, time_col])

    # Next event time
    df['next_time'] = df.groupby(player_col)[time_col].shift(-1)

    # Time gap
    df['time_gap_hours'] = (
        (df['next_time'] - df[time_col]).dt.total_seconds() / 3600
    )

    # Fast return (< 1 hour)
    df['fast_return'] = df['time_gap_hours'] < 1.0

    # Streaks
    def calculate_streaks(group, target_value):
        streaks = []
        current = 0
        for val in group[outcome_col]:
            if val == target_value:
                current += 1
            else:
                current = 0
            streaks.append(current)
        return pd.Series(streaks, index=group.index)

    # Loss streak
    df['loss_streak'] = df.groupby(player_col).apply(
        lambda x: calculate_streaks(x, 0)
    ).reset_index(level=0, drop=True)

    # Win streak
    df['win_streak'] = df.groupby(player_col).apply(
        lambda x: calculate_streaks(x, 1)
    ).reset_index(level=0, drop=True)

    return df
```

**Player Aggregation Template**:
```python
def aggregate_player_features(timeline_df, player_col, min_events=10):
    """
    Aggregate timeline to player level
    """
    # Filter to active players
    event_counts = timeline_df.groupby(player_col).size()
    active_players = event_counts[event_counts >= min_events].index
    filtered = timeline_df[timeline_df[player_col].isin(active_players)]

    # Aggregate
    aggregated = filtered.groupby(player_col).agg({
        'time': ['count', 'min', 'max'],
        'outcome': 'mean',
        'time_gap_hours': ['mean', 'median', 'std'],
        'fast_return': 'mean',
        'loss_streak': 'max',
        'win_streak': 'max',
    }).reset_index()

    # Flatten columns
    aggregated.columns = [
        player_col,
        'event_count', 'first_time', 'last_time',
        'win_rate',
        'avg_gap', 'median_gap', 'std_gap',
        'fast_return_rate',
        'max_loss_streak', 'max_win_streak'
    ]

    return aggregated
```

### Learning Resources

**Streamlit**:
- Official tutorial: https://docs.streamlit.io/library/get-started
- Gallery examples: https://streamlit.io/gallery
- Time investment: 2-3 hours to learn basics

**Temporal Feature Engineering**:
- pandas `.shift()` documentation
- Time series feature engineering guide
- Cohort analysis tutorials

**Churn Prediction**:
- Scikit-learn imbalanced classes: `class_weight='balanced'`
- ROC-AUC vs Accuracy for imbalanced data
- Calibration plots: `sklearn.calibration.calibration_curve`

---

## Conclusion

The winning team's success came from **asking a different question**. Instead of "What wins battles?", they asked "What keeps players engaged?" This reframing led to:

1. **Higher accuracy**: 90% (churn) vs 52-60% (battles)
2. **More actionable insights**: Retention strategies vs card balance
3. **Better storytelling**: Player psychology vs game mechanics
4. **Stronger business case**: Revenue impact vs competitive meta

**Your team's work was technically solid**, but the winners understood that **competitions reward problem framing as much as problem solving**.

For your next competition:
- ✅ Spend 20% of time on problem framing (what to predict?)
- ✅ Think "business value" before "technical complexity"
- ✅ Consider temporal patterns (when do things happen?)
- ✅ Use interactive deliverables (Streamlit, dashboards)
- ✅ Tell stories with data (case studies, comparisons)

**You now have a complete roadmap to reverse-engineer their approach.** Start with Phase 1 (player timelines), validate the behavioral tilt findings, and build toward that 90% accuracy churn model.

Good luck, and remember: The best analysis answers the question the judges didn't know they wanted answered! 🚀

---

**Document prepared by**: Claude (Sonnet 4.5)
**Date**: November 18, 2025
**Purpose**: Learning and improvement for future competitions
