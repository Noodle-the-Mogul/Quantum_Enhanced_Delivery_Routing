# This file merges the superclusters and the clusters to form a global route containing all our
# devivery nodes. It uses the intra-cluster and intra-supercluster routing files and combines them
# with the inter-supercluster path to store it as a JSON

import os
import json

ROUTE_DIR = "OR_clusters"
MAPPING_PATH = "supercluster_visit_order_expanded.json"
OUTPUT_PATH = "full_global_route.json"

with open(MAPPING_PATH, "r") as f:
    supercluster_order = json.load(f)


def load_cluster_route(cluster_id):
    path = os.path.join(ROUTE_DIR, f"route_cluster_{cluster_id}.json")
    if not os.path.exists(path):
        print(f"-) Warning: Route for cluster {cluster_id} not found.")
        return []
    with open(path, "r") as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get("route", [])


global_path = []

for entry in supercluster_order:
    sid = entry["supercluster"]
    clusters = entry["clusters"]
    print(f"-> Supercluster {sid} contains clusters: {clusters}")

    for cid in clusters:
        route = load_cluster_route(cid)
        if not route:
            print(f"-) Empty or missing route for cluster {cid}, skipping.")
            continue

        if global_path and route[0] == global_path[-1]:
            global_path.extend(route[1:])
        else:
            global_path.extend(route)

with open(OUTPUT_PATH, "w") as f:
    json.dump(global_path, f, indent=2)

print(f"-> Global route saved to {OUTPUT_PATH}")
