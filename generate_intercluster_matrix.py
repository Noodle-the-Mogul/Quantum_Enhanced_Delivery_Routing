# This file uses OR tools to generate a time based inter cluster matrix from the clustered delivery
# points csv file. It gets travel times via the TraCi API calls on the simulation net file.

import traci
import os
import json
import pandas as pd
from itertools import product
from collections import defaultdict

NET_FILE = "faridabad.net.xml"
INPUT_CSV = "Delivery/clustered_delivery_points.csv"
OUTPUT_JSON = "inter_cluster_matrix.json"
VEHICLE_TYPE = "delivery"
DELTA_T = 1000.0
MAX_STEPS = 3000

df = pd.read_csv(INPUT_CSV)
cluster_dict = df.groupby("cluster")["edge_id"].apply(list).to_dict()
clusters = list(cluster_dict.keys())


# Gets travel time between two edge pairs, returns inf if the edges are not traversible from one another
def get_travel_time(from_edge, to_edge):
    route_id = f"r_{from_edge}_{to_edge}"
    veh_id = f"v_{from_edge}_{to_edge}"

    try:
        route = traci.simulation.findRoute(from_edge, to_edge, VEHICLE_TYPE)
        if len(route.edges) == 0 or route.length < 1:
            raise Exception("No valid route")

        traci.route.add(route_id, [from_edge, to_edge])
        traci.vehicle.add(veh_id, route_id, typeID=VEHICLE_TYPE)

        step = 0
        entered = False

        while step < MAX_STEPS:
            traci.simulationStep()
            step += 1
            if not entered and veh_id in traci.vehicle.getIDList():
                entered = True
            if entered and veh_id not in traci.vehicle.getIDList():
                break

        if veh_id in traci.vehicle.getIDList():
            traci.vehicle.remove(veh_id)

        if entered:
            return step * DELTA_T / 1000.0  # in seconds
        else:
            return float("inf")

    except Exception as e:
        try:
            if veh_id in traci.vehicle.getIDList():
                traci.vehicle.remove(veh_id)
        except:
            pass
        return float("inf")


# Builds the inter cluster matrix by looping thru the clusters and the edges inside them
def build_inter_cluster_matrix():
    print("-> Launching SUMO...")
    traci.start(["sumo", "-n", NET_FILE, "-a", "vehicles.add.xml", "--start"])

    try:
        matrix = defaultdict(dict)
        total_pairs = len(clusters) ** 2
        for idx, (i, j) in enumerate(product(clusters, repeat=2)):
            edge_i = cluster_dict[i][0]
            edge_j = cluster_dict[j][0]

            time_taken = get_travel_time(edge_i, edge_j)
            matrix[str(i)][str(j)] = time_taken

            print(f"[{idx+1}/{total_pairs}] Cluster {i} → {j}: {time_taken:.2f} sec")

    finally:
        traci.close()
        print("-> SUMO session closed.")

    with open(OUTPUT_JSON, "w") as f:
        json.dump(matrix, f, indent=2)
    print(f"-> Matrix saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    build_inter_cluster_matrix()
