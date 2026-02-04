# Setup and Run Guide for Notebook 03

## Quick Start (5 minutes)

### 1. Install Required Packages

```bash
cd /mnt/c/Users/Danny/Documents/GitHub/HeHeHaHa_DataRoyale

# Install pip if needed
sudo apt-get update
sudo apt-get install python3-pip

# Install all dependencies
pip3 install -r requirements.txt

# Or install individually if needed:
pip3 install duckdb pandas numpy matplotlib seaborn jupyter
```

### 2. Launch Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# This will open in your browser. Navigate to:
# notebooks/03-eda-card-analysis.ipynb
```

### 3. Run the Notebook

**Option A: Run All Cells**
- Click "Cell" → "Run All"
- Wait ~10-15 minutes for completion

**Option B: Run Cell-by-Cell**
- Press `Shift + Enter` to run each cell
- Review outputs as you go

---

## What's Already Implemented

### ✅ Working Cells

1. **Cell 0**: Title and overview
2. **Cell 1**: Imports and setup
3. **Cell 2**: Helper functions (card name mapping, trophy brackets)
4. **Cell 3**: Global card win rates + visualizations
5. **Cell 5**: Global 2-card synergy analysis + lift metrics
6. **Cell 6**: Trophy-bracket section header
7. **Cell 7**: Card win rates by trophy bracket
8. **Cells 9-12**: Deck clustering, elixir analysis
9. **Cell 14**: Save artifacts

### ⚠️ Known Issues

- **Cells 4 and 8 are duplicates** - safe to ignore/delete
- Some cells may show errors if run out of order
- First run will be slower (DuckDB query compilation)

---

## Expected Runtime

| Section | Time | Notes |
|---------|------|-------|
| Setup & Imports | 10s | Fast |
| Global Card Win Rates | 2-3 min | 16 UNION ALL operations |
| Global Synergy Analysis | 3-5 min | 28 pair combinations |
| Trophy-Bracket Win Rates | 3-5 min | 8 brackets × 16 operations |
| Deck Clustering | 30s | Sample-based (100k decks) |
| Elixir Analysis | 30s | Aggregations |
| **TOTAL** | **10-15 min** | Full notebook |

---

## Outputs You'll Get

### Artifacts Created

All saved to `artifacts/` directory:

1. ✅ `card_win_rates.parquet` - Global card statistics
2. ✅ `top_synergy_pairs.parquet` - Top 100 card pairs
3. ✅ `elixir_analysis.parquet` - Elixir cost analysis
4. ✅ `card_win_rates_by_bracket.parquet` - Trophy-segmented card stats

### Visualizations

**Card Win Rates (4 panels)**:
- Top 20 cards by win rate
- Bottom 20 cards by win rate
- Win rate distribution
- Usage vs win rate scatter

**Card Synergy (4 panels)**:
- Top 20 synergy pairs
- Lift metric distribution
- Expected vs actual win rates
- Usage vs lift scatter

**Trophy-Bracket Analysis (8 panels)**:
- Top 10 cards per trophy bracket (0-1k through 7k+)
- Shows meta evolution across skill levels

**Deck Clustering (4 panels)**:
- Cluster scatter plot
- Archetype distribution
- Win rate by archetype
- Elixir cost by cluster

**Elixir Analysis (4 panels)**:
- Battle distribution by elixir
- Trophy gain by elixir
- Trophy gain box plots
- Average crowns by elixir

---

## Key Insights You'll Discover

### 1. Card Balance Issues
- **Question**: Are any cards too strong or too weak?
- **Answer**: Cards with >52% or <48% win rate + high usage

### 2. Synergy Patterns
- **Question**: Which card combos have highest win rates?
- **Answer**: Pairs with Lift > 1.1 (positive synergy)

### 3. Meta Shifts by Trophy Range
- **Question**: Do different cards dominate at different skill levels?
- **Answer**: Compare top cards across 0-1k vs 7k+ brackets

### 4. Optimal Deck Building
- **Question**: What's the ideal elixir cost?
- **Answer**: Sweet spot shown in elixir analysis

### 5. Deck Archetypes
- **Question**: Which playstyle wins most?
- **Answer**: Beatdown/Cycle/Control win rate comparison

---

## Troubleshooting

### Error: "No module named 'duckdb'"
```bash
pip3 install duckdb pandas numpy matplotlib seaborn
```

### Error: "battles.parquet not found"
```bash
# Make sure battles.parquet exists in project root
ls -lh battles.parquet

# If only battles.csv exists, DuckDB will use it (slower)
```

### Error: "cards.json not found"
```bash
# Verify artifacts/cards.json exists
ls -lh artifacts/cards.json
```

### Kernel Dies / Out of Memory
- Close other applications
- Run cells individually instead of "Run All"
- Comment out clustering section (cells 9-10) if needed

### Slow Performance
- ✅ Using `battles.parquet`: ~10-15 min total
- ❌ Using `battles.csv`: ~30-60 min total
- Check which file is being used in Cell 1 output

---

## Optional Enhancements (Not Yet Added)

If you want to extend the analysis:

### Add 2-Card Synergy by Trophy Bracket

Insert after Cell 7:

```python
# Calculate 2-card synergy by trophy bracket
print("Analyzing card pair synergies across trophy brackets...")
# ... (code available in implementation notes)
```

**Runtime**: +10-15 minutes
**Value**: Shows how synergies evolve across skill levels

### Add 3-Card Synergy Analysis

Insert after 2-card synergy:

```python
# Calculate 3-card combinations (C(8,3) = 56 per deck)
print("Analyzing triple-card synergies...")
# ... (code available)
```

**Runtime**: +15-20 minutes
**Value**: Identifies dominant triple combos in high-level meta

---

## For Your Presentation

### What's Ready Now

After running the notebook, you'll have:

✅ **Slide 1**: Card win rate distribution (identify balance issues)
✅ **Slide 2**: Top synergy pairs (deck building recommendations)
✅ **Slide 3**: Trophy-bracket meta analysis (skill-based insights)
✅ **Slide 4**: Optimal elixir cost (player guidance)
✅ **Slide 5**: Deck archetype performance (playstyle recommendations)

### Talking Points

1. **Data-Driven Balance**
   - "X cards exceed 52% win rate with high usage → potential nerfs"
   - "Y cards below 48% win rate → need buffs"

2. **Synergy Discovery**
   - "Card A + Card B has 1.15x lift → powerful combo"
   - "Card C + Card D has 0.85x lift → avoid pairing"

3. **Meta Evolution**
   - "At 2k-3k trophies, Card X dominates"
   - "At 7k+, Card Y takes over → skill-dependent meta"

4. **Actionable Insights**
   - "Optimal elixir: 3.5-4.0 for trophy pushing"
   - "Beatdown archetype has highest win rate"

---

## Next Steps After Running

1. ✅ Review all visualizations
2. ✅ Export key charts for slides (right-click → Save Image)
3. ✅ Copy insights to presentation notes
4. ✅ Practice 8-minute walkthrough
5. ✅ Prepare for Q&A (judges may ask about methodology)

---

## Competition Judging Criteria Alignment

Your analysis addresses all 5 criteria:

1. **Clarity & Storytelling** ✅
   - Clear narrative: Balance → Synergy → Meta Evolution

2. **Data Understanding** ✅
   - 9.2M rows analyzed
   - Trophy segmentation shows depth

3. **Technical Rigor** ✅
   - Lift metrics (expected vs actual win rates)
   - Statistical thresholds (>500 usage)
   - Proper aggregations

4. **Insights & Recommendations** ✅
   - Specific cards to buff/nerf
   - Deck building advice
   - Player progression guidance

5. **Visuals & Delivery** ✅
   - 20+ presentation-ready charts
   - Color-blind friendly palettes
   - Clear labels and titles

---

## GPU Acceleration Note

Your RTX 3080 was detected but:
- **DuckDB doesn't support CUDA** (CPU-only)
- Uses multi-core parallelization instead
- Performance is still excellent with Parquet format

If you wanted GPU acceleration, you'd need RAPIDS cuDF (major refactor).

---

## Contact / Questions

If you hit issues:
1. Check error message carefully
2. Verify all packages installed
3. Confirm `battles.parquet` and `artifacts/cards.json` exist
4. Try running cells individually to isolate problem

Good luck with your presentation! 🎉
