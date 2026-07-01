import pandas as pd
import numpy as np
from openpyxl import load_workbook

# Load data
df = pd.read_csv(r'C:\Users\Paa Yaw\Downloads\ABA\ashesi_basketball_2025_26_full.csv')

# Filter to regular season
rs = df[df['game_type'].isin(['Regular Season', 'Regular Season (Forfeit)'])].copy()

# ============================================================
# PLAYER ADVANCED STATS
# ============================================================

# Per-game stats for Game Score and EFF (computed per game row, then averaged)
rs['game_score'] = (rs['pts'] + 0.4*rs['fgm'] - 0.7*rs['fga']
                    - 0.4*(rs['fta'] - rs['ftm']) + 0.5*rs['reb']
                    + rs['stl'] + 0.7*rs['ast'] + 0.7*rs['blk']
                    - 0.4*rs['fouls'] - rs['tov'])

rs['eff'] = ((rs['pts'] + rs['reb'] + rs['ast'] + rs['stl'] + rs['blk'])
             - ((rs['fga'] - rs['fgm']) + (rs['fta'] - rs['ftm']) + rs['tov']))

# Group by player+team
pg = rs.groupby(['player_name', 'team']).agg(
    position=('position', 'first'),
    games_played=('game_number', 'nunique'),
    # totals for per-game averages
    total_pts=('pts', 'sum'),
    total_reb=('reb', 'sum'),
    total_ast=('ast', 'sum'),
    total_stl=('stl', 'sum'),
    total_blk=('blk', 'sum'),
    total_tov=('tov', 'sum'),
    total_fouls=('fouls', 'sum'),
    # shooting totals
    total_fgm=('fgm', 'sum'),
    total_fga=('fga', 'sum'),
    total_3pm=('three_pm', 'sum'),
    total_3pa=('three_pa', 'sum'),
    total_ftm=('ftm', 'sum'),
    total_fta=('fta', 'sum'),
    # averages for game score and eff
    avg_game_score=('game_score', 'mean'),
    avg_eff=('eff', 'mean'),
).reset_index()

gp = pg['games_played']

player_stats = pd.DataFrame({
    'player_name': pg['player_name'],
    'team': pg['team'],
    'position': pg['position'],
    'games_played': gp,
    'ppg': (pg['total_pts'] / gp).round(1),
    'rpg': (pg['total_reb'] / gp).round(1),
    'apg': (pg['total_ast'] / gp).round(1),
    'spg': (pg['total_stl'] / gp).round(1),
    'bpg': (pg['total_blk'] / gp).round(1),
    'topg': (pg['total_tov'] / gp).round(1),
    'fpg': (pg['total_fouls'] / gp).round(1),
    'fgm': pg['total_fgm'],
    'fga': pg['total_fga'],
    'fg_pct': np.where(pg['total_fga'] > 0, (pg['total_fgm'] / pg['total_fga'] * 100).round(1), 0.0),
    'three_pm': pg['total_3pm'],
    'three_pa': pg['total_3pa'],
    'three_pct': np.where(pg['total_3pa'] > 0, (pg['total_3pm'] / pg['total_3pa'] * 100).round(1), 0.0),
    'ftm': pg['total_ftm'],
    'fta': pg['total_fta'],
    'ft_pct': np.where(pg['total_fta'] > 0, (pg['total_ftm'] / pg['total_fta'] * 100).round(1), 0.0),
    'efg_pct': np.where(pg['total_fga'] > 0, ((pg['total_fgm'] + 0.5 * pg['total_3pm']) / pg['total_fga'] * 100).round(1), 0.0),
    'ts_pct': np.where(
        (pg['total_fga'] + 0.44 * pg['total_fta']) > 0,
        (pg['total_pts'] / (2 * (pg['total_fga'] + 0.44 * pg['total_fta'])) * 100).round(1),
        0.0
    ),
    'game_score': pg['avg_game_score'].round(1),
    'eff': pg['avg_eff'].round(1),
    'ast_tov': np.where(pg['total_tov'] > 0, (pg['total_ast'] / pg['total_tov']).round(1), np.nan),
})

# Sort by ppg descending
player_stats = player_stats.sort_values('ppg', ascending=False).reset_index(drop=True)

# ============================================================
# TEAM ADVANCED STATS
# ============================================================

# Get one row per team per game for team-level stats
team_game = rs.groupby(['team', 'game_number']).agg(
    opponent=('opponent', 'first'),
    team_score=('team_score', 'first'),
    opponent_score=('opponent_score', 'first'),
    game_outcome=('game_outcome', 'first'),
    pts=('pts', 'sum'),
    reb=('reb', 'sum'),
    ast=('ast', 'sum'),
    stl=('stl', 'sum'),
    blk=('blk', 'sum'),
    tov=('tov', 'sum'),
    fouls=('fouls', 'sum'),
    fgm=('fgm', 'sum'),
    fga=('fga', 'sum'),
    three_pm=('three_pm', 'sum'),
    three_pa=('three_pa', 'sum'),
    ftm=('ftm', 'sum'),
    fta=('fta', 'sum'),
).reset_index()

# For opponent rebounds: look up opponent's team stats from the same game
opp_reb = team_game[['team', 'game_number', 'reb']].rename(columns={'team': 'opponent', 'reb': 'opp_reb'})
team_game = team_game.merge(opp_reb, on=['opponent', 'game_number'], how='left')

# Opponent shooting stats
opp_shooting = team_game[['team', 'game_number', 'fgm', 'fga']].rename(
    columns={'team': 'opponent', 'fgm': 'opp_fgm', 'fga': 'opp_fga'})
team_game = team_game.merge(opp_shooting, on=['opponent', 'game_number'], how='left')

# Opponent points (from player sums for the opponent team in same game)
opp_pts = team_game[['team', 'game_number', 'pts']].rename(
    columns={'team': 'opponent', 'pts': 'opp_pts_sum'})
team_game = team_game.merge(opp_pts, on=['opponent', 'game_number'], how='left')

# Opponent possessions
opp_poss_data = team_game[['team', 'game_number', 'fga', 'tov', 'fta']].rename(
    columns={'team': 'opponent', 'fga': 'opp_fga_poss', 'tov': 'opp_tov', 'fta': 'opp_fta_poss'})
team_game = team_game.merge(opp_poss_data, on=['opponent', 'game_number'], how='left')

# Aggregate per team
team_agg = team_game.groupby('team').agg(
    games_played=('game_number', 'nunique'),
    wins=('game_outcome', lambda x: (x == 'Won').sum()),
    total_pts=('pts', 'sum'),
    total_opp_pts=('opponent_score', lambda x: x.astype(float).sum()),
    total_fgm=('fgm', 'sum'),
    total_fga=('fga', 'sum'),
    total_3pm=('three_pm', 'sum'),
    total_3pa=('three_pa', 'sum'),
    total_ftm=('ftm', 'sum'),
    total_fta=('fta', 'sum'),
    total_ast=('ast', 'sum'),
    total_tov=('tov', 'sum'),
    total_reb=('reb', 'sum'),
    total_opp_reb=('opp_reb', 'sum'),
    total_opp_fgm=('opp_fgm', 'sum'),
    total_opp_fga=('opp_fga', 'sum'),
    total_opp_pts_sum=('opp_pts_sum', 'sum'),
    total_opp_fga_poss=('opp_fga_poss', 'sum'),
    total_opp_tov=('opp_tov', 'sum'),
    total_opp_fta_poss=('opp_fta_poss', 'sum'),
).reset_index()

ta = team_agg
gp_t = ta['games_played']

team_poss = ta['total_fga'] + ta['total_tov'] + 0.44 * ta['total_fta']

team_stats = pd.DataFrame({
    'team': ta['team'],
    'games_played': gp_t,
    'wins': ta['wins'],
    'losses': gp_t - ta['wins'],
    'win_pct': (ta['wins'] / gp_t * 100).round(1),
    'ppg': (ta['total_pts'] / gp_t).round(1),
    'opp_ppg': (ta['total_opp_pts'] / gp_t).round(1),
    'point_differential': ((ta['total_pts'] - ta['total_opp_pts']) / gp_t).round(1),
    'team_efg_pct': np.where(ta['total_fga'] > 0, ((ta['total_fgm'] + 0.5 * ta['total_3pm']) / ta['total_fga'] * 100).round(1), 0.0),
    'team_ts_pct': np.where(
        (ta['total_fga'] + 0.44 * ta['total_fta']) > 0,
        (ta['total_pts'] / (2 * (ta['total_fga'] + 0.44 * ta['total_fta'])) * 100).round(1),
        0.0
    ),
    'three_pt_rate': np.where(ta['total_fga'] > 0, (ta['total_3pa'] / ta['total_fga'] * 100).round(1), 0.0),
    'ft_rate': np.where(ta['total_fga'] > 0, (ta['total_fta'] / ta['total_fga'] * 100).round(1), 0.0),
    'ast_rate': np.where(ta['total_fgm'] > 0, (ta['total_ast'] / ta['total_fgm'] * 100).round(1), 0.0),
    'team_ast_tov': np.where(ta['total_tov'] > 0, (ta['total_ast'] / ta['total_tov']).round(1), np.nan),
    'reb_pct': np.where(
        (ta['total_reb'] + ta['total_opp_reb']) > 0,
        (ta['total_reb'] / (ta['total_reb'] + ta['total_opp_reb']) * 100).round(1),
        0.0
    ),
    'opp_fg_pct': np.where(ta['total_opp_fga'] > 0, (ta['total_opp_fgm'] / ta['total_opp_fga'] * 100).round(1), 0.0),
    'off_rating': np.where(team_poss > 0, (ta['total_pts'] / team_poss * 100).round(1), 0.0),
    'def_rating': np.where(team_poss > 0, (ta['total_opp_pts_sum'] / team_poss * 100).round(1), 0.0),
})

team_stats = team_stats.sort_values('win_pct', ascending=False).reset_index(drop=True)

# ============================================================
# WRITE TO EXCEL (preserving existing sheets)
# ============================================================

excel_path = r'C:\Users\Paa Yaw\Downloads\ABA\ABA_2025_26.xlsx'

with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    player_stats.to_excel(writer, sheet_name='Player Advanced Stats', index=False)
    team_stats.to_excel(writer, sheet_name='Team Advanced Stats', index=False)

print("Done! Sheets written.")
print(f"\nPlayer Advanced Stats: {len(player_stats)} rows")
print(player_stats.head(10).to_string())
print(f"\nTeam Advanced Stats: {len(team_stats)} rows")
print(team_stats.to_string())
