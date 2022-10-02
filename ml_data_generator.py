from fake_market import cities, suppliers, objects
import numpy as np
import random
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.preprocessing import StandardScaler

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


scaler_x=StandardScaler()


training_set= [(pareto_front[i][1::], 1) for i in range(16)]
training_set=training_set+[(dominated_front[i][1::], 0) for i in range(16)]
random.shuffle(training_set)
training_set_x, training_set_y = [x[0] for x in training_set], [y[1] for y in training_set]
training_set_x=scaler_x.fit_transform(training_set_x)

test_set= [(pareto_front[i][1::], 1) for i in range(16,21)]
test_set=test_set+[(dominated_front[i][1::], 0) for i in range(16,21)]
# random.shuffle(test_set)
test_set_x, test_set_y = [x[0] for x in test_set], [y[1] for y in test_set]
test_set_x=scaler_x.transform(test_set_x)

model=GaussianProcessClassifier().fit(training_set_x,training_set_y)
predictions=model.predict(test_set_x)
print(predictions,test_set_y)
correctness=[predictions[i]==test_set_y[i] for i in range(len(predictions))]
print(correctness,"\nAccuracy:",sum(correctness)*100/len(correctness),"%")
print()