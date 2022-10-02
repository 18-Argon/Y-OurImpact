from fake_market import cities, suppliers, objects
import numpy as np

front=[obj.F for obj in objects]
pareto_front=list(front)
dominated_front=[]

for F1 in pareto_front:
    for F2 in pareto_front:
        if (F1[1::]<=F2[1::]).all() and (F1[1::]<F2[1::]).any():
            pareto_front=[F for F in pareto_front if not (F[0]==F2[0])]
            dominated_front.append(F2)

print(front==pareto_front)
print(len(dominated_front)+len(pareto_front), len(front))
print()