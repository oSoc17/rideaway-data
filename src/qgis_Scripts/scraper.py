import urllib2

GFR_SOURCE = "http://data-mobility.irisnet.be/resources/icr-2016-01-01.json"
OSM_SOURCE = "http://overpass-api.de/api/map?bbox="
BBOX = [4.24124261076, 50.7631624449, 4.47975783302, 50.9133209049]

GFR_LOCATION = "../data/gfr.geojson"
OSM_LOCATION = "../data/map.osm"

CHUNK_SIZE = 16 * 1024


def download_file(url, output_location):
    response = urllib2.urlopen(url)
    with open(output_location, 'wb') as fp:
        for chunk in iter(lambda: response.read(CHUNK_SIZE), ''):
            fp.write(chunk)


# Download Brussels GFR data

download_file(GFR_SOURCE, GFR_LOCATION)

# Download OSM data

download_file(OSM_SOURCE + ','.join(map(str, BBOX)), GFR_LOCATION)
