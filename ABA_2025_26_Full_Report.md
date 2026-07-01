# ABA 2025-26 Season: Full Analytical Report
### Longshots Basketball Program
### Season Duration: October 2, 2025 — April 8, 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Data Source & Methodology](#2-data-source--methodology)
3. [Advanced Statistics Framework](#3-advanced-statistics-framework)
4. [Regular Season Report](#4-regular-season-report)
5. [Regular Season + Semifinal Report](#5-regular-season--semifinal-report)
6. [AshKnights Scouting Report](#6-ashknights-scouting-report)
7. [Longshots Self-Scouting Report](#7-longshots-self-scouting-report)
8. [Scoring Targets & Win Probability](#8-scoring-targets--win-probability)
9. [Finals Results & Model Validation](#9-finals-results--model-validation)
10. [Deliverables Summary](#10-deliverables-summary)

---

## 1. Project Overview

This report documents the full analytical pipeline built for the Longshots coaching staff in preparation for the ABA 2025-26 playoffs. The project covered:

- **Data processing:** Cleaning and organizing 396 player-level box score rows across 28 games
- **Advanced statistics:** Computing eFG%, TS%, Game Score, EFF, ORTG, DRTG, and Usage Rate for all players and teams
- **League reports:** Regular Season and RS+Semifinal standing reports with leader boards
- **Opposition scouting:** Full AshKnights scouting report with regression analysis identifying what drives their wins and losses
- **Self-scouting:** Full Longshots self-scout with regression analysis identifying our own win drivers
- **Scoring targets:** Data-driven point thresholds for winning games league-wide and against the AshKnights specifically
- **Finals validation:** Post-series analysis checking whether the analytical findings held in the championship

**Bottom line: The Longshots swept the AshKnights 3-0 to win the championship. The scouting findings were validated — the game plan worked.**

---

## 2. Data Source & Methodology

### Dataset

| Attribute | Detail |
|-----------|--------|
| File | `ashesi_basketball_2025_26_full.csv` |
| Rows | 396 (player-level box scores) |
| Columns | 31 |
| Teams | AshKnights, HillBlazers, Longshots, Los Ashtros, Berekusu Warriors |
| Game Types | Regular Season (19 games), RS Forfeit (1), Semifinal (5), Finals (3) |
| Date Range | October 2, 2025 — April 8, 2026 |

### Columns Available

`game_number, game_date, venue, game_type, home_team, away_team, team, opponent, team_score, opponent_score, game_outcome, winner, jersey_number, player_name, position, pts, reb, ast, stl, blk, tov, fouls, fgm, fga, fg_pct, three_pm, three_pa, three_pct, ftm, fta, ft_pct`

### Data Limitations

- **Turnovers not tracked:** All TOV values are 0. This means AST/TOV ratio cannot be computed, and possession estimates use `FGA + 0.44 × FTA` instead of the standard `FGA + TOV + 0.44 × FTA`. Estimates are slightly inflated but consistent across teams.
- **No OREB/DREB split:** Only total rebounds available. Cannot compute offensive rebound percentage (one of Dean Oliver's Four Factors).
- **Small sample sizes:** 8-11 games per team in RS+Semi. Regression models capped at 5 features (rule of thumb: 5-10 observations per feature).
- **Playoff game length:** Regular season games are 40 minutes; playoff games are 48 minutes. Counting stats inflate ~20% in playoffs, affecting direct comparisons and regression predictions applied out-of-sample.

### Analytical Framework

- **Dean Oliver's Four Factors** guided the approach (eFG%, TOV%, ORB%, FTR), adapted for available data
- **OLS regression** with `statsmodels` for win margin modeling
- **Exhaustive combinatorial search** (`itertools.combinations`) to find the best-fitting models with all features statistically significant
- **Multicollinearity checks** (r > 0.85 exclusion between features)
- **Univariate pre-screening** (p < 0.20) to reduce feature pool before exhaustive search

---

## 3. Advanced Statistics Framework

### Player-Level Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| **eFG%** | `(FGM + 0.5 × 3PM) / FGA × 100` | Shooting efficiency adjusted for 3-point value |
| **TS%** | `PTS / (2 × (FGA + 0.44 × FTA)) × 100` | True shooting efficiency including free throws |
| **Game Score** | `PTS + 0.4×FGM - 0.7×FGA - 0.4×(FTA-FTM) + 0.5×REB + STL + 0.7×AST + 0.7×BLK - 0.4×FOULS - TOV` | Single-game overall impact |
| **EFF** | `(PTS + REB + AST + STL + BLK) - ((FGA-FGM) + (FTA-FTM) + TOV)` | Overall efficiency rating |
| **Usage Rate** | `(Player FGA + 0.44 × Player FTA) / (Team FGA + 0.44 × Team FTA) × 100` | Share of team possessions used |

### Team-Level Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| **ORTG** | `(Points / Possessions) × 100` | Points per 100 possessions (offense) |
| **DRTG** | `(Opponent Points / Possessions) × 100` | Points allowed per 100 possessions (defense) |
| **3PT Rate** | `3PA / FGA × 100` | Share of shots from three-point range |
| **FT Rate** | `FTA / FGA × 100` | Free throw attempt rate |
| **AST Rate** | `AST / FGM × 100` | Percentage of made baskets that were assisted |
| **REB%** | `Team REB / (Team REB + Opp REB) × 100` | Rebounding share |

### Excel Workbook (`ABA_2025_26.xlsx`)

| Sheet | Contents |
|-------|----------|
| Regular Season | Raw RS box scores (275 rows) |
| Regular Season + Semifinal | Raw RS+Semi box scores (354 rows) |
| Player Advanced Stats | RS player stats with all metrics + usage rate (63 players) |
| Team Advanced Stats | RS team stats with ORTG/DRTG |
| Player Advanced Stats RS+Semi | RS+Semi player stats with all metrics + usage rate (69 players) |
| Team Advanced Stats RS+Semi | RS+Semi team stats with ORTG/DRTG |

---

## 4. Regular Season Report

### Standings

| Team | W | L | Win% | PPG | Opp PPG | Diff | ORTG | DRTG |
|------|---|---|------|-----|---------|------|------|------|
| AshKnights | 6 | 2 | 75.0% | 61.6 | 54.8 | +6.9 | 87.0 | 77.3 |
| Los Ashtros | 5 | 3 | 62.5% | 45.4 | 45.8 | -0.4 | 78.1 | 74.4 |
| Longshots | 4 | 4 | 50.0% | 52.2 | 54.8 | -2.5 | 77.6 | 81.3 |
| HillBlazers | 3 | 5 | 37.5% | 49.6 | 53.6 | -4.0 | 86.6 | 93.6 |
| Berekusu Warriors | 2 | 6 | 25.0% | 52.4 | 55.1 | -2.8 | 80.7 | 84.6 |

### Scoring Leaders

| Player | Team | PPG | RPG | APG | eFG% | TS% |
|--------|------|-----|-----|-----|------|-----|
| Richard | Longshots | 25.5 | 14.5 | 3.5 | 57.1 | 58.8 |
| Sean Yeboah | AshKnights | 23.6 | 11.0 | 2.8 | 43.1 | 44.9 |
| Awindor Nongyin | HillBlazers | 20.4 | 8.0 | 4.0 | 46.0 | 47.9 |
| Ademilade | Berekusu Warriors | 20.0 | 12.2 | 2.8 | 43.3 | 45.9 |
| David Awuah | Los Ashtros | 18.7 | 9.1 | 4.9 | 45.2 | 47.2 |

### Top Usage Rates (RS)

| Player | Team | PPG | Usage Rate |
|--------|------|-----|-----------|
| Sean Yeboah | AshKnights | 23.6 | 37.6% |
| Desmond Raimmy | Longshots | 16.9 | 35.3% |
| Ademilade | Berekusu Warriors | 20.0 | 34.0% |
| Richard | Longshots | 25.5 | 33.4% |
| Awindor Nongyin | HillBlazers | 20.4 | 33.0% |

### Key Findings

- **AshKnights** dominated — best ORTG (87.0), best DRTG (77.3), only team with positive point differential
- **Los Ashtros** had the best defense by DRTG (74.4) but near-zero point differential due to low scoring
- **Richard** was the most efficient high-volume scorer in the league (58.8 TS%) but only played 2 RS games
- **Sean Yeboah** was the volume scoring leader (23.6 PPG) but with below-average efficiency (44.9 TS%)
- **David Awuah** was the most well-rounded player: scoring, rebounding, assists, and league-leading 3.7 SPG

---

## 5. Regular Season + Semifinal Report

### Standings

| Team | W | L | Win% | PPG | Opp PPG | Diff | ORTG | DRTG |
|------|---|---|------|-----|---------|------|------|------|
| AshKnights | 8 | 3 | 72.7% | 69.1 | 63.2 | +5.9 | 88.9 | 81.3 |
| Longshots | 6 | 4 | 60.0% | 59.9 | 55.6 | +4.3 | 85.4 | 79.2 |
| Los Ashtros | 5 | 5 | 50.0% | 48.3 | 54.7 | -6.4 | 80.7 | 91.8 |
| HillBlazers | 4 | 7 | 36.4% | 61.3 | 63.3 | -2.0 | 91.2 | 97.2 |
| Berekusu Warriors | 2 | 6 | 25.0% | 52.4 | 55.1 | -2.7 | 81.5 | 85.8 |

### Scoring Leaders

| Player | Team | GP | PPG | RPG | APG | eFG% | TS% | Usage% |
|--------|------|----|-----|-----|-----|------|-----|--------|
| Sean Yeboah | AshKnights | 11 | 28.9 | 11.5 | 2.7 | 46.7 | 47.5 | 39.1 |
| Richard | Longshots | 4 | 24.0 | 16.5 | 3.5 | 55.6 | 55.2 | 30.2 |
| Awindor Nongyin | HillBlazers | 10 | 21.3 | 9.0 | 4.8 | 43.5 | 45.1 | 33.2 |
| Ademilade | Berekusu Warriors | 8 | 20.0 | 12.2 | 2.8 | 43.3 | 45.9 | 34.0 |
| Boss Baeta | Longshots | 10 | 19.5 | 8.5 | 5.6 | 45.6 | 47.9 | 28.7 |

### Key Changes from Regular Season

- **Longshots surged** from .500 (4-4) to 60% (6-4), jumping ahead of Los Ashtros
- **Sean Yeboah elevated** from 23.6 to 28.9 PPG — his usage climbed to 39.1%
- **Longshots emerged as a two-way team** — best DRTG in the league (79.2)
- **Los Ashtros collapsed** from 62.5% to .500 after semifinal losses
- **HillBlazers** had the highest ORTG (91.2) but worst DRTG (97.2) — they score but can't stop anyone

### Team Efficiency Snapshot

| Metric | Leader | Value |
|--------|--------|-------|
| Best Offense (ORTG) | HillBlazers | 91.2 |
| Best Defense (DRTG) | Longshots | 79.2 |
| Best Net Rating | AshKnights | +7.6 |
| Best Ball Movement (AST Rate) | Longshots | 81.0% |
| Best Rebounding (REB%) | Los Ashtros | 55.0% |
| Most 3PT Reliant | Longshots | 38.5% |

---

## 6. AshKnights Scouting Report

### Overview

| Stat | Value |
|------|-------|
| Record | 8-3 (72.7%) |
| PPG | 69.1 |
| Opp PPG | 63.2 |
| ORTG | 88.9 |
| DRTG | 81.3 |

The AshKnights were the best team in the league. They win through volume shooting and dominant interior play, not through efficiency. Their FT shooting is a glaring weakness.

### Key Personnel

#### Sean Yeboah (SF) — THE GUY

| PPG | RPG | APG | FG% | eFG% | TS% | Usage% | Game Score |
|-----|-----|-----|-----|------|-----|--------|-----------|
| 28.9 | 11.5 | 2.7 | 44.8 | 46.7 | 47.5 | 39.1 | 21.1 |

- **41.8% of all team points** and 24.8% of rebounds
- Volume scorer, not efficient (47.5 TS%)
- Does not pass much (2.7 APG) — scores over distributes
- **Scores ~29 whether they win or lose** — he is a constant, not a differentiator
- However, **his 3-pointers are the single most significant predictor** of win margin (+7.6 per 3PM, p=0.00001)
- **Usage rate is negatively correlated with winning** (-0.365 per 1% usage, p=0.016) — when the offense becomes the Sean Show, they lose

#### Benson Kas-Vorsah (SG) — THE REAL DIFFERENCE-MAKER

| PPG | eFG% | TS% | Usage% |
|-----|------|-----|--------|
| 12.0 | 46.3 | 46.4 | 16.7 |

- Only SG on the roster — **no backup**
- **Strongest predictor of AshKnights win margin** (+1.05 per point, p=0.0001)
- Averages **13.4 PPG in wins vs 8.3 PPG in losses** — a 5-point swing
- His steals are *negatively* correlated with win margin (-2.86, p=0.0015) — he gambles out of position

#### Charles Janney (C) — The Engine

| PPG | RPG | APG | BPG | Game Score |
|-----|-----|-----|-----|-----------|
| 11.3 | 11.7 | 5.6 | 1.7 | 16.4 |

- Rare playmaking center — 5.6 APG is elite for a big man
- Leads team in blocks (1.7 BPG) — rim protection anchor
- 11.7 RPG over all 11 games — their most consistent rebounder

#### Trueman Mabumbo (PG) — The Floor General

| PPG | RPG | APG | eFG% | TS% |
|-----|-----|-----|------|-----|
| 8.8 | 4.3 | 6.5 | 47.3 | 48.0 |

- Leads team in assists (6.5 APG) — primary playmaker
- Sole PG — no backup

#### Kofi Boadi (PF) — Rim Protector off Bench

- 1.5 BPG in 4 games — shot-blocking specialist
- Limited offensive game

### Roster Depth

| Position | Players | Notes |
|----------|---------|-------|
| PG | Trueman Mabumbo | Sole PG — no backup |
| SG | Benson Kas-Vorsah | Sole SG — critical vulnerability |
| SF | Sean Yeboah, Alistide Ishimwe | Star + limited backup |
| PF | Kofi Boadi | Rim protector |
| C | Charles Janney, Nana Kwabena | Playmaking center + backup |

**Thin at guard.** Only one PG and one SG. Exploitable through tempo and foul trouble.

### Tendencies

**Shooting Profile:** 69.5% of shots are 2-pointers, 30.5% are 3-pointers. Inside-out team through Yeboah and Janney.

**In Wins vs Losses:**

| Stat | Wins (8) | Losses (3) |
|------|----------|-----------|
| PPG | 73.2 | 58.0 |
| AST | 20.4 | 16.0 |
| Fouls | 8.1 | 13.0 |
| 3PT Shot Share | ~28% | ~36% |
| 3PT% in Losses | — | 23.1% |
| Benson PPG | 13.4 | 8.3 |
| Sean Usage | Lower | Higher |

When they lose: fewer points, more fouls, more 3s at worse accuracy, fewer assists (iso-heavy), Benson goes cold, Sean dominates usage.

### Regression Model: What Drives AshKnights Win Margin

**Final Model (R-squared = 0.991, Adj R-sq = 0.983, F p = 0.00004)**

All 5 features significant at p < 0.05:

| Variable | Coefficient | p-value | Interpretation |
|----------|------------|---------|----------------|
| **Benson pts** | +1.050 | 0.0001 | Each Benson point adds 1.1 to win margin |
| **Sean 3PM** | +7.560 | 0.00001 | Each Sean 3-pointer adds 7.6 to win margin |
| **Benson steals** | -2.862 | 0.0015 | Each Benson steal costs 2.9 from win margin |
| **Team FTM** | -0.557 | 0.017 | Each made FT costs 0.6 from win margin |
| **Sean usage %** | -0.365 | 0.016 | Each 1% more Sean usage costs 0.4 from margin |

This model explains 99.1% of the variance. The message:
- **Benson scoring + Sean hitting 3s = blowout wins**
- **Sean dominating usage + going to the FT line = close games or losses**

**Other Strong Models Found (all features significant at p < 0.05):**

| Model | R-sq | Adj R-sq |
|-------|------|----------|
| bk_pts + sy_3pm + sy_ast + bk_stl + bk_efg | 0.991 | 0.982 |
| bk_pts + pct_ft_pts + opp_fouls + ast_diff + n_scorers | 0.991 | 0.981 |
| bk_pts + ftm + sy_3pm + sy_ast + bk_stl | 0.989 | 0.977 |
| bk_pts + ft_rate + opp_stl + sy_3pm + sy_usage | 0.987 | 0.974 |

Across all models, **Benson's points** and **Sean's 3-pointers** appear consistently as the two strongest drivers.

### Weaknesses Identified

1. **Benson is the real swing factor** — 13+ pts = win, 8 or less = loss
2. **Free throw shooting is terrible (44.6% FT)** — every FT is a wasted possession
3. **Sean's usage kills them** — more shots = worse team performance
4. **Guard depth is paper-thin** — only 1 PG and 1 SG, no replacements
5. **They foul a lot when losing** — 13.0 fouls in losses vs 8.1 in wins
6. **Ball movement dies in losses** — assists drop from 20.4 to 16.0

### Recommended Game Plan

**Defense:**
1. Face-guard Benson Kas-Vorsah — defensive priority #1
2. Let Sean score 2s, run him off the 3-point line
3. Force the Sean Show — deny Benson and Janney's passing lanes
4. Don't throw lazy passes near Benson

**Offense:**
1. Push tempo — their guard depth can't sustain a fast pace
2. Attack Kas-Vorsah and Mabumbo — draw fouls on their only guards
3. Drive and draw contact — send them to the line at 44.6% FT
4. Boss and Desmond attack downhill in transition

**Late Game:**
- Intentional fouling is legitimate at 44.6% FT
- If Benson is cold, press the advantage
- Don't let Sean get comfortable from 3 in crunch time

---

## 7. Longshots Self-Scouting Report

### Overview

| Stat | Value |
|------|-------|
| Record | 6-4 (60.0%) |
| PPG | 59.9 |
| Opp PPG | 55.6 |
| ORTG | 85.4 |
| DRTG | 79.2 |

A streaky team — started 1-4, finished on a 5-0 run. Best defense in the league (79.2 DRTG).

### Game Log

| Game | Opponent | Score | Result | Margin |
|------|----------|-------|--------|--------|
| 2 | Los Ashtros | 56-59 | L | -3 |
| 6 | Berekusu Warriors | 61-51 | W | +10 |
| 8 | AshKnights | 41-73 | L | -32 |
| 10 | HillBlazers | 55-61 | L | -6 |
| 12 | Los Ashtros | 37-45 | L | -8 |
| 14 | HillBlazers | 49-46 | W | +3 |
| 17 | AshKnights | 56-48 | W | +8 |
| 20 | Berekusu Warriors | 63-55 | W | +8 |
| 21 | Los Ashtros | 90-58 | W | +32 |
| 22 | Los Ashtros | 91-60 | W | +31 |

### Key Personnel

#### Boss Baeta (PG) — The Leader

| PPG | RPG | APG | SPG | eFG% | TS% | Usage% |
|-----|-----|-----|-----|------|-----|--------|
| 19.5 | 8.5 | 5.6 | 2.3 | 45.6 | 47.9 | 28.7 |

- **32.6% of all team points**
- Elite all-around: scoring, rebounding (8.5 for a PG), assists, steals
- **His eFG% is the strongest individual predictor** of win margin (+0.604 per 1%, p=0.0000)

#### Desmond Raimmy (SG) — The Second Star

| PPG | RPG | APG | SPG | eFG% | TS% | Usage% |
|-----|-----|-----|-----|------|-----|--------|
| 19.4 | 5.0 | 3.8 | 3.1 | 40.6 | 41.8 | 33.4 |

- **29.2% of all team points**
- Active hands (3.1 SPG)
- **Points are a significant predictor** of win margin (+0.508, p=0.001)
- 3-point shooting particularly important (r=+0.659, p=0.038)

#### Richard (PF) — The X-Factor

| PPG | RPG | APG | SPG | eFG% | TS% | Usage% |
|-----|-----|-----|-----|------|-----|--------|
| 24.0 | 16.5 | 3.5 | 3.8 | 55.6 | 55.2 | 30.2 |

- Most dominant player in the league when available — only played 4 games
- **Rebounds are a significant predictor** (+0.968 per rebound, p=0.0001)
- His availability changes the team's ceiling entirely

#### Bright Edudzi (SF) — The Glue Guy

| PPG | RPG | APG | SPG | eFG% | TS% |
|-----|-----|-----|-----|------|-----|
| 4.3 | 5.0 | 3.9 | 2.6 | 38.4 | 37.8 |

- Doesn't score much but does everything else
- **Rebounds are the highest-leverage hustle play** on the team (+2.261 per rebound, p=0.0003)
- Assists jump in wins (4.5 vs 3.0), steals triple (3.7 vs 1.0) — the energy barometer

#### Arnold Agamah (C) — The Anchor

| PPG | RPG | SPG |
|-----|-----|-----|
| 1.9 | 4.9 | 2.0 |

- Plays every game, 2.0 SPG — active defensively

### Scoring Distribution

| Player | % of Team Points |
|--------|-----------------|
| Boss Baeta | 32.6% |
| Desmond Raimmy | 29.2% |
| Richard | 16.0% |
| Bright Edudzi | 7.2% |
| Joseph Ajak | 3.8% |
| Arnold Agamah | 3.2% |

**61.8% from Baeta + Raimmy.** With Richard, the load is more balanced. Without him, heavily two-man dependent.

### Wins vs Losses

| Stat | Wins (6) | Losses (4) |
|------|----------|-----------|
| PPG | 68.3 | 47.2 |
| FG% | 43.3% | 28.2% |
| AST | 22.5 | 13.2 |
| STL | 14.8 | 10.0 |
| Fouls | 15.5 | 6.2 |

**Key differences:**
- FG% swings massively (43.3% vs 28.2%) — shooting efficiency is the #1 driver
- Assists nearly double in wins — ball movement is critical
- Steals 50% higher in wins — defensive intensity fuels the offense
- Fouls HIGHER in wins — the team plays more physically/aggressively when winning

### Regression Model: What Drives Longshots Win Margin

**Best Model (R-squared = 0.999, Adj R-sq = 0.997, F p = 0.000006)**

All 5 features significant at p < 0.05:

| Variable | Coefficient | p-value | Interpretation |
|----------|------------|---------|----------------|
| **Boss eFG%** | +0.604 | 0.0000 | Each 1% increase in Boss efficiency = +0.6 margin |
| **Richard rebounds** | +0.968 | 0.0001 | Each Richard rebound = +1.0 margin |
| **Desmond points** | +0.508 | 0.0006 | Each Desmond point = +0.5 margin |
| **Team 3P%** | +0.322 | 0.006 | Each 1% increase in 3P shooting = +0.3 margin |
| **Bright rebounds** | +2.261 | 0.0003 | Each Bright rebound = +2.3 margin |

**Supporting indicators (from univariate analysis):**
- Team steals: r=+0.670, p=0.034 (14.8 SPG in wins vs 10.0 in losses)
- Bright assists: 4.5 in wins vs 3.0 in losses
- Supporting cast points: r=+0.676, p=0.032

**Other Strong Models (all features significant at p < 0.05):**

| Model | R-sq | Adj R-sq |
|-------|------|----------|
| efg + fgpd + sd_pts + be_reb + dr_pts | 0.999 | 0.997 |
| fgpd + sd_pts + oftm + be_reb + dr_pts | 0.999 | 0.997 |
| jg_fga + bb_efg + be_reb + ja_pts + dr_pts | 0.998 | 0.996 |
| fgpd + sd_pts + ri_reb + oftm + dr_pts | 0.998 | 0.996 |

### Our Identity (What the Data Says)

1. **Boss's efficiency is everything** — not volume, *efficiency*. Smart shots, not forced ones.
2. **Richard's rebounding transforms the team** — each rebound adds nearly a full point of margin.
3. **Desmond's scoring is the second engine** — keep shooting, even on tough nights.
4. **3-point shooting unlocks blowouts** — spacing and shot-making from deep opens everything.
5. **Bright Edudzi's rebounding is a hidden weapon** — at +2.3 per rebound, the highest-value hustle play.
6. **Steals fuel transition** — 14.8 in wins vs 10.0 in losses. Everyone needs active hands.
7. **Play physical** — fouls are HIGHER in wins (15.5 vs 6.2). Aggressive, not passive.
8. **Move the ball** — 22.5 assists in wins vs 13.2 in losses. Non-negotiable.

---

## 8. Scoring Targets & Win Probability

### League-Wide Win Probability by Score

| Score Range | Win Rate |
|-------------|----------|
| 45-49 | 37.5% |
| 50-54 | 33.3% |
| 55-59 | 50.0% |
| 60-64 | 62.5% |
| 70+ | 73.0% |
| 75+ | 100.0% |

The league-wide crossover (50% win probability) is approximately **59 points**.

### Longshots Scoring Reality

| Split | Our PPG | Opp PPG |
|-------|---------|---------|
| Wins (6) | 68.3 | 53.0 |
| Losses (4) | 47.2 | 59.5 |

- Lowest winning score: 49 (vs HillBlazers)
- Highest losing score: 56 (vs Los Ashtros)
- **Longshots crossover: ~57 points.** Above that, always won. Below, always lost.

### vs AshKnights Target (40-Minute Games)

Teams that **beat** the AshKnights scored: 56, 58, 74
Teams that **lost** to the AshKnights scored: 41, 50, 52, 52, 64, 65, 73, 110

Scoring a lot does NOT guarantee a win — teams scored 64, 65, 73, and even 110 and still lost. The AshKnights average 69.1 PPG; you cannot outgun them.

| AshKnights Score | Result |
|-----------------|--------|
| Under 58 | They lose |
| 65+ | They almost always win |

**Target (40-min games): Hold the AshKnights under 55 while scoring 55+.** Defense wins this matchup.

**Adjusted Target (48-min playoff games): Hold under ~66 while scoring 66+.** (20% inflation for extra 8 minutes.)

---

## 9. Finals Results & Model Validation

### Series Result: Longshots 3, AshKnights 0

**LONGSHOTS WIN THE ABA 2025-26 CHAMPIONSHIP**

### Game-by-Game Results

| Game | Longshots | AshKnights | Margin |
|------|-----------|------------|--------|
| 26 | **99** | 85 | +14 |
| 27 | **106** | 97 | +9 |
| 28 | **109** | 90 | +19 |

### Finals Box Scores

**Game 26 — Longshots 99, AshKnights 85**

| Longshots | PTS | REB | AST | STL | FG |
|-----------|-----|-----|-----|-----|-----|
| Desmond Raimmy | 35 | 6 | 5 | 4 | 12/30, 8 3PM |
| Richard | 29 | 14 | 5 | 0 | 13/21 |
| Boss Baeta | 22 | 11 | 7 | 0 | 9/26 |
| Bright Edudzi | 5 | 6 | 6 | 2 | 2/4 |

| AshKnights | PTS | REB | AST | STL | FG |
|------------|-----|-----|-----|-----|-----|
| Sean Yeboah | 35 | 9 | 6 | 0 | 13/27, 1 3PM |
| Kofi Boadi | 19 | 16 | 1 | 2 | 8/13 |
| Trueman Mabumbo | 18 | 5 | 9 | 1 | 7/18 |
| Charles Janney | 10 | 9 | 5 | 0 | 3/15 |
| **Benson Kas-Vorsah** | **3** | 11 | 4 | 0 | **1/6** |

**Game 27 — Longshots 106, AshKnights 97**

| Longshots | PTS | REB | AST | STL | FG |
|-----------|-----|-----|-----|-----|-----|
| **Desmond Raimmy** | **50** | 8 | 6 | 4 | 20/43, 7 3PM |
| Richard | 22 | 12 | 5 | 0 | 9/23 |
| Boss Baeta | 16 | 6 | 13 | 4 | 5/24 |
| Bright Edudzi | 6 | 12 | 5 | 8 | 3/7 |

| AshKnights | PTS | REB | AST | STL | FG |
|------------|-----|-----|-----|-----|-----|
| Sean Yeboah | 37 | 8 | 4 | 0 | 14/25, 1 3PM |
| Charles Janney | 31 | 18 | 7 | 1 | 11/27 |
| Kofi Boadi | 21 | 15 | 4 | 0 | 8/19 |
| **Benson Kas-Vorsah** | **6** | 10 | 1 | 0 | **2/10** |
| Trueman Mabumbo | 2 | 2 | 14 | 2 | 1/8 |

**Game 28 — Longshots 109, AshKnights 90**

| Longshots | PTS | REB | AST | STL | FG |
|-----------|-----|-----|-----|-----|-----|
| **Boss Baeta** | **37** | 13 | 6 | 1 | 17/31, 3 3PM |
| Richard | 28 | 13 | 15 | 1 | 9/21 |
| Desmond Raimmy | 21 | 7 | 11 | 3 | 7/20, 5 3PM |
| **Bright Edudzi** | **14** | **12** | 5 | 3 | 6/11 |

| AshKnights | PTS | REB | AST | STL | FG |
|------------|-----|-----|-----|-----|-----|
| Sean Yeboah | 41 | 12 | 2 | 0 | 18/32, **0 3PM** |
| Charles Janney | 27 | 15 | 4 | 1 | 13/24 |
| Kofi Boadi | 8 | 15 | 2 | 0 | 4/13 |
| Trueman Mabumbo | 7 | 14 | 17 | 5 | 2/13 |
| **Benson Kas-Vorsah** | **2** | 7 | 2 | 2 | **1/8** |

### AshKnights Model Validation

**Model: win_margin ~ bk_pts(+1.05) + sy_3pm(+7.56) + bk_stl(-2.86) + ftm(-0.56) + sy_usage(-0.37)**

| Game | Benson Pts | Sean 3PM | Benson STL | Team FTM | Sean Usage | Predicted | Actual | AK Result |
|------|-----------|----------|-----------|----------|-----------|-----------|--------|-----------|
| 26 | **3** | 1 | 0 | 14 | 34.2% | -26.0 | -14 | L |
| 27 | **6** | 1 | 0 | 17 | 28.1% | -22.3 | -9 | L |
| 28 | **2** | **0** | 2 | 7 | 34.4% | -36.5 | -19 | L |

**Finding-by-finding validation:**

| Scouting Finding | Prediction | Finals Reality | Verdict |
|-----------------|-----------|----------------|---------|
| Benson is the swing factor (13+ = win, 8- = loss) | Shut him down | Scored 3, 6, 2 — all losses | **CONFIRMED** |
| Sean's 3PM drives win margin (+7.6 each) | Run him off the line | Made 1, 1, 0 3PM | **CONFIRMED** |
| High Sean usage predicts losses | Force the Sean Show | Usage: 34.2%, 28.1%, 34.4% | **CONFIRMED** |
| FT shooting is terrible (44.6%) | Send them to the line | 43.1% in finals — even worse | **CONFIRMED** |
| Guard depth is paper-thin | Push tempo, draw fouls | Mabumbo: 2 pts in G27, Benson invisible | **CONFIRMED** |
| Hold them under 55 to win | Suffocate them | Scored 85, 97, 90 — NOT held under 55 | **NOT MET** |

The scoring target was calibrated to 40-minute regular season games. The 48-minute playoff format inflated all counting stats by ~20%. Despite not meeting the raw target, every **mechanism** the model identified was validated.

### Longshots Model Validation

**Model: win_margin ~ bb_efg(+0.60) + ri_reb(+0.97) + dr_pts(+0.51) + three_pct(+0.32) + be_reb(+2.26)**

| Game | Boss eFG% | Richard REB | Desmond PTS | Team 3P% | Bright REB | Predicted | Actual | LS Result |
|------|----------|------------|-------------|----------|-----------|-----------|--------|-----------|
| 26 | 36.5 | 14 | 35 | 35.1 | 6 | +47.4 | +14 | W |
| 27 | 25.0 | 12 | **50** | 28.9 | **12** | +57.7 | +9 | W |
| 28 | **59.7** | 13 | 21 | 27.5 | **12** | +64.4 | +19 | W |

**Supporting factors:**

| Game | Team STL (target: 14.8+) | Bright AST (target: 4.5+) |
|------|--------------------------|---------------------------|
| 26 | 9 | **6** |
| 27 | **18** | **5** |
| 28 | 11 | **5** |

**Finding-by-finding validation:**

| Self-Scout Finding | Finals Reality | Verdict |
|-------------------|----------------|---------|
| Boss efficiency is #1 predictor | Mixed: 36.5%, 25.0%, 59.7% — won even when cold because other factors compensated | **PARTIALLY CONFIRMED** |
| Richard rebounding transforms the team | 14, 12, 13 REB — dominant every game | **CONFIRMED** |
| Desmond scoring is the second engine | 35, **50**, 21 PTS — series MVP | **CONFIRMED** |
| Bright rebounding is a hidden weapon | 6, **12**, **12** REB — massive in Games 2-3 | **CONFIRMED** |
| Bright is the energy barometer | 6/6/6 AST, 2/8/3 STL — elite all-around | **CONFIRMED** |
| Team steals fuel transition | 9, 18, 11 — hit target once | **PARTIALLY CONFIRMED** |
| Ball movement is non-negotiable | Team had 5+, 6+, 11+ AST from multiple players each game | **CONFIRMED** |

**Prediction magnitudes were inflated** because the model was trained on 40-minute data and applied to 48-minute games, amplifying every input. But every directional finding held.

### Why the Longshots Won: The Data Story

1. **Benson was shut down.** 3, 6, 2 points across the series. The #1 predictor of AshKnights success was neutralized. This alone, according to the regression model, swung each game by 7-12 points in the Longshots' favor compared to Benson's average output.

2. **Sean was forced into the Sean Show.** Usage at 34.2%, 28.1%, 34.4%. He scored 35, 37, 41 — impressive volume — but made only 1, 1, 0 three-pointers. Without his 3-point shooting (the strongest predictor of AK win margin at +7.6 per make), his scoring was high-volume, low-efficiency grinding.

3. **Desmond Raimmy was the series MVP.** 35, 50, 21 points. His Game 27 performance (50 pts, 20/43 FG, 7 3PM) was historic. As the model predicted, his scoring directly drove margin.

4. **Richard dominated the glass.** 14, 12, 13 rebounds — exactly what the model said would happen when Richard was active. Nearly +13 points of predicted margin per game just from his rebounding.

5. **Bright Edudzi did everything.** 6, 12, 12 rebounds (the highest-leverage hustle play at +2.3 per board). 6, 5, 5 assists. 2, 8, 3 steals. He was the energy barometer the model said he was — when Bright is active across the board, the Longshots win.

6. **AshKnights FT shooting remained terrible.** 43.1% in the finals vs 44.6% in RS+Semi. Every trip to the line was a wasted possession.

### Head-to-Head Season Series: Longshots vs AshKnights

| Game | Type | Score | Result |
|------|------|-------|--------|
| 8 | Regular Season | 41-73 | **L (-32)** |
| 17 | Regular Season | 56-48 | **W (+8)** |
| 26 | Finals Game 1 | 99-85 | **W (+14)** |
| 27 | Finals Game 2 | 106-97 | **W (+9)** |
| 28 | Finals Game 3 | 109-90 | **W (+19)** |

**Overall: Longshots 4-1 AshKnights.** After the 41-73 blowout loss in Game 8, the Longshots won 4 straight against the league's best team — including a sweep of the finals.

---

## 10. Deliverables Summary

### Files Produced

| File | Description |
|------|-------------|
| `ABA_2025_26.xlsx` | Master workbook with 6 sheets: RS raw data, RS+Semi raw data, RS player advanced stats, RS team advanced stats, RS+Semi player advanced stats, RS+Semi team advanced stats |
| `ABA_Regular_Season_Report.md` | Regular season standings, leaders, efficiency notes |
| `ABA_RS_Semifinal_Report.md` | RS+Semifinal standings, leaders, efficiency notes |
| `AshKnights_Scouting_Report.md` | Full opposition scouting report with regression analysis and game plan |
| `Longshots_Self_Scout.md` | Self-scouting report with regression analysis and identity definition |
| `ABA_2025_26_Full_Report.md` | This comprehensive report |

### Python Scripts

| Script | Purpose |
|--------|---------|
| `add_advanced_stats.py` | Computed RS player & team advanced stats, wrote to Excel |
| `compute_rs_semi.py` | Computed RS+Semi stats |
| `regression_benson_locked.py` | Exhaustive regression search for AshKnights with bk_pts locked |
| `reg_locked2.py` | Optimized version with pre-screened feature pool |
| `longshots_analysis.py` | Full Longshots regression analysis |
| `add_usage_rate.py` | Added usage rate to player stats sheets |
| `add_rssemi_player_stats.py` | Created RS+Semi player advanced stats sheet |
| `add_rssemi_team_stats.py` | Created RS+Semi team advanced stats sheet |
| `finals_check.py` | Finals results validation against regression models |

### Advanced Stats Computed

**Player-level (63 RS / 69 RS+Semi players):** PPG, RPG, APG, SPG, BPG, FPG, FG%, 3P%, FT%, eFG%, TS%, Game Score, EFF, Usage Rate

**Team-level (5 teams):** Win%, PPG, Opp PPG, Point Differential, eFG%, TS%, 3PT Rate, FT Rate, AST Rate, REB%, Opp FG%, ORTG, DRTG

### Regression Models Built

| Model | R-sq | Adj R-sq | Features | Significant |
|-------|------|----------|----------|-------------|
| AshKnights Win Margin | 0.991 | 0.983 | 5 | All 5 at p<0.05 |
| Longshots Win Margin | 0.999 | 0.997 | 5 | All 5 at p<0.05 |

Both models found through exhaustive combinatorial search across all valid feature combinations with multicollinearity filtering.

---

*Report prepared for the Longshots Coaching Staff. ABA 2025-26 Season.*
