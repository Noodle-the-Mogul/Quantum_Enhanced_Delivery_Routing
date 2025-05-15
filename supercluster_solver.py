import json
import os
import numpy as np
from itertools import combinations

with open("inter_cluster_matrix_filtered.json") as f:
    raw_matrix = json.load(f)

superclusters = {}
for fname in os.listdir("superclusters"):
    if fname.endswith(".json"):
        with open(os.path.join("superclusters", fname)) as f:
            data = json.load(f)
            superclusters[data["supercluster"]] = data["clusters"]


supercluster_matrix = {}
for i, j in combinations(superclusters.keys(), 2):
    clusters_i = superclusters[i]
    clusters_j = superclusters[j]

    distances = []
    for ci in clusters_i:
        for cj in clusters_j:
            val = raw_matrix.get(str(ci), {}).get(str(cj), None)
            if val is not None:
                distances.append(val)
    if distances:
        avg_dist = sum(distances) / len(distances)
    else:
        avg_dist = float("inf")

    supercluster_matrix.setdefault(str(i), {})[str(j)] = avg_dist
    supercluster_matrix.setdefault(str(j), {})[str(i)] = avg_dist


for k in superclusters:
    supercluster_matrix.setdefault(str(k), {})[str(k)] = 0.0

with open("super_cluster_matrix.json", "w") as f:
    json.dump(supercluster_matrix, f, indent=2)

print("-> Saved super_cluster_matrix.json")
