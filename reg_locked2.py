import pandas as pd, numpy as np, statsmodels.api as sm
from itertools import combinations

df = pd.read_csv('ashesi_basketball_2025_26_full.csv')
rs = df[df['game_type'].isin(['Regular Season','Regular Season (Forfeit)','Playoff - Semifinal'])]
ak = rs[rs['team']=='AshKnights']

g = ak.groupby('game_number').agg(ts=('team_score','first'),os_=('opponent_score','first'),
    fgm=('fgm','sum'),fga=('fga','sum'),tpm=('three_pm','sum'),tpa=('three_pa','sum'),
    ftm=('ftm','sum'),fta=('fta','sum'),reb=('reb','sum'),ast=('ast','sum'),
    stl=('stl','sum'),blk=('blk','sum'),fouls=('fouls','sum')).reset_index()
g['wm']=g['ts']-g['os_']
g['efg']=(g['fgm']+0.5*g['tpm'])/g['fga']*100
g['fgp']=g['fgm']/g['fga']*100
g['ftr']=g['fta']/g['fga']*100
g['ftp']=np.where(g['fta']>0,g['ftm']/g['fta']*100,0)
g['pct_ft_pts']=g['ftm']/g['ts']*100

opp=rs[rs['opponent']=='AshKnights']
og=opp.groupby('game_number').agg(ofgm=('fgm','sum'),ofga=('fga','sum'),
    o3pm=('three_pm','sum'),oreb=('reb','sum'),oast=('ast','sum'),
    ostl=('stl','sum'),ofta=('fta','sum'),ofouls=('fouls','sum')).reset_index()
og['ofgp']=og['ofgm']/og['ofga']*100
og['oefg']=(og['ofgm']+0.5*og['o3pm'])/og['ofga']*100
og['oftr']=og['ofta']/og['ofga']*100
g=g.merge(og,on='game_number',how='left')
g['efgd']=g['efg']-g['oefg']
g['astd']=g['ast']-g['oast']

for pn,pre,cols in [('Sean Yeboah','sy',['pts','blk','three_pm','fta','fgm','fga','ast']),
    ('Benson Kas-Vorsah','bk',['pts','fgm','fga','three_pm','three_pa','stl']),
    ('Charles Janney','cj',['pts','reb','ast','blk','fgm','fga']),
    ('Trueman Mabumbo','tm',['pts','ast','fgm','fga','three_pm']),
    ('Alex Yeboah','ay',['pts','fgm','reb'])]:
    pd2=ak[ak['player_name']==pn][['game_number']+cols].rename(columns={c:f"{pre}_{c}" for c in cols})
    g=g.merge(pd2,on='game_number',how='left').fillna(0)

g['sy_fgp']=np.where(g['sy_fga']>0,g['sy_fgm']/g['sy_fga']*100,0)
g['sy_efg']=np.where(g['sy_fga']>0,(g['sy_fgm']+0.5*g['sy_three_pm'])/g['sy_fga']*100,0)
g['sy_usage']=np.where(g['fga']>0,g['sy_fga']/g['fga']*100,0)
g['bk_fgp']=np.where(g['bk_fga']>0,g['bk_fgm']/g['bk_fga']*100,0)
g['bk_efg']=np.where(g['bk_fga']>0,(g['bk_fgm']+0.5*g['bk_three_pm'])/g['bk_fga']*100,0)
g['bk_3p']=np.where(g['bk_three_pa']>0,g['bk_three_pm']/g['bk_three_pa']*100,0)
g['cj_fgp']=np.where(g['cj_fga']>0,g['cj_fgm']/g['cj_fga']*100,0)
g['tm_fgp']=np.where(g['tm_fga']>0,g['tm_fgm']/g['tm_fga']*100,0)

bn=ak[ak['pts']>0].groupby('game_number')['player_name'].nunique().reset_index()
bn.columns=['game_number','n_scorers']
g=g.merge(bn,on='game_number',how='left')

y=g['wm']

# Pre-screen: univariate p < 0.20
pool=[]
skip_cols=['game_number','wm','ts','os_','bk_pts']
for c in g.columns:
    if c in skip_cols: continue
    if g[c].dtype not in ['float64','int64','float32','int32']: continue
    if g[c].std()==0: continue
    X=sm.add_constant(g[[c]])
    try:
        m=sm.OLS(y,X).fit()
        if m.pvalues[c]<0.20: pool.append(c)
    except: pass

pool=[f for f in pool if abs(g['bk_pts'].corr(g[f]))<0.85]
print(f"Feature pool ({len(pool)}): {pool}")

locked=['bk_pts']

# 3-feature
print("\n"+"="*70)
print("3-FEATURE: bk_pts + 2 (all 3 sig at p<0.05)")
print("="*70)
r3=[]
for combo in combinations(pool,2):
    if abs(g[combo[0]].corr(g[combo[1]]))>0.85: continue
    feats=locked+list(combo)
    X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
    ns=sum(1 for v in feats if m.pvalues[v]<0.05)
    if ns>=3: r3.append((feats,m,ns,m.rsquared_adj))
r3.sort(key=lambda x:(-x[2],-x[3]))
print(f"Found {len(r3)}\n")
for feats,m,ns,ar in r3[:8]:
    print(f"  {' + '.join(feats)}")
    print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f}")
    for v in feats:
        s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
        print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
    print()

# 4-feature
print("="*70)
print("4-FEATURE: bk_pts + 3 (all 4 sig at p<0.05)")
print("="*70)
r4=[]
for combo in combinations(pool,3):
    bad=False
    for i,j in combinations(range(3),2):
        if abs(g[combo[i]].corr(g[combo[j]]))>0.85: bad=True; break
    if bad: continue
    feats=locked+list(combo)
    X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
    ns=sum(1 for v in feats if m.pvalues[v]<0.05)
    if ns>=4: r4.append((feats,m,ns,m.rsquared_adj))
r4.sort(key=lambda x:(-x[2],-x[3]))
print(f"Found {len(r4)}\n")
for feats,m,ns,ar in r4[:8]:
    print(f"  {' + '.join(feats)}")
    print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f}")
    for v in feats:
        s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
        print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
    print()

# 5-feature
print("="*70)
print("5-FEATURE: bk_pts + 4 (all 5 sig at p<0.05)")
print("="*70)
r5=[]
for combo in combinations(pool,4):
    bad=False
    for i,j in combinations(range(4),2):
        if abs(g[combo[i]].corr(g[combo[j]]))>0.85: bad=True; break
    if bad: continue
    feats=locked+list(combo)
    X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
    ns=sum(1 for v in feats if m.pvalues[v]<0.05)
    if ns>=5: r5.append((feats,m,ns,m.rsquared_adj))
r5.sort(key=lambda x:(-x[2],-x[3]))
print(f"Found {len(r5)}\n")
for feats,m,ns,ar in r5[:8]:
    print(f"  {' + '.join(feats)}")
    print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f}")
    for v in feats:
        s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
        print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
    print()

# If no 5-all-sig, relax 5th to p<0.10
if not r5:
    print("="*70)
    print("5-FEATURE: bk_pts + 4 (4 at p<0.05, 5th at p<0.10)")
    print("="*70)
    r5b=[]
    for combo in combinations(pool,4):
        bad=False
        for i,j in combinations(range(4),2):
            if abs(g[combo[i]].corr(g[combo[j]]))>0.85: bad=True; break
        if bad: continue
        feats=locked+list(combo)
        X=sm.add_constant(g[feats]); m=sm.OLS(y,X).fit()
        n5=sum(1 for v in feats if m.pvalues[v]<0.05)
        n10=sum(1 for v in feats if m.pvalues[v]<0.10)
        if n5>=4 and n10>=5: r5b.append((feats,m,n5,n10,m.rsquared_adj))
    r5b.sort(key=lambda x:(-x[3],-x[4]))
    print(f"Found {len(r5b)}\n")
    for feats,m,n5,n10,ar in r5b[:8]:
        print(f"  {' + '.join(feats)}")
        print(f"    R2={m.rsquared:.3f} AdjR2={ar:.3f} Fp={m.f_pvalue:.4f} @05={n5} @10={n10}")
        for v in feats:
            s="**" if m.pvalues[v]<0.05 else "*" if m.pvalues[v]<0.10 else ""
            print(f"      {v:<20s}: {m.params[v]:+8.3f} p={m.pvalues[v]:.4f} {s}")
        print()

# Print best overall
best_pool = r5 if r5 else (r5b if not r5 and 'r5b' in dir() and r5b else r4)
if best_pool:
    bm = best_pool[0]
    print("="*70)
    print("BEST MODEL FULL OUTPUT")
    print("="*70)
    print(bm[1].summary())
