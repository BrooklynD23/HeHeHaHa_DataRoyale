# Quick Start: Reverse Engineering the Winning Approach

**Goal**: Transform your game-centric analysis into a player-centric retention strategy

**Estimated Time**: 17-25 hours
**Expected Accuracy Improvement**: 52-60% → 88-92%

---

## TL;DR - What Changed?

| Aspect | Your Approach | Winning Approach |
|--------|---------------|------------------|
| **Question** | "What deck wins?" | "What keeps players engaged?" |
| **Unit** | Battle (16.9M rows) | Player (N players) |
| **Target** | Battle outcome | Player churn |
| **Accuracy** | 52-60% | 90% |
| **Key Feature** | Card composition | Return time behavior |
| **Deliverable** | Static slides | Interactive dashboard |

---

## Phase 1: Player Timeline (4-6 hours)

### Step 1: Create Player-Battle Pairs

**New notebook**: `notebooks/09-player-timeline-construction.ipynb`

```python
# Extract player-battle pairs (both winner and loser perspectives)
# Group by player_tag
# Sort by battleTime (chronological order)
# Output: artifacts/player_timeline.parquet
```

### Step 2: Calculate Temporal Features

**5 Critical Features**:
1. `next_battleTime` - When did they play again?
2. `return_gap_hours` - Time between battles
3. `fast_return_1hr` - Returned within 1 hour? (Boolean)
4. `loss_streak` - Consecutive losses (0, 1, 2, ..., 10+)
5. `win_streak` - Consecutive wins

**Output**: `artifacts/player_timeline_features.parquet`

### Step 3: Filter to Active Players

```python
# Keep only players with 10+ matches
# Aggregate to player level
# Output: artifacts/player_aggregated.parquet
```

**Key Columns**:
- `match_count`
- `win_rate`
- `avg_return_gap_hours`
- `fast_return_rate`
- `max_loss_streak`

---

## Phase 2: Behavioral Tilt (2-3 hours)

### The "Secret Sauce" Metric

**Definition**: % of losses followed by fast return (< 1 hour)

**Calculation**:
```python
def calculate_tilt(player_battles):
    losses = player_battles[player_battles['outcome'] == 0]
    fast_returns = losses['fast_return_1hr'].sum()
    total_losses = len(losses)
    return fast_returns / total_losses
```

### Analyze by Loss Streak

**Expected Pattern**:
- 0 losses: 35% fast return (baseline)
- 1-2 losses: 48% fast return ⬆️ (tilt spike)
- 3-5 losses: 52% fast return ⬆️ (peak tilt)
- 6-10 losses: 28% fast return ⬇️ (discouraged)
- 10+ losses: 15% fast return ⬇️ (churn)

**Output**: Chart showing tilt curve (for presentation)

---

## Phase 3: Churn Model (3-4 hours)

### Define Churn

```python
# Churn = No battle in last 7 days of dataset
player_aggregated['churned'] = (days_since_last_battle > 7).astype(int)
```

### Train Random Forest

**Features** (10 total):
1. `match_count`
2. `avg_return_gap_hours` ⭐
3. `fast_return_rate` ⭐
4. `behavioral_tilt_score` ⭐
5. `win_rate`
6. `max_loss_streak`
7. `trophy_momentum`
8. `days_active`
9. `median_return_gap_hours`
10. `starting_trophies`

**Expected Results**:
- Accuracy: 88-92%
- Top feature: `avg_return_gap_hours` (~28% importance)

---

## Phase 4: Streamlit Dashboard (4-6 hours)

### Learn Streamlit (2 hours)
- Tutorial: https://docs.streamlit.io/library/get-started
- Install: `pip install streamlit plotly`

### Build Dashboard (3-4 hours)

**Required Components**:
1. **Filters**: Minimum matches, trophy range sliders
2. **Metrics**: Win rate, churn rate, median return gap, avg tilt
3. **Tilt Chart**: Bar chart of fast return % by loss streak
4. **Player Comparison**: Side-by-side (high-risk vs engaged)
5. **Scatter Plot**: Return gap vs win rate (colored by churn)

**Run**:
```bash
streamlit run streamlit_dashboard.py
```

---

## Phase 5: New Presentation (2-3 hours)

### Updated Story (8 minutes)

**Slide 1**: Title (30s)

**Slide 2**: The Reframe (1 min)
- Traditional: "What deck wins?"
- Our approach: "What behaviors predict retention?"

**Slide 3**: Data Transformation (1.5 min)
- 16.9M battles → Player timelines
- Temporal features: return_gap, loss_streaks, tilt

**Slide 4**: Behavioral Tilt (2 min) ⭐ KEY SLIDE
- **Show tilt chart**
- Spike at 2-3 losses (emotional)
- Collapse at 7-10 losses (churn)

**Slide 5**: 90% Accuracy Model (1.5 min)
- Random Forest churn prediction
- Top features: Return time > Win rate
- Engagement > Skill for retention

**Slide 6**: Player Profiles (1 min)
- **Show dashboard screenshot**
- High-risk: 14 matches, churned
- Engaged: 28 matches, retained

**Slide 7**: Business Recommendations (1.5 min)
- 2-3 losses: Loss protection
- 7-10 losses: Cool-down prompts
- Use return time in matchmaking

**Slide 8**: Impact (30s)
- 90% accuracy vs 52-60%
- Actionable retention strategies
- Interactive monitoring tool

---

## Validation Checklist

Before presenting, verify:

- [ ] Player timeline created (chronological order per player)
- [ ] Temporal features calculated (next_battleTime, return_gap, streaks)
- [ ] Filtered to 10+ match players
- [ ] Behavioral tilt calculated per player
- [ ] Tilt by loss streak chart shows spike at 2-3, collapse at 7-10
- [ ] Churn defined (7-day threshold)
- [ ] Random Forest trained (88-92% accuracy)
- [ ] Feature importance: return_gap is #1
- [ ] Streamlit dashboard runs locally
- [ ] Dashboard has filters, metrics, tilt chart, player comparison
- [ ] Presentation updated with new story
- [ ] Timing: 7:30 (30s buffer)

---

## Common Pitfalls

### 1. Not Sorting by Time
❌ **Wrong**: `player_timeline.groupby('player_tag')`
✅ **Right**: `player_timeline.sort_values(['player_tag', 'battleTime']).groupby('player_tag')`

### 2. Including Last Battle in Tilt
❌ **Wrong**: Count all losses
✅ **Right**: Exclude last battle (no "next battle" to measure)

### 3. Wrong Churn Definition
❌ **Wrong**: Players who lost their last battle
✅ **Right**: Players who haven't played in 7 days

### 4. Forgetting Stratification
❌ **Wrong**: `train_test_split(X, y)`
✅ **Right**: `train_test_split(X, y, stratify=y)`

### 5. Not Handling Imbalance
❌ **Wrong**: `RandomForestClassifier()`
✅ **Right**: `RandomForestClassifier(class_weight='balanced')`

---

## File Structure After Implementation

```
DataRoyale/
├── notebooks/
│   ├── 09-player-timeline-construction.ipynb (NEW)
│   ├── 10-behavioral-tilt-analysis.ipynb (NEW)
│   ├── 11-churn-prediction-model.ipynb (NEW)
│   └── 12-winning-presentation-synthesis.ipynb (NEW)
│
├── artifacts/
│   ├── player_timeline.parquet (NEW)
│   ├── player_timeline_features.parquet (NEW)
│   ├── player_aggregated.parquet (NEW)
│   ├── tilt_by_loss_streak.parquet (NEW)
│   └── churn_model_rf.pkl (NEW)
│
├── presentation/figures/
│   ├── fig_tilt_by_loss_streak.png (NEW)
│   ├── fig_churn_confusion_matrix.png (NEW)
│   └── fig_player_comparison.png (NEW)
│
└── streamlit_dashboard.py (NEW)
```

---

## Quick Wins (If Short on Time)

**Minimum Viable Implementation** (8-10 hours):

1. **Phase 1 only**: Create player timeline with temporal features
2. **Calculate tilt**: Compute behavioral tilt by loss streak
3. **Create chart**: Plot tilt curve (spike at 2-3, collapse at 7-10)
4. **Update presentation**: Add tilt slide, reframe story
5. **Skip**: Streamlit dashboard (use static chart instead)

**This alone** demonstrates:
- ✅ Problem reframing
- ✅ Temporal feature engineering
- ✅ Key behavioral insight
- ✅ Different approach than competitors

---

## Success Metrics

**You'll know you succeeded if**:

1. **Tilt curve matches expected pattern**:
   - Baseline: ~35%
   - Peak: ~50% at 2-3 losses
   - Collapse: ~15-20% at 10+ losses

2. **Churn model achieves 85-92% accuracy**
   - Higher than battle prediction (52-60%)
   - Top feature is return_gap (not card stats)

3. **Presentation tells a different story**:
   - Focus: Player psychology > Game strategy
   - Recommendations: Retention > Balance
   - Deliverable: Interactive > Static

4. **Judges' reaction**:
   - "This is a fresh perspective!"
   - "How did you think of this approach?"
   - "This has real business value!"

---

## Resources

**Full Analysis**: `WINNING_TEAM_ANALYSIS.md` (50+ pages, all details)

**Code Templates**: See Part 8 of WINNING_TEAM_ANALYSIS.md
- Temporal feature engineering function
- Player aggregation function
- Tilt calculation function

**Learning**:
- Streamlit tutorial: 2-3 hours
- pandas `.shift()` for temporal features
- Scikit-learn imbalanced learning

---

## Next Action

**Right Now**:
```bash
cd /home/user/HeHeHaHa_DataRoyale
jupyter notebook
# Create: notebooks/09-player-timeline-construction.ipynb
# Start with Step 1: Extract player-battle pairs
```

**First Code Cell**:
```python
import duckdb
import pandas as pd
from datetime import timedelta

# This is the paradigm shift:
# From 16.9M battles → N players with timelines

con = duckdb.connect()
con.execute("""
    CREATE VIEW battles AS
    SELECT * FROM read_csv_auto('battles.csv',
        SAMPLE_SIZE=-1, IGNORE_ERRORS=true
    )
""")

# Let's begin!
```

---

**Remember**: The winning team didn't have better data or more time. They had a **better question**.

Your turn! 🚀
