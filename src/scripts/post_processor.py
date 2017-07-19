import os, geojson, errno
from shutil import copyfile, rmtree
from constants import *


def merge_differences(route, missing_file, wrong_file, output):
    with open(TAGS_LOCATION + route) as fp:
        tags = geojson.loads(fp.read())
        properties = tags.features[0].properties

    with open(missing_file) as fp:
        missing = geojson.loads(fp.read())

    with open(wrong_file) as fp:
        wrong = geojson.loads(fp.read())

    if len(missing.features[0].geometry.coordinates) > 0 and len(wrong.features[0].geometry.coordinates) == 0:
        missing.features[0].properties['difference_type'] = 'missing'
        missing.features[0].properties.update(properties)

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(missing))

        return True
    elif len(wrong.features[0].geometry.coordinates) > 0 and len(missing.features[0].geometry.coordinates) == 0:
        wrong.features[0].properties['difference_type'] = 'wrong'
        wrong.features[0].properties.update(properties)

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(wrong))

        return True
    elif len(missing.features[0].geometry.coordinates) > 0 and len(wrong.features[0].geometry.coordinates) > 0:
        missing.features[0].properties['difference_type'] = 'missing'
        missing.features[0].properties.update(properties)
        wrong.features[0].properties['difference_type'] = 'wrong'
        wrong.features[0].properties.update(properties)

        with open(output, 'w') as fp:
            fp.write(geojson.dumps(geojson.FeatureCollection([missing.features[0], wrong.features[0]])))

        return True
    else:
        return False


def copy_to_site():
    if os.path.exists(SITE_GFR):
        rmtree(SITE_GFR)

    try:
        os.makedirs(SITE_GFR)
    except OSError as e:
        # We don't care if it already exists although it shouldn't exist
        if e.errno != errno.EEXIST:
            raise

    for route in os.listdir(GFR_ROUTES_LOCATION):
        copyfile(GFR_ROUTES_LOCATION + route, SITE_GFR + route)

    if os.path.exists(SITE_OUTPUT):
        rmtree(SITE_OUTPUT)

    try:
        os.makedirs(SITE_OUTPUT)
    except OSError as e:
        # We don't care if it already exists although it shouldn't exist
        if e.errno != errno.EEXIST:
            raise

    for route in os.listdir(OUTPUT_LOCATION):
        copyfile(OUTPUT_LOCATION + route, SITE_OUTPUT + route)


def post_process():
    for route in os.listdir(GFR_ROUTES_LOCATION):
        if os.path.isfile(MISSING_LOCATION + route):
            copyfile(MISSING_LOCATION + route, OUTPUT_LOCATION + route)
        elif os.path.isfile(DIFF_MISSING_LOCATION + route) and os.path.isfile(DIFF_WRONG_LOCATION + route) \
                and merge_differences(route, DIFF_MISSING_LOCATION + route, DIFF_WRONG_LOCATION + route,
                                      OUTPUT_LOCATION + route):
            pass
        elif os.path.isfile(TAGS_LOCATION + route):
            copyfile(TAGS_LOCATION + route, OUTPUT_LOCATION + route)
        else:
            raise Exception("No output file could be generated for route: " + route)

    copy_to_site()
