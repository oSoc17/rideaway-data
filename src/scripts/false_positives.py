import os
import geojson

from constants import *


def add_geometry(source, destination):
    geometry = source.features[0].geometry
    if geometry.type == "LineString":
        geometry.coordinates.append(
            destination.features[0].geometry.coordinates
        )
    elif geometry.type == "MultiLineString":
        geometry.coordinates.extend(
            destination.features[0].geometry.coordinates
        )
    else:
        raise Exception("Invalid geometry for false positives")

    source.features[0].geometry = geometry

    return source


def manage_false_positives():
    for route in os.listdir(GFR_FALSE_POSITIVES):
        if os.path.isfile(GFR_ROUTES_LOCATION + route):
            with open(GFR_FALSE_POSITIVES + route) as src, open(GFR_ROUTES_LOCATION + route) as dest:
                src_geojson = geojson.loads(src.read())
                dest_geojson = geojson.loads(dest.read())

                result = add_geometry(src_geojson, dest_geojson)

            with open(GFR_ROUTES_LOCATION + route, 'w') as fp:
                fp.write(geojson.dumps(result))

    for route in os.listdir(OSM_FALSE_POSITIVES):
        if os.path.isfile(OSM_ROUTES_LOCATION + route):
            with open(OSM_FALSE_POSITIVES + route) as src, open(OSM_ROUTES_LOCATION + route) as dest:
                src_geojson = geojson.loads(src.read())
                dest_geojson = geojson.loads(dest.read())

                result = add_geometry(src_geojson, dest_geojson)

            with open(OSM_ROUTES_LOCATION + route, 'w') as fp:
                fp.write(geojson.dumps(result))
