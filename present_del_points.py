# Colors the delivery points via a green dot to better represent the target vehicle passing them
# in our Simulation. It lables the points in clustered_delivery_points as points of interest and is
# added as an additional file in the SUMO config

import pandas as pd
from sumolib.net import readNet
import xml.etree.ElementTree as ET

CSV_PATH = "Delivery/clustered_delivery_points.csv"
NET_FILE = "faridabad.net.xml"
OUTPUT_FILE = "delivery_pois.add.xml"

net = readNet(NET_FILE)
df = pd.read_csv(CSV_PATH)

root = ET.Element("additional")

for i, row in df.iterrows():
    edge_id = row["edge_id"]
    pos = float(row["position"])
    try:
        lane = net.getEdge(edge_id).getLanes()[0]
        x, y = lane.getShape()[int(pos / lane.getLength() * len(lane.getShape()) - 1)]
        poi = ET.SubElement(
            root,
            "poi",
            {
                "id": f"dp_{i}",
                "x": str(x),
                "y": str(y),
                "color": "0,1,0",
                "type": "delivery",
            },
        )
    except Exception as e:
        print(f"-) Failed to place POI for edge {edge_id}: {e}")

ET.ElementTree(root).write(OUTPUT_FILE, encoding="UTF-8", xml_declaration=True)
print(f"-> POIs saved to {OUTPUT_FILE}")
