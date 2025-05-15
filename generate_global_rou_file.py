# This file converts the final route generated (containing all the nodes that the vehicle will traverse
# on its way to the delivery points) into a route file that we can feed into the simulation.
# This creates our test vehicle (delivery_van) and assigns it a distinct colour from other vehicles in
# our simulation.

import json

INPUT_ROUTE = "final_route_dijkstra.json"  # initially final_connected_route.json
OUTPUT_XML = "final_dijkstra_route.rou.xml"  # initially final_global_route.rou.xm

vehicle_id = "delivery_dijk"  # initially delivery_van
route_id = "dijkstra_route"  # initially global_route
vtype = "car"

with open(INPUT_ROUTE, "r") as f:
    edges = json.load(f)

with open(OUTPUT_XML, "w") as f:
    f.write("<routes>\n")
    f.write(
        f'    <vType id="{vtype}" vClass="delivery" color="1,0,0" accel="1.0" decel="4.5" length="7.5" minGap="2.5" maxSpeed="30"/>\n'
    )
    f.write(f'    <route id="{route_id}" edges="{" ".join(edges)}"/>\n')
    f.write(
        f'    <vehicle id="{vehicle_id}" type="{vtype}" route="{route_id}" depart="0" color="1,0,0"/>\n'
    )
    f.write("</routes>\n")

print(f"-> SUMO route file written to: {OUTPUT_XML}")
