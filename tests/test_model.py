from pathlib import Path
import sys,itertools,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import solve_planting


def test_budget_overlap_and_spacing():
    coverage=[{0,1},{1,2},{3},{0,3}];weights=[3.,5.,6.,4.];conflicts=[(0,3)]
    for budget in [0,1,2,3]:
        feasible=[s for r in range(budget+1) for s in itertools.combinations(range(4),r) if not(0 in s and 3 in s)]
        def benefit(s):return sum(weights[q] for q in set().union(*(coverage[j] for j in s))) if s else 0
        optimum=max(benefit(s) for s in feasible)
        result=solve_planting(coverage,weights,budget,conflicts)
        assert abs(result['benefit']-optimum)<1e-7
        assert len(result['selected'])==min(len(s) for s in feasible if benefit(s)==optimum)


def test_empty_instance():
    assert solve_planting([],[],10)['selected']==[]


def test_processed_data_integrity():
    root=Path(__file__).resolve().parents[1]
    for item in json.loads((root/'data/manifest.json').read_text()):
        assert hashlib.sha256((root/item['file']).read_bytes()).hexdigest()==item['sha256']
