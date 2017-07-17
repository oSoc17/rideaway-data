import geojson, pyproj
from constants import *

colours = {
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


def to_ref(icr, part):
    if part is not None:
        return icr + part.lower()

    return icr


def extract_routes():
    routes = {}

    with open(GFR_LOCATION) as fp:
        feature_collection = geojson.loads(fp.read())

    for feature in feature_collection.features:
        properties = feature.properties
        ref = to_ref(properties['icr'], properties['part'])

        if properties['colour'] is not None:
            if ref in routes:
                routes[ref].geometry.coordinates.extend(feature.geometry.coordinates)
            else:
                routes[ref] = feature

    return routes


def convert_tags(ref, properties):
    return {
        "name": "Itin\u00e9raires Cyclables R\u00e9gionaux - Gewestelijke Fietsroutes",
        "type": "route",
        "route": "bicycle",
        "network": "rcn",
        "ref": ref,
        "operator": "Bruxelles Mobilit\u00e9 - Brussel Mobiliteit",
        "colour": colours[properties['icr']]
    }


def project_coordinates(multi_line_string):
    wgs84 = pyproj.Proj("+init=EPSG:4326")
    lambert72 = pyproj.Proj("+init=EPSG:31370")
    converted = []

    for line_string in multi_line_string:
        new = []
        for coordinates in line_string:
            x, y = pyproj.transform(lambert72, wgs84, coordinates[0], coordinates[1])
            new.append([x, y])

        converted.append(new)

    return converted


if __name__ == "__main__":
    routes = extract_routes()

    for ref, feature in routes.items():
        feature.properties = convert_tags(ref, feature.properties)

    for feature in routes.values():
        feature.geometry.coordinates = project_coordinates(feature.geometry.coordinates)

    for ref, feature in routes.items():
        with open(GFR_ROUTES_LOCATION + ref + ".geojson", "w") as fp:
            feature_collection = geojson.FeatureCollection([feature])
            fp.write(geojson.dumps(feature_collection).decode('unicode-escape'))
