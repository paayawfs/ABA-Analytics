import pandas as pd
import numpy as np
from openpyxl import load_workbook

df = pd.read_csv(r'C:\Users\Paa Yaw\Downloads\ABA\ashesi_basketball_2025_26_full.csv')

# Usage rate = (Player FGA + 0.44 * Player FTA) / (Team FGA + 0.44 * Team FTA) * 100
# TOV is all zeros so excluded

def compute_usage(subset, label):
    # Team possessions per game
    team_poss = subset.groupby(['team', 'game_number']).agg(
        team_fga=('fga', 'sum'),
        team_fta=('fta', 'sum')
    ).reset_index()
    team_poss['team_poss'] = team_poss['team_fga'] + 0.44 * team_poss['team_fta']

    # Merge back to player rows
    merged = subset.merge(team_poss[['team', 'game_number', 'team_poss']], on=['team', 'game_number'])
    merged['player_poss'] = merged['fga'] + 0.44 * merged['fta']
    merged['usage_rate'] = np.where(merged['team_poss'] > 0,
                                     merged['player_poss'] / merged['team_poss'] * 100, 0)

    # Average usage rate per player across games
    player_usage = merged.groupby(['player_name', 'team'])['usage_rate'].mean().reset_index()
    player_usage['usage_rate'] = player_usage['usage_rate'].round(1)
    return player_usage

# Regular Season
rs = df[df['game_type'].isin(['Regular Season', 'Regular Season (Forfeit)'])].copy()
rs_usage = compute_usage(rs, 'RS')

# RS + Semifinal
rs_semi = df[df['game_type'].isin(['Regular Season', 'Regular Season (Forfeit)', 'Playoff - Semifinal'])].copy()
rss_usage = compute_usage(rs_semi, 'RS+Semi')

# Update Excel
excel_path = r'C:\Users\Paa Yaw\Downloads\ABA\ABA_2025_26.xlsx'

# Read existing sheets
rs_players = pd.read_excel(excel_path, sheet_name='Player Advanced Stats')
rss_players = pd.read_excel(excel_path, sheet_name='Player Advanced Stats RS+Semi') if 'Player Advanced Stats RS+Semi' in pd.ExcelFile(excel_path).sheet_names else None

# Check what sheets exist
xf = pd.ExcelFile(excel_path)
print(f"Existing sheets: {xf.sheet_names}")

# Add usage_rate to RS player stats
if 'usage_rate' in rs_players.columns:
    rs_players = rs_players.drop(columns=['usage_rate'])
rs_players = rs_players.merge(rs_usage, on=['player_name', 'team'], how='left')
rs_players['usage_rate'] = rs_players['usage_rate'].fillna(0)

print(f"\nRS Player Stats - top 15 by usage rate:")
print(rs_players.nlargest(15, 'usage_rate')[['player_name', 'team', 'ppg', 'usage_rate']].to_string(index=False))

# Write back
with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    rs_players.to_excel(writer, sheet_name='Player Advanced Stats', index=False)

# Now handle RS+Semi sheet
for sheet_name in xf.sheet_names:
    if 'semi' in sheet_name.lower() and 'player' in sheet_name.lower():
        rss_players = pd.read_excel(excel_path, sheet_name=sheet_name)
        if 'usage_rate' in rss_players.columns:
            rss_players = rss_players.drop(columns=['usage_rate'])
        rss_players = rss_players.merge(rss_usage, on=['player_name', 'team'], how='left')
        rss_players['usage_rate'] = rss_players['usage_rate'].fillna(0)
        print(f"\n{sheet_name} - top 15 by usage rate:")
        print(rss_players.nlargest(15, 'usage_rate')[['player_name', 'team', 'ppg', 'usage_rate']].to_string(index=False))
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            rss_players.to_excel(writer, sheet_name=sheet_name, index=False)
        break

print("\nDone! Usage rate added.")
