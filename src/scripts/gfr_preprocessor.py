import geojson, pyproj
from constants import *


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
        "name": NAME_TAG.format(ref),
        "name:nl": NAME_TAG_NL.format(ref),
        "name:fr": NAME_TAG_FR.format(ref),
        "type": TYPE_TAG,
        "route": ROUTE_TAG,
        "network": NETWORK_TAG,
        "ref": ref,
        "operator": OPERATOR_TAG,
        "colour": COLOURS[properties['icr']]
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


def preprocess():
    routes = extract_routes()

    for ref, feature in routes.items():
        feature.properties = convert_tags(ref, feature.properties)

    for feature in routes.values():
        feature.geometry.coordinates = project_coordinates(feature.geometry.coordinates)

    for ref, feature in routes.items():
        with open(GFR_ROUTES_LOCATION + ref + ".geojson", "w") as fp:
            feature_collection = geojson.FeatureCollection([feature])
            fp.write(geojson.dumps(feature_collection).decode('unicode-escape'))
