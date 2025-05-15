import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import sumolib

# === CONFIG ===
NET_FILE = "faridabad.net.xml"
CSV_FILE = "Delivery/delivery_points.csv"
OUTPUT_FILE = "Delivery/clustered_delivery_points.csv"
NUM_CLUSTERS = 20

# === Load SUMO Net ===
net = sumolib.net.readNet(NET_FILE)

# === Load Delivery Points CSV ===
df = pd.read_csv(CSV_FILE)

coords = []
valid_rows = []

# === Convert edge+position to coordinates ===
for index, row in df.iterrows():
    edge_id = row["edge_id"]
    pos = float(row["position"])
    try:
        edge = net.getEdge(edge_id)
        lane = edge.getLanes()[0]
        x, y = lane.getShape()[int(pos) if pos < len(lane.getShape()) else -1]
        coords.append([x, y])
        valid_rows.append(row)
    except Exception as e:
        print(f"Skipping invalid point: {edge_id} at pos {pos} — {e}")

coords = np.array(coords)
valid_df = pd.DataFrame(valid_rows)

# === Perform KMeans Clustering ===
kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
labels = kmeans.fit_predict(coords)

# === Add cluster labels back to DataFrame ===
valid_df["cluster"] = labels

# === Save Output ===
valid_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nClustered {len(valid_df)} delivery points into {NUM_CLUSTERS} clusters.")
print(f"Output saved to {OUTPUT_FILE}")
