import os

from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.problems.quadratic_program import QuadraticProgram

from quantagonia import HybridSolver, HybridSolverParameters
from quantagonia.qubo.model import QuboModel

API_KEY = os.environ["QUANTAGONIA_API_KEY"]


def build_qiskit_qp() -> QuadraticProgram:
    """Builds a small subset sum quadratic optimization problem."""
    weights = [9, 7, 2, 1]
    capacity = 10

    qp = QuadraticProgram()

    # create binary variables (y_j = 1 if bin j is used, x_i_j = 1 if item i
    # is packed in bin j)
    for j in range(len(weights)):
        qp.binary_var(f"y_{j}")
    for i in range(len(weights)):
        for j in range(len(weights)):
            qp.binary_var(f"x_{i}_{j}")

    # minimize the number of used bins
    qp.minimize(linear={f"y_{j}": 1 for j in range(len(weights))})

    # ensure that each item is packed in exactly one bin
    for i in range(len(weights)):
        qp.linear_constraint(
            name=f"item_placing_{i}", linear={f"x_{i}_{j}": 1 for j in range(len(weights))}, sense="==", rhs=1
        )

    # ensure that the total weight of items in each bin does not exceed the capacity
    for j in range(len(weights)):
        lhs_x = {f"x_{i}_{j}": weights[i] for i in range(len(weights))}
        lhs_y = {f"y_{j}": -capacity}
        qp.linear_constraint(name=f"capacity_bin_{j}", linear={**lhs_x, **lhs_y}, sense="<=", rhs=0)

    return qp


# build qiskit qp
qp = build_qiskit_qp()
# use qiskit to convert qp to qubo
qp2qubo = QuadraticProgramToQubo()
qiskit_qubo = qp2qubo.convert(qp)

# read the qiskit qubo
qubo = QuboModel.from_qiskit_qubo(qiskit_qubo)

# solve with Quantagonia
params = HybridSolverParameters()
hybrid_solver = HybridSolver(API_KEY)
qubo.solve(hybrid_solver, params)

# to be used in tests
obj = qubo.eval()
if obj != -18.0:
    msg = f"Objective value is not correct: {obj} instead of -18.0"
    raise ValueError(msg)
