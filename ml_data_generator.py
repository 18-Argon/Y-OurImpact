from fake_market import cities, suppliers, objects
import numpy as np

front=[obj.F for obj in objects]
pareto_front=list(front)

for F1 in pareto_front:
    for F2 in pareto_front:
        if (F1<=F2).all() and (F1<F2).any():
            pareto_front=[F for F in pareto_front if not (F==F2).all()]
    
print(front==pareto_front)
print()