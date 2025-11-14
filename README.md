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

### Phase 1: Setup & Exploration 
1. Run `00-setup-and-validation.ipynb` - Verify environment
2. Run `01-data-profiling.ipynb` - Understand data quality
3. Generate sample: `python create_sample.py`
4. Upload sample to Google Drive for team access

### Phase 2: Analysis 
1. Work on trophy range patterns (notebook 2)
2. Work on card win rates and synergy (notebook 3)
3. Work on trophy walls (blockage) and skills progression (notebook 4)
4. Do feature engineering to prepare for modeling (predicting who will win based on their cards combinations)  (notebook 5)

**Our group used Discord to share findings with each others in group chat**

### Phase 3: Modeling & Visualization
1. Build predictive model (notebook 6)
2. Create presentation charts (notebook 7)
3. Export figures to `presentation/figures/` (We used Google Drive to save figures and used them in presentation later.)

### Phase 4: Presentation
1. Review and consolidate our story (what makes a champion wins the matches) (skills or money) 
2. Create Google Slide
3. Present our findings and sliding to Megan Bee (president of DS&AI club)  
4. Email source code to ajsantos@cpp.edu by **11:30 AM**

## Key Technical Details

### Working with Large CSV

We chose not loading the data to local memory. We chose to use DuckDB:

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

**Own team decided that each person will owns and work on specific notebooks to avoid conflicts.**

### Accessing Custom Utilities

```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), '..', 'src'))

from duckdb_utils import get_connection, query_to_df
from feature_engineering import create_matchup_features
from visualization import setup_presentation_style
```


