import os
import geojson

from constants import *


def add_geometry(source, destination):
    """
    Adds the geometry of the first feature of the source data to the first feature of the destination data.

    :param source: Feature collection containing the geometry to add.
    :param destination: Feature collection where the geometry should be added to.
    :return: GeoJSON feature collection of the result.
    """
    geometry = source.features[0].geometry
    if geometry.type == "LineString":
        destination.features[0].geometry.coordinates.append(
            geometry.coordinates
        )
    elif geometry.type == "MultiLineString":
        destination.features[0].geometry.coordinates.extend(
            geometry.coordinates
        )
    else:
        raise Exception("Invalid geometry for false positives")

    return destination


def manage_false_positives():
    """
    Manages the false positives by adding the geometries to the source data, so they will be excluded from the differences.
    """
    # Handle the GFR false positives
    for route in os.listdir(GFR_FALSE_POSITIVES):
        if os.path.isfile(GFR_ROUTES_LOCATION + route):
            with open(GFR_FALSE_POSITIVES + route) as src, open(GFR_ROUTES_LOCATION + route) as dest:
                src_geojson = geojson.loads(src.read())
                dest_geojson = geojson.loads(dest.read())

                result = add_geometry(src_geojson, dest_geojson)

            # Write result to the route file
            with open(GFR_ROUTES_LOCATION + route, 'w') as fp:
                fp.write(geojson.dumps(result))

    # Handle the OSM false positives
    for route in os.listdir(OSM_FALSE_POSITIVES):
        if os.path.isfile(OSM_ROUTES_LOCATION + route):
            with open(OSM_FALSE_POSITIVES + route) as src, open(OSM_ROUTES_LOCATION + route) as dest:
                src_geojson = geojson.loads(src.read())
                dest_geojson = geojson.loads(dest.read())

                result = add_geometry(src_geojson, dest_geojson)

            # Write result to the route file
            with open(OSM_ROUTES_LOCATION + route, 'w') as fp:
                fp.write(geojson.dumps(result))
