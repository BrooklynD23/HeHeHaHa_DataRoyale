# DataRoyale - Clash Royale Data Analysis Competition

**Competition**: Data Science Presentation Competition
**Deadline**: Friday the 14th, 11:30 AM
**Judging**: Friday the 14th, 12:15 PM
**Format**: 8-minute presentation + 2-4 min Q&A

## Quick Start

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

### 2. Create Sample Dataset

The full `battles.csv` is 9.2GB - too large to load into memory. Create a 10% sample for fast iteration:

```bash
python create_sample.py --pct 10
```

This creates `artifacts/sample_battles_10pct.parquet` (~920MB) that loads instantly.

### 3. Start Jupyter

```bash
jupyter notebook
# or
jupyter lab
```

Then open notebooks in order: `00-setup-and-validation.ipynb` → `01-data-profiling.ipynb` → etc.

## For Google Colab Users

### Option 1: Use Google Drive (Recommended for team)

1. Upload `battles.csv` to Google Drive folder: `/MyDrive/DataRoyale/`
2. Upload generated `artifacts/*.parquet` files to same folder
3. In Colab notebooks, uncomment the Drive mounting section:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

### Option 2: Use Sample Dataset

1. Generate sample locally: `python create_sample.py`
2. Upload `artifacts/sample_battles_10pct.parquet` to Colab (faster than full CSV!)
3. Work with sample for EDA and modeling

## Project Structure

```
DataRoyale/
├── battles.csv                    # 9.2GB raw data (NOT in git)
├── peek.py                        # Quick data inspection
├── create_sample.py               # Generate Parquet samples
│
├── notebooks/                     # Jupyter notebooks (numbered workflow)
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
├── src/                           # Reusable Python modules
│   ├── duckdb_utils.py           # Data access helpers
│   ├── feature_engineering.py    # Feature creation functions
│   └── visualization.py          # Presentation-ready charts
│
├── artifacts/                     # Intermediate data (shared via Drive)
│   ├── sample_battles_10pct.parquet
│   ├── card_win_rates.parquet    # Created in notebook 03
│   ├── deck_archetypes.parquet   # Created in notebook 03
│   └── model_features.parquet    # Created in notebook 05
│
└── presentation/                  # Final deliverables
    ├── figures/                   # Exported charts (PNG)
    └── slides.pptx               # Final presentation deck
```

## Workflow

### Phase 1: Setup & Exploration (Day 1)
1. Run `00-setup-and-validation.ipynb` - Verify environment
2. Run `01-data-profiling.ipynb` - Understand data quality
3. Generate sample: `python create_sample.py`
4. Upload sample to Google Drive for team access

### Phase 2: Analysis (Days 2-3)
**Divide and conquer** - assign notebooks to team members:
- **Person 1**: `02-eda-battle-metadata.ipynb` (arenas, trophy patterns)
- **Person 2**: `03-eda-card-analysis.ipynb` (card win rates, synergy)
- **Person 3**: `04-eda-player-progression.ipynb` (trophy walls, skill)
- **Person 4**: `05-feature-engineering.ipynb` (prepare data for modeling)

**Daily sync**: Share findings in group chat, identify top insights

### Phase 3: Modeling & Visualization (Day 4)
1. Run `06-modeling-deck-prediction.ipynb` - Build predictive model
2. Run `07-visualization-library.ipynb` - Create presentation charts
3. Export figures to `presentation/figures/`

### Phase 4: Presentation (Day 5 - Friday)
1. Run `08-final-insights-synthesis.ipynb` - Consolidate story
2. Create slide deck (PowerPoint/Google Slides)
3. Practice presentation (aim for 7:30 to leave buffer)
4. Email to ajsantos@cpp.edu by **11:30 AM**

## Key Technical Details

### Working with Large CSV

**NEVER** load full CSV into memory! Always use DuckDB:

```python
import duckdb
con = duckdb.connect()

con.execute("""
    CREATE VIEW battles AS
    SELECT * FROM read_csv_auto('battles.csv',
        SAMPLE_SIZE=-1,
        IGNORE_ERRORS=true
    )
""")

# Query the view, get pandas DataFrame
result = con.sql("SELECT * FROM battles LIMIT 100").df()
```

### Notebook Collaboration

We use **jupytext** to avoid merge conflicts:

```bash
# Pair notebooks with .py files (auto-generated)
jupytext --set-formats ipynb,py:percent notebooks/*.ipynb

# Git commits the .py version (readable diffs)
# .ipynb stays local for execution
```

**Best practice**: Each person owns specific notebooks to avoid conflicts.

### Accessing Custom Utilities

```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), '..', 'src'))

from duckdb_utils import get_connection, query_to_df
from feature_engineering import create_matchup_features
from visualization import setup_presentation_style
```

## Competition Judging Criteria

Your presentation will be scored on:

1. **Clarity and Storytelling** (20%) - Coherent narrative, accessible to non-technical audience
2. **Data Understanding** (20%) - Meaningful insights beyond surface-level
3. **Technical Rigor** (20%) - Appropriate methods, proper validation
4. **Insights & Recommendations** (20%) - Actionable, data-backed conclusions
5. **Visuals & Delivery** (20%) - Clear charts, professional presentation

**Pro tips**:
- Lead with the "So what?" - make every insight matter
- Use contrast: "Most players do X, but winners do Y 23% more often"
- Acknowledge limitations (shows maturity)
- Practice timing: 8 minutes is shorter than you think!

## Troubleshooting

**Problem**: `battles.csv not found`
**Solution**: Ensure CSV is in project root. Check path with `os.path.exists('battles.csv')`

**Problem**: Out of memory errors
**Solution**: Never use `pd.read_csv()` on full file. Use DuckDB views or sample dataset.

**Problem**: Notebook won't import custom modules
**Solution**: Add src/ to path (see notebooks for example code)

**Problem**: Git merge conflicts in .ipynb files
**Solution**: Use jupytext to commit .py versions instead

**Problem**: Colab runs slow with Drive mounting
**Solution**: Copy Parquet files to Colab runtime disk first, then load from local path

## Resources

- **CLAUDE.md**: Detailed technical documentation
- **Competition brief**: `docs/judging_rubric.md`
- **Artifact schemas**: `artifacts/README.md`
- **Visualization examples**: `src/visualization.py`

## Team Communication

- **Daily standup**: 15 min sync
  - What did you create yesterday? (artifacts)
  - What are you exploring today?
  - Any blockers?

- **Shared resources**:
  - Google Drive: `/DataRoyale/artifacts/` (intermediate files)
  - GitHub: Version-controlled notebooks
  - Slack/Discord: Quick questions

## Final Checklist

Before submission (Friday 11:30 AM):
- [ ] All visualizations exported as high-res PNGs
- [ ] Slide deck created (8 slides recommended)
- [ ] Every claim backed by specific statistics
- [ ] Slides readable from 20 feet (font 18+)
- [ ] Story flows logically (problem → insights → impact)
- [ ] Practiced delivery to 7:30
- [ ] Prepared Q&A answers
- [ ] Emailed to ajsantos@cpp.edu

**Good luck! Go tell a great data story.**
