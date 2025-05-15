import networkx as nx
import xml.etree.ElementTree as ET
import json


def extract_edge_weights(net_file_path):
    tree = ET.parse(net_file_path)
    root = tree.getroot()

    edge_weights = {}
    for edge in root.findall(".//edge"):
        edge_id = edge.get("id")
        if edge_id.startswith(":"):
            continue
        lanes = edge.findall(".//lane")
        if lanes:
            lane = lanes[0]
            length = float(lane.get("length", 0))
            speed = float(lane.get("speed", 1))
            travel_time = length / speed
            edge_weights[edge_id] = travel_time
    return edge_weights


def calculate_travel_time(edge_path, edge_weights):
    missing = [eid for eid in edge_path if eid not in edge_weights]
    if missing:
        print(f"[!] {len(missing)} edge IDs in path not found in network:")
        for eid in missing:
            print(" -", eid)
    return sum(edge_weights[eid] for eid in edge_path if eid in edge_weights)


edge_weights = extract_edge_weights("faridabad.net.xml")

with open("final_route_dijkstra.json") as f:  # initially final_connected_route.json
    edge_path = json.load(f)

total_time = calculate_travel_time(edge_path, edge_weights)

print(f"Total travel time: {total_time:.2f} seconds")
