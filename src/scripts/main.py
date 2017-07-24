from shutil import rmtree
import os
import errno
import sys
import logging

import scraper, gfr_preprocessor, osm_processor, metadata, diff_checker, post_processor
from constants import *


def clean(clean_osm=True):
    """
    Cleans the data folders where the script will place the GeoJSON data files.

    :param clean_osm: Should the OSM data be cleaned as well. This file can be huge so it's not always preferred.
                      Defaults to True.
    """

    if clean_osm and os.path.exists(DATA_FOLDER):
        rmtree(DATA_FOLDER)
    else:
        logging.info("\tSkipping OSM data.")

        if os.path.isfile(GFR_LOCATION):
            os.remove(GFR_LOCATION)

        for folder in DATA_FOLDERS:
            if os.path.exists(folder):
                rmtree(folder)

    for folder in DATA_FOLDERS:
        try:
            os.makedirs(folder)
        except OSError as e:
            # We don't care if it already exists although it shouldn't exist.
            if e.errno != errno.EEXIST:
                raise


if __name__ == "__main__":
    # Set up a logger to debug the program
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler("debug.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    logging.info("Script starting...")

    # Check the passed parameters of the script.
    # If True, or nothing, is passed, the OSM data is cleaned,
    # if False is passed then the OSM data will be reused.
    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()

        if arg not in ['true', 'false']:
            logging.error("Invalid argument")
        else:
            refresh_osm = arg == 'true'
    elif len(sys.argv) > 2:
        logging.error("Invalid number of arguments")
    else:
        refresh_osm = True

    try:
        logging.info("Cleaning directories...")
        clean(clean_osm=refresh_osm)

        logging.info("Scraping data...")
        scraper.scrape(download_osm=refresh_osm)

        logging.info("Preprocessing GFR data...")
        gfr_preprocessor.preprocess()

        logging.info("Processing OSM data...")
        osm_processor.process_osm()

        logging.info("Checking metadata...")
        metadata.check_metadata()

        logging.info("Checking geometries...")
        diff_checker.check()

        logging.info("Post processing output files...")
        post_processor.post_process()

        logging.info("Script finished!")
    except Exception:
        logging.exception("Fatal error while running the script!")