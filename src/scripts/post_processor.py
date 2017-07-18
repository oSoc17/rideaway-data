import os
from shutil import copyfile

GFR_LOCATION = "../data/gfr/"
OSM_LOCATION = "../data/osm/"
MISSING_LOCATION = "../data/missing/"
TAGS_LOCATION = "../data/tags/"
DIFF_MISSING_LOCATION = "../data/diff/missing/"
DIFF_WRONG_LOCATION = "../data/diff/wrong/"
OUTPUT_LOCATION = "../data/output/"

for route in os.listdir(GFR_LOCATION):
    if os.path.isfile(MISSING_LOCATION + route):
        copyfile(MISSING_LOCATION + route, OUTPUT_LOCATION + route)
    elif os.path.isfile(DIFF_MISSING_LOCATION + route) or os.path.isfile(DIFF_WRONG_LOCATION + route):
        if os.path.isfile(DIFF_MISSING_LOCATION + route):
            copyfile(DIFF_MISSING_LOCATION + route, OUTPUT_LOCATION + route)
        elif os.path.isfile(DIFF_WRONG_LOCATION + route):
            copyfile(DIFF_WRONG_LOCATION + route, OUTPUT_LOCATION + route)
    else:
        copyfile(TAGS_LOCATION + route, OUTPUT_LOCATION + route)
