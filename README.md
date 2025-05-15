Several delivery firms like Amazon, DHL, FedEx etc. have several employees working in the logistics sector in order to carry out hundreds of 
deliveries across multiple locations in dense, metropolitan areas. These firms use a state of the art system that relays the optimal path to traverse
these delivery locations while also factoring in the current traffic conditions. Almost all of them utilise classical heuristics to carry out this task, which are serviceable,
no doubt, but in cases involving massive scale and dynamically changing traffic conditions, struggle to perform.
To better cope with such conditions, this project aims to combine the powers of classical heuristics with those of quantum optimisation algorithms. 

Quantum computing's counterpart to traditional bits is Qubits, which are subatomic particles that can be manipulated to relay digital information just like regular bits do. 
More often then not, Qubits are kept at near-absolute zero temperatures in order to both preserve their very existence and to minimise the error in their relaying of information.
Qubits utilise the concepts of Quantum Superposition and Quantum Entanglement to perform tasks that regular bits take years to compute, in minutes. 

Features : 
1)  Realistic traffic-aware delivery simulation using SUMO
2)  Intra-cluster optimization using OR-Tools (Google)
3)  Inter-cluster TSP solved using QAOA or Dijkstra
4)  Route stitching into a global route for full 200-point delivery
5)  Visual delivery path and performance metrics
6)  Modular architecture: clusters, quantum, classical all separated

BEFORE RUNNING THE CODE, MAKE SURE TO INSTALL ALL THE NECESSARY PACKAGES MENTIONED IN **requirements.txt** 

Technologies Used : 
1)  SUMO
2)  OR-Tools
3)  Qiskit
4)  Python - (Numpy, Pandas, Sklearn, TraCi, json, os)
5)  OpenStreetMap - (For obtaining the map)


**FILES ARE LISTED AND EXPLAINED AS PER THE CHRONOLOGICAL USE ORDER**

[faridabad.osm] : This is the roadway map of Faridabad obtained via querying OpenStreetMap. 

[fetch_fbd.py] : Script to fetch the roadway map of Faridabad.

[faridabad.net.xml] : The roadway map converted into a usable graph form. 

[faridabad.rou.xml & faridabad.alt.rou.xml] : Routing files for simulating vehicles on our map.

[faridabad.trips.xml] : Actual trips that vehicles in the simulation perform. 

[vehicles.add.xml] : Contains all the vehicle types to be added into the simulation to better represent Indian Traffic. 

[vdistrib.add.xml] : Provides the density and popularity of each vehicle type on the map.

[behavior.add.xml] : Provides tendencies to the vehicles that better represent Indian Traffic. eg. Ignoring Signals

[faridabad.sumocfg] : The SUMO Config file to run the simulation. It has references to all additional files used to aid the Simulation.

[Delivery/delivery_pt_generation.py] : Script to generate 200 delivery points accross the map randomly but also to make sure that these points are traversible.

[Delivery/delivery_points.csv] : CSV file containing all the delivery points. 

[Delivery/cluster_delivery_points.py] : Script to cluster the 200 delivery points into 20 clusters of 10 points each.

[Delivery/clustered_delivery_points.csv] : CSV file containing the delivery points and their respective cluster IDs.

[present_del_points.py] : Script to highlight the delivery points in the simulation using green dots. 

[sim_probe_traffic.py] : Script to probe the simulated traffic between delivery points inside clusters to get a time-based distance matrix.

[cache] : Folder containing inter cluster probes in JSON format. 

[combined_matrix] : Folder containing the same probes but in usable formatting. 

[generate_intercluster_matrix.py] : Script to obtain time-based distance matrix among the clusters. 

[resolver.py] : Script to remove two clusters from the input set due to intraversibilty. 

[inter_cluster_matrix_filtered.json] : JSON file containing the filtered inter cluster matrix.

[cluster_solver.py] : Script to solve intra cluster TSP using OR tools.

[OR_clusters] : Folder containing all the solved clusters in JSON format.

[Delivery/cluster_to_supercluster.py] : Script to create superclusters from existing clusters. 

[superclusters] : Folder containing all the superclusters. 

[supercluster_solver.py] : Script to solve intra supercluster TSP using OR tools. 

[superclusters/super_cluster_matrix.json] : JSON file containing the time based distance matrix but for superclusters.

[supercluster_qaoa.py] : Script to perform Quantum Approximation Optimisation Algorithm on intra supercluster TSP. 

[supercluster_visit_order.json] : JSON file containing the order to visit the superclusters in. 

[supercluster_ordering_helper.py] : Script to format the visiting order into a more usable one. 

[supercluster_visit_order_expanded.json] : Expanded, usable order to visit the superclusters in. 

[create_global_route.py] : Uses all the resources in hand to form the global visiting order of the 200 delivery points (minus the intraversible ones)

[full_global_route.json] : JSON file containing the global visiting order of the delivery points.

[route_builder.py] : Script that fills the gap between the 200 delivery points to generate the final global route.

[final_connected_route.json] : JSON file containg the final global route.

[generate_global_rou_file.py] : Script that converts the JSON file containing the full route into an rou.xml file that can be used in the simulation.

[final_global_route.rou.xml] : Route file for the final route of the delivery vehicle.

[dijkstra_path.py] : Script to solve the TSP using Dijkstra's algorithm in order to compare the benchmarks.

[Quantum_time.py] : Script to benchmark the performance of the delivery vehicle given a route. 

[Logs] : Folder containing the benchmarks and additional txt files to explain more about the working.


This project is licensed under the MIT License - see the LICENSE file for details.
Developed by Aditya Wadhwa. (Noodle-the-Mogul)
