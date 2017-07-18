import urllib2
from constants import *

CHUNK_SIZE = 16 * 1024


def download_file(url, output_location):
    response = urllib2.urlopen(url)
    with open(output_location, 'wb') as fp:
        for chunk in iter(lambda: response.read(CHUNK_SIZE), ''):
            fp.write(chunk)


def scrape(download_osm=True):
    # Download Brussels GFR data
    download_file(GFR_SOURCE, GFR_LOCATION)

    if download_osm:
        # Download OSM data
        download_file(OSM_SOURCE + ','.join(map(str, BBOX)), OSM_LOCATION)
