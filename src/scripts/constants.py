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
NETWORK_OUTPUT = "../data/network.geojson"

SITE_OUTPUT = "../brumob/static/brumob/data/output/"
SITE_GFR = "../brumob/static/brumob/data/routes/"
SITE_NETWORK = "../brumob/static/brumob/data/network.geojson"

DATA_FOLDERS = [OSM_ROUTES_LOCATION, GFR_ROUTES_LOCATION, TAGS_LOCATION, MISSING_LOCATION, DIFF_MISSING_LOCATION,
                DIFF_WRONG_LOCATION, OUTPUT_LOCATION]

COLOURS = {
    '1': '#89C13D',
    '2': '#77AAD2',
    '3': '#ED1C24',
    '4': '#C23E96',
    '5': '#009549',
    '6': '#009549',
    '7': '#932F34',
    '8': '#89C13D',
    '9': '#C23E96',
    '10': '#ED1C24',
    '11': '#77AAD2',
    '12': '#009549',
    'PP': '#932F34',
    'MM': '#2E3192',
    'SZ': '#00A9E9',
    'CK': '#00A9E9',
    'A': '#F6A31A',
    'B': '#F6A31A',
    'C': '#F6A31A'
}

NAME_TAG = "{} Itin\u00e9raire Cyclable R\u00e9gional - Gewestelijke Fietsroute"
NAME_TAG_NL = "{} Gewestelijke Fietsroute"
NAME_TAG_FR = "{} Itin\u00e9raire Cyclable R\u00e9gional"
TYPE_TAG = "route"
ROUTE_TAG = "bicycle"
NETWORK_TAG = "lcn"
OPERATOR_TAG = "Brussels Mobility"

EXECUTABLE = "../../nts/bin/Release/NTS-BufferingTest.exe"
