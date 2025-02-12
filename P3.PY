from pyomo.environ import *

model = ConcreteModel()

model.R = RangeSet(1, 5)
model.A = RangeSet(1, 3)

valor_recurso = {1: 50, 2: 100, 3: 120, 4: 60, 5: 40}
peso_recurso = {1: 15, 2: 5, 3: 20, 4: 18, 5: 10}
volumen_recurso = {1: 8, 2: 2, 3: 10, 4: 12, 5: 6}
capacidad_peso = {1: 30, 2: 40, 3: 50}
capacidad_volumen = {1: 25, 2: 30, 3: 35}


model.valR = Param(model.R, initialize = valor_recurso)
model.pesR = Param(model.R, initialize = peso_recurso)
model.volR = Param(model.R, initialize = volumen_recurso)
model.pesA = Param(model.A, initialize = capacidad_peso)
model.volA = Param(model.A, initialize = capacidad_volumen)

model.X = Var(model.R, model.A, within = Binary)

model.obj = Objective(expr = sum(model.valR[i]*model.X[i, j] for i in model.R for j in model.A), sense = maximize)

model.restPeso = ConstraintList()
for j in model.A:
    model.restPeso.add(expr = sum(model.pesR[i] * model.X[i, j] for i in model.R) <= model.pesA[j])

model.restVol = ConstraintList()
for j in model.A:
    model.restVol.add(expr = sum(model.volR[i] * model.X[i, j] for i in model.R) <= model.volA[j])
    
model.restSeguridad = ConstraintList()
for i in model.R:
    for j in model.A:
        if j == 1 and i == 2:
            model.restSeguridad.add(expr = model.X[2, 1] == 0)

model.restComp = ConstraintList()
for j in model.A:
    model.restComp.add(expr = sum(model.X[i, j] for i in model.R if i == 3 or i == 4) <= 1)
    
from pyomo . opt import SolverFactory
solver = SolverFactory ("glpk")
solver.solve(model)

for i in model.R:
    for j in model.A:
        if model.X[i, j].value == 1:
            print(f"recurso {i} asignada al avión {j}")