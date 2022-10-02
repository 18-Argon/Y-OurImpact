from fake_market import cities, suppliers, objects
import numpy as np
import random

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

training_set= [(pareto_front[i], 1) for i in range(16)]
training_set=training_set+[(dominated_front[i], 0) for i in range(16)]
random.shuffle(training_set)
training_set_x, training_set_y = [x[0] for x in training_set], [y[1] for y in training_set]

test_set= [(pareto_front[i], 1) for i in range(16,21)]
test_set=test_set+[(dominated_front[i], 0) for i in range(16,21)]
random.shuffle(test_set)
test_set_x, test_set_y = [x[0] for x in test_set], [y[1] for y in test_set]
print()