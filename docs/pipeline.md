# Pipeline: Data Cleaning → Modeling → Presentation

This document describes the end-to-end workflow, including design choices and the modeling strategy.

## 1) Data Ingestion & Validation

**Inputs**:
- `battles.csv` (raw dataset)
- Optional `battles.parquet` (optimized dataset)

**Actions**:
- Use DuckDB to create views over CSV/Parquet to avoid full in-memory loads.
- Validate the dataset shape, schema, and file paths in `00-setup-and-validation.ipynb`.

**Effect**: Ensures large data can be queried safely on commodity hardware while keeping early checks reproducible.

## 2) Data Profiling & Cleaning

**Actions**:
- Profile column types and missing values in `01-data-profiling.ipynb`.
- Establish basic data quality expectations (null checks, distributions, and row counts).
- Use sampling (`create_sample.py`) to reduce iteration time while preserving distribution trends.

**Effect**: Identifies data gaps early and enables faster analysis cycles without sacrificing overall trends.

## 3) Exploratory Analysis & Feature Definition

**Actions**:
- EDA notebooks (`02`–`04.5`) explore card win rates, synergies, trophy brackets, and progression patterns.
- `05-feature-engineering.ipynb` produces model-ready features such as deck composition stats, trophy differences, and engineered archetype indicators.

**Effect**: Establishes a defensible set of predictors and explanatory signals used in modeling and presentation narratives.

## 4) Modeling Strategy & Effects

**Goal**: Predict battle outcomes using deck composition and related features.

**Models in `06-modeling-deck-prediction.ipynb`**:
1. **Logistic Regression** (baseline)
2. **Random Forest** (non-linear relationships + feature importance)
3. **XGBoost** (higher-performing gradient boosting, GPU-capable)

**Metrics**: Accuracy, precision/recall, ROC-AUC, and feature importance.

**Effects & Tradeoffs**:
- **Logistic Regression** provides a quick, interpretable baseline and helps validate that features carry signal.
- **Random Forest** captures non-linear interactions and yields feature importance for storytelling.
- **XGBoost** targets stronger predictive performance at the cost of higher compute and more tuning overhead.

This tiered approach supports both **technical rigor** (multiple models + evaluation) and **storytelling** (feature importance informs insights).

## 5) Visualization & Presentation

**Actions**:
- `07-visualization-library.ipynb` standardizes styling for presentation-ready plots.
- `08-final-insights-synthesis.ipynb` consolidates key findings into a narrative arc.
- Final figures are exported to `presentation/figures/` and used in slides.

**Effect**: Ensures visuals are consistent, readable, and aligned with the judging rubric’s emphasis on clarity and storytelling.

## Design Choices (Summary)

| Decision | Why | Effect |
| --- | --- | --- |
| DuckDB for data access | Stream large CSV/Parquet without loading into RAM | Enables analysis on laptops and Colab; faster queries |
| Parquet conversion | Columnar compression + faster reads | 10–50x faster analytics on repeated queries |
| Sampling workflow | Lower iteration cost | Faster notebook turnaround while keeping trends |
| Notebook pipeline | Rapid exploration + collaboration | Clear stages from setup → modeling → narrative |
| Multi-model evaluation | Balance interpretability and performance | Stronger technical rigor + better storytelling |
