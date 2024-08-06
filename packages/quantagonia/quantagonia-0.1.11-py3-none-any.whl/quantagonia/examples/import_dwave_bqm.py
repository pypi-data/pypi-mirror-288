import os

from dimod import BinaryQuadraticModel
from dimod.generators import combinations

from quantagonia import HybridSolver, HybridSolverParameters
from quantagonia.qubo import QuboModel

# build the map coloring bqm model from here:
# https://github.com/dwavesystems/dwave-ocean-sdk/blob/master/docs/examples/map_coloring_full_code.rst

# Represent the map as the nodes and edges of a graph
provinces = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
neighbors = [
    ("AB", "BC"),
    ("AB", "NT"),
    ("AB", "SK"),
    ("BC", "NT"),
    ("BC", "YT"),
    ("MB", "NU"),
    ("MB", "ON"),
    ("MB", "SK"),
    ("NB", "NS"),
    ("NB", "QC"),
    ("NL", "QC"),
    ("NT", "NU"),
    ("NT", "SK"),
    ("NT", "YT"),
    ("ON", "QC"),
]

colors = ["y", "g", "r", "b"]

# Add constraint that each node (province) select a single color
bqm_one_color = BinaryQuadraticModel("BINARY")
for province in provinces:
    variables = [province + "_" + c for c in colors]
    bqm_one_color.update(combinations(variables, 1))

# Add constraint that each pair of nodes with a shared edge not both select one color
bqm_neighbors = BinaryQuadraticModel("BINARY")
for neighbor in neighbors:
    v, u = neighbor
    interactions = [(v + "_" + c, u + "_" + c) for c in colors]
    for interaction in interactions:
        bqm_neighbors.add_quadratic(interaction[0], interaction[1], 1)

bqm = bqm_one_color + bqm_neighbors

# read bqm file into QuboModel
qubo = QuboModel.from_dwave_bqm(bqm)

# solve QUBO with Quantagonia's solver
API_KEY = os.environ["QUANTAGONIA_API_KEY"]
params = HybridSolverParameters()
hybrid_solver = HybridSolver(API_KEY)
qubo.solve(hybrid_solver, params)

# print solution vector
print("Optimal solution vector:")
for var_name, var in qubo.vars.items():
    print("\t", var_name, "\t", var.eval())

# in order to use these as test
obj = qubo.eval()
if obj != 0.0:
    msg = f"Objective value is not correct: {obj} instead of 0.0"
    raise ValueError(msg)
