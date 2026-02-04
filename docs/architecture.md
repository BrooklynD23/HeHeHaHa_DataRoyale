# Architecture Overview

## System Goals

DataRoyale is structured to support fast, repeatable analysis over a very large dataset (9.2GB CSV). The architecture prioritizes:

- **Scalable data access** (DuckDB + Parquet) without loading full CSV into memory.
- **Notebook-first analysis** for rapid exploration and presentation-ready insights.
- **Reusable modules** in `src/` for consistent feature engineering and visualization.
- **Artifact outputs** (Parquet/CSV/PNG) that support collaboration and presentation reuse.

## High-Level Components

```
Raw Data → DuckDB Views → Notebooks → Artifacts → Presentation
```

### 1) Data Layer

- **Primary raw data**: `battles.csv` (9.2GB, not committed to git)
- **Optimized format**: `battles.parquet` (generated via `convert_to_parquet.py`)
- **Sampling**: `create_sample.py` generates smaller Parquet subsets for iteration.

### 2) Access Layer (DuckDB)

- DuckDB is used to query large datasets without loading the full CSV into memory.
- Helper utilities in `src/duckdb_utils.py` create reusable views and query patterns.

### 3) Analysis Layer (Notebooks)

The numbered notebooks under `notebooks/` form the analysis pipeline:

- `00-setup-and-validation.ipynb`: environment checks + data access validation
- `01-data-profiling.ipynb`: schema review + missing data assessment
- `02-04.x`: EDA on battle metadata, cards, progression, and advanced meta
- `05-feature-engineering.ipynb`: model-ready features
- `06-modeling-deck-prediction.ipynb`: predictive modeling (logistic regression, random forest, XGBoost)
- `07-visualization-library.ipynb`: presentation-ready chart templates
- `08-final-insights-synthesis.ipynb`: storyline consolidation

### 4) Reusable Code (`src/`)

- **duckdb_utils.py**: standardized data access with format auto-detection.
- **feature_engineering.py**: feature creation logic reused across notebooks.
- **visualization.py**: consistent chart styling for presentation outputs.

### 5) Artifacts & Presentation

- `artifacts/`: Parquet/CSV outputs of intermediate results (card win rates, archetypes, model features).
- `presentation/`: exported figures and slide deck assets.

## Data Storage & Flow

```
Raw CSV
  └─ convert_to_parquet.py → battles.parquet
       └─ DuckDB queries + notebooks
            ├─ artifacts/*.parquet
            └─ presentation/figures/*.png
```

## Collaboration Support

- The team uses sample datasets (`artifacts/sample_battles_10pct.parquet`) for quick iteration.
- Notebook outputs are stored as Parquet for consistent sharing and reuse across notebooks.
