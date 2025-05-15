import sumolib
import random
import xml.etree.ElementTree as ET
import csv

# === CONFIGURATION ===
NET_FILE = "faridabad.net.xml"
OUTPUT_CSV = "Delivery/delivery_points.csv"
OUTPUT_TRIPS_XML = "Delivery/delivery_points.trips.xml"
NUM_DELIVERIES = 200
VEHICLE_TYPE = "delivery"

# === LOAD NETWORK ===
net = sumolib.net.readNet(NET_FILE)

# === FILTER VALID EDGES ===
valid_edges = [
    edge
    for edge in net.getEdges()
    if not edge.getID().startswith(":") and edge.allows(VEHICLE_TYPE)
]

if len(valid_edges) < NUM_DELIVERIES:
    raise ValueError(
        f"Only {len(valid_edges)} valid edges found. Need at least {NUM_DELIVERIES}."
    )

# === SAMPLE EDGES ===
delivery_edges = random.sample(valid_edges, NUM_DELIVERIES)

# === WRITE CSV ===
with open(OUTPUT_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "edge_id", "position"])
    for i, edge in enumerate(delivery_edges):
        delivery_id = f"dp{i+1}"
        pos = edge.getLength() / 2  # Midpoint of edge
        writer.writerow([delivery_id, edge.getID(), pos])

print(f" Delivery points saved to {OUTPUT_CSV}")

# === OPTIONAL: WRITE trips.xml FOR SUMO TESTING ===
root = ET.Element("routes")
for i, edge in enumerate(delivery_edges):
    trip = ET.SubElement(
        root,
        "trip",
        {
            "id": f"delivery{i+1}",
            "type": VEHICLE_TYPE,
            "depart": str(i),  # Stagger departures
            "from": edge.getID(),
            "to": edge.getID(),
        },
    )

tree = ET.ElementTree(root)
tree.write(OUTPUT_TRIPS_XML, encoding="utf-8", xml_declaration=True)

print(f"SUMO trips file saved to {OUTPUT_TRIPS_XML}")
