import numpy as np
import json
import os
from sklearn.cluster import AgglomerativeClustering

# Load inter-cluster distance matrix
with open("inter_cluster_matrix_filtered.json") as f:
    raw_matrix = json.load(f)

cluster_ids = sorted(map(int, raw_matrix.keys()))
N = len(cluster_ids)

# Build distance matrix
matrix = np.zeros((N, N))
for i, ci in enumerate(cluster_ids):
    for j, cj in enumerate(cluster_ids):
        val = raw_matrix[str(ci)].get(str(cj), float("inf"))
        matrix[i, j] = val

# Handle infinities
finite_max = np.max(matrix[np.isfinite(matrix)])
matrix[~np.isfinite(matrix)] = finite_max * 10

# Run clustering
n_superclusters = 4
print(f"[→] Clustering {N} clusters into {n_superclusters} superclusters...")

clustering = AgglomerativeClustering(
    n_clusters=n_superclusters, metric="precomputed", linkage="average"
)
labels = clustering.fit_predict(matrix)

# Group clusters into superclusters
superclusters = {i: [] for i in range(n_superclusters)}
for idx, label in enumerate(labels):
    cluster_id = cluster_ids[idx]
    superclusters[label].append(cluster_id)

# Save each supercluster to a JSON file
os.makedirs("superclusters", exist_ok=True)
for i, cluster_list in superclusters.items():
    path = f"superclusters/supercluster_{i}.json"
    with open(path, "w") as f:
        json.dump({"supercluster": i, "clusters": cluster_list}, f, indent=2)
    print(f"[✓] Saved supercluster {i} with clusters: {cluster_list}")

print("[✓] All superclusters saved in 'superclusters/'")
