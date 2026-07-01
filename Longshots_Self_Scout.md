# Longshots Self-Scouting Report
### ABA 2025-26 | Regular Season + Semifinals

---

## Overview

| Stat | Value |
|------|-------|
| Record | 6-4 (60.0%) |
| PPG | 59.9 |
| Opp PPG | 55.6 |
| Point Diff | +4.3 |
| ORTG | 85.4 |
| DRTG | 79.2 |

The Longshots are a streaky team — they started 1-4 and finished on a 5-0 run. When their offense clicks, they blow teams out. When it doesn't, they're below average.

---

## Game Log

| Game | Date | Opponent | Score | Result | Margin |
|------|------|----------|-------|--------|--------|
| 2 | Oct 2 | Los Ashtros | 56-59 | L | -3 |
| 6 | Oct 15 | Berekusu Warriors | 61-51 | W | +10 |
| 8 | Nov 12 | AshKnights | 41-73 | L | -32 |
| 10 | Nov 19 | HillBlazers | 55-61 | L | -6 |
| 12 | Nov 26 | Los Ashtros | 37-45 | L | -8 |
| 14 | Dec 3 | HillBlazers | 49-46 | W | +3 |
| 17 | Feb 11 | AshKnights | 56-48 | W | +8 |
| 20 | Feb 13 | Berekusu Warriors | 63-55 | W | +8 |
| 21 | Feb 18 | Los Ashtros | 90-58 | W | +32 |
| 22 | Feb 25 | Los Ashtros | 91-60 | W | +31 |

The team clearly improved as the season progressed. The last 5 games are all wins, including two blowouts (90-58, 91-60).

---

## Key Personnel

### Boss Baeta (PG) — The Leader
| PPG | RPG | APG | SPG | eFG% | TS% | Games |
|-----|-----|-----|-----|------|-----|-------|
| 19.5 | 8.5 | 5.6 | 2.3 | 45.6 | 47.9 | 10 |

- **32.6% of all team points** — the primary scorer and playmaker
- Elite all-around player: scoring, rebounding (8.5 for a PG), assists, steals
- His **eFG% is the strongest individual predictor** of win margin (+0.525 correlation, appears in best models at p < 0.001)
- When Boss shoots efficiently, the Longshots win. When he's cold, they struggle.

### Desmond Raimmy (SG) — The Second Star
| PPG | RPG | APG | SPG | eFG% | TS% | Games |
|-----|-----|-----|-----|------|-----|-------|
| 19.4 | 5.0 | 3.8 | 3.1 | 40.6 | 41.8 | 9 |

- **29.2% of all team points** — second scoring option
- Active hands on defense (3.1 SPG)
- Lower efficiency than Baeta (41.8 TS%) — volume shooter
- **REGRESSION FINDING:** Desmond's points are a significant predictor of win margin (+0.508, p=0.001 in best model). His 3-point shooting (dr_3pct, r=+0.659, p=0.038) is particularly important.

### Richard (PF) — The X-Factor
| PPG | RPG | APG | SPG | eFG% | TS% | Games |
|-----|-----|-----|-----|------|-----|-------|
| 24.0 | 16.5 | 3.5 | 3.8 | 55.6 | 55.2 | 4 |

- The most dominant player in the league when available — 24.0/16.5/3.5 on elite efficiency
- Only played 4 games but his impact is massive
- **REGRESSION FINDING:** Richard's rebounds are a significant predictor of win margin (+0.968, p=0.0001). When Richard is on the glass, the Longshots dominate.
- His availability changes the team's ceiling entirely.

### Bright Edudzi (SF) — The Glue Guy
| PPG | RPG | APG | SPG | eFG% | TS% | Games |
|-----|-----|-----|-----|------|-----|-------|
| 4.3 | 5.0 | 3.9 | 2.6 | 38.4 | 37.8 | 10 |

- Doesn't score much but does everything else: 5.0 RPG, 3.9 APG, 2.6 SPG
- **REGRESSION FINDING:** Bright's rebounds are a significant predictor of win margin (+2.261, p=0.0003). When Bright crashes the boards, the team wins bigger. This is a hustle/energy indicator.

### Arnold Agamah (C) — The Anchor
| PPG | RPG | SPG | Games |
|-----|-----|-----|-------|
| 1.9 | 4.9 | 2.0 | 10 |

- Not a scorer but plays every game
- 2.0 SPG — active defensively
- His steals show up in regression models as a significant factor

### Joseph Ajak (SF) — Role Player
| PPG | RPG | APG | Games |
|-----|-----|-----|-------|
| 2.6 | 4.2 | 1.4 | 9 |

- Rebounder and connector — 4.2 RPG, 1.4 APG
- His points appear positively in some regression models — scoring from him is a bonus

### Joshua Babu (C) — Backup Big
| PPG | RPG | Games |
|-----|-----|-------|
| 2.0 | 6.0 | 5 |

- Strong rebounder in limited minutes (6.0 RPG)
- **REGRESSION FINDING:** His points are *negatively* correlated with win margin (-0.735). When Babu is scoring, it likely means the starters are struggling.

### Samuel Duke (SF) — Spark Plug
| PPG | SPG | Games |
|-----|-----|-------|
| 1.0 | 0.8 | 4 |

- Limited minutes but significant impact in regression models
- His points (+17.0 correlation coefficient univariate, p=0.010) and steals (+22.4, p=0.081) predict big wins — he's a momentum player off the bench

---

## Scoring Distribution

| Player | % of Team Points |
|--------|-----------------|
| Boss Baeta | 32.6% |
| Desmond Raimmy | 29.2% |
| Richard | 16.0% |
| Bright Edudzi | 7.2% |
| Joseph Ajak | 3.8% |
| Arnold Agamah | 3.2% |

**61.8% of scoring comes from Baeta + Raimmy.** With Richard available, the load is more balanced (16%). Without Richard, the team is heavily two-man dependent.

---

## Wins vs Losses

| Stat | Wins (6) | Losses (4) |
|------|----------|-----------|
| PPG | 68.3 | 47.2 |
| Opp PPG | 53.0 | 59.5 |
| FG% | 43.3% | 28.2% |
| 3PM/3PA | 5.8/23.8 | 4.0/24.5 |
| FTM/FTA | 8.5/18.5 | 6.8/15.2 |
| REB | 41.8 | 39.8 |
| AST | 22.5 | 13.2 |
| STL | 14.8 | 10.0 |
| Fouls | 15.5 | 6.2 |

**Key differences:**
- **FG% swings massively** — 43.3% in wins vs 28.2% in losses. Shooting efficiency is the #1 driver.
- **Assists nearly double in wins** (22.5 vs 13.2) — ball movement is critical.
- **Steals are 50% higher in wins** (14.8 vs 10.0) — defensive intensity fuels the offense.
- **Fouls are HIGHER in wins** (15.5 vs 6.2) — counterintuitive, but the Longshots play more physically when winning. They're more aggressive, which generates both fouls and steals.

---

## Opponent Breakdown

| Opponent | Record | PPG | Opp PPG | Diff |
|----------|--------|-----|---------|------|
| Los Ashtros | 2-2 | 68.5 | 55.5 | +13.0 |
| Berekusu Warriors | 2-0 | 62.0 | 53.0 | +9.0 |
| AshKnights | 1-1 | 48.5 | 60.5 | -12.0 |
| HillBlazers | 1-1 | 52.0 | 53.5 | -1.5 |

The AshKnights are the toughest matchup — the only opponent with a negative point differential. The 41-73 loss (Game 8) is the worst result of the season, but the team bounced back to beat them 56-48 (Game 17).

---

## Home vs Away

| Split | Record | PPG | Opp PPG |
|-------|--------|-----|---------|
| Home | 3-3 | 61.2 | 59.8 |
| Away | 3-1 | 58.0 | 49.2 |

Better on the road. Home games are tighter.

---

## Regression Model: What Drives Longshots Win Margin

### Best Model (R-squared = 0.999, all 5 features significant at p < 0.05)

| Variable | Coefficient | p-value | Meaning |
|----------|------------|---------|---------|
| **bb_efg** (Boss eFG%) | +0.604 | 0.0000 | Each 1% increase in Boss shooting efficiency = +0.6 margin |
| **ri_reb** (Richard rebounds) | +0.968 | 0.0001 | Each Richard rebound = +1.0 margin |
| **dr_pts** (Desmond points) | +0.508 | 0.0006 | Each Desmond point = +0.5 margin |
| **three_pct** (Team 3P%) | +0.322 | 0.006 | Each 1% increase in 3P shooting = +0.3 margin |
| **be_reb** (Bright rebounds) | +2.261 | 0.0003 | Each Bright rebound = +2.3 margin |

**Model fit:** R-sq = 0.999, Adj R-sq = 0.997, F-statistic = 676.7, p = 0.000006

### What this tells us about our identity

1. **Boss Baeta's efficiency is everything** — Not his volume, his *efficiency*. When Boss takes smart shots and hits them, the whole offense opens up. He should be selective, not volume-heavy.

2. **Richard's rebounding transforms the team** — Each rebound adds nearly a full point of margin. When Richard is available and active on the boards, the Longshots are a different team.

3. **Desmond's scoring is the second engine** — His points directly drive margin. He needs to keep shooting, even on tough nights.

4. **3-point shooting unlocks blowouts** — The team's 3P% is the team-level shooting factor that matters. Spacing and shot-making from deep opens everything else.

5. **Bright Edudzi's rebounding is a hidden weapon** — At +2.3 per rebound, his effort on the glass is the highest-value hustle play on the team. He should crash the boards every possession.

### Univariate Correlations with Win Margin (Top 15)

| Feature | Correlation | p-value |
|---------|------------|---------|
| Team eFG% | +0.977 | 0.0000 |
| Team FG% | +0.944 | 0.0000 |
| eFG% differential | +0.889 | 0.0006 |
| Team FGM | +0.852 | 0.0017 |
| Assist differential | +0.841 | 0.0023 |
| FG% differential | +0.795 | 0.0060 |
| Samuel Duke pts | +0.764 | 0.0101 |
| Richard rebounds | +0.761 | 0.0106 |
| Team 3P% | +0.747 | 0.0130 |
| Team assists | +0.733 | 0.0158 |
| Team 3PM | +0.728 | 0.0170 |
| Richard assists | +0.695 | 0.0256 |
| Supporting cast pts | +0.676 | 0.0319 |
| Richard steals | +0.675 | 0.0324 |
| Team steals | +0.670 | 0.0340 |

### Other Strong Models (all features significant at p < 0.05)

| Model | R-sq | Adj R-sq |
|-------|------|----------|
| efg + fgpd + sd_pts + be_reb + dr_pts | 0.999 | 0.997 |
| fgpd + sd_pts + oftm + be_reb + dr_pts | 0.999 | 0.997 |
| jg_fga + bb_efg + be_reb + ja_pts + dr_pts | 0.998 | 0.996 |
| fgpd + sd_pts + ri_reb + oftm + dr_pts | 0.998 | 0.996 |

Across all models: **Boss Baeta's efficiency**, **Desmond Raimmy's scoring**, **Bright Edudzi's rebounding**, and **shooting differentials** appear consistently.

---

## Keys to Beating AshKnights

Based on our self-scouting and the AshKnights scouting report:

1. **Boss must be efficient, not just active** — His eFG% is the #1 predictor of our wins. Take smart shots. Don't force.

2. **Get Richard on the glass** — If Richard is available, his rebounding alone adds ~1 point of margin per board. He needs to dominate the paint.

3. **Desmond must keep shooting** — Even when it's tough. His scoring is a direct margin driver. Attack from 3 if possible (his 3P% is significant).

4. **Bright Edudzi does everything** — His rebounding is worth +2.3 per rebound (highest-leverage hustle play). His assists also jump in wins (4.5 vs 3.0) and his steals triple (3.7 vs 1.0). He's the energy barometer — when Bright is active across the board, we win.

5. **Generate steals** — Team steals are significantly correlated with winning (r=+0.670, p=0.034). We average 14.8 SPG in wins vs 10.0 in losses. Steals fuel transition which drives FG%. Everyone needs active hands.

6. **Shoot 3s well** — Team 3P% is a significant predictor. Get good looks from deep, don't settle for contested ones.

7. **Play physical** — Our fouls are HIGHER in wins (15.5 vs 6.2). We win when we play aggressive, not passive. Crash boards, draw contact, disrupt passing lanes.

8. **Move the ball** — 22.5 assists in wins vs 13.2 in losses. Ball movement is non-negotiable.

---

## Scoring Targets

### League-Wide Thresholds

| Score | Win Rate |
|-------|----------|
| 45-49 | 37.5% |
| 50-54 | 33.3% |
| 55-59 | 50.0% |
| 60-64 | 62.5% |
| 70+ | 73.0% |
| 75+ | 100.0% |

The league-wide crossover is ~59 points — that's where P(win) = 50%.

### Longshots Scoring Reality

| Split | Our PPG | Opp PPG |
|-------|---------|---------|
| Wins (6) | 68.3 | 53.0 |
| Losses (4) | 47.2 | 59.5 |

- **Lowest winning score: 49** (vs HillBlazers)
- **Highest losing score: 56** (vs Los Ashtros)
- **Our crossover: ~57 points.** Above that, we've always won. Below, we've always lost.

### vs AshKnights Target

The AshKnights score 69.1 PPG on average but we beat them 56-48 by holding them to 48 — way below their average. Teams that beat them scored 56, 58, and 74. Teams that scored 64, 65, even 73 and 110 still lost to them.

**The target isn't a specific offensive number — it's holding the AshKnights under 55 while scoring 55+.** Defense wins this matchup, not offense. We can't outgun a team that averages 69.1 PPG, but we can suffocate them.

---

## Summary

The Longshots are a team built on two stars (Baeta + Raimmy = 61.8% of scoring), elevated by Richard's availability and Bright Edudzi's all-around hustle. The regression is clear: **Boss's efficiency, Desmond's scoring, team 3-point shooting, and rebounding from Richard and Bright drive our wins.** Team steals (14.8 in wins vs 10.0 in losses) and Bright's assists (4.5 vs 3.0) are strong supporting indicators of winning — they fuel the transition game that makes this team dangerous. When all cylinders fire, we blow teams out (+31, +32). When the offense stalls and becomes iso-heavy, we lose. Against the AshKnights, we need Boss to be smart, Desmond to be aggressive, Bright to do everything, and the whole team to generate steals, crash the glass, and move the ball.
