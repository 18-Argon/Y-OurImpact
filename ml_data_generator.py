from fake_market import cities, suppliers, objects
import numpy as np
import random
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.preprocessing import StandardScaler
import sqlite3

front = [obj.F for obj in objects]
pareto_front = list(front)
dominated_front = []

for F1 in pareto_front:
    for F2 in pareto_front:
        if (F1[2::] <= F2[2::]).all() and (F1[2::] < F2[2::]).any():
            pareto_front = [F for F in pareto_front if not (F[0] == F2[0])]
            dominated_front.append(F2)

print(front == pareto_front)
print(len(dominated_front)+len(pareto_front), len(front))

conn = sqlite3.connect("myimpact_database.db")
cursor = conn.cursor()

def init_sql():
    cursor.execute('DROP TABLE IF EXISTS "WHOLEMARKET"')
    cursor.execute('DROP TABLE IF EXISTS "PARETOFRONT"')
    cursor.execute('DROP TABLE IF EXISTS "DOMINATEDFRONT"')

    cursor.execute('CREATE TABLE "WHOLEMARKET" ( \
	"ObjIndex"	INTEGER, \
	"Rating"	NUMERIC, \
	"MaterialRating"	NUMERIC, \
	"SupplierCSR"	NUMERIC, \
	"Price"	NUMERIC, \
	PRIMARY KEY("ObjIndex") \
)')

    cursor.execute('CREATE TABLE "PARETOFRONT" ( \
	"ObjIndex"	INTEGER, \
	"Rating"	NUMERIC, \
	"MaterialRating"	NUMERIC, \
	"SupplierCSR"	NUMERIC, \
	"Price"	NUMERIC, \
	PRIMARY KEY("ObjIndex") \
)')

    cursor.execute('CREATE TABLE "DOMINATEDFRONT" ( \
	"ObjIndex"	INTEGER, \
	"Rating"	NUMERIC, \
	"MaterialRating"	NUMERIC, \
	"SupplierCSR"	NUMERIC, \
	"Price"	NUMERIC, \
	PRIMARY KEY("ObjIndex") \
)')

def point_to_sql(point: np.array, table: str):
    cursor.execute(f'INSERT INTO {table} VALUES ({point[0]},{point[2]},{-point[3]},{-point[4]},{-point[5]})')

def fill_pts_to_sql(pts,table):
    for point in pts:
        point_to_sql(point, table)

def run_test_gpr_model():
    scaler_x = StandardScaler()

    training_set = [(pareto_front[i][2::], 1) for i in range(16)]
    training_set = training_set + \
        [(dominated_front[i][2::], 0) for i in range(16)]
    random.shuffle(training_set)
    training_set_x, training_set_y = [
        x[0] for x in training_set], [y[1] for y in training_set]
    training_set_x = scaler_x.fit_transform(training_set_x)

    test_set = [(pareto_front[i][2::], 1) for i in range(16, 21)]
    test_set = test_set+[(dominated_front[i][2::], 0) for i in range(16, 21)]
    # random.shuffle(test_set)
    test_set_x, test_set_y = [x[0] for x in test_set], [y[1] for y in test_set]
    test_set_x = scaler_x.transform(test_set_x)

    model = GaussianProcessClassifier().fit(training_set_x, training_set_y)
    predictions = model.predict(test_set_x)
    print(predictions, test_set_y)
    correctness = [predictions[i] == test_set_y[i]
                   for i in range(len(predictions))]
    print(correctness, "\nAccuracy:", sum(
        correctness)*100/len(correctness), "%")
    return model
    print()

init_sql()
fill_pts_to_sql(front, 'wholemarket')
fill_pts_to_sql(pareto_front, 'paretofront')
fill_pts_to_sql(dominated_front, 'dominatedfront')
conn.commit()
conn.close()

run_test_gpr_model()