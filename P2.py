from pyomo.environ import *

model = ConcreteModel()


model.C = RangeSet(1, 5)
model.T = RangeSet(1,3)


h_values = {1: 8, 
             2:10, 
             3:6}  
g_values = {1: 50, 
             2:60, 
             3:40, 
             4:70,
             5:30} 
t_values = {1: 4, 
             2:5, 
             3:3, 
             4:6,
             5:2} 

model.h = Param(model.T, initialize=h_values)
model.g = Param(model.C, initialize=g_values)
model.t = Param(model.C, initialize=t_values)

model.X = Var(model.C, model.T, within=Binary)


model.obj = Objective(expr=sum(model.g[i] * model.X[i,j] for i in model.C for j in model.T), sense=maximize)

model.workhours = ConstraintList()
for j in model.T:
    model.workhours.add(expr=sum(model.t[i] * model.X[i,j] for i in model.C) <= model.h[j])

model.amounttask = ConstraintList()
for i in model.C:
    model.amounttask.add(sum(model.X[i,j] for j in model.T ) <= 1)

from pyomo . opt import SolverFactory
solver = SolverFactory ("glpk")
solver.solve(model)


for i in model.C:
    for j in model.T:
        if model.X[i, j].value == 1:
            print(f"trabajo {i} asignada al trabajador {j}")