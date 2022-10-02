from ml_data_generator import *

model = run_test_gpr_model()

PRICE_THRESHOLD=1.1

target_product=list(eval(input("Enter product type, rating, material score, supplier csr and price:")))
# target_product[2]=-target_product[2]
# target_product[3]=-target_product[3]
# target_product[4]=-target_product[4]
is_green=model.predict([target_product[1::]])
alternatives=[]

if not is_green:
    print("Product is not green! Searching market for alternatives...")
    for product in front:
        if len(alternatives)>5:
            break
        if not product[1]==target_product[0]:
            continue
        if model.predict([product[2::]]) and (product[-1]<=1.1*target_product[-1]):
            alternatives.append(product)

print(f"{len(alternatives)} pareto-optimal solutions were found in your budget!")

print("Full detailed list:")
for entry in alternatives:
    print("Full details:",entry)

print("Quick list:")
for entry in alternatives:
    print(f"UID: {entry[0]} Price: {entry[-1]}")