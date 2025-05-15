# The full global path route file only contains the order in which the delivery nodes are to be
# traversed but it does not provide the extended path for the vehicle too follow. Therefore, the vehicle
# can get stuck on these points and not be able to find its way forward.
# This file aims to fill in those gaps by generating a complete route to follow between the delivery
# points via TraCi API.

import json
import traci

NET_FILE = "faridabad.net.xml"
INPUT_ROUTE = "global_route_dijkstra.json"  # initially full_global_route.json
OUTPUT_ROUTE = "final_route_dijkstra.json"  # initially final_connected_route.son
VEHICLE_TYPE = "car"

with open(INPUT_ROUTE, "r") as f:
    original_edges = json.load(f)

traci.start(["sumo", "-n", NET_FILE, "-a", "vehicles.add.xml", "--start"])

connected_route = []
unreachable_segments = 0

try:
    for i in range(len(original_edges) - 1):
        src = original_edges[i]
        dst = original_edges[i + 1]

        try:
            route = traci.simulation.findRoute(src, dst, VEHICLE_TYPE)

            if len(route.edges) == 0:
                print(f"-) Unreachable: {src} → {dst}")
                unreachable_segments += 1
                continue
            connected_route.extend(route.edges[:-1])

        except Exception as e:
            print(f"-) Error on {src} → {dst}: {e}")
            unreachable_segments += 1

    connected_route.append(original_edges[-1])

finally:
    traci.close()

final_route = []
for edge in connected_route:
    if not final_route or final_route[-1] != edge:
        final_route.append(edge)

with open(OUTPUT_ROUTE, "w") as f:
    json.dump(final_route, f, indent=2)

print(f"\n-> Final connected route saved to: {OUTPUT_ROUTE}")
print(f"-) Skipped unreachable segments: {unreachable_segments}")
