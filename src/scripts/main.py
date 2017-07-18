from shutil import rmtree
import os, errno, sys

import scraper, gfr_preprocessor, osm_processor, metadata, post_processor
from constants import *


def clean(clean_osm=True):
    if clean_osm:
        rmtree(DATA_FOLDER)
    else:
        os.remove(GFR_LOCATION)

        for folder in DATA_FOLDERS:
            rmtree(folder)

    for folder in DATA_FOLDERS:
        try:
            os.makedirs(folder)
        except OSError as e:
            # We don't care if it already exists although it shouldn't exist
            if e.errno != errno.EEXIST:
                raise


if __name__ == "__main__":
    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()

        if arg not in ['true', 'false']:
            print "Invalid argument"
        else:
            refresh_osm = arg == 'true'
    elif len(sys.argv) > 2:
        print "Invalid number of arguments"
    else:
        refresh_osm = True

    clean(clean_osm=False)

    scraper.scrape(download_osm=False)
    gfr_preprocessor.preprocess()
    osm_processor.process_osm()
    metadata.check_metadata()
    post_processor.post_process()
