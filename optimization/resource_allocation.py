from pulp import LpMaximize, LpProblem, LpVariable

def optimize_allocation(forecast):
    model = LpProblem("Retail_Resource_Allocation", LpMaximize)

    # Variables: allocation per product
    resources = {p: LpVariable(p, lowBound=0) for p in forecast}

    # Objective: Maximize weighted allocation
    model += sum(forecast[p] * resources[p] for p in forecast)

    # Constraint: total resources ≤ 100
    model += sum(resources.values()) <= 100

    model.solve()
    return {p: resources[p].value() for p in forecast}
