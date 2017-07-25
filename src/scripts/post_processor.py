from shutil import copyfile, rmtree
import os
import geojson
import errno

from constants import *


def merge_differences(route, missing_file, wrong_file, output):
    """
    Merge the missing and wrong differences into one file.

    :param route: Route GeoJSON file.
    :param missing_file: File containing missing geometries.
    :param wrong_file: File containing wrong geometries.
    :param output: Output file location.
    :return: True if there was a difference or False otherwise.
    """
    with open(TAGS_LOCATION + route) as fp:
        tags = geojson.loads(fp.read())
        properties = tags.features[0].properties

    with open(missing_file) as fp:
        missing = geojson.loads(fp.read())

    with open(wrong_file) as fp:
        wrong = geojson.loads(fp.read())

    if len(missing.features[0].geometry.coordinates) > 0 and len(wrong.features[0].geometry.coordinates) == 0:
        # Only missing geometries are present, so output that.

        missing.features[0].properties['difference_type'] = 'missing'
        missing.features[0].properties.update(properties)

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(missing))

        return True
    elif len(wrong.features[0].geometry.coordinates) > 0 and len(missing.features[0].geometry.coordinates) == 0:
        # Only wrong geometries are present, so output that.
        wrong.features[0].properties['difference_type'] = 'wrong'
        wrong.features[0].properties.update(properties)

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(wrong))

        return True
    elif len(missing.features[0].geometry.coordinates) > 0 and len(wrong.features[0].geometry.coordinates) > 0:
        # Both differences are present, so combine the features into one GeoJSON file.

        missing.features[0].properties['difference_type'] = 'missing'
        missing.features[0].properties.update(properties)
        wrong.features[0].properties['difference_type'] = 'wrong'
        wrong.features[0].properties.update(properties)

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(geojson.FeatureCollection([missing.features[0], wrong.features[0]])))

        return True
    else:
        return False


def add_property(path, key, value):
    """
    Add a property to every feature in a GeoJSON file.

    :param path: Path to the GeoJSON file.
    :param key: Key of the property to add.
    :param value: Value of the property to add.
    """
    with open(path) as fp:
        features = geojson.loads(fp.read())

    for feature in features.features:
        feature.properties[key] = value

    with open(path, 'w') as fp:
        fp.write(geojson.dumps(features))


def copy_to_site():
    """
    Copy the necessary files to the Django static folder location.
    """
    if os.path.exists(SITE_GFR):
        rmtree(SITE_GFR)

    try:
        os.makedirs(SITE_GFR)
    except OSError as e:
        # We don't care if it already exists although it shouldn't exist.
        if e.errno != errno.EEXIST:
            raise

    for route in os.listdir(GFR_ROUTES_LOCATION):
        copyfile(GFR_ROUTES_LOCATION + route, SITE_GFR + route)

    if os.path.exists(SITE_OUTPUT):
        rmtree(SITE_OUTPUT)

    try:
        os.makedirs(SITE_OUTPUT)
    except OSError as e:
        # We don't care if it already exists although it shouldn't exist.
        if e.errno != errno.EEXIST:
            raise

    for route in os.listdir(OUTPUT_LOCATION):
        copyfile(OUTPUT_LOCATION + route, SITE_OUTPUT + route)

    if os.path.exists(SITE_OSM):
        rmtree(SITE_OSM)

    try:
        os.makedirs(SITE_OSM)
    except OSError as e:
        # We don't care if it already exists although it shouldn't exist.
        if e.errno != errno.EEXIST:
            raise

    for route in os.listdir(RELATIONS_LOCATION):
        copyfile(RELATIONS_LOCATION + route, SITE_OSM + route)

    copyfile(NETWORK_OUTPUT, SITE_NETWORK)


def combine_in_network():
    """
    Combine all the routes from OSM into one GeoJSON file.
    """
    features = []

    for route in os.listdir(OSM_ROUTES_LOCATION):
        with open(OSM_ROUTES_LOCATION + route) as fp:
            feature = geojson.loads(fp.read()).features[0]
            if len(feature.geometry.coordinates) > 0:
                features.append(feature)

    with open(NETWORK_OUTPUT, 'w') as fp:
        fp.write(geojson.dumps(geojson.FeatureCollection(features)))


def post_process():
    """
    * Post process the outputted data files and publish one output file to the output folder
    * Publish a GeoJSON file containing the whole OSM cycling network
    * Copy the reference data, output files and OSM cycling network to the Django site
    """
    for route in os.listdir(GFR_ROUTES_LOCATION):
        if os.path.isfile(MISSING_LOCATION + route):
            # If the route is missing, output the reference data with correct OSM tags.

            copyfile(MISSING_LOCATION + route, OUTPUT_LOCATION + route)
            add_property(OUTPUT_LOCATION + route, 'error_type', 'missing')
        elif os.path.isfile(DIFF_MISSING_LOCATION + route) and os.path.isfile(DIFF_WRONG_LOCATION + route) \
                and merge_differences(route, DIFF_MISSING_LOCATION + route, DIFF_WRONG_LOCATION + route,
                                      OUTPUT_LOCATION + route):
            # If there's a geometrical difference, combine the two difference files and output it.

            add_property(OUTPUT_LOCATION + route, 'error_type', 'difference')
        elif os.path.isfile(TAGS_LOCATION + route):
            # When there's no geometrical difference, output the OSM data possibly containing missing tags.

            copyfile(TAGS_LOCATION + route, OUTPUT_LOCATION + route)
        else:
            raise Exception("No output file could be generated for route: " + route)

    combine_in_network()
    copy_to_site()
