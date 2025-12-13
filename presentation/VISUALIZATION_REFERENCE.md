# Quick Visualization Reference Guide

## For Each Slide: Which Notebook Cell to Open

| Slide # | Finding | Visualization File | Notebook | Cell # | How to Access |
|---------|---------|-------------------|----------|--------|---------------|
| **1** | Title/Hook | Custom design | - | - | Create in PowerPoint |
| **2** | Dataset Overview | None (text only) | 00-setup-validation | - | Summary stats from notebook |
| **3** | Card Level Importance | `fig1_feature_importance.png` | **06-modeling-deck-prediction** | **Cell 9** | Already saved ✅ |
| **4** | Trophy Walls | `fig2_trophy_distribution.png` | **04-eda-player-progression** | **Cell 3** | Already saved ✅ |
| **4 (alt)** | Trophy Walls (detected) | `fig5_detected_walls.png` | **04.5-advanced-meta-analysis** | **Cell 6** | Already saved ✅ |
| **5** | Matchup Fairness | `fig_matchup_fairness.png` | **04-eda-player-progression** | **Cell 9** | Already saved ✅ |
| **6** | Deck Evolution | `fig_deck_evolution.png` | **04-eda-player-progression** | **Cell 7** | Already saved ✅ |
| **7** | Model Comparison | `fig4_model_comparison.png` | **06-modeling-deck-prediction** | **Cell 11** | Already saved ✅ |
| **7 (alt)** | Model Calibration | `fig_model_calibration.png` | **06-modeling-deck-prediction** | **Cell 10** | Already saved ✅ |
| **8** | Recommendations | None (summary) | - | - | Text-based slide |

---

## Verified Figures in presentation/figures/

```bash
✅ fig1_feature_importance.png     - XGBoost top 15 features (Card level diff = 27.83%)
✅ fig2_trophy_distribution.png    - Trophy clustering at 4k/5k/6k/7k walls
✅ fig4_model_comparison.png       - Accuracy & ROC-AUC for 3 models
✅ fig5_detected_walls.png         - Data-driven wall detection algorithm
✅ fig7_optimal_elixir.png         - Elixir cost vs win rate (backup slide)
✅ fig_deck_evolution.png          - 4-panel deck changes across trophy tiers
✅ fig_matchup_fairness.png        - 4-panel fairness analysis
✅ fig_model_calibration.png       - Calibration curves for all models
✅ fig_trophy_change_analysis.png  - Risk/volatility by trophy (backup)
```

All figures saved at **300 DPI** - presentation ready!

---

## How to Verify/Regenerate Any Figure

### Example: Feature Importance (Slide 3)

1. **Open Jupyter:**
   ```bash
   jupyter notebook
   ```

2. **Navigate to:** `notebooks/06-modeling-deck-prediction.ipynb`

3. **Run Cell 9:**
   - This cell generates the XGBoost feature importance chart
   - Saves as `presentation/figures/fig1_feature_importance.png`

4. **Verify output:**
   - Check the bar chart shows "card_level_diff" at 27.83%
   - Top 15 features displayed
   - Saved at 300 DPI

### Example: Trophy Walls (Slide 4)

1. **Open Jupyter**

2. **Navigate to:** `notebooks/04-eda-player-progression.ipynb`

3. **Run Cell 3:**
   - Trophy distribution histogram with vertical lines at 4k/5k/6k/7k/8k
   - Saves as `presentation/figures/fig2_trophy_distribution.png`

4. **Verify output:**
   - Clear peaks before each wall (4000, 5000, 6000)
   - Drop-offs after each wall
   - Annotation showing % of battles in each range

---

## Actual Numbers from Notebooks

### Slide 3: Feature Importance (Notebook 06, Cell 9)
```
Top 5 Features:
1. card_level_diff              27.83%
2. opponent.totalcard.level      2.53%
3. player.totalcard.level        2.53%
4. player.startingTrophies       2.14%
5. column00                      2.09%
```

### Slide 4: Trophy Distribution (Notebook 04, Cell 3)
```
Trophy Walls Identified: [4000, 5000, 6000, 7000, 8000]
Battle Concentration: ~75% in 4000-5000 range
```

### Slide 5: Matchup Fairness (Notebook 04, Cell 9)
```
4-Panel Analysis:
- Trophy difference distribution (bell curve at 0)
- Win rate by favorite/underdog status
- Underdog win rate: ~40-45%
- Fairness score: Most matches within ±100 trophies
```

### Slide 6: Deck Evolution (Notebook 04, Cell 7)
```
4 Metrics Tracked:
- Average Elixir Cost (increases with trophies)
- Legendary Card Usage (sharp rise above 6k)
- Spell Count (varies by meta)
- Troop Count (inverse relationship)
```

### Slide 7: Model Performance (Notebook 06, Cell 11)
```
Model                  Accuracy    ROC-AUC
Logistic Regression    50.50%      0.5061
Random Forest          58.18%      0.6240
XGBoost (BEST)         58.98%      0.6365

Benchmark: 56.94%
Improvement: +2.04%
```

---

## If You Need to Regenerate a Figure

### Step-by-Step Process:

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

3. **Open the correct notebook** (see table above)

4. **Run the cell** that generates the visualization

5. **Check `presentation/figures/`** for the saved PNG

6. **Verify:**
   - Figure matches what's described in the slide
   - Saved at 300 DPI (check file size - should be 100KB-1MB)
   - All axes labeled
   - Title matches the insight

---

## Cell Execution Notes

### Notebook 04: Player Progression
- **Cell 3** (Trophy Distribution): Fast (~2 seconds)
- **Cell 5** (Trophy Change): Fast (~3 seconds)
- **Cell 7** (Deck Evolution): Medium (~10 seconds, 4 charts)
- **Cell 9** (Matchup Fairness): Medium (~15 seconds, 4 charts)

### Notebook 04.5: Advanced Meta Analysis
- **Cell 6** (Trophy Walls): Fast (~2 seconds)
- **Cell 7** (Optimal Elixir): Fast (~3 seconds)

### Notebook 06: Modeling
- **Cell 9** (Feature Importance): Fast (~1 second, model already trained)
- **Cell 10** (Calibration): Fast (~2 seconds)
- **Cell 11** (Model Comparison): Fast (~1 second)

**Note:** Cells 1-8 in Notebook 06 train the models and take longer (5-10 minutes total). If you just need the visualizations, cells 9-11 run instantly using cached results.

---

## What Each Figure Shows

### `fig1_feature_importance.png` (Slide 3)
- **Type:** Horizontal bar chart
- **X-axis:** Feature importance (%)
- **Y-axis:** Feature names
- **Key Insight:** Card level difference is 27.83%, rest are <3%
- **Comparison:** Shows both Random Forest and XGBoost importances

### `fig2_trophy_distribution.png` (Slide 4)
- **Type:** Histogram with vertical annotation lines
- **X-axis:** Trophy count
- **Y-axis:** Number of battles
- **Key Insight:** Massive peak at 4000-5000 (75% of battles)
- **Annotations:** Vertical lines at 4k, 5k, 6k, 7k, 8k

### `fig_matchup_fairness.png` (Slide 5)
- **Type:** 4-panel subplot
  - Panel 1: Trophy difference distribution (histogram)
  - Panel 2: Win rate by trophy difference (line chart)
  - Panel 3: Underdog performance (bar chart)
  - Panel 4: Fairness score distribution (histogram)
- **Key Insight:** Bell curve at 0 = fair matchmaking

### `fig_deck_evolution.png` (Slide 6)
- **Type:** 4-panel subplot (line charts)
  - Panel 1: Avg elixir cost by trophy bracket
  - Panel 2: Legendary usage by trophy bracket
  - Panel 3: Spell count by trophy bracket
  - Panel 4: Troop count by trophy bracket
- **Key Insight:** Deck composition shifts dramatically across trophy tiers

### `fig4_model_comparison.png` (Slide 7)
- **Type:** Grouped bar chart
- **X-axis:** Models (LR, RF, XGBoost)
- **Y-axis:** Performance metrics
- **Bars:** Accuracy (left) and ROC-AUC (right) for each model
- **Key Insight:** XGBoost wins with 58.98% accuracy

---

## Backup Figures (Not in Main 8 Slides)

Available if you have extra time or need them for Q&A:

| Figure | Notebook | Cell | What It Shows |
|--------|----------|------|---------------|
| `fig7_optimal_elixir.png` | 04.5-advanced-meta | Cell 7 | Elixir cost vs win rate (shows 2.0 optimal, but small sample) |
| `fig_trophy_change_analysis.png` | 04-player-progression | Cell 5 | Trophy volatility increases at higher trophies |
| `fig_model_calibration.png` | 06-modeling | Cell 10 | Calibration curves (technical rigor proof) |

---

## Common Issues & Solutions

### Issue: "Figure doesn't match slide description"
**Solution:** Check the cell number - make sure you're looking at the right notebook and cell. Some notebooks have similar analyses.

### Issue: "Figure not found in presentation/figures/"
**Solution:**
1. Open the notebook
2. Run the cell that generates it
3. Check the cell output - it should print "Saved: presentation/figures/figX_name.png"
4. Verify file exists with `ls presentation/figures/`

### Issue: "Cell gives an error when running"
**Solution:**
1. Check if you ran all previous cells (some cells depend on earlier data loading)
2. Make sure virtual environment is activated
3. Check if `battles.csv` is in the correct location
4. For Notebook 06, you may need to run cells 1-8 first to train the models

### Issue: "Figure looks different from what's described"
**Solution:**
1. Check if the notebook was updated after the audit
2. Verify you're running the exact cell number mentioned
3. Some figures are multi-panel - make sure you're looking at all panels
4. Check the file timestamp - it should match when the cell was last run

---

## Quick Test: Verify All Figures Exist

```bash
# From project root directory
ls -lh presentation/figures/fig1_feature_importance.png
ls -lh presentation/figures/fig2_trophy_distribution.png
ls -lh presentation/figures/fig4_model_comparison.png
ls -lh presentation/figures/fig5_detected_walls.png
ls -lh presentation/figures/fig_deck_evolution.png
ls -lh presentation/figures/fig_matchup_fairness.png
```

**Expected output:** File sizes between 100KB - 700KB each (high resolution PNGs)

If any are missing, open the corresponding notebook and run the cell to regenerate.

---

## Ready to Build Your Presentation! 🎯

1. **Open PowerPoint/Google Slides**
2. **Create 8 slides** using the structure in `ACCURATE_8_SLIDE_DECK.md`
3. **Insert figures** from `presentation/figures/` directory
4. **Add text** from the slide descriptions
5. **Apply design specs** (fonts, colors, layout)
6. **Practice delivery** to 7:30 timing
7. **Save and submit** to ajsantos@cpp.edu

**All your visualizations are ready - no need to recreate them!**
