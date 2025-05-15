# This is done to probe inter cluster delivery points for travel times between them to generate
# 20 different intercluster matrices. This utilises OR tools and is arguably the slowest step.
# This can be made exponentially faster with the help of parallel processing but due to unexpected
# errors and sytem crashing it is beyond our scope.

import traci
import json
import os
import pandas as pd
from itertools import product
import time

NET_FILE = "faridabad.net.xml"
VEHICLE_TYPE = "delivery"
INPUT_CSV = "Delivery/clustered_delivery_points.csv"
CACHE_DIR = "cache"
MAX_STEPS = 3000  # Sim timeout
DELTA_T = 1000.0  # in seconds

os.makedirs(CACHE_DIR, exist_ok=True)

df = pd.read_csv(INPUT_CSV)
all_edges = df["edge_id"].unique().tolist()


def get_valid_edges(edge_ids):
    valid = []
    for eid in edge_ids:
        try:
            num_lanes = traci.edge.getLaneNumber(eid)
            for i in range(num_lanes):
                lane_id = f"{eid}_{i}"
                allowed = traci.lane.getAllowed(lane_id)
                if not allowed or "passenger" in allowed or "all" in allowed:
                    valid.append(eid)
                    break
        except traci.exceptions.TraCIException:
            continue
    return valid


def simulate_single_session():
    print("[*] Starting SUMO...")
    traci.start(
        [
            "sumo",
            "-n",
            NET_FILE,
            "-a",
            "vehicles.add.xml",
            "--start",
        ]
    )
    try:
        print("-> Validating usable edges...")
        valid_edges = get_valid_edges(all_edges)
        df_filtered = df[df["edge_id"].isin(valid_edges)]
        clusters = df_filtered.groupby("cluster")["edge_id"].apply(list).to_dict()
        print(f"-> {len(valid_edges)} valid edges found. Starting cluster probing...\n")

        for idx, (cluster, edges) in enumerate(clusters.items()):
            cache_file = os.path.join(CACHE_DIR, f"cache_cluster_{cluster}.json")
            if os.path.exists(cache_file):
                print(f"-> Cluster {cluster} already cached, skipping.")
                continue

            print(
                f"[{time.strftime('%H:%M:%S')}] -> Probing cluster {cluster} ({idx + 1}/{len(clusters)})..."
            )
            pairs = [(src, dst) for src, dst in product(edges, edges) if src != dst]
            cache = {}

            for i, (src, dst) in enumerate(pairs):
                key = f"{src}->{dst}"
                route_id = f"r_{src}_{dst}"
                veh_id = f"v_{src}_{dst}"

                try:
                    route = traci.simulation.findRoute(src, dst, VEHICLE_TYPE)
                    if len(route.edges) == 0 or route.length < 1:
                        raise Exception("-) No valid route")

                    traci.route.add(route_id, [src, dst])
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

                    if entered:
                        travel_time = step * DELTA_T / 1000.0
                        cache[key] = travel_time if step < MAX_STEPS else float("inf")
                    else:
                        cache[key] = float("inf")

                    if veh_id in traci.vehicle.getIDList():
                        traci.vehicle.remove(veh_id)

                except Exception as e:
                    cache[key] = float("inf")
                    print(f"-) Failed for {key}: {e}")
                    try:
                        if veh_id in traci.vehicle.getIDList():
                            traci.vehicle.remove(veh_id)
                    except:
                        pass

                if (i + 1) % 20 == 0 or i == len(pairs) - 1:
                    print(f"    → {i + 1}/{len(pairs)} pairs done")

            with open(cache_file, "w") as f:
                json.dump(cache, f)

            print(f"-> Finished cluster {cluster}")

    finally:
        traci.close()
        print("\n-> All clusters complete. SUMO session closed.")


if __name__ == "__main__":
    simulate_single_session()
