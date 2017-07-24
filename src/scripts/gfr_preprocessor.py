import geojson
import pyproj

from constants import *


def to_ref(icr, part):
    """
    Converts a icr tag and part tag to a ref tag.

    :param icr: Value of the icr tag, cannot be NULL.
    :param part: Value of the part tag, can be NULL.
    :return: The corresponding ref tag.
    """
    if part is not None:
        return icr + part.lower()

    return icr


def extract_routes():
    """
    Extracts the features from the reference data and puts all the features of one route together in a file.

    :return: A dictionary containing the GeoJSON for each route.
    """
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
    """
    Generates the correct metadata the route should have.

    :param ref: Reference tag of the route.
    :param properties: Properties of the reference data.
    :return: JSON containing the correct metadata for the given route.
    """

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
    """
    Projects the coordinates from the reference data from Lambert72 to WGS84.

    :param multi_line_string: Coordinates of the geometry.
    :return: Projected coordinates.
    """
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
    """
    Pre-process the reference data:
        * Split the data into routes
        * Give routes the correct OSM tags
        * Project coordinates to WGS84 reference system
        * Write a GeoJSON file for each route
    """
    routes = extract_routes()

    for ref, feature in routes.items():
        feature.properties = convert_tags(ref, feature.properties)

    for feature in routes.values():
        feature.geometry.coordinates = project_coordinates(feature.geometry.coordinates)

    for ref, feature in routes.items():
        with open(GFR_ROUTES_LOCATION + ref + ".geojson", "w") as fp:
            feature_collection = geojson.FeatureCollection([feature])

            # Do unicode-escape for French characters.
            fp.write(geojson.dumps(feature_collection).decode('unicode-escape'))
