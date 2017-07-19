import os, subprocess

GFR_ROUTES_LOCATION = "../data/gfr/"
TAGS_LOCATION = "../data/tags/"
MISSING_LOCATION = "../data/missing/"
DIFF_MISSING_LOCATION = "../data/diff/missing/"
DIFF_WRONG_LOCATION = "../data/diff/wrong/"

EXECUTABLE = "../../nts/bin/Release/NTS-BufferingTest.exe"

for route in os.listdir(GFR_ROUTES_LOCATION):
    if not os.path.isfile(MISSING_LOCATION + route) and os.path.isfile(TAGS_LOCATION + route):
        print route
        subprocess.check_call(['mono', EXECUTABLE, TAGS_LOCATION + route, GFR_ROUTES_LOCATION + route,
                               '../../nts/bin/Release/intersection.geojson', DIFF_MISSING_LOCATION + route])
        subprocess.check_call(['mono', EXECUTABLE, GFR_ROUTES_LOCATION + route, TAGS_LOCATION + route,
                               '../../nts/bin/Release/intersection.geojson', DIFF_WRONG_LOCATION + route])
