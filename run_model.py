"""Reproduce the eight tree-placement scenarios from processed coverage data."""
from pathlib import Path
import json,sys
import pandas as pd

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from model import solve_planting


def main():
    candidates=pd.read_csv(ROOT/'data/candidate_review.csv')
    identifiers=candidates.id.tolist()
    if len(identifiers)!=len(set(identifiers)):raise ValueError('Duplicate candidate IDs')
    index={name:j for j,name in enumerate(identifiers)}
    patterns=pd.read_csv(ROOT/'data/coverage_patterns.csv')
    pairs=pd.read_csv(ROOT/'data/spacing_conflicts.csv')
    conflicts=[(index[r.site_a],index[r.site_b]) for r in pairs.itertuples()]
    meta=json.loads((ROOT/'data/metadata.json').read_text())
    rows=[]
    for design,group in patterns.groupby('crown_scenario',sort=False):
        coverage=[set() for _ in identifiers];weights=[]
        for q,r in enumerate(group.itertuples()):
            if r.benefit_weight<0:raise ValueError('Negative benefit weight')
            weights.append(r.benefit_weight)
            for site in r.candidate_ids.split(';'):coverage[index[site]].add(q)
        for budget in [0,5,10,20]:
            result=solve_planting(coverage,weights,budget,conflicts)
            selected=result.pop('selected')
            rows.append(dict(crown_scenario=design,tree_budget=budget,trees_selected=len(selected),
                selected=','.join(identifiers[j] for j in selected),
                mean_sun_minutes_saved=result['benefit']/meta['reachable_population'],**result))
    table=pd.DataFrame(rows)
    (ROOT/'results').mkdir(exist_ok=True)
    table.to_csv(ROOT/'results/reproduced_summary.csv',index=False)
    expected=pd.read_csv(ROOT/'results/scenario_summary.csv')
    check=table.merge(expected,on=['crown_scenario','tree_budget'],suffixes=('_new','_saved'),validate='one_to_one')
    if len(check)!=8 or not ((check.benefit_new-check.benefit_saved).abs()<1e-5).all():
        raise AssertionError('Reproduced benefits do not match the saved results')
    print(table[['crown_scenario','tree_budget','trees_selected','benefit','mean_sun_minutes_saved','status']].to_string(index=False))
    print('\nAll eight benefit values match the saved results. Equivalent optimal site sets may differ.')
    return table


if __name__=='__main__':main()
