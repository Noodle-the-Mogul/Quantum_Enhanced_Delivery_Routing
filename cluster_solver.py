# This code scans the 20 (actually 18) clusters in the combined matrix folder and
# uses OR tools to find the inter cluster optimal route. It saves them in the OR_clusters folder

import os
import json
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_tsp(distance_matrix):
    n = len(distance_matrix)

    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return int(
            distance_matrix[manager.IndexToNode(from_index)][
                manager.IndexToNode(to_index)
            ]
        )

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)
    if not solution:
        return None

    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(node)
        index = solution.Value(routing.NextVar(index))

    return route


def solve_all_clusters(folder="combined_matrix"):
    for i in range(20):
        path = os.path.join(folder, f"matrix_cluster_{i}.json")
        if not os.path.exists(path):
            print(f"-) Cluster {i} file not found.")
            continue

        with open(path, "r") as f:
            data = json.load(f)

        nodes = data["Nodes"]
        matrix = data["Matrix"]
        route_indices = solve_tsp(matrix)

        if route_indices is None:
            print(f"-) Failed to solve TSP for cluster {i}")
            continue

        route_nodes = [nodes[i] for i in route_indices]
        print(f"-> Cluster {i} route: {route_nodes}")

        output_path = f"OR_clusters/route_cluster_{i}.json"
        os.makedirs("OR_clusters", exist_ok=True)
        with open(output_path, "w") as f_out:
            json.dump({"cluster": i, "route": route_nodes}, f_out, indent=2)


if __name__ == "__main__":
    solve_all_clusters()
