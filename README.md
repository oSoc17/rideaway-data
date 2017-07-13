# rideaway-data
Brussels Mobility 1 - Data validation and integration into OpenStreetMap

Brussels Mobility has planned a bicycle network with routes they believe are the best for cycling around in Brussels. To make this data available to the public, it should be published on the open platform OpenStreetMap so it is available for use by cycling applications. The OpenStreetMap community does this mapping process manually to ensure a high level of quality and detail.

This tool supports the community in this mapping process of the cycling network of Brussels, by identifying missing or incomplete routes and routes with wrong metadata.

## Installation
* Install Python version 2
* Install the following dependencies with `pip`:
  - django
  - geojson
* Install the PyOsmium library from [here](https://github.com/osmcode/pyosmium)

The webtool can be started by running the Django development server or by setting up a web server like Apache or NGINX.

## Server
The server can currently be visited at http://cyclenetworks.osm.be/

## Credits
Website based on https://github.com/jbelien/oSoc-2017-Brussels-Mobility - Jonathan Beliën
