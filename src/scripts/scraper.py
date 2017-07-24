import urllib2
import logging

from constants import *

CHUNK_SIZE = 16 * 1024


def download_file(url, output_location):
    """
    Downloads data from a URL to the given output location.

    :param url: URL to download data from.
    :param output_location: Output location to write data to.
    """
    response = urllib2.urlopen(url)
    with open(output_location, 'wb') as fp:
        for chunk in iter(lambda: response.read(CHUNK_SIZE), ''):
            fp.write(chunk)


def scrape(download_osm=True):
    """
    Scrape the reference data and OSM data. The scraping of OSM data can be skipped with the download_osm parameters as
    it can be quite large.

    :param download_osm: True if the OSM data needs to be downloaded.
    """
    # Download Brussels GFR data
    logging.info("\t*) GFR data")
    download_file(GFR_SOURCE, GFR_LOCATION)

    if download_osm:
        # Download OSM data
        logging.info("\t*) OSM data")
        download_file(OSM_SOURCE + ','.join(map(str, BBOX)), OSM_LOCATION)
    else:
        logging.info("\tSkipping OSM data.")
