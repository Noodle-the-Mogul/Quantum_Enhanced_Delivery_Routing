# Query to fetch the map data for faridabad thru OpenStreetMap using the overpass API and then
# using it to get highway(roadway) nodes. The XML map is then parsed into an OSM file for further
# usage

import requests

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:xml][timeout:90];
area["name"="Faridabad"]->.searchArea;
(
  way["highway"](area.searchArea);
  >; 
);
out body;
"""

response = requests.get(overpass_url, params={"data": overpass_query})
with open("faridabad.osm", "wb") as f:
    f.write(response.content)
