# ABA 2025-26 Season Analytics

Basketball analytics project for the **Longshots** in the Ashesi Basketball Association (ABA) 2025-26 season. Covers the full pipeline from raw box scores to advanced stats, scouting reports, regression modeling, and post-season validation.

**Result: Longshots swept the AshKnights 3-0 to win the championship.**

## Project Structure

### Data
| File | Description |
|------|-------------|
| `ashesi_basketball_2025_26_full.csv` | Source data — 396 player-level box scores across 28 games (5 teams, 4 game types) |
| `ABA_2025_26.xlsx` | Master workbook with 6 sheets: RS and RS+Semi raw data, player advanced stats (with usage rate), and team advanced stats |

### Reports
| File | Description |
|------|-------------|
| `ABA_2025_26_Full_Report.md` | Comprehensive report covering everything: methodology, all stats, both scouting reports, regression models, finals validation |
| `ABA_Regular_Season_Report.md` | Regular season standings, scoring/rebounding/assists leaders, efficiency notes |
| `ABA_RS_Semifinal_Report.md` | Regular season + semifinal report with updated standings and leaders |
| `AshKnights_Scouting_Report.md` | Opposition scouting report with regression analysis, personnel breakdown, and game plan |
| `Longshots_Self_Scout.md` | Self-scouting report with regression analysis and team identity |

### Scripts
| File | Description |
|------|-------------|
| `add_advanced_stats.py` | Computes regular season player and team advanced stats (eFG%, TS%, Game Score, EFF, ORTG, DRTG) and writes to Excel |
| `compute_rs_semi.py` | Computes RS+Semifinal stats and prints leader boards |
| `add_usage_rate.py` | Adds usage rate to player advanced stats sheets |
| `add_rssemi_player_stats.py` | Creates RS+Semi player advanced stats sheet with all metrics |
| `add_rssemi_team_stats.py` | Creates RS+Semi team advanced stats sheet |
| `reg_locked2.py` | Exhaustive regression search for AshKnights win margin with Benson's points locked as a feature |
| `longshots_analysis.py` | Full Longshots regression analysis with exhaustive feature search |
| `finals_check.py` | Validates finals results against both regression models |

## Advanced Stats Computed

**Player-level:** eFG%, TS%, Game Score, EFF, Usage Rate

**Team-level:** ORTG, DRTG, eFG%, TS%, 3PT Rate, FT Rate, AST Rate, REB%, Opp FG%

## Key Findings

### AshKnights Regression Model (R-sq = 0.991)
Win margin predicted by: Benson Kas-Vorsah's points (+1.05), Sean Yeboah's 3PM (+7.56), Benson's steals (-2.86), team FTM (-0.56), Sean's usage rate (-0.37). All significant at p < 0.05.

### Longshots Regression Model (R-sq = 0.999)
Win margin predicted by: Boss Baeta's eFG% (+0.60), Richard's rebounds (+0.97), Desmond Raimmy's points (+0.51), team 3P% (+0.32), Bright Edudzi's rebounds (+2.26). All significant at p < 0.05.

### Finals Validation
Both models were directionally validated in the finals. Benson was held to 3, 6, 2 points (model predicted AshKnights lose when he scores under 8). Sean made only 1, 1, 0 three-pointers. Richard grabbed 14, 12, 13 rebounds. Desmond scored 35, 50, 21 points. The game plan worked.

## Tools Used

- Python (pandas, numpy, statsmodels, openpyxl, scipy)
- OLS regression with exhaustive combinatorial feature search
- Multicollinearity filtering (r > 0.85 exclusion)

## Data Notes

- Turnovers were not tracked (all zeros) — AST/TOV ratio excluded, possession estimates use `FGA + 0.44 * FTA`
- No OREB/DREB split — only total rebounds available
- Regular season games are 40 minutes; playoff games are 48 minutes — counting stats inflate ~20% in playoffs
- Small sample sizes (8-11 games per team) — regression models capped at 5 features
"# ABA-Analytics" 
