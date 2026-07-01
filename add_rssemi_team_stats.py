import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\Paa Yaw\Downloads\ABA\ashesi_basketball_2025_26_full.csv')
rs = df[df['game_type'].isin(['Regular Season', 'Regular Season (Forfeit)', 'Playoff - Semifinal'])].copy()

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

# Opponent stats from same games
opp_reb = team_game[['team', 'game_number', 'reb']].rename(columns={'team': 'opponent', 'reb': 'opp_reb'})
team_game = team_game.merge(opp_reb, on=['opponent', 'game_number'], how='left')

opp_shooting = team_game[['team', 'game_number', 'fgm', 'fga']].rename(
    columns={'team': 'opponent', 'fgm': 'opp_fgm', 'fga': 'opp_fga'})
team_game = team_game.merge(opp_shooting, on=['opponent', 'game_number'], how='left')

opp_pts = team_game[['team', 'game_number', 'pts']].rename(
    columns={'team': 'opponent', 'pts': 'opp_pts_sum'})
team_game = team_game.merge(opp_pts, on=['opponent', 'game_number'], how='left')

opp_poss_data = team_game[['team', 'game_number', 'fga', 'fta']].rename(
    columns={'team': 'opponent', 'fga': 'opp_fga_poss', 'fta': 'opp_fta_poss'})
team_game = team_game.merge(opp_poss_data, on=['opponent', 'game_number'], how='left')

ta = team_game.groupby('team').agg(
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
    total_reb=('reb', 'sum'),
    total_opp_reb=('opp_reb', 'sum'),
    total_opp_fgm=('opp_fgm', 'sum'),
    total_opp_fga=('opp_fga', 'sum'),
    total_opp_pts_sum=('opp_pts_sum', 'sum'),
).reset_index()

gp = ta['games_played']
team_poss = ta['total_fga'] + 0.44 * ta['total_fta']

team_stats = pd.DataFrame({
    'team': ta['team'],
    'games_played': gp,
    'wins': ta['wins'],
    'losses': gp - ta['wins'],
    'win_pct': (ta['wins'] / gp * 100).round(1),
    'ppg': (ta['total_pts'] / gp).round(1),
    'opp_ppg': (ta['total_opp_pts'] / gp).round(1),
    'point_differential': ((ta['total_pts'] - ta['total_opp_pts']) / gp).round(1),
    'team_efg_pct': np.where(ta['total_fga'] > 0, ((ta['total_fgm'] + 0.5 * ta['total_3pm']) / ta['total_fga'] * 100).round(1), 0.0),
    'team_ts_pct': np.where(
        (ta['total_fga'] + 0.44 * ta['total_fta']) > 0,
        (ta['total_pts'] / (2 * (ta['total_fga'] + 0.44 * ta['total_fta'])) * 100).round(1),
        0.0
    ),
    'three_pt_rate': np.where(ta['total_fga'] > 0, (ta['total_3pa'] / ta['total_fga'] * 100).round(1), 0.0),
    'ft_rate': np.where(ta['total_fga'] > 0, (ta['total_fta'] / ta['total_fga'] * 100).round(1), 0.0),
    'ast_rate': np.where(ta['total_fgm'] > 0, (ta['total_ast'] / ta['total_fgm'] * 100).round(1), 0.0),
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

excel_path = r'C:\Users\Paa Yaw\Downloads\ABA\ABA_2025_26.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    team_stats.to_excel(writer, sheet_name='Team Advanced Stats RS+Semi', index=False)

print(f"Team Advanced Stats RS+Semi: {len(team_stats)} rows\n")
print(team_stats.to_string(index=False))
print("\nDone!")
