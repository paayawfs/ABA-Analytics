import pandas as pd, numpy as np, statsmodels.api as sm
from itertools import combinations

df = pd.read_csv('ashesi_basketball_2025_26_full.csv')
rs = df[df['game_type'].isin(['Regular Season','Regular Season (Forfeit)','Playoff - Semifinal'])]
ls = rs[rs['team']=='Longshots']

print("="*70)
print("LONGSHOTS OVERVIEW")
print("="*70)

# Game-level
g = ls.groupby('game_number').agg(
    date=('game_date','first'), opp=('opponent','first'),
    outcome=('game_outcome','first'),
    ts=('team_score','first'), os_=('opponent_score','first'),
    fgm=('fgm','sum'), fga=('fga','sum'),
    tpm=('three_pm','sum'), tpa=('three_pa','sum'),
    ftm=('ftm','sum'), fta=('fta','sum'),
    reb=('reb','sum'), ast=('ast','sum'),
    stl=('stl','sum'), blk=('blk','sum'),
    tov=('tov','sum'), fouls=('fouls','sum')
).reset_index()
g['wm'] = g['ts'] - g['os_']
g['win'] = (g['outcome']=='Won').astype(int)

print("\nGame-by-game:")
print(g[['game_number','date','opp','ts','os_','outcome','wm']].to_string(index=False))
print(f"\nRecord: {g['win'].sum()}-{(1-g['win']).sum():.0f}")
print(f"PPG: {g['ts'].mean():.1f}, Opp PPG: {g['os_'].mean():.1f}, Diff: {(g['ts']-g['os_']).mean():.1f}")

# Player averages
print("\n\n"+"="*70)
print("PLAYER STATS")
print("="*70)
pa = ls.groupby(['player_name','position']).agg(
    gp=('game_number','nunique'),
    pts=('pts','sum'), reb=('reb','sum'), ast=('ast','sum'),
    stl=('stl','sum'), blk=('blk','sum'), fouls=('fouls','sum'),
    fgm=('fgm','sum'), fga=('fga','sum'),
    tpm=('three_pm','sum'), tpa=('three_pa','sum'),
    ftm=('ftm','sum'), fta=('fta','sum')
).reset_index()
pa['ppg']=(pa['pts']/pa['gp']).round(1)
pa['rpg']=(pa['reb']/pa['gp']).round(1)
pa['apg']=(pa['ast']/pa['gp']).round(1)
pa['spg']=(pa['stl']/pa['gp']).round(1)
pa['bpg']=(pa['blk']/pa['gp']).round(1)
pa['efg']=((pa['fgm']+0.5*pa['tpm'])/pa['fga']*100).round(1)
pa['ts_pct']=(pa['pts']/(2*(pa['fga']+0.44*pa['fta']))*100).round(1)
pa = pa.sort_values('ppg', ascending=False)
print(pa[['player_name','position','gp','ppg','rpg','apg','spg','bpg','efg','ts_pct']].to_string(index=False))

# Wins vs Losses
print("\n\n"+"="*70)
print("WINS vs LOSSES")
print("="*70)
for label, sub in [('Wins', g[g['win']==1]), ('Losses', g[g['win']==0])]:
    print(f"\n{label} ({len(sub)} games):")
    print(f"  PPG: {sub['ts'].mean():.1f}, Opp PPG: {sub['os_'].mean():.1f}")
    print(f"  FGM/FGA: {sub['fgm'].mean():.1f}/{sub['fga'].mean():.1f} ({sub['fgm'].sum()/sub['fga'].sum()*100:.1f}%)")
    print(f"  3PM/3PA: {sub['tpm'].mean():.1f}/{sub['tpa'].mean():.1f}")
    print(f"  FTM/FTA: {sub['ftm'].mean():.1f}/{sub['fta'].mean():.1f}")
    print(f"  REB: {sub['reb'].mean():.1f}, AST: {sub['ast'].mean():.1f}")
    print(f"  STL: {sub['stl'].mean():.1f}, BLK: {sub['blk'].mean():.1f}")
    print(f"  Fouls: {sub['fouls'].mean():.1f}")

# Vs each opponent
print("\n\n"+"="*70)
print("VS EACH OPPONENT")
print("="*70)
for opp in g['opp'].unique():
    sub = g[g['opp']==opp]
    w = sub['win'].sum()
    l = len(sub) - w
    print(f"  vs {opp:<20s}: {w}-{l}  PPG={sub['ts'].mean():.1f}  OppPPG={sub['os_'].mean():.1f}  Diff={sub['wm'].mean():+.1f}")

# Home/Away
print("\n\n"+"="*70)
print("HOME vs AWAY")
print("="*70)
home = rs[(rs['team']=='Longshots')].groupby('game_number').first().reset_index()
for label, mask in [('Home', home['home_team']=='Longshots'), ('Away', home['home_team']!='Longshots')]:
    sub = home[mask]
    gn = sub['game_number'].tolist()
    gsub = g[g['game_number'].isin(gn)]
    w = gsub['win'].sum()
    print(f"  {label}: {w}-{len(gsub)-w}  PPG={gsub['ts'].mean():.1f}  OppPPG={gsub['os_'].mean():.1f}")

# Player dependency
print("\n\n"+"="*70)
print("SCORING DEPENDENCY")
print("="*70)
total_pts = pa['pts'].sum()
for _, r in pa.iterrows():
    pct = r['pts']/total_pts*100
    if pct > 3:
        print(f"  {r['player_name']:<25s}: {pct:.1f}% of team points")

# =============================================
# REGRESSION: FEATURE ENGINEERING
# =============================================
print("\n\n"+"="*70)
print("BUILDING REGRESSION FEATURES")
print("="*70)

g['efg'] = (g['fgm']+0.5*g['tpm'])/g['fga']*100
g['fgp'] = g['fgm']/g['fga']*100
g['ftr'] = g['fta']/g['fga']*100
g['ftp'] = np.where(g['fta']>0, g['ftm']/g['fta']*100, 0)
g['three_rate'] = g['tpa']/g['fga']*100
g['three_pct'] = np.where(g['tpa']>0, g['tpm']/g['tpa']*100, 0)
g['pct_ft_pts'] = g['ftm']/g['ts']*100

# Opponent
opp = rs[rs['opponent']=='Longshots']
og = opp.groupby('game_number').agg(
    ofgm=('fgm','sum'), ofga=('fga','sum'),
    o3pm=('three_pm','sum'), o3pa=('three_pa','sum'),
    oreb=('reb','sum'), oast=('ast','sum'),
    ostl=('stl','sum'), ofta=('fta','sum'),
    oftm=('ftm','sum'), ofouls=('fouls','sum')
).reset_index()
og['ofgp'] = og['ofgm']/og['ofga']*100
og['oefg'] = (og['ofgm']+0.5*og['o3pm'])/og['ofga']*100
og['oftr'] = og['ofta']/og['ofga']*100
g = g.merge(og, on='game_number', how='left')
g['efgd'] = g['efg'] - g['oefg']
g['astd'] = g['ast'] - g['oast']
g['rebd'] = g['reb'] - g['oreb']
g['fgpd'] = g['fgp'] - g['ofgp']

# Player features
for pn, pre, cols in [
    ('Boss Baeta','bb',['pts','reb','ast','stl','fgm','fga','three_pm','three_pa','ftm','fta']),
    ('Desmond Raimmy','dr',['pts','reb','ast','stl','fgm','fga','three_pm','three_pa','ftm','fta']),
    ('Richard','ri',['pts','reb','ast','stl','fgm','fga','three_pm']),
    ('Bright Edudzi','be',['pts','reb','ast','stl','fgm','fga']),
    ('Arnold Agamah','aa',['pts','reb','stl','fgm','fga']),
    ('Joseph Ajak','ja',['pts','reb','fgm','fga']),
    ('Jamal Gbana','jg',['pts','reb','fgm','fga','three_pm']),
    ('Joshua Babu','jb',['pts','reb','blk','fgm']),
    ('Samuel Duke','sd',['pts','ast','stl']),
]:
    pd2 = ls[ls['player_name']==pn][['game_number']+cols].rename(columns={c:f"{pre}_{c}" for c in cols})
    g = g.merge(pd2, on='game_number', how='left').fillna(0)

# Derived
g['bb_fgp'] = np.where(g['bb_fga']>0, g['bb_fgm']/g['bb_fga']*100, 0)
g['bb_efg'] = np.where(g['bb_fga']>0, (g['bb_fgm']+0.5*g['bb_three_pm'])/g['bb_fga']*100, 0)
g['bb_3pct'] = np.where(g['bb_three_pa']>0, g['bb_three_pm']/g['bb_three_pa']*100, 0)
g['bb_usage'] = np.where(g['fga']>0, g['bb_fga']/g['fga']*100, 0)
g['dr_fgp'] = np.where(g['dr_fga']>0, g['dr_fgm']/g['dr_fga']*100, 0)
g['dr_efg'] = np.where(g['dr_fga']>0, (g['dr_fgm']+0.5*g['dr_three_pm'])/g['dr_fga']*100, 0)
g['dr_3pct'] = np.where(g['dr_three_pa']>0, g['dr_three_pm']/g['dr_three_pa']*100, 0)
g['dr_usage'] = np.where(g['fga']>0, g['dr_fga']/g['fga']*100, 0)
g['be_fgp'] = np.where(g['be_fga']>0, g['be_fgm']/g['be_fga']*100, 0)
g['ri_fgp'] = np.where(g['ri_fga']>0, g['ri_fgm']/g['ri_fga']*100, 0)
g['aa_fgp'] = np.where(g['aa_fga']>0, g['aa_fgm']/g['aa_fga']*100, 0)

bn = ls[ls['pts']>0].groupby('game_number')['player_name'].nunique().reset_index()
bn.columns = ['game_number','n_scorers']
g = g.merge(bn, on='game_number', how='left')

g['supporting_pts'] = g['ts'] - g['bb_pts'] - g['dr_pts']

y = g['wm']

# =============================================
# UNIVARIATE SCREEN
# =============================================
print("\n"+"="*70)
print("UNIVARIATE SCREEN: correlation with win_margin")
print("="*70)

skip_cols = ['game_number','wm','ts','os_','outcome','win','date','opp']
results = []
for c in g.columns:
    if c in skip_cols: continue
    if g[c].dtype not in ['float64','int64','float32','int32']: continue
    if g[c].std() == 0: continue
    X = sm.add_constant(g[[c]])
    try:
        m = sm.OLS(y,X).fit()
        results.append((c, m.params[c], m.pvalues[c], m.rsquared, y.corr(g[c])))
    except: pass

results.sort(key=lambda x: x[2])
print(f"\n{'Feature':<25s} {'Coef':>8s} {'p-val':>8s} {'R-sq':>6s} {'Corr':>6s}")
print("-"*55)
for name,coef,pval,rsq,corr in results[:35]:
    sig = "***" if pval<0.01 else "**" if pval<0.05 else "*" if pval<0.1 else ""
    print(f"  {name:<23s} {coef:+8.3f} {pval:8.4f} {rsq:6.3f} {corr:+6.3f} {sig}")

print(f"\nFeatures p<0.05: {sum(1 for _,_,p,_,_ in results if p<0.05)}")
print(f"Features p<0.10: {sum(1 for _,_,p,_,_ in results if p<0.10)}")

# =============================================
# COMBINATION SEARCH
# =============================================
pool = []
for c,_,p,_,_ in results:
    if p < 0.20: pool.append(c)

# Remove high correlations between pool features
pool_clean = []
for f in pool:
    too_corr = False
    for existing in pool_clean:
        if abs(g[f].corr(g[existing])) > 0.85:
            too_corr = True
            break
    if not too_corr:
        pool_clean.append(f)

print(f"\nFeature pool for combos ({len(pool_clean)}): {pool_clean}")

# 3-feature: all 3 sig
print("\n"+"="*70)
print("3-FEATURE MODELS (all 3 sig at p<0.05)")
print("="*70)
r3=[]
for combo in combinations(pool_clean, 2):
    if abs(g[combo[0]].corr(g[combo[1]]))>0.85: continue
    for locked in pool_clean:
        if locked in combo: continue
        feats = [locked]+list(combo)
        if len(set(feats))!=3: continue
        if tuple(sorted(feats)) in [tuple(sorted(f)) for f,_,_,_ in r3]: continue
        X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
        ns=sum(1 for v in feats if m.pvalues[v]<0.05)
        if ns>=3: r3.append((feats,m,ns,m.rsquared_adj))
# Deduplicate
seen=set()
r3_dedup=[]
for feats,m,ns,ar in r3:
    key=tuple(sorted(feats))
    if key not in seen:
        seen.add(key)
        r3_dedup.append((feats,m,ns,ar))
r3_dedup.sort(key=lambda x:(-x[2],-x[3]))
print(f"Found {len(r3_dedup)}\n")
for feats,m,ns,ar in r3_dedup[:10]:
    print(f"  {' + '.join(feats)}")
    print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f}")
    for v in feats:
        s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
        print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
    print()

# 4-feature
print("="*70)
print("4-FEATURE MODELS (all 4 sig at p<0.05)")
print("="*70)
r4=[]
for combo in combinations(pool_clean, 4):
    bad=False
    for i,j in combinations(range(4),2):
        if abs(g[combo[i]].corr(g[combo[j]]))>0.85: bad=True; break
    if bad: continue
    feats=list(combo)
    X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
    ns=sum(1 for v in feats if m.pvalues[v]<0.05)
    if ns>=4: r4.append((feats,m,ns,m.rsquared_adj))
r4.sort(key=lambda x:(-x[2],-x[3]))
print(f"Found {len(r4)}\n")
for feats,m,ns,ar in r4[:10]:
    print(f"  {' + '.join(feats)}")
    print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f}")
    for v in feats:
        s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
        print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
    print()

# 5-feature
print("="*70)
print("5-FEATURE MODELS (all 5 sig at p<0.05)")
print("="*70)
r5=[]
for combo in combinations(pool_clean, 5):
    bad=False
    for i,j in combinations(range(5),2):
        if abs(g[combo[i]].corr(g[combo[j]]))>0.85: bad=True; break
    if bad: continue
    feats=list(combo)
    X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
    ns=sum(1 for v in feats if m.pvalues[v]<0.05)
    if ns>=5: r5.append((feats,m,ns,m.rsquared_adj))
r5.sort(key=lambda x:(-x[2],-x[3]))
print(f"Found {len(r5)}\n")
for feats,m,ns,ar in r5[:10]:
    print(f"  {' + '.join(feats)}")
    print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f}")
    for v in feats:
        s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
        print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
    print()

# If no 5-all-sig, relax
if not r5:
    print("Relaxing to 4@p<0.05 + 1@p<0.10:")
    r5b=[]
    for combo in combinations(pool_clean, 5):
        bad=False
        for i,j in combinations(range(5),2):
            if abs(g[combo[i]].corr(g[combo[j]]))>0.85: bad=True; break
        if bad: continue
        feats=list(combo)
        X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
        n5=sum(1 for v in feats if m.pvalues[v]<0.05)
        n10=sum(1 for v in feats if m.pvalues[v]<0.10)
        if n5>=4 and n10>=5: r5b.append((feats,m,n5,n10,m.rsquared_adj))
    r5b.sort(key=lambda x:(-x[3],-x[4]))
    print(f"Found {len(r5b)}\n")
    for feats,m,n5,n10,ar in r5b[:10]:
        print(f"  {' + '.join(feats)}")
        print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f} @05={n5} @10={n10}")
        for v in feats:
            s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
            print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
        print()

# Best model output
best_pool = r5 if r5 else (r5b if 'r5b' in dir() and r5b else r4 if r4 else r3_dedup)
if best_pool:
    bm = best_pool[0]
    print("="*70)
    print("BEST MODEL FULL OUTPUT")
    print("="*70)
    print(bm[1].summary() if len(bm)==4 else bm[1].summary())
