from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

model.Set = Set(initialize=[0, 1])

# Parameters
model.fill_time = Param(model.Set, initialize={0: 6/3600, 1: 12/3600}, name="Filling time of both bars")

model.selling_prices = Param(model.Set, initialize={0: 0.8, 1: 1.5}, name="Contribution margin of both bars")


model.max_filling_time = Param(initialize=8*3600, name="Availability of filling machine")

model.coating_time = Param(model.Set, initialize={0: 2/3600, 1: 4/3600}, name="Coating time of both bars")

model.max_coating_time = Param(initialize=6*3600,name="Avaiability of coating machine")


model.max_sell_amount = Param(model.Set, initialize={0: 10_000_000, 1: 50_000_000}, name="Maximum sales number of both bars")

# Variables
model.unit_production = Var(model.Set, within=NonNegativeReals, name="Number of each bar to produce")


# Constraints
def sell_constraint1(model):
    return model.max_sell_amount[0] >= model.unit_production[0]
model.constraint_1 = Constraint(rule=sell_constraint1)

def sell_constraint2(model):
    return model.max_sell_amount[1] >= model.unit_production[1]
model.constraint_2 = Constraint(rule=sell_constraint2)

def fill_constraint(model):
    return model.max_filling_time >= model.fill_time[0] * model.unit_production[0] + \
           model.fill_time[1] * model.unit_production[1]
model.constraint_3 = Constraint(rule=fill_constraint)

def coating_constraint(model):
    return model.max_coating_time >= model.coating_time[0] * model.unit_production[0] + \
            model.coating_time[1] * model.unit_production[1]
model.constraing_4 = Constraint(rule=coating_constraint)

def objective_function(model):
    return model.unit_production[0] * model.selling_prices[0] +\
           model.unit_production[1] * model.selling_prices[1]

model.Zielfunktion = Objective(rule=objective_function, sense=maximize)

results = SolverFactory("glpk").solve(model)
results.write()

