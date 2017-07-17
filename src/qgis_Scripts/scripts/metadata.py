import geojson, os

GFR_LOCATION = "../../data/gfr/"
OSM_LOCATION = "../../data/osm/"
OUTPUT_LOCATION = "../../data/tags/"


def compare_tags(gfr, osm):
    gfr_tags = gfr.features[0].properties
    osm_tags = osm.features[0].properties
    errors = ""

    for key, value in gfr_tags.items():
        if key not in osm_tags:
            errors += "Missing tag: " + key + "=" + value + ";"
        elif osm_tags[key] != value:
            errors += "Wrong tag: " + key + "=" + osm_tags[key] + ", value should be:" + value + ";"

    return errors


for route_file in os.listdir(GFR_LOCATION):
    if os.path.isfile(OSM_LOCATION + route_file):
        with open(GFR_LOCATION + route_file) as fp:
            gfr = geojson.loads(fp.read())

        with open(OSM_LOCATION + route_file) as fp:
            osm = geojson.loads(fp.read())

        errors = compare_tags(gfr, osm)

        if errors != "":
            osm.features[0].properties['errors'] = errors

        with open(OUTPUT_LOCATION + route_file, 'w') as fp:
            fp.write(geojson.dumps(osm))
