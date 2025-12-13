# Slide-by-Slide Build Guide
## DataRoyale Presentation - Quick Reference

---

## 📊 SLIDE 1: TITLE
**Time: 30 seconds**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│         What Separates Winners from Losers?            │
│    Data-Driven Insights from 16.8 Million Battles      │
│                                                         │
│         Team [Your Name]                                │
│         Cal Poly Pomona Data Science Competition        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- Large title (44pt)
- Subtitle (24pt)
- Background: Clash Royale arena image (optional, semi-transparent)
- Team name at bottom

**Say:** "Welcome! We analyzed 16.8 million battles to answer: What determines who wins?"

**Files Needed:** None (custom design)

---

## 📊 SLIDE 2: THE DATA
**Time: 45 seconds**

```
┌─────────────────────────────────────────────────────────┐
│  From 9.2GB of Battle Data to Actionable Insights      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 THE DATA       🔬 THE METHOD      💡 THE GOAL      │
│                                                         │
│  • 16.8M battles   • DuckDB           • Predict wins   │
│  • 70+ features    • ML models        • Find patterns  │
│  • 4000+ trophies  • XGBoost          • Optimize decks │
│  • 102 cards       • Feature eng.     • Guide players  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- 3-column layout
- Icons or emoji for visual interest
- Bullet points (18-20pt)

**Say:** "9.2GB, 16.8M battles, top 6% of players. We used DuckDB and XGBoost to predict outcomes and find patterns."

**Files Needed:** None (text only)

---

## 📊 SLIDE 3: FINDING #1 - CARD LEVELS
**Time: 1 min 15 sec**

```
┌─────────────────────────────────────────────────────────┐
│  Card Level Difference: Most Important (27.83%)        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [INSERT: fig1_feature_importance.png]                  │
│                                                         │
│  Top 5 Features:                                        │
│  1. Card Level Diff        27.83% ⭐ DOMINANT          │
│  2. Opponent Total Level    2.53%                       │
│  3. Player Total Level      2.53%                       │
│  4. Starting Trophies       2.14%                       │
│  5. Arena ID                2.09%                       │
│                                                         │
│  💡 Card levels = 28%, Strategy = 72%                  │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- Feature importance chart (left side)
- Top 5 list (right side)
- Callout box at bottom

**Say:** "Card level difference is #1 at 28%. BUT 72% comes from strategy, composition, and skill. Smart deck building WORKS."

**Files Needed:**
- `presentation/figures/fig1_feature_importance.png`
- **Source:** Notebook 06, Cell 9

---

## 📊 SLIDE 4: FINDING #2 - TROPHY WALLS
**Time: 1 min 15 sec**

```
┌─────────────────────────────────────────────────────────┐
│  Trophy Walls Are Real: 4k, 5k, 6k, 7k                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [INSERT: fig2_trophy_distribution.png]                 │
│                                                         │
│  Trophy Range    Battles      Visual                   │
│  4000-5000       75%          ████████████             │
│  5000-6000       19%          ███                       │
│  6000-7000       5%           █                         │
│  7000+           <1%          ▌                         │
│                                                         │
│  💡 75% of battles in 4k-5k = major bottleneck         │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- Trophy distribution histogram (main visual)
- Data table (right side or overlay)
- Vertical lines at 4k, 5k, 6k, 7k walls

**Say:** "Trophy walls are real barriers. 75% of competitive battles happen between 4000-5000. Clear peaks before each wall where players get stuck."

**Files Needed:**
- `presentation/figures/fig2_trophy_distribution.png` OR
- `presentation/figures/fig5_detected_walls.png`
- **Source:** Notebook 04, Cell 3 (or Notebook 04.5, Cell 6)

---

## 📊 SLIDE 5: FINDING #3 - MATCHMAKING
**Time: 1 min 15 sec**

```
┌─────────────────────────────────────────────────────────┐
│  Fair Matchmaking: Underdogs Win 40%+ of the Time      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [INSERT: fig_matchup_fairness.png - 4 panels]          │
│                                                         │
│  Key Stats:                                             │
│  🟢 Fair matches (±50 trophies):    60%                │
│  🟡 Slight mismatch (±100):         30%                │
│  🔴 Major mismatch (>100):          10%                │
│                                                         │
│  Underdog win rate: 40-45%                              │
│                                                         │
│  💡 Matchmaking works - skill matters!                 │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- 4-panel chart (main visual, takes up most of slide)
- Key stats box (right side or bottom)
- Color-coded categories

**Say:** "Matchmaking is fair - trophy differences center at zero. Even when outmatched, underdogs win 40-45% of the time. Skill beats small disadvantages."

**Files Needed:**
- `presentation/figures/fig_matchup_fairness.png`
- **Source:** Notebook 04, Cell 9

---

## 📊 SLIDE 6: FINDING #4 - DECK EVOLUTION
**Time: 1 min 15 sec**

```
┌─────────────────────────────────────────────────────────┐
│  How Winning Decks Change as You Climb                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [INSERT: fig_deck_evolution.png - 4 panels]            │
│                                                         │
│  Trophy Range   Elixir   Legendary   Deck Style        │
│  4000-5000      3.6-3.8  Low         Cycle/Fast        │
│  5000-6000      3.7-3.9  Medium      Balanced          │
│  6000-7000      3.8-4.0  High        Beatdown          │
│  7000+          3.9-4.1  Very High   Heavy/Control     │
│                                                         │
│  💡 Meta shifts - adapt your deck to your tier         │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- 4-panel deck evolution chart (main visual)
- Summary table (right side or bottom)
- Trophy tier breakdowns

**Say:** "Deck composition must evolve. At 4k-5k, fast cycle wins. Above 6k, beatdown with legendaries dominates. Adapt your deck as you climb."

**Files Needed:**
- `presentation/figures/fig_deck_evolution.png`
- **Source:** Notebook 04, Cell 7

---

## 📊 SLIDE 7: MODEL PERFORMANCE
**Time: 1 min**

```
┌─────────────────────────────────────────────────────────┐
│  Machine Learning: 58.98% Accuracy Predicting Wins     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [INSERT: fig4_model_comparison.png]                    │
│                                                         │
│  Model               Accuracy    ROC-AUC                │
│  Logistic Regression  50.50%     0.5061  (baseline)    │
│  Random Forest        58.18%     0.6240  ✓             │
│  XGBoost ⭐           58.98%     0.6365  ✓✓ BEST       │
│                                                         │
│  Benchmark: 56.94% | Our model: 58.98% (+2.04%)        │
│                                                         │
│  💡 Deck composition explains 59% of outcomes           │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- Model comparison bar chart (left side)
- Results table (right side)
- Benchmark comparison line
- Key insight callout

**Say:** "XGBoost achieves 59% accuracy, beating the 56.94% benchmark. Why not higher? Clash Royale has randomness - player decisions, card rotation. 59% means deck choice matters, but so does skill."

**Files Needed:**
- `presentation/figures/fig4_model_comparison.png`
- **Source:** Notebook 06, Cell 11

---

## 📊 SLIDE 8: RECOMMENDATIONS
**Time: 1 min 30 sec**

```
┌─────────────────────────────────────────────────────────┐
│  From Data to Action: What Should You Do?              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  👥 FOR PLAYERS    │  🎮 FOR DESIGNERS │  📊 ANALYSTS  │
│                    │                   │               │
│  1. Level cards    │  1. Trophy walls  │  1. Card level│
│     - Levels = 28% │     at 4k/5k/6k   │     #1 feature│
│                    │     are real      │     (27.83%)  │
│  2. Adapt deck to  │                   │               │
│     trophy tier:   │  2. Matchmaking   │  2. Deck comp │
│     • 4k-5k: Cycle │     works well    │     = 59% of  │
│     • 6k+: Beatdown│     - Fair match  │     outcomes  │
│                    │     - Underdogs   │               │
│  3. Strategy beats │     win 40%       │  3. Remaining │
│     small gaps     │                   │     41% is    │
│     - 40% underdog │  3. Meta evolves  │     skill &   │
│     wins prove it  │     by trophy     │     tactics   │
│                    │     tier          │               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🏆 KEY TAKEAWAYS:                                      │
│  1️⃣ Card levels matter (28%) BUT strategy = 72%       │
│  2️⃣ Trophy walls are real skill barriers               │
│  3️⃣ Matchmaking is fair - underdogs can win            │
│  4️⃣ Deck composition must evolve as you climb          │
│                                                         │
│  ⚠️ LIMITATIONS: Snapshot in time, 75% data in 4k-5k   │
│                                                         │
│  Questions?                                             │
└─────────────────────────────────────────────────────────┘
```

**Elements:**
- 3-column recommendation table (top)
- Key takeaways box (middle)
- Limitations acknowledgment (bottom)
- "Questions?" prompt

**Say:** "Three audiences, specific actions. Players: level cards, adapt decks to your tier. Designers: walls are real, matchmaking works. Analysts: levels are #1 but strategy explains 72%. We acknowledge limitations: this is a snapshot, 75% in one trophy range. Future work: temporal tracking, player experience data, real-time recommendations. Thank you!"

**Files Needed:** None (text only)

---

## QUICK BUILD CHECKLIST

**Before you start:**
- [ ] All 6 figure files exist in `presentation/figures/`
- [ ] PowerPoint or Google Slides open
- [ ] Design specs ready (fonts, colors)

**For each slide:**
- [ ] Title in header bar (36-44pt)
- [ ] Insert visualization (if applicable)
- [ ] Add text content (18-24pt body)
- [ ] Add insight callout box
- [ ] Check readability from 20 feet away
- [ ] Add page number and team name to footer

**Final checks:**
- [ ] Total slide count: 8 slides
- [ ] All figures high resolution (not pixelated)
- [ ] Consistent fonts across slides
- [ ] Consistent color scheme
- [ ] Speaker notes added (optional but helpful)
- [ ] Practice delivery to 7:30 timing

---

## TIMING BREAKDOWN

| Slide | Topic | Time | Running Total |
|-------|-------|------|---------------|
| 1 | Title | 0:30 | 0:30 |
| 2 | Data | 0:45 | 1:15 |
| 3 | Card Levels | 1:15 | 2:30 |
| 4 | Trophy Walls | 1:15 | 3:45 |
| 5 | Matchmaking | 1:15 | 5:00 |
| 6 | Deck Evolution | 1:15 | 6:15 |
| 7 | Model | 1:00 | 7:15 |
| 8 | Recommendations | 1:30 | **8:45** |

**Buffer:** 15 seconds (stay under 9 minutes)

**Strategy:** If running long, condense Slide 8 by skipping the "For Analysts" column.

---

## DESIGN QUICK REFERENCE

**Fonts:**
- Titles: **Bebas Neue** or **Impact**, 36-44pt
- Body: **Arial** or **Calibri**, 18-24pt
- Labels: 14-16pt, bold

**Colors (Hex):**
- Blue: `#2E86AB` (primary, use for headers)
- Purple: `#A23B72` (secondary)
- Orange: `#F18F01` (accent)
- Green: `#06A77D` (success/positive)
- Red: `#D62839` (warning/negative)
- Gray: `#4A4A4A` (neutral)

**Layout:**
- White background
- Colored header bar (blue) with slide title
- Left text, right visual (or full-width visual)
- Small footer with page # and team name

---

## WHAT TO SAY FOR EACH SLIDE

### Slide 1 (0:30)
"Welcome! Today we're diving into 16.8 million competitive Clash Royale battles to answer one question: What separates winners from losers? Is it card levels? Deck composition? Strategy? Let's find out."

### Slide 2 (0:45)
"Our dataset is massive - 9.2 gigabytes with 16.8 million battles from the top 6% of players, above 4000 trophies. We used DuckDB for data processing and XGBoost for machine learning to predict outcomes and identify patterns."

### Slide 3 (1:15)
"Our first major finding: card level difference is the #1 predictor at 27.83% importance. This confirms levels matter. BUT - and this is crucial - 72% of what determines victory comes from OTHER factors: deck composition, player skill, strategic choices. This means smart deck building CAN overcome a level disadvantage."

### Slide 4 (1:15)
"Finding #2: trophy walls are real structural barriers. 75% of all competitive battles happen in the 4000-5000 trophy range. We see clear clustering right before each wall at 4k, 5k, 6k, 7k - these are players trying to break through. The sharp drop-offs after each wall show only the most skilled or best-equipped players advance."

### Slide 5 (1:15)
"Finding #3 validates the matchmaking system. The trophy difference distribution is a perfect bell curve centered at zero - most matches are between equally-skilled players. Even more interesting: when there IS a mismatch, underdogs still win 40-45% of the time. This proves Clash Royale isn't purely pay-to-win - smart strategy can overcome disadvantages."

### Slide 6 (1:15)
"Finding #4: deck composition must evolve as you climb. At 4000-5000 trophies, fast cycle decks with low elixir costs dominate. But above 6000 trophies, successful players shift to heavier beatdown decks with more legendary cards. This isn't just about card availability - it's about meta strategy. The optimal deck at 4500 will fail at 6500."

### Slide 7 (1:00)
"Our XGBoost model achieves 58.98% accuracy predicting battle outcomes, beating the 56.94% published benchmark. Some might ask, 'Why not higher?' Here's the key: Clash Royale has inherent randomness - player decisions, card rotation timing, real-time tactics. Our model uses ONLY pre-battle deck composition. 59% means deck choice explains more than half of outcomes, but player skill still matters significantly."

### Slide 8 (1:30)
"So what should you DO with these insights? For players: yes, level your cards - it's the #1 factor. But also adapt your deck to your trophy tier. At 4k-5k, play cycle. At 6k+, shift to beatdown. And remember: underdogs win 40% of the time, so strategy matters.

For game designers: your matchmaking algorithm works great. Trophy walls at 4k, 5k, 6k are real barriers where players get stuck - consider progression smoothing.

For data scientists: XGBoost works well for game data. Card level dominates at 28%, but 72% comes from compositional and strategic factors.

We acknowledge our limitations: this is a snapshot in time, 75% of battles are in one trophy range. Future work includes temporal meta tracking and building a real-time deck recommendation system.

Thank you! Questions?"

---

## YOU'RE READY TO BUILD! 🚀

**Process:**
1. Open PowerPoint/Google Slides
2. Create 8 blank slides
3. Apply header/footer template to all
4. Go slide-by-slide, copying text and inserting figures
5. Apply fonts and colors
6. Practice delivery
7. Save as .pptx AND .pdf
8. Submit to ajsantos@cpp.edu

**All your figures are ready in `presentation/figures/` - just insert them!**

**Good luck! You've got solid science and a compelling story. Go win! 🏆**
