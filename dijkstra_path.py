import json
import os
import heapq

INTER_CLUSTER_MATRIX = "inter_cluster_matrix_filtered.json"
INTRA_ROUTE_DIR = "OR_clusters"
OUTPUT_PATH = "global_route_dijkstra.json"


def load_matrix(path):
    with open(path, "r") as f:
        raw = json.load(f)
    nodes = sorted(map(int, raw.keys()))
    matrix = {
        i: {
            int(j): float(raw[str(i)][str(j)])
            for j in raw[str(i)]
            if str(j) in raw[str(i)]
        }
        for i in nodes
    }
    return matrix, nodes


def dijkstra_order(matrix, start=0):
    visited = set()
    current = start
    order = [current]
    visited.add(current)

    while len(visited) < len(matrix):
        next_node = None
        min_cost = float("inf")

        for candidate in matrix[current]:
            if candidate not in visited and matrix[current][candidate] < min_cost:
                min_cost = matrix[current][candidate]
                next_node = candidate

        if next_node is None:
            break  # disconnected node?
        order.append(next_node)
        visited.add(next_node)
        current = next_node

    return order


def load_cluster_route(cluster_id):
    path = os.path.join(INTRA_ROUTE_DIR, f"route_cluster_{cluster_id}.json")
    if not os.path.exists(path):
        print(f"[!] Route for cluster {cluster_id} not found.")
        return []
    with open(path, "r") as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get("route", [])


def stitch_routes(cluster_order):
    global_route = []
    for cid in cluster_order:
        cluster_route = load_cluster_route(cid)
        if not cluster_route:
            print(f"[!] Empty route for cluster {cid}, skipping.")
            continue
        if global_route and global_route[-1] == cluster_route[0]:
            global_route.extend(cluster_route[1:])
        else:
            global_route.extend(cluster_route)
    return global_route


def main():
    print("[*] Loading inter-cluster matrix...")
    matrix, nodes = load_matrix(INTER_CLUSTER_MATRIX)

    print("[→] Finding cluster visit order using greedy Dijkstra heuristic...")
    cluster_order = dijkstra_order(matrix, start=nodes[0])
    print(f"[✓] Cluster visit order: {cluster_order}")

    print("[→] Stitching global route...")
    route = stitch_routes(cluster_order)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(route, f, indent=2)
    print(f"[✓] Route saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
