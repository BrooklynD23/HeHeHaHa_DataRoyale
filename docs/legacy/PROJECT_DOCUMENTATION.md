# DataRoyale - Complete Project Documentation

**Competition**: Data Science Presentation Competition  
**Deadline**: Friday the 14th, 11:30 AM  
**Judging**: Friday the 14th, 12:15 PM  
**Format**: 8-minute presentation + 2-4 min Q&A

---

## Table of Contents

1. [Quick Start Guide](#quick-start-guide)
2. [Project Overview](#project-overview)
3. [Data Architecture & Why Parquet](#data-architecture--why-parquet)
4. [Notebooks Guide](#notebooks-guide)
5. [Development Guidelines](#development-guidelines)
6. [Competition Strategy](#competition-strategy)
7. [Tools & Scripts](#tools--scripts)
8. [Technical Reference](#technical-reference)

---

## Quick Start Guide

### 1. Environment Setup (Local)

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install/update dependencies
pip install -r requirements.txt

# Verify setup
python peek.py
```

### 2. Convert CSV to Parquet (Recommended)

The project now uses **Parquet format** for faster queries (10-50x faster than CSV):

```bash
# One-time conversion (takes 5-15 minutes)
python convert_to_parquet.py

# This creates battles.parquet (~1-2GB, compressed from 9.2GB CSV)
# All scripts and notebooks automatically use Parquet if available
```

### 3. Create Sample Dataset

For fast iteration during development:

```bash
python create_sample.py --pct 10
```

This creates `artifacts/sample_battles_10pct.parquet` (~920MB) that loads instantly.

### 4. Start Jupyter

```bash
jupyter notebook
# or
jupyter lab
```

Then open notebooks in order: `00-setup-and-validation.ipynb` → `01-data-profiling.ipynb` → etc.

---

## Project Overview

DataRoyale is a competitive data science project analyzing Clash Royale battle data for a presentation-based competition. The repository contains a large dataset (9.2GB `battles.csv` or ~1-2GB `battles.parquet`) with detailed battle records including player stats, card compositions, trophy changes, and match outcomes.

**Competition Goal**: Explore, clean, and analyze the dataset to deliver compelling, data-driven insights through an 8-minute presentation.

### Project Structure

```
DataRoyale/
├── battles.parquet              # Primary dataset (Parquet format, recommended)
├── battles.csv                 # Original dataset (CSV format, fallback)
├── peek.py                     # Quick data inspection
├── convert_to_parquet.py       # Convert CSV to Parquet
├── create_sample.py            # Generate Parquet samples
├── id_to_name.py               # Convert card IDs to names
│
├── notebooks/                   # Jupyter notebooks (numbered workflow)
│   ├── 00-setup-and-validation.ipynb
│   ├── 01-data-profiling.ipynb
│   ├── 02-eda-battle-metadata.ipynb
│   ├── 03-eda-card-analysis.ipynb
│   ├── 04-eda-player-progression.ipynb
│   ├── 05-feature-engineering.ipynb
│   ├── 06-modeling-deck-prediction.ipynb
│   ├── 07-visualization-library.ipynb
│   └── 08-final-insights-synthesis.ipynb
│
├── src/                         # Reusable Python modules
│   ├── duckdb_utils.py          # Data access helpers (auto-detects Parquet)
│   ├── feature_engineering.py  # Feature creation functions
│   └── visualization.py        # Presentation-ready charts
│
├── Datasets/                    # Data files
│   ├── cards.json              # Card ID to name mapping
│   └── battles_with_names.csv  # Output from id_to_name.py
│
├── artifacts/                   # Intermediate data
│   ├── sample_battles_10pct.parquet
│   ├── card_win_rates.parquet
│   ├── deck_archetypes.parquet
│   └── model_features.parquet
│
└── presentation/                # Final deliverables
    ├── figures/                 # Exported charts (PNG)
    └── slides.pptx              # Final presentation deck
```

---

## Data Architecture & Why Parquet

### Primary Dataset

The dataset contains comprehensive battle records with 70+ columns including:
- **Battle metadata**: battleTime, arena.id, gameMode.id, average.startingTrophies
- **Winner data**: tag, startingTrophies, trophyChange, crowns, kingTowerHitPoints, princessTowersHitPoints, clan info
- **Loser data**: Same structure as winner
- **Card compositions**: 8 cards per player with IDs and levels (winner.card1.id through winner.card8.level, same for loser)
- **Deck statistics**: totalcard.level, troop.count, structure.count, spell.count, rarity counts, elixir.average

### Why Parquet Instead of CSV?

**Parquet Advantages:**
- ✅ **10-50x faster** for repeated queries
- ✅ **5-10x smaller** file size (9.2GB CSV → ~1-2GB Parquet)
- ✅ **Type information stored** (no inference needed)
- ✅ **Columnar format** (perfect for analytical queries)
- ✅ **Industry standard** (used by pandas, Spark, BigQuery)

**The project automatically uses Parquet if available**, falling back to CSV if not found. All utilities (`duckdb_utils.py`, `peek.py`, etc.) auto-detect and use the best format.

### Why DuckDB?

**DuckDB is perfect for this project because:**
1. **No conversion needed** - Can query CSV/Parquet directly
2. **Fast analytical queries** - Optimized for aggregations, GROUP BY, JOINs
3. **Memory efficient** - Streams data, doesn't load full file into RAM
4. **Zero setup** - No server, just `import duckdb`

**Data Access Pattern:**

```python
import duckdb
from src.duckdb_utils import get_connection, create_battles_view

# Create connection
con = get_connection()

# Create view (automatically uses Parquet if available, falls back to CSV)
create_battles_view(con, 'battles.parquet')  # or 'battles.csv'

# Query the view
result = con.sql("SELECT COUNT(*) FROM battles").df()
```

**CRITICAL**: Never load the full dataset into memory with `pd.read_csv()`. Always use DuckDB views.

---

## Notebooks Guide

The notebooks are designed to be run in sequence, building upon each other's outputs:

```
00 (Setup) → 01 (Profiling) → 02-04 (EDA) → 05 (Features) → 06 (Modeling) → 07 (Viz) → 08 (Synthesis)
```

### 00 - Setup and Validation
**Purpose**: Verify environment setup and establish data access

**What it does**:
- Checks Python version and installed packages
- Configures file paths (local or Google Colab)
- Verifies dataset exists and shows file size
- Creates DuckDB connection for efficient data access
- Creates a view over the dataset (streaming, no full load into memory)
- Performs basic validation (row count, schema, sample queries)

**When to run**: First thing, before any analysis

### 01 - Data Profiling
**Purpose**: Understand data quality and identify issues

**What it does**:
- Analyzes missing values (null counts and percentages)
- Validates data types
- Detects outliers (extreme trophy values, invalid card levels)
- Examines distributions (trophies, arenas, game modes)
- Creates data quality report

**When to run**: After setup, before deep analysis

### 02 - EDA: Battle Metadata
**Purpose**: Explore battle-level patterns across arenas, game modes, and trophy levels

**Key Questions**:
- How are battles distributed across arenas?
- Do win rates vary by trophy level?
- Are certain game modes more popular?
- What's the average trophy change per battle?

**When to run**: Early exploration phase

### 03 - EDA: Card Analysis
**Purpose**: Analyze individual cards and deck compositions

**Key Questions**:
- Which cards have the highest win rates?
- Are evolution cards dominant?
- What card pairs appear together frequently (synergy)?
- How does rarity affect win rates?

**When to run**: After understanding battle patterns

### 04 - EDA: Player Progression
**Purpose**: Understand trophy progression patterns and player skill development

**Key Questions**:
- Where do players hit trophy "walls"?
- How do deck characteristics change with trophy level?
- What separates winners from losers at different skill levels?

**When to run**: After card analysis

### 05 - Feature Engineering
**Purpose**: Create derived features for modeling and deeper analysis

**Features Created**:
- Matchup features (trophy diff, elixir diff, card level diff)
- Deck complexity scores
- Archetype indicators (Beatdown, cycle, spell-heavy flags)
- Card synergy scores
- Trophy bracket categorical variables

**When to run**: After EDA, before modeling

### 06 - Modeling: Deck Prediction
**Purpose**: Build predictive models for technical rigor scoring

**Goal**: Predict battle outcomes based on deck composition alone

**Benchmark**: Previous research achieved **56.94% accuracy** - aim to beat this!

**Models**: Logistic Regression, Random Forest, XGBoost

**When to run**: After feature engineering

### 07 - Visualization Library
**Purpose**: Create publication-quality charts for the presentation

**What it does**:
- Generates 5-8 compelling visualizations
- Uses presentation-ready styling (large fonts, colorblind-friendly palettes)
- Exports high-resolution PNGs for slides

**When to run**: After modeling, before presentation

### 08 - Final Insights Synthesis
**Purpose**: Consolidate all findings into a coherent story for the presentation

**What it does**:
- Synthesizes insights from all previous notebooks
- Creates presentation structure (8-minute format)
- Documents key findings with supporting data
- Identifies actionable recommendations

**When to run**: Final step before presentation

---

## Development Guidelines

### Working with the Dataset

1. **Always use DuckDB** - Never use `pd.read_csv()` on the full dataset
2. **Use Parquet format** - Convert CSV to Parquet for 10-50x faster queries
3. **Create views** - Use `CREATE VIEW` for reusable queries
4. **Use .df() conversion** - Convert DuckDB results to pandas only for final analysis/visualization
5. **Filter early** - Apply WHERE clauses in SQL before converting to DataFrame
6. **Use LIMIT** - Test queries with LIMIT before running on full dataset

### Analysis Workflow

Typical pattern for new analysis:
1. Use DuckDB to filter/aggregate data (stays fast, low memory)
2. Convert small result set to pandas DataFrame
3. Use pandas/matplotlib/seaborn for visualization
4. Use scikit-learn for ML on processed datasets only

### Column Access

Column names use dot notation (e.g., `winner.tag`, `arena.id`). In DuckDB queries, quote these:

```sql
SELECT "winner.tag", "arena.id", "winner.card1.id" FROM battles
```

Or use backticks:

```sql
SELECT `winner.tag`, `arena.id` FROM battles
```

---

## Competition Strategy

### Judging Criteria

Your work will be evaluated across five categories:

1. **Clarity and Storytelling** (Non-technical accessibility)
   - Coherent narrative: problem → insight → impact
   - Concise, clear, engaging presentation
   - Understandable for general audience

2. **Data Understanding and Exploration**
   - Meaningful insights beyond surface-level observations
   - Acknowledgment of data limitations or biases
   - Depth of analysis

3. **Modeling and Technical Rigor**
   - Appropriate analytical/modeling techniques
   - Proper validation and evaluation (metrics, train/test splits)
   - Demonstrated real-world application

4. **Insights and Recommendations**
   - Actionable conclusions supported by data
   - Connection to real-world decisions, strategies, or impact
   - Business or social relevance

5. **Visuals and Delivery**
   - Clear, well-labeled charts and graphs
   - Readable fonts, good color contrast
   - Confident, professional delivery

### Analysis Priorities

**Analysis should prioritize**:
- **Storytelling over complexity**: Every analysis should support a narrative
- **Actionable insights**: Focus on findings that matter
- **Visual clarity**: Design visualizations for presentation slides
- **Balance depth and accessibility**: Technical rigor without jargon

### Workflow Recommendations

**Phase 1: Initial Exploration (Day 1-2)**
1. Run `python peek.py` to understand dataset structure
2. Convert CSV to Parquet: `python convert_to_parquet.py`
3. Run `00-setup-and-validation.ipynb` and `01-data-profiling.ipynb`
4. Generate sample: `python create_sample.py`
5. Explore key dimensions and document observations

**Phase 2: Deep Analysis (Days 2-3)**
**Divide and conquer** - assign notebooks to team members:
- **Person 1**: `02-eda-battle-metadata.ipynb` (arenas, trophy patterns)
- **Person 2**: `03-eda-card-analysis.ipynb` (card win rates, synergy)
- **Person 3**: `04-eda-player-progression.ipynb` (trophy walls, skill)
- **Person 4**: `05-feature-engineering.ipynb` (prepare data for modeling)

**Daily sync**: Share findings in group chat, identify top insights

**Phase 3: Modeling & Visualization (Day 4)**
1. Run `06-modeling-deck-prediction.ipynb` - Build predictive model
2. Run `07-visualization-library.ipynb` - Create presentation charts
3. Export figures to `presentation/figures/`

**Phase 4: Presentation (Day 5 - Friday)**
1. Run `08-final-insights-synthesis.ipynb` - Consolidate story
2. Create slide deck (PowerPoint/Google Slides)
3. Practice presentation (aim for 7:30 to leave buffer)
4. Email to ajsantos@cpp.edu by **11:30 AM**

### Key Questions to Explore

- What card combinations have the highest win rates?
- How does deck composition affect win probability at different trophy levels?
- What's the "meta" deck archetype? Is there a counter-meta?
- How do average elixir costs correlate with success?
- Are there unexpected patterns in tower damage vs. match outcomes?
- Can we predict match outcomes based on deck composition alone?

---

## Tools & Scripts

### peek.py
Quick data inspection script. Automatically uses Parquet if available.

```bash
python peek.py
```

Shows:
- First 50 rows
- Schema with inferred types
- Total row count

### convert_to_parquet.py
Convert battles.csv to Parquet format for faster queries.

```bash
python convert_to_parquet.py
```

**One-time conversion** (takes 5-15 minutes):
- Creates `battles.parquet` (~1-2GB, compressed from 9.2GB CSV)
- All scripts automatically use Parquet if available
- 10-50x faster queries after conversion

### create_sample.py
Generate a stratified sample of the dataset for faster iteration.

```bash
python create_sample.py --pct 10
```

Creates `artifacts/sample_battles_10pct.parquet` (~920MB) that loads instantly.

### id_to_name.py
Convert Clash Royale card IDs to human-readable card names.

```bash
python id_to_name.py
```

**Automatically finds files** in `Datasets/` folder:
- Reads `Datasets/cards.json` to build ID-to-name mapping
- Processes `Datasets/battles.csv` (or battles.parquet if available)
- Creates `Datasets/battles_with_names.csv` with added name columns

**Preserves all original columns** and adds new `*_name` columns:
- Original: `winner.card1.id` → New: `winner.card1.name`
- And so on for all 8 cards per player (16 total new columns)

---

## Technical Reference

### Visualization Best Practices

**For presentation slides**:
- Use **Seaborn** or **Plotly** for publication-quality plots
- Increase font sizes (title: 16-18pt, labels: 14-16pt, ticks: 12-14pt)
- Choose colorblind-friendly palettes (`sns.color_palette("colorblind")`)
- Label axes clearly with units
- Add informative titles that state the insight
- Remove chart junk (unnecessary gridlines, borders)
- Use annotations to highlight key findings

**Example visualization setup**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for presentation
sns.set_style("whitegrid")
sns.set_context("talk")  # Larger fonts for presentations
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 14
```

**Chart types by use case**:
- **Win rate comparisons**: Horizontal bar charts (easier to read labels)
- **Distributions**: Violin plots, box plots, or histograms
- **Trends over time**: Line charts with confidence intervals
- **Relationships**: Scatter plots with regression lines
- **Compositions**: Stacked bar charts or pie charts (use sparingly)
- **Correlations**: Heatmaps with annotations

### Tech Stack

- **DuckDB**: Primary data processing engine (streaming SQL over Parquet/CSV)
- **Pandas**: Data manipulation for small-to-medium result sets
- **NumPy**: Numerical operations
- **Matplotlib/Seaborn/Plotly**: Visualization
- **SciPy/Statsmodels**: Statistical analysis
- **Scikit-learn**: Machine learning
- **Jupyter**: Interactive development and notebooks

### Common Commands

**Peek at dataset:**
```bash
python peek.py
```

**Start Jupyter for analysis:**
```bash
jupyter notebook
# or
jupyter lab
```

**Interactive Python with dataset:**
```python
import duckdb
from src.duckdb_utils import get_connection, create_battles_view

con = get_connection()
create_battles_view(con, 'battles.parquet')  # Auto-detects Parquet

# Example queries
con.sql("SELECT COUNT(*) FROM battles").df()
con.sql("SELECT gameMode.id, COUNT(*) as count FROM battles GROUP BY gameMode.id").df()
con.sql("SELECT * FROM battles WHERE winner.trophyChange > 30 LIMIT 10").df()
```

### For Google Colab Users

**Option 1: Use Google Drive (Recommended for team)**
1. Upload `battles.parquet` to Google Drive folder: `/MyDrive/DataRoyale/`
2. Upload generated `artifacts/*.parquet` files to same folder
3. In Colab notebooks, uncomment the Drive mounting section

**Option 2: Use Sample Dataset**
1. Generate sample locally: `python create_sample.py`
2. Upload `artifacts/sample_battles_10pct.parquet` to Colab (faster than full dataset!)
3. Work with sample for EDA and modeling

---

## Summary

This project uses **Parquet format** for optimal performance:
- ✅ **10-50x faster** queries than CSV
- ✅ **5-10x smaller** file size
- ✅ **Automatic detection** - all scripts use Parquet if available
- ✅ **Easy conversion** - one command: `python convert_to_parquet.py`

All utilities automatically detect and use the best format, so you don't need to change your code - just convert once and enjoy faster queries!

---

**Last Updated**: After Parquet migration  
**Project Status**: Ready for analysis with optimized Parquet format


