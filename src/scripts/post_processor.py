import os
from shutil import copyfile
from constants import *


def post_process():
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
