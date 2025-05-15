import json
import numpy as np
from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.primitives import Sampler
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals

with open("superclusters/super_cluster_matrix.json", "r") as f:
    raw_matrix = json.load(f)

supercluster_ids = sorted(map(int, raw_matrix.keys()))
N = len(supercluster_ids)

matrix = np.array(
    [[raw_matrix[str(i)][str(j)] for j in supercluster_ids] for i in supercluster_ids]
)
matrix[np.isinf(matrix)] = np.max(matrix[np.isfinite(matrix)]) * 10

tsp = Tsp(matrix)
qp = tsp.to_quadratic_program()
converter = QuadraticProgramToQubo()
qubo = converter.convert(qp)

algorithm_globals.random_seed = 42
sampler = Sampler()
qaoa = QAOA(sampler=sampler, reps=1, optimizer=COBYLA(maxiter=20))
optimizer = MinimumEigenOptimizer(qaoa)

print("-> Solving supercluster TSP with QAOA…")
result = optimizer.solve(qubo)
