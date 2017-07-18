GFR_SOURCE = "http://data-mobility.brussels/geoserver/bm_bike/wfs?service=wfs&request=GetFeature&typeName=bm_bike:icr&outputFormat=application/json"
OSM_SOURCE = "http://overpass-api.de/api/map?bbox="
BBOX = [4.24124261076, 50.7631624449, 4.47975783302, 50.9133209049]

DATA_FOLDER = "../data/"

GFR_LOCATION = "../data/gfr.geojson"
OSM_LOCATION = "../data/map.osm"

OSM_ROUTES_LOCATION = "../data/osm/"
GFR_ROUTES_LOCATION = "../data/gfr/"
TAGS_LOCATION = "../data/tags/"
MISSING_LOCATION = "../data/missing/"
DIFF_MISSING_LOCATION = "../data/diff/missing/"
DIFF_WRONG_LOCATION = "../data/diff/wrong/"
OUTPUT_LOCATION = "../data/output/"

DATA_FOLDERS = [OSM_ROUTES_LOCATION, GFR_ROUTES_LOCATION, TAGS_LOCATION, MISSING_LOCATION, DIFF_MISSING_LOCATION, DIFF_WRONG_LOCATION, OUTPUT_LOCATION]