import json
import os

ORDER_PATH = "supercluster_visit_order.json"
SUPERCLUSTER_DIR = "superclusters"
OUTPUT_PATH = "supercluster_visit_order_expanded.json"

with open(ORDER_PATH, "r") as f:
    order = json.load(f)
expanded = []

for sid in order:
    path = os.path.join(SUPERCLUSTER_DIR, f"supercluster_{sid}.json")
    if not os.path.exists(path):
        print(f"-) File not found for supercluster {sid}")
        continue

    with open(path, "r") as f:
        clusters = json.load(f).get("clusters", [])

    expanded.append({"supercluster": sid, "clusters": clusters})

with open(OUTPUT_PATH, "w") as f:
    json.dump(expanded, f, indent=2)

print(f"-> Expanded supercluster visit order saved to {OUTPUT_PATH}")
