import os, subprocess
from constants import *


def check():
    for route in os.listdir(GFR_ROUTES_LOCATION):
        if not os.path.isfile(MISSING_LOCATION + route) and os.path.isfile(TAGS_LOCATION + route):
            print route
            subprocess.check_call(['mono', EXECUTABLE, TAGS_LOCATION + route, GFR_ROUTES_LOCATION + route,
                                   '../../nts/bin/Release/intersection.geojson', DIFF_MISSING_LOCATION + route])
            subprocess.check_call(['mono', EXECUTABLE, GFR_ROUTES_LOCATION + route, TAGS_LOCATION + route,
                                   '../../nts/bin/Release/intersection.geojson', DIFF_WRONG_LOCATION + route])
