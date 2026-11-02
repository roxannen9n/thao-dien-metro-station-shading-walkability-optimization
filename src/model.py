"""Select tree sites using a budgeted maximum-coverage MILP."""
import pyomo.environ as pyo


def solve_planting(coverage, weights, count_budget, conflicts=(), time_limit=120):
    """Aggregate identical coverage patterns before solving binary site selection."""
    n=len(coverage)
    by_sample={}
    for j,samples in enumerate(coverage):
        for q in samples:by_sample.setdefault(int(q),[]).append(j)
    patterns={}
    for q,sites in by_sample.items():
        if weights[q]>0:
            key=tuple(sites);patterns[key]=patterns.get(key,0.)+float(weights[q])
    keys=list(patterns)
    model=pyo.ConcreteModel();model.J=pyo.Set(initialize=range(n));model.Q=pyo.Set(initialize=range(len(keys)))
    model.x=pyo.Var(model.J,domain=pyo.Binary)
    model.y=pyo.Var(model.Q,bounds=(0,1))
    model.budget=pyo.Constraint(expr=sum(model.x[j] for j in model.J)<=count_budget) if n else pyo.Constraint(expr=pyo.Constraint.Feasible)
    model.cover=pyo.Constraint(model.Q,rule=lambda m,q:m.y[q]<=sum(m.x[j] for j in keys[q]))
    model.spacing=pyo.ConstraintList()
    for a,b in conflicts:model.spacing.add(model.x[a]+model.x[b]<=1)
    model.obj=pyo.Objective(expr=sum(patterns[keys[q]]*model.y[q] for q in model.Q),sense=pyo.maximize)
    if not patterns:return dict(selected=[],benefit=0.,status='optimal_empty',gap=0.,patterns=0)
    solver=pyo.SolverFactory('appsi_highs');solver.options['time_limit']=time_limit
    result=solver.solve(model)
    status=str(result.solver.termination_condition)
    # Cardinality tie-break only after primary proven optimal.
    if status=='optimal':
        optimum=pyo.value(model.obj)
        model.floor=pyo.Constraint(expr=model.obj.expr>=optimum-1e-7)
        model.obj.deactivate();model.tie=pyo.Objective(expr=sum(model.x[j] for j in model.J))
        tie=solver.solve(model)
        tie_status=str(tie.solver.termination_condition)
    else:tie_status='not_requested'
    selected=[j for j in model.J if pyo.value(model.x[j],exception=False) is not None and pyo.value(model.x[j])>.5]
    union=set().union(*(coverage[j] for j in selected)) if selected else set()
    benefit=float(sum(weights[q] for q in union))
    assert len(selected)<=count_budget
    assert all(not(a in selected and b in selected) for a,b in conflicts)
    return dict(selected=selected,benefit=benefit,status=status,tie_status=tie_status,patterns=len(patterns))
