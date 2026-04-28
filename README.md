#  A Basketball Analytics Case Study


## Overview

The Ashesi Basketball Association (ABA), a five-team university league at Ashesi University, Ghana. Longshots finished the regular season 4-4. Using statistical analysis developed throughout the playoffs, we swept both series (2-0 vs Los Ashtros, 3-0 vs AshKnights) and won the championship.

This project documents the full analytics workflow: exploratory analysis, association/splits analysis, opponent scouting, and regression modeling. Every coaching decision in the playoffs was informed by the data in this notebook.

## Key Findings

**Team FG% is the master variable.** It explained 89.1% of our winning margin variance (R²=0.891). Above 35% FG we were 9-0. Below 35% we were 0-4. Every other insight in this project feeds into this one number.

**Team assists drive FG%.** Assists explained 61.7% of our FG% variance. More assists means better shot quality. When we got 22+ assists we never lost. The chain is clear: ball movement creates open shots, open shots raise FG%, higher FG% wins games.

**Bright Edudzi was our most important player and his box score never showed it.** Bright is our best off-ball defender. We assigned him to Benson , the AshKnights' second option, because the regression showed Benson's scoring was the strongest predictor of AshKnights wins (+0.668 correlation). Sean's scoring had near-zero correlation with their winning. Bright held Benson to 13, 4, 3, 6, and 2 points across five meetings. AshKnights went from 4-0 when Benson scores 13+ to losing every game in the finals.

Bright's assists tell a separate story. When Bright records high assists, it means we have broken the defense down and the ball is moving. He is not a primary creator. He is a connector. If Bright is getting 5-6 assists, it means the defense has collapsed and the ball is moving around. His assist totals correlated with team FG% at R²=0.442, the highest of any individual player.

**Desmond's improvement was the series arc.** In the regular season, Desmond shot 28.2% from the field and 16.7% from three. When he took 20+ shots, we were 0-3 and he shot 23.4%. When he took fewer than 20, we were 3-1 and he shot 33.3%. The association analysis told us to limit his volume and let the game come to him. In the playoffs, Desmond's scoring went 17, 40, 35, 50, 21 across five games. 

**Richard is a floor raiser.** He played only 2 of 8 regular season games. With him, our FG% jumped from 32.7% to 41.0%, our assists from 15.0 to 21.0, and our record was 2-0 vs 2-4 without him. Richard's gravity as a scorer and rebounder opened up everything for Boss and Desmond. In the playoffs he averaged 24.8 PPG on 56.7% shooting while guarding the opposing team's best player every night.


**High fouls correlate with winning, not losing.** This seems counterintuitive, but our foul totals were a byproduct of aggressive pressure defense. The same intensity that generated 14-17 steals per game also produced fouls. The steals created transition opportunities and easy baskets. The fouls were a cost of doing business, not a problem to solve.

**The AshKnights regression flipped the preparation focus.** Sean averaged 37.7 PPG in the finals and his team lost every game. Benson FG% explained 65.6% of AshKnights' margin variance. Sean's points explained 6.6%. We let their best player score and shut down the variable that actually mattered.

## Regression Targets

Before each finals game, we set specific targets derived from the regression analysis:

| Metric | Target | Game 1 | Game 2 | Game 3 |
|--------|--------|--------|--------|--------|
| Team FG% | >35% | 44.3% | 41.2% | 46.2% |
| Team AST | >22 | 24 | 32 | 38 |
| Team STL | >11 | 9 | 18 | 11 |
| Bright STL | >2 | 2 | 8 | 3 |
| Boss AST | >6 | 7 | 13 | 6 |
| Desmond 3PM | >3 | 8 | 7 | 5 |
| Benson PTS | <10 | 3 | 6 | 2 |
| **Result** | **Win** | **99-85** | **106-97** | **109-90** |

## Tools

- Python (pandas, NumPy, scikit-learn, SciPy)
- matplotlib, seaborn
- Google Colab

## Files

- `ABA_analytics.ipynb` — Full analysis notebook
- `ashesi_basketball_2025_26_full.csv` — Complete dataset (20 regular season + 8 playoff games, player-level box scores)

## How to Run

1. Upload both files to Google Drive
2. Open the notebook in Google Colab
3. Update the file path in the first cell to match your Drive location
4. Run all cells

## Author

**Paa Yaw** 
