import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\Users\Paa Yaw\Downloads\ABA\ashesi_basketball_2025_26_full.csv')
rs = df[df['game_type'].isin(['Regular Season', 'Regular Season (Forfeit)', 'Playoff - Semifinal'])].copy()

# Game Score and EFF per row
rs['game_score'] = (rs['pts'] + 0.4*rs['fgm'] - 0.7*rs['fga']
                    - 0.4*(rs['fta'] - rs['ftm']) + 0.5*rs['reb']
                    + rs['stl'] + 0.7*rs['ast'] + 0.7*rs['blk']
                    - 0.4*rs['fouls'] - rs['tov'])
rs['eff'] = ((rs['pts'] + rs['reb'] + rs['ast'] + rs['stl'] + rs['blk'])
             - ((rs['fga'] - rs['fgm']) + (rs['fta'] - rs['ftm']) + rs['tov']))

# Team possessions per game (for usage rate)
team_poss = rs.groupby(['team', 'game_number']).agg(
    team_fga=('fga', 'sum'), team_fta=('fta', 'sum')
).reset_index()
team_poss['team_poss'] = team_poss['team_fga'] + 0.44 * team_poss['team_fta']
rs = rs.merge(team_poss[['team', 'game_number', 'team_poss']], on=['team', 'game_number'])
rs['player_poss'] = rs['fga'] + 0.44 * rs['fta']
rs['usage_rate_game'] = np.where(rs['team_poss'] > 0, rs['player_poss'] / rs['team_poss'] * 100, 0)

pg = rs.groupby(['player_name', 'team']).agg(
    position=('position', 'first'),
    games_played=('game_number', 'nunique'),
    total_pts=('pts', 'sum'),
    total_reb=('reb', 'sum'),
    total_ast=('ast', 'sum'),
    total_stl=('stl', 'sum'),
    total_blk=('blk', 'sum'),
    total_tov=('tov', 'sum'),
    total_fouls=('fouls', 'sum'),
    total_fgm=('fgm', 'sum'),
    total_fga=('fga', 'sum'),
    total_3pm=('three_pm', 'sum'),
    total_3pa=('three_pa', 'sum'),
    total_ftm=('ftm', 'sum'),
    total_fta=('fta', 'sum'),
    avg_game_score=('game_score', 'mean'),
    avg_eff=('eff', 'mean'),
    avg_usage=('usage_rate_game', 'mean'),
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
    'usage_rate': pg['avg_usage'].round(1),
})

player_stats = player_stats.sort_values('ppg', ascending=False).reset_index(drop=True)

excel_path = r'C:\Users\Paa Yaw\Downloads\ABA\ABA_2025_26.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    player_stats.to_excel(writer, sheet_name='Player Advanced Stats RS+Semi', index=False)

print(f"Player Advanced Stats RS+Semi: {len(player_stats)} rows")
print("\nTop 15 by usage rate:")
print(player_stats.nlargest(15, 'usage_rate')[['player_name', 'team', 'games_played', 'ppg', 'efg_pct', 'ts_pct', 'usage_rate']].to_string(index=False))
print("\nDone!")
