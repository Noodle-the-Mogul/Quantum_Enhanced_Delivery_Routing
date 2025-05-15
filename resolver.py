# Due to some mapping faults in the net file, two clusters were deemed as intraversible by the
# simulation. This file aims to remove those two clusters from the inter cluster matrix to a filtered
# form. THIS CODE HAS ALREADY BEEN UTILISED AND SERVES NO MORE FUNCTIONALITY GOING FORWARD

import json
import os
import numpy as np

EXCLUDED_CLUSTERS = {0, 15}

with open("inter_cluster_matrix.json") as f:
    full_matrix = json.load(f)

filtered_matrix = {
    str(i): {str(j): cost for j, cost in sub.items() if int(j) not in EXCLUDED_CLUSTERS}
    for i, sub in full_matrix.items()
    if int(i) not in EXCLUDED_CLUSTERS
}

with open("inter_cluster_matrix_filtered.json", "w") as f:
    json.dump(filtered_matrix, f, indent=2)

print(f"-> Inter-cluster matrix reduced to {len(filtered_matrix)} clusters.")
