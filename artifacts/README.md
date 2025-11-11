# Artifacts Directory

This directory contains intermediate data products generated during analysis. These files are **not stored in Git** (too large) but should be **shared via Google Drive** for team collaboration.

## Files

### `sample_battles_10pct.parquet`
**Created by**: `create_sample.py` or notebook `00-setup-and-validation.ipynb`
**Size**: ~920 MB (10% of battles.csv)
**Rows**: ~10% of total battles
**Use**: Fast iteration for EDA and model development

**Schema**: Same as battles.csv (70+ columns)

**How to use**:
```python
import pandas as pd
sample = pd.read_parquet('artifacts/sample_battles_10pct.parquet')
```

---

### `card_win_rates.parquet`
**Created in**: Notebook `03-eda-card-analysis.ipynb`
**Size**: ~100 KB
**Rows**: One per unique card

**Schema**:
- `card_id` (int/str): Unique card identifier
- `card_name` (str): Card name (if available)
- `usage_count` (int): Total times card appeared in battles
- `win_count` (int): Times card was in winning deck
- `win_rate` (float): Win percentage (0-1)
- `usage_rate` (float): Percentage of all battles

**How to use**:
```python
card_stats = pd.read_parquet('artifacts/card_win_rates.parquet')
top_cards = card_stats.nlargest(15, 'win_rate')
```

---

### `card_synergy_pairs.parquet`
**Created in**: Notebook `03-eda-card-analysis.ipynb`
**Size**: ~50 MB
**Rows**: One per unique card pair

**Schema**:
- `card_1` (int/str): First card ID (sorted)
- `card_2` (int/str): Second card ID (sorted)
- `pair_usage_count` (int): Times this pair appeared together
- `pair_win_count` (int): Times pair won together
- `pair_win_rate` (float): Win percentage for the pair
- `card_1_win_rate` (float): Individual win rate of card 1
- `card_2_win_rate` (float): Individual win rate of card 2
- `lift` (float): pair_win_rate / (card_1_wr * card_2_wr) - synergy metric

**Lift interpretation**:
- `lift > 1`: Positive synergy (cards win more together than expected)
- `lift = 1`: No synergy (independent)
- `lift < 1`: Anti-synergy (cards hurt each other)

**How to use**:
```python
synergies = pd.read_parquet('artifacts/card_synergy_pairs.parquet')
best_combos = synergies.nlargest(20, 'lift')
```

---

### `deck_archetypes.parquet`
**Created in**: Notebook `03-eda-card-analysis.ipynb`
**Size**: ~500 MB
**Rows**: One per battle (includes both winner and loser decks)

**Schema**:
- Battle identifiers (same as battles.csv)
- `archetype` (str): Cluster label (e.g., "Beatdown", "Cycle", "Control")
- `archetype_id` (int): Numeric cluster ID
- Deck features used for clustering:
  - `avg_elixir` (float)
  - `spell_count` (int)
  - `troop_count` (int)
  - `legendary_count` (int)

**How to use**:
```python
archetypes = pd.read_parquet('artifacts/deck_archetypes.parquet')
archetype_performance = archetypes.groupby('archetype').agg({
    'win_rate': 'mean',
    'battle_count': 'size'
})
```

---

### `arena_progression.parquet`
**Created in**: Notebook `04-eda-player-progression.ipynb`
**Size**: ~10 MB
**Rows**: One per arena/trophy bracket

**Schema**:
- `arena_id` (int): Arena identifier
- `trophy_bracket` (str): Trophy range (e.g., "3000-4000")
- `battle_count` (int): Number of battles in this bracket
- `avg_trophy_change` (float): Average trophy gain/loss
- `avg_crowns` (float): Average crown count
- `three_crown_pct` (float): Percentage of 3-crown wins

**How to use**:
```python
progression = pd.read_parquet('artifacts/arena_progression.parquet')
# Find trophy "walls"
walls = progression[progression['battle_count'] > progression['battle_count'].quantile(0.75)]
```

---

### `model_features.parquet`
**Created in**: Notebook `05-feature-engineering.ipynb`
**Size**: ~500 MB
**Rows**: Same as sample (battles restructured for modeling)

**Schema**:
All original columns from battles.csv PLUS:
- `trophy_diff` (int): Winner trophy - loser trophy
- `elixir_diff` (float): Winner elixir - loser elixir
- `card_level_diff` (int): Winner card level - loser card level
- `spell_diff` (int): Winner spell count - loser spell count
- `crown_diff` (int): Winner crowns - loser crowns
- `winner_beatdown` (int): 1 if beatdown deck, 0 otherwise
- `winner_cycle` (int): 1 if cycle deck, 0 otherwise
- `winner_spell_heavy` (int): 1 if 3+ spells, 0 otherwise
- `loser_beatdown` (int): Same for loser
- `loser_cycle` (int): Same for loser
- `loser_spell_heavy` (int): Same for loser
- `trophy_bracket` (str): Categorical trophy range
- `close_game` (int): 1 if crown_diff <= 1, 0 otherwise
- `three_crown_win` (int): 1 if 3-crown victory, 0 otherwise

**How to use**:
```python
features = pd.read_parquet('artifacts/model_features.parquet')

# Select numeric features for modeling
model_cols = ['trophy_diff', 'elixir_diff', 'card_level_diff',
              'winner_beatdown', 'loser_cycle', 'close_game']
X = features[model_cols]
y = features['outcome']  # 1 = winner won, 0 = loser won
```

---

## Sharing Strategy

### For Local Development
Generated artifacts stay in `artifacts/` directory.

### For Google Colab Collaboration

**Option 1: Upload to Google Drive**
```python
# In Colab
from google.colab import drive
drive.mount('/content/drive')

# Copy from Drive to Colab runtime (faster access)
!cp /content/drive/MyDrive/DataRoyale/artifacts/*.parquet /content/artifacts/
```

**Option 2: Share via Colab Files**
```python
# Upload directly to Colab session
from google.colab import files
uploaded = files.upload()  # Select .parquet file
```

### For Team Sync
1. Person A creates artifact in their notebook
2. Person A saves with descriptive name: `save_to_parquet(df, 'artifacts/my_analysis.parquet')`
3. Person A uploads to shared Google Drive folder
4. Persons B, C, D download and use in their notebooks

---

## Regenerating Artifacts

If artifacts are missing or corrupted:

```bash
# Regenerate sample
python create_sample.py --pct 10

# Regenerate analysis artifacts
jupyter notebook
# Then run notebooks 01-05 in order
```

---

## Artifact Best Practices

1. **Always use Parquet** (not CSV) - 10-100x smaller, instant loading
2. **Document schema** - Update this README when creating new artifacts
3. **Use descriptive names** - `card_win_rates.parquet` > `analysis_v2.parquet`
4. **Save metadata** - Include date created, sample size used
5. **Version if needed** - `model_features_v2.parquet` for iterations

---

## File Sizes Reference

| File | Uncompressed | Parquet | Compression Ratio |
|------|-------------|---------|-------------------|
| battles.csv | 9.2 GB | ~1.4 GB | 6.5x |
| 10% sample | 920 MB | ~140 MB | 6.5x |
| Card stats | ~5 MB | ~100 KB | 50x |
| Feature matrix | ~800 MB | ~150 MB | 5.3x |

**Takeaway**: Parquet is essential for efficient storage and fast loading.
