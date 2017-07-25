# rideaway-data
Brussels Mobility 1 - Data validation and integration into OpenStreetMap

Brussels have has developed region wide cycling network. Known as the ICR (Itinéraires Cyclables Régionaux) in French or the GFR (Gewestelijke Fietsroutes) in Dutch, the network aims for fluid and safe journeys spanning all 19 communes of the region. The cycling infrastructure is represented by is open and online map data. Individual routes has information about their corresponding route colour and name. 

This is a useful reference for OSM mappers, however if one was to compare the completeness and correctness of OSM, a manual comparison will be too tedious. To ease the process of OSM editing in relation to a reference map of the cycling network, a webtool was developed that compares the Brussels route data with that of OSM. The result provides a map that continously updates itself compared to OSM and shows a map of potential missing or incomplete routes and metadata on tags. 

## Installation
* Install Python version 2
* Install the following dependencies with `pip`:
  - django:  `pip install django`
  - geojson: `pip install geojson`
  - pyproj: `pip install pyproj`
* Install the PyOsmium library from [here](https://github.com/osmcode/pyosmium)
* Run the `install.sh` script or install following software manually:
  - flatpak: `apt install flatpak`
  - mono-devel: `apt install mono-devel`
  - monodevelop: `flatpak install --user --from https://download.mono-project.com/repo/monodevelop.flatpakref`

Make a settings_local.py file containing (sensitive) information to run the Django server. The settings_local.template file can be used as an example.

The webtool can be started by running the Django development server or by setting up a web server like Apache or NGINX. To run the script periodically, a cron job should be set-up to run `main.py` (e.g. every 15 minutes).

## Server
The server can currently be visited at https://cyclenetworks.osm.be/

## Credits
Website based on https://github.com/jbelien/oSoc-2017-Brussels-Mobility - Jonathan Beliën
