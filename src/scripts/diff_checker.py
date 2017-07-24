import os
import subprocess
import logging

from constants import *


def check():
    """
    Runs the NTS Difference Checker for each route two times. Once to find missing segments and once to find incorrect
    segments.
    """
    devnull = open(os.devnull, 'wb')

    for route in os.listdir(GFR_ROUTES_LOCATION):
        if not os.path.isfile(MISSING_LOCATION + route) and os.path.isfile(TAGS_LOCATION + route):
            logging.info("\t*) Checking route %s", route)
            subprocess.check_call(
                ['mono', EXECUTABLE, TAGS_LOCATION + route, GFR_ROUTES_LOCATION + route, DIFF_MISSING_LOCATION + route],
                stdout=devnull)
            subprocess.check_call(
                ['mono', EXECUTABLE, GFR_ROUTES_LOCATION + route, TAGS_LOCATION + route, DIFF_WRONG_LOCATION + route],
                stdout=devnull)

    devnull.close()
