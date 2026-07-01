import pandas as pd
import numpy as np

df = pd.read_csv('ashesi_basketball_2025_26_full.csv')
finals = df[df['game_type'] == 'Playoff - Finals']

if finals.empty:
    print("No finals games found!")
    exit()

games = sorted(finals['game_number'].unique())
print(f"Finals Games Found: {len(games)} (Games {games})")
print("=" * 80)

# Process each game
for gn in games:
    gdata = finals[finals['game_number'] == gn]
    teams = gdata['team'].unique()
    ts = gdata[['team','team_score','opponent_score']].drop_duplicates('team')
    print(f"\n{'='*80}")
    print(f"GAME {gn}")
    for _, row in ts.iterrows():
        result = "W" if row['team_score'] > row['opponent_score'] else "L"
        print(f"  {row['team']}: {row['team_score']} ({result})  vs  {row['opponent_score']}")
    print()

    # AshKnights stats
    ak = gdata[gdata['team'] == 'AshKnights']
    if not ak.empty:
        ak_score = ak['team_score'].iloc[0]
        ak_opp = ak['opponent_score'].iloc[0]
        ak_wm = ak_score - ak_opp

        # Benson pts
        bk = ak[ak['player_name'] == 'Benson Kas-Vorsah']
        bk_pts = bk['pts'].sum() if not bk.empty else 0

        # Sean stats
        sy = ak[ak['player_name'] == 'Sean Yeboah']
        sy_3pm = sy['three_pm'].sum() if not sy.empty else 0
        sy_fga = sy['fga'].sum() if not sy.empty else 0
        team_fga = ak['fga'].sum()
        sy_usage = (sy_fga / team_fga * 100) if team_fga > 0 else 0

        # Benson steals
        bk_stl = bk['stl'].sum() if not bk.empty else 0

        # Team FTM
        team_ftm = ak['ftm'].sum()

        # Predicted win margin from AshKnights model
        predicted_wm = (-16.450 + 1.050 * bk_pts + 7.560 * sy_3pm +
                        (-2.862) * bk_stl + (-0.557) * team_ftm +
                        (-0.365) * sy_usage)

        print(f"  ASHKNIGHTS MODEL CHECK:")
        print(f"    Benson pts:    {bk_pts:5.0f}  (coef +1.050)  -> contribution: {1.050*bk_pts:+.1f}")
        print(f"    Sean 3PM:      {sy_3pm:5.0f}  (coef +7.560)  -> contribution: {7.560*sy_3pm:+.1f}")
        print(f"    Benson steals: {bk_stl:5.0f}  (coef -2.862)  -> contribution: {-2.862*bk_stl:+.1f}")
        print(f"    Team FTM:      {team_ftm:5.0f}  (coef -0.557)  -> contribution: {-0.557*team_ftm:+.1f}")
        print(f"    Sean usage%:   {sy_usage:5.1f}  (coef -0.365)  -> contribution: {-0.365*sy_usage:+.1f}")
        print(f"    Predicted margin: {predicted_wm:+.1f}  |  Actual margin: {ak_wm:+.0f}  |  Error: {abs(predicted_wm - ak_wm):.1f}")
        print()

    # Longshots stats
    ls = gdata[gdata['team'] == 'Longshots']
    if not ls.empty:
        ls_score = ls['team_score'].iloc[0]
        ls_opp = ls['opponent_score'].iloc[0]
        ls_wm = ls_score - ls_opp

        # Boss Baeta eFG%
        bb = ls[ls['player_name'] == 'Boss Baeta']
        bb_fgm = bb['fgm'].sum() if not bb.empty else 0
        bb_fga = bb['fga'].sum() if not bb.empty else 0
        bb_3pm = bb['three_pm'].sum() if not bb.empty else 0
        bb_efg = ((bb_fgm + 0.5 * bb_3pm) / bb_fga * 100) if bb_fga > 0 else 0

        # Desmond pts
        dr = ls[ls['player_name'] == 'Desmond Raimmy']
        dr_pts = dr['pts'].sum() if not dr.empty else 0

        # Richard rebounds
        ri = ls[ls['player_name'] == 'Richard']
        ri_reb = ri['reb'].sum() if not ri.empty else 0

        # Bright Edudzi rebounds
        be = ls[ls['player_name'] == 'Bright Edudzi']
        be_reb = be['reb'].sum() if not be.empty else 0

        # Team 3P%
        team_3pm = ls['three_pm'].sum()
        team_3pa = ls['three_pa'].sum()
        three_pct = (team_3pm / team_3pa * 100) if team_3pa > 0 else 0

        # Team steals (supporting)
        team_stl = ls['stl'].sum()

        # Bright assists (supporting)
        be_ast = be['ast'].sum() if not be.empty else 0

        # Predicted win margin from Longshots model
        predicted_wm_ls = (-30.887 + 0.604 * bb_efg + 0.968 * ri_reb +
                           0.508 * dr_pts + 0.322 * three_pct + 2.261 * be_reb)

        print(f"  LONGSHOTS MODEL CHECK:")
        print(f"    Boss eFG%:     {bb_efg:5.1f}  (coef +0.604)  -> contribution: {0.604*bb_efg:+.1f}")
        print(f"    Richard reb:   {ri_reb:5.0f}  (coef +0.968)  -> contribution: {0.968*ri_reb:+.1f}")
        print(f"    Desmond pts:   {dr_pts:5.0f}  (coef +0.508)  -> contribution: {0.508*dr_pts:+.1f}")
        print(f"    Team 3P%:      {three_pct:5.1f}  (coef +0.322)  -> contribution: {0.322*three_pct:+.1f}")
        print(f"    Bright reb:    {be_reb:5.0f}  (coef +2.261)  -> contribution: {2.261*be_reb:+.1f}")
        print(f"    --- Supporting factors ---")
        print(f"    Team steals:   {team_stl:5.0f}  (target: 14.8+ in wins)")
        print(f"    Bright assists:{be_ast:5.0f}  (target: 4.5+ in wins)")
        print(f"    Predicted margin: {predicted_wm_ls:+.1f}  |  Actual margin: {ls_wm:+.0f}  |  Error: {abs(predicted_wm_ls - ls_wm):.1f}")
        print()

    # Scoring targets
    print(f"  SCORING TARGET CHECK:")
    ak_sc = ak['team_score'].iloc[0] if not ak.empty else 0
    ls_sc = ls['team_score'].iloc[0] if not ls.empty else 0
    held_under_55 = "YES" if ak_sc < 55 else "NO"
    scored_55_plus = "YES" if ls_sc >= 55 else "NO"
    print(f"    AshKnights scored: {ak_sc}  |  Held under 55? {held_under_55}")
    print(f"    Longshots scored:  {ls_sc}  |  Scored 55+?    {scored_55_plus}")
    winner = "Longshots" if ls_sc > ak_sc else "AshKnights" if ak_sc > ls_sc else "TIE"
    print(f"    Winner: {winner}")

# Series summary
print("\n" + "=" * 80)
print("SERIES SUMMARY")
print("=" * 80)

ls_wins = 0
ak_wins = 0
for gn in games:
    gdata = finals[finals['game_number'] == gn]
    ls = gdata[gdata['team'] == 'Longshots']
    if not ls.empty:
        if ls['team_score'].iloc[0] > ls['opponent_score'].iloc[0]:
            ls_wins += 1
        else:
            ak_wins += 1

print(f"  Longshots {ls_wins} - {ak_wins} AshKnights")
if ls_wins > ak_wins:
    print(f"  LONGSHOTS WIN THE CHAMPIONSHIP!")
elif ak_wins > ls_wins:
    print(f"  ASHKNIGHTS WIN THE CHAMPIONSHIP!")
else:
    print(f"  Series tied!")

# Aggregate analysis
print("\n" + "=" * 80)
print("AGGREGATE: DID THE SCOUTING FINDINGS HOLD?")
print("=" * 80)

# AshKnights aggregates
ak_finals = finals[finals['team'] == 'AshKnights']
ls_finals = finals[finals['team'] == 'Longshots']

print("\n  ASHKNIGHTS SCOUTING REPORT VALIDATION:")
for gn in games:
    gdata = finals[finals['game_number'] == gn]
    ak = gdata[gdata['team'] == 'AshKnights']
    bk = ak[ak['player_name'] == 'Benson Kas-Vorsah']
    sy = ak[ak['player_name'] == 'Sean Yeboah']
    bk_pts = bk['pts'].sum() if not bk.empty else 0
    ak_result = "W" if ak['team_score'].iloc[0] > ak['opponent_score'].iloc[0] else "L"
    print(f"    Game {gn}: Benson {bk_pts} pts, Sean {sy['three_pm'].sum() if not sy.empty else 0} 3PM -> AK {ak_result}")

print(f"\n  Finding: 'Benson scores 13+ = AK wins, 8 or less = AK loses'")
print(f"  Finding: 'Sean 3PM is strongest predictor of AK win margin'")
print(f"  Finding: 'High Sean usage predicts AK losses'")
print(f"  Finding: 'AK FT shooting is terrible (44.6%) - exploit it'")
print(f"  Finding: 'Hold AK under 55, score 55+ to win'")

ak_ft = ak_finals.groupby('game_number').agg(ftm=('ftm','sum'), fta=('fta','sum')).reset_index()
ak_ft['ft_pct'] = np.where(ak_ft['fta'] > 0, ak_ft['ftm'] / ak_ft['fta'] * 100, 0)
print(f"\n  AK FT% in finals: {ak_ft['ft_pct'].mean():.1f}%  (RS+Semi avg: 44.6%)")

print("\n  LONGSHOTS SELF-SCOUT VALIDATION:")
for gn in games:
    gdata = finals[finals['game_number'] == gn]
    ls = gdata[gdata['team'] == 'Longshots']
    if ls.empty:
        continue
    bb = ls[ls['player_name'] == 'Boss Baeta']
    dr = ls[ls['player_name'] == 'Desmond Raimmy']
    ri = ls[ls['player_name'] == 'Richard']
    be = ls[ls['player_name'] == 'Bright Edudzi']
    bb_fgm = bb['fgm'].sum() if not bb.empty else 0
    bb_fga = bb['fga'].sum() if not bb.empty else 0
    bb_3pm = bb['three_pm'].sum() if not bb.empty else 0
    bb_efg = ((bb_fgm + 0.5 * bb_3pm) / bb_fga * 100) if bb_fga > 0 else 0
    dr_pts = dr['pts'].sum() if not dr.empty else 0
    ri_reb = ri['reb'].sum() if not ri.empty else 0
    be_reb = be['reb'].sum() if not be.empty else 0
    ls_result = "W" if ls['team_score'].iloc[0] > ls['opponent_score'].iloc[0] else "L"
    print(f"    Game {gn}: Boss eFG {bb_efg:.1f}%, Desmond {dr_pts} pts, Richard {ri_reb} reb, Bright {be_reb} reb -> LS {ls_result}")

print(f"\n  Finding: 'Boss efficiency is everything - eFG% is #1 predictor'")
print(f"  Finding: 'Richard rebounding transforms the team (+0.97/reb)'")
print(f"  Finding: 'Desmond scoring is second engine (+0.51/pt)'")
print(f"  Finding: 'Bright rebounding is hidden weapon (+2.26/reb)'")
print(f"  Finding: 'Team steals fuel transition (14.8 in wins vs 10.0 in losses)'")
