from shutil import copyfile
import geojson
import os

from constants import *


def compare_tags(gfr, osm):
    """
    Compares the properties between two data sets taking the properties of the first argument as reference data.

    :param gfr: Reference GeoJSON data.
    :param osm: GeoJSON data to compare metadata from.
    :return: Semicolon delimited string containing all the metadata errors.
    """
    gfr_tags = gfr.features[0].properties
    osm_tags = osm.features[0].properties
    errors = ""

    for key, value in gfr_tags.items():
        if key not in osm_tags:
            errors += "Missing tag: " + key + "=" + value + ";"
        elif osm_tags[key] != value:
            errors += "Wrong tag: " + key + "=" + osm_tags[key] + ", value should be: " + value + ";"

    return errors


def check_metadata():
    """
    Compares the metadata of each route separately of the routes available in the corresponding data folders. A new file
    is written containing the OSM geometry with extra tags describing the metadata issues.
    """
    for route_file in os.listdir(GFR_ROUTES_LOCATION):
        if os.path.isfile(OSM_ROUTES_LOCATION + route_file):
            with open(GFR_ROUTES_LOCATION + route_file) as fp:
                gfr = geojson.loads(fp.read())

            with open(OSM_ROUTES_LOCATION + route_file) as fp:
                osm = geojson.loads(fp.read())

            if len(osm.features[0].geometry.coordinates) > 0:
                errors = compare_tags(gfr, osm)

                if errors != "":
                    osm.features[0].properties['error_type'] = 'tagging'
                    osm.features[0].properties['tagging_errors'] = errors

                with open(TAGS_LOCATION + route_file, 'w') as fp:
                    fp.write(geojson.dumps(osm))
            else:
                copyfile(GFR_ROUTES_LOCATION + route_file, MISSING_LOCATION + route_file)
        else:
            # If the OSM data didn't contain this route, we copy the reference data to the missing data folder.
            copyfile(GFR_ROUTES_LOCATION + route_file, MISSING_LOCATION + route_file)
