# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DataRoyale is a competitive data science project analyzing Clash Royale battle data for a presentation-based competition. The repository contains a large dataset (9.2GB `battles.csv`) with detailed battle records including player stats, card compositions, trophy changes, and match outcomes.

**Competition Goal**: Explore, clean, and analyze the dataset to deliver compelling, data-driven insights through an 8-minute presentation.

## Competition Context

### Deliverables
- **Presentation**: 8-minute slide deck + 2-4 minutes Q&A
- **Deadline**: Friday the 14th, 11:30 AM (email to ajsantos@cpp.edu)
- **Judging**: Friday the 14th, 12:15 PM start time
- **Results**: Friday the 14th, 3:30 PM

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

### Competition Strategy

**Analysis should prioritize**:
- **Storytelling over complexity**: Every analysis should support a narrative
- **Actionable insights**: Focus on findings that matter
- **Visual clarity**: Design visualizations for presentation slides
- **Balance depth and accessibility**: Technical rigor without jargon

## Environment Setup

The project uses Python 3.12+ with a virtual environment (`.venv`).

**Activate virtual environment:**
```bash
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Data Architecture

### Primary Dataset: battles.csv (9.2GB)

The CSV contains comprehensive battle records with 70+ columns including:
- **Battle metadata**: battleTime, arena.id, gameMode.id, average.startingTrophies
- **Winner data**: tag, startingTrophies, trophyChange, crowns, kingTowerHitPoints, princessTowersHitPoints, clan info
- **Loser data**: Same structure as winner
- **Card compositions**: 8 cards per player with IDs and levels (winner.card1.id through winner.card8.level, same for loser)
- **Deck statistics**: totalcard.level, troop.count, structure.count, spell.count, rarity counts, elixir.average

### Data Access Pattern

**CRITICAL**: Never load the full CSV into memory. The dataset is 9.2GB and will cause memory issues.

Use **DuckDB** for all data operations. DuckDB provides streaming access without loading data into RAM.

**Reference implementation** (`peek.py`):
```python
import duckdb
con = duckdb.connect()  # in-memory SQL engine
con.execute("""
  CREATE VIEW v AS
  SELECT * FROM read_csv_auto('battles.csv',
    SAMPLE_SIZE=-1,
    IGNORE_ERRORS=true,
    hive_partitioning=0
  );
""")
# Query the view, not the raw CSV
results = con.sql("SELECT * FROM v LIMIT 50").df()
```

## Common Commands

**Peek at dataset:**
```bash
python peek.py
```
This script shows:
- First 50 rows
- Schema with inferred types
- Total row count

**Start Jupyter for analysis:**
```bash
jupyter notebook
# or
jupyter lab
```

**Interactive Python with dataset:**
```python
import duckdb
con = duckdb.connect()
con.execute("CREATE VIEW battles AS SELECT * FROM read_csv_auto('battles.csv', SAMPLE_SIZE=-1, IGNORE_ERRORS=true)")

# Example queries
con.sql("SELECT COUNT(*) FROM battles").df()
con.sql("SELECT gameMode.id, COUNT(*) as count FROM battles GROUP BY gameMode.id").df()
con.sql("SELECT * FROM battles WHERE winner.trophyChange > 30 LIMIT 10").df()
```

## Development Guidelines

### Working with the Dataset

1. **Always use DuckDB** - Never use `pd.read_csv()` on battles.csv
2. **Create views** - Use `CREATE VIEW` for reusable queries
3. **Use .df() conversion** - Convert DuckDB results to pandas only for final analysis/visualization: `con.sql("...").df()`
4. **Filter early** - Apply WHERE clauses in SQL before converting to DataFrame
5. **Use LIMIT** - Test queries with LIMIT before running on full dataset

### Analysis Workflow

Typical pattern for new analysis:
1. Use DuckDB to filter/aggregate data (stays fast, low memory)
2. Convert small result set to pandas DataFrame
3. Use pandas/matplotlib/seaborn for visualization
4. Use scikit-learn for ML on processed datasets only

### Competition Workflow Recommendations

**Phase 1: Initial Exploration (Day 1-2)**
1. Run `python peek.py` to understand dataset structure
2. Identify data quality issues (nulls, outliers, inconsistencies)
3. Explore key dimensions:
   - Win rate patterns by trophy level, arena, game mode
   - Card usage frequency and win rates
   - Deck composition patterns (elixir cost, card types, rarities)
   - Meta shifts over time (if battleTime spans multiple periods)
4. Document interesting observations and potential story angles

**Phase 2: Deep Analysis (Day 3-4)**
1. Choose 2-3 compelling questions to investigate
2. Clean and prepare data for modeling
3. Build and validate models (if applicable)
4. Generate key visualizations for presentation
5. Validate findings and check for biases

**Phase 3: Presentation Development (Day 5)**
1. Craft narrative arc for 8-minute story
2. Create slide deck with clear visuals
3. Practice timing and delivery
4. Prepare for Q&A questions

**Key Questions to Explore**:
- What card combinations have the highest win rates?
- How does deck composition affect win probability at different trophy levels?
- What's the "meta" deck archetype? Is there a counter-meta?
- How do average elixir costs correlate with success?
- Are there unexpected patterns in tower damage vs. match outcomes?
- Can we predict match outcomes based on deck composition alone?

### Column Access

Column names use dot notation (e.g., `winner.tag`, `arena.id`). In DuckDB queries, quote these:
```sql
SELECT "winner.tag", "arena.id", "winner.card1.id" FROM battles
```

Or use backticks:
```sql
SELECT `winner.tag`, `arena.id` FROM battles
```

## Visualization Best Practices for Competition

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

## Tech Stack

- **DuckDB**: Primary data processing engine (streaming SQL over large CSV)
- **Pandas**: Data manipulation for small-to-medium result sets
- **NumPy**: Numerical operations
- **Matplotlib/Seaborn/Plotly**: Visualization
- **SciPy/Statsmodels**: Statistical analysis
- **Scikit-learn**: Machine learning
- **Jupyter**: Interactive development and notebooks
