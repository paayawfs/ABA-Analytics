import pandas as pd

df = pd.read_csv('ashesi_basketball_2025_26_full.csv')
rs = df[df['game_type'].isin(['Regular Season', 'Regular Season (Forfeit)', 'Playoff - Semifinal'])]

# TEAM STATS
team_games = rs.groupby(['team','game_number']).first().reset_index()
team_agg = team_games.groupby('team').agg(
    games_played=('game_number','nunique'),
    wins=('game_outcome', lambda x: (x=='Won').sum()),
    losses=('game_outcome', lambda x: (x=='Lost').sum()),
    total_pts=('team_score','sum'),
    total_opp_pts=('opponent_score','sum')
).reset_index()
team_agg['win_pct'] = (team_agg['wins']/team_agg['games_played']*100).round(1)
team_agg['ppg'] = (team_agg['total_pts']/team_agg['games_played']).round(1)
team_agg['opp_ppg'] = (team_agg['total_opp_pts']/team_agg['games_played']).round(1)
team_agg['point_differential'] = (team_agg['ppg'] - team_agg['opp_ppg']).round(1)

team_shooting = rs.groupby('team').agg(
    fgm=('fgm','sum'), fga=('fga','sum'),
    three_pm=('three_pm','sum'), three_pa=('three_pa','sum'),
    ftm=('ftm','sum'), fta=('fta','sum'),
    ast=('ast','sum'), reb=('reb','sum')
).reset_index()
pts_by_team = rs.groupby('team')['pts'].sum().reset_index().rename(columns={'pts':'total_player_pts'})
team_shooting = team_shooting.merge(pts_by_team, on='team')
team_shooting['team_efg_pct'] = ((team_shooting['fgm'] + 0.5*team_shooting['three_pm'])/team_shooting['fga']*100).round(1)
team_shooting['team_ts_pct'] = (team_shooting['total_player_pts'] / (2*(team_shooting['fga'] + 0.44*team_shooting['fta']))*100).round(1)
team_shooting['three_pt_rate'] = (team_shooting['three_pa']/team_shooting['fga']*100).round(1)
team_shooting['ft_rate'] = (team_shooting['fta']/team_shooting['fga']*100).round(1)
team_shooting['ast_rate'] = (team_shooting['ast']/team_shooting['fgm']*100).round(1)
team_shooting['possessions'] = team_shooting['fga'] + 0.44*team_shooting['fta']

opp = rs.groupby('opponent').agg(opp_fgm=('fgm','sum'), opp_fga=('fga','sum'), opp_reb=('reb','sum')).reset_index().rename(columns={'opponent':'team'})
team_shooting = team_shooting.merge(opp, on='team', how='left')
team_shooting['opp_fg_pct'] = (team_shooting['opp_fgm']/team_shooting['opp_fga']*100).round(1)
team_shooting['reb_pct'] = (team_shooting['reb']/(team_shooting['reb']+team_shooting['opp_reb'])*100).round(1)

team_final = team_agg.merge(team_shooting[['team','team_efg_pct','team_ts_pct','three_pt_rate','ft_rate','ast_rate','reb_pct','opp_fg_pct','possessions','total_player_pts']], on='team')
team_final['off_rating'] = (team_final['total_player_pts']/team_final['possessions']*100).round(1)
team_final['def_rating'] = (team_final['total_opp_pts']/team_final['possessions']*100).round(1)

print('=== TEAM STATS ===')
cols = ['team','games_played','wins','losses','win_pct','ppg','opp_ppg','point_differential','team_efg_pct','team_ts_pct','three_pt_rate','ft_rate','ast_rate','reb_pct','opp_fg_pct','off_rating','def_rating']
print(team_final[cols].sort_values('win_pct', ascending=False).to_string(index=False))

# PLAYER STATS
pa = rs.groupby(['player_name','team','position']).agg(
    games_played=('game_number','nunique'),
    total_pts=('pts','sum'), total_reb=('reb','sum'), total_ast=('ast','sum'),
    total_stl=('stl','sum'), total_blk=('blk','sum'), total_tov=('tov','sum'),
    total_fouls=('fouls','sum'),
    total_fgm=('fgm','sum'), total_fga=('fga','sum'),
    total_3pm=('three_pm','sum'), total_3pa=('three_pa','sum'),
    total_ftm=('ftm','sum'), total_fta=('fta','sum')
).reset_index()

p = pa
p['ppg'] = (p['total_pts']/p['games_played']).round(1)
p['rpg'] = (p['total_reb']/p['games_played']).round(1)
p['apg'] = (p['total_ast']/p['games_played']).round(1)
p['spg'] = (p['total_stl']/p['games_played']).round(1)
p['bpg'] = (p['total_blk']/p['games_played']).round(1)
p['fg_pct'] = (p['total_fgm']/p['total_fga']*100).round(1)
p['efg_pct'] = ((p['total_fgm']+0.5*p['total_3pm'])/p['total_fga']*100).round(1)
p['ts_pct'] = (p['total_pts']/(2*(p['total_fga']+0.44*p['total_fta']))*100).round(1)

gs = rs.copy()
gs['game_score'] = gs['pts'] + 0.4*gs['fgm'] - 0.7*gs['fga'] - 0.4*(gs['fta']-gs['ftm']) + 0.5*gs['reb'] + gs['stl'] + 0.7*gs['ast'] + 0.7*gs['blk'] - 0.4*gs['fouls'] - gs['tov']
gs['eff'] = (gs['pts']+gs['reb']+gs['ast']+gs['stl']+gs['blk']) - ((gs['fga']-gs['fgm'])+(gs['fta']-gs['ftm'])+gs['tov'])
gs_avg = gs.groupby(['player_name','team']).agg(game_score=('game_score','mean'), eff=('eff','mean')).reset_index()
gs_avg['game_score'] = gs_avg['game_score'].round(1)
gs_avg['eff'] = gs_avg['eff'].round(1)
p = p.merge(gs_avg, on=['player_name','team'], how='left')

print('\n=== TOP 10 SCORERS ===')
print(p.nlargest(10,'ppg')[['player_name','team','position','games_played','ppg','rpg','apg','fg_pct','efg_pct','ts_pct']].to_string(index=False))
print('\n=== TOP 10 REBOUNDERS ===')
print(p.nlargest(10,'rpg')[['player_name','team','rpg','games_played']].to_string(index=False))
print('\n=== TOP 10 ASSISTS ===')
print(p.nlargest(10,'apg')[['player_name','team','apg','games_played']].to_string(index=False))
print('\n=== TOP 10 GAME SCORE ===')
print(p.nlargest(10,'game_score')[['player_name','team','game_score','ppg','efg_pct','ts_pct']].to_string(index=False))
print('\n=== TOP 5 STEALS ===')
print(p.nlargest(5,'spg')[['player_name','team','spg','games_played']].to_string(index=False))
print('\n=== TOP 5 BLOCKS ===')
print(p.nlargest(5,'bpg')[['player_name','team','bpg','games_played']].to_string(index=False))
print('\n=== TOP 10 EFF ===')
print(p.nlargest(10,'eff')[['player_name','team','eff','ppg','rpg','apg']].to_string(index=False))
print('\n=== TOP 10 TS% (min 3 games, min 15 fga) ===')
q = p[(p['games_played']>=3) & (p['total_fga']>=15)]
print(q.nlargest(10,'ts_pct')[['player_name','team','ts_pct','efg_pct','ppg','total_fga']].to_string(index=False))
