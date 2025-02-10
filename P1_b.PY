from pyomo.environ import *

model = ConcreteModel()


model.C = RangeSet(1, 11)
model.T = RangeSet(1,4)


Ph_values = {1: 5, 
             2:3, 
             3:13, 
             4:1,
             5:21,
             6:2,
             7:2,
             8:5,
             9:8,
             10:13,
             11:21}  
Pr_values = {1: 7, 
             2:5, 
             3:4, 
             4:3,
             5:1,
             6:4,
             7:6,
             8:6,
             9:2,
             10:7,
             11:6} 

model.Ph = Param(model.C, initialize=Ph_values)
model.Pr = Param(model.C, initialize=Pr_values)

model.X = Var(model.C, model.T, within=Binary)


model.obj = Objective(expr=sum(model.Pr[i] * model.X[i,j] for i in model.C for j in model.T), sense=maximize)

model.history_constraint = Constraint(expr=sum(model.Ph[i] * model.X[i,j] for i in model.C for j in model.T) <= 52)

model.developers = ConstraintList()
for j in model.T:
    model.developers.add(expr=sum(model.Ph[i] * model.X[i,j] for i in model.C) <= 13 )

model.amounttask = ConstraintList()
for i in model.C:
    model.amounttask.add(sum(model.X[i,j] for j in model.T ) <= 1)


from pyomo . opt import SolverFactory
solver = SolverFactory ("glpk")
solver.solve(model)


for i in model.C:
    for j in model.T:
        if model.X[i, j].value == 1:
            print(f"Tarea {i} asignada al desarrollador {j}")

