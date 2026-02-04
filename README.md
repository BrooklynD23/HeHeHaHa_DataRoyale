# DataRoyale

DataRoyale is a competitive data science project analyzing Clash Royale battle data for a presentation-based competition. The repository contains notebooks, reusable Python modules, and supporting artifacts used to explore card performance, deck archetypes, and match outcomes.

## Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Quick dataset sanity check
python peek.py
```

If you have the full dataset available, you can generate Parquet files and a smaller sample for faster iteration:

```bash
python convert_to_parquet.py
python create_sample.py --pct 10
```

## Documentation Index

- **Project docs overview**: [`docs/README.md`](docs/README.md)
- **Architecture & system layout**: [`docs/architecture.md`](docs/architecture.md)
- **Pipeline (data cleaning → modeling → presentation)**: [`docs/pipeline.md`](docs/pipeline.md)
- **Documentation audit**: [`docs/documentation_audit.md`](docs/documentation_audit.md)
- **Judging rubric**: [`docs/judging_rubric.md`](docs/judging_rubric.md)
- **Why DuckDB**: [`docs/why_duckdb_and_alternatives.md`](docs/why_duckdb_and_alternatives.md)

## Repository Layout (High-Level)

```
.
├── notebooks/          # Numbered analysis workflow
├── src/                # Reusable Python modules
├── artifacts/          # Derived data outputs (Parquet, CSV)
├── presentation/       # Figures and slide deck
└── docs/               # Project documentation
```

## Notebook Workflow

The core analysis runs in order:

```
00 → 01 → 02 → 03 → 04 → 04.5 → 05 → 06 → 07 → 08
```

See the pipeline doc for details on the outputs and how each stage contributes to the final presentation.
