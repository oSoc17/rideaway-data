import os, geojson
from shutil import copyfile
from constants import *


def merge_differences(missing_file, wrong_file, output):
    with open(missing_file) as fp:
        missing = geojson.loads(fp.read())

    with open(wrong_file) as fp:
        wrong = geojson.loads(fp.read())

    if len(missing.features[0].geometry.coordinates) > 0 and len(wrong.features[0].geometry.coordinates) == 0:
        missing.features[0].properties['difference_type'] = 'missing'

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(missing))

        return True
    elif len(wrong.features[0].geometry.coordinates) > 0 and len(missing.features[0].geometry.coordinates) == 0:
        wrong.features[0].properties['difference_type'] = 'wrong'

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(wrong))

        return True
    elif len(missing.features[0].geometry.coordinates) > 0 and len(wrong.features[0].geometry.coordinates) > 0:
        missing.features[0].properties['difference_type'] = 'missing'
        wrong.features[0].properties['difference_type'] = 'wrong'

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(geojson.FeatureCollection([missing.features[0], wrong.features[0]])))

        return True
    else:
        return False


def post_process():
    for route in os.listdir(GFR_ROUTES_LOCATION):
        if os.path.isfile(MISSING_LOCATION + route):
            copyfile(MISSING_LOCATION + route, OUTPUT_LOCATION + route)
        elif os.path.isfile(DIFF_MISSING_LOCATION + route) and os.path.isfile(DIFF_WRONG_LOCATION + route) \
                and merge_differences(DIFF_MISSING_LOCATION + route, DIFF_WRONG_LOCATION + route, OUTPUT_LOCATION + route):
            pass
        elif os.path.isfile(TAGS_LOCATION + route):
            copyfile(TAGS_LOCATION + route, OUTPUT_LOCATION + route)
        else:
            raise Exception("No output file could be generated for route: " + route)
