import sqlite3 as sql
import networkx as nx
from itertools import combinations
import math
import random
import matplotlib.pyplot as plt
import numpy as np

# HAVE NOT IMPLEMENTED FROM CITY SHIPPING COST YET
PER_UNIT_SHIPPING_COST = 10

MINCITYPRICE_RANDRANGE = (0, 10)
CITYPRICE_RANGE = (0, 100)
OBJPRICE_RANGE = (10, 100)

n_cities = 10
max_suppliers_per_city = 3
n_object_types = 10
p_remove_edge = 0.4

random.seed(0)


city_to_supplier_dict = {}
supplier_to_obj_dict = {}

suppliers = []
cities = []
objects = []


def generate_random_graph(n, p):
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        a = random.random()
        if a < p:
            E.add(combination)

    g = nx.Graph()
    g.add_nodes_from(V)
    g.add_edges_from(E)

    return g


while True:     # Guarantee connected graph
    cities_graph = generate_random_graph(n_cities, p_remove_edge)
    if nx.is_connected(cities_graph):
        break
pos = nx.spring_layout(cities_graph)
nx.draw_networkx(cities_graph, pos)
plt.title("City Layout")
plt.savefig("City Layout")

# Vertices are cities. Cities have location scores of CSR and Price. Contain suppliers
# Suppliers have objects
# Objects. They have home city, base price (ignored during sorting, as common to all same objects), rating


class City:
    city_index = 0
    city_mean_CSR = random.randint(0, 100)
    city_base_price = random.randint(
        MINCITYPRICE_RANDRANGE[0], MINCITYPRICE_RANDRANGE[1])

    def __init__(self, city_index):
        self.city_index = city_index

        self.city_mean_CSR = random.randint(0, 100)
        self.city_base_price = random.randint(
            MINCITYPRICE_RANDRANGE[0], MINCITYPRICE_RANDRANGE[1])

        cities.append(self)


class Supplier:
    city_index = 0
    supplier_index = 0
    supplier_csr = random.triangular(0, 50, 100)
    supplier_object_types = []

    def __init__(self, city_index, supplier_index):
        self.city_index = city_index
        self.supplier_index = supplier_index

        self.supplier_csr = random.triangular(
            0, cities[city_index].city_mean_CSR, 100)

        while len(self.supplier_object_types) == 0:  # Ensure atleast one object per supplier
            self.supplier_object_types = random.choices(
                [i for i in range(n_object_types)], k=random.randint(0, n_object_types))

        suppliers.append(self)


class Object:
    supplier_index = 0
    city_index = 0
    obj_index = 0
    obj_type = 0
    rating = -random.triangular(0, 2.5, 5)
    material = -random.randint(0, 5)
    obj_base_price = random.randint(0, 100)
    F = np.array([])

    def __init__(self, city_index, supplier_index, obj_index, obj_type):
        self.city_index = city_index
        self.supplier_index = supplier_index
        self.obj_index = obj_index
        self.obj_type = obj_type

        self.rating = random.triangular(0, 2.5, 5)
        self.rating *= 1/(1+math.exp(-self.obj_base_price))

        self.material = random.randint(0, 5)
        self.obj_base_price = random.randint(
            0, 100) + cities[city_index].city_base_price

        self.F = np.array([self.obj_index, self.obj_type, -self.rating, -self.material, -
                          suppliers[self.supplier_index].supplier_csr, self.obj_base_price])

        objects.append(self)

    def update_price_by_delivery(self, delivery_city_index):
        return self.obj_base_price+PER_UNIT_SHIPPING_COST*nx.shortest_path_length(cities_graph, source=self.city_index, target=delivery_city_index)

    def new_F(self, delivery_city_index):
        self.F[-1] = self.get_price(delivery_city_index)
        return self.F


def generateData():
    global city_to_supplier_dict
    global supplier_to_obj_dict
    supplierIndex = 0
    objIndex = 0
    for cityIndex in range(n_cities):
        City(cityIndex)
        city_to_supplier_dict[cityIndex] = []
        for i in range(max_suppliers_per_city):
            sup = Supplier(cityIndex, supplierIndex)
            city_to_supplier_dict[cityIndex].append(sup)

            supplier_to_obj_dict[supplierIndex] = []
            for objType in sup.supplier_object_types:
                obj = Object(cityIndex, supplierIndex, objIndex, objType)
                supplier_to_obj_dict[supplierIndex].append(obj)
                objIndex += 1
                # print(objIndex)
            supplierIndex += 1


generateData()
print()
