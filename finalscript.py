from qgis.core import *
from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
from qgis.core import QgsMapLayerRegistry
import sys

#from PyQt4.QtGui import *
app = QApplication([])
QgsApplication.setPrefixPath("/usr", True)
QgsApplication.initQgis()

# Prepare processing framework 
sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *



# read location
OSM_INPUT_LOCATION="/home/rideaway/rideaway-data/src/qgis_Scripts/datasources/osm.json"
GFR_INPUT_LOCATION="/home/rideaway/rideaway-data/src/qgis_Scripts/datasources/gfr.geojson"

#output location
OSM_OUTPUT_LOCATION="/home/rideaway/rideaway-data/src/qgis_Scripts/osm.geojson" #not used
GFR_OUTPUT_LOCATION="/home/rideaway/rideaway-data/src/qgis_Scripts/GFR.geojson" #not used
GFRBUFFER_OUTPUT_LOCATION="/home/rideaway/rideaway-data/src/qgis_Scripts/buffered_gfr.shp"


#load GFR data and osm data
osmlayer = QgsVectorLayer(OSM_INPUT_LOCATION,"osmgeojson","ogr")
gfrlayer = QgsVectorLayer(GFR_INPUT_LOCATION,"gfrgeojson","ogr")

#write output
writer = QgsVectorFileWriter.writeAsVectorFormat(osmlayer,r"/home/rideaway/rideaway-data/src/qgis_Scripts/osm.shp","utf-8",None,"ESRI Shapefile")
writer = QgsVectorFileWriter.writeAsVectorFormat(gfrlayer,r"/home/rideaway/rideaway-data/src/qgis_Scripts/gfr.shp","utf-8",None,"ESRI Shapefile")

#read shape files
osmshape = QgsVectorLayer("/home/rideaway/rideaway-data/src/qgis_Scripts/osm.shp", "osmshape", "ogr")
gfrshape = QgsVectorLayer("/home/rideaway/rideaway-data/src/qgis_Scripts/gfr.shp", "gfrshape", "ogr")

#buffer
QgsGeometryAnalyzer().buffer(gfrshape, GFRBUFFER_OUTPUT_LOCATION, 0.0003, False, False, -1)
gfr_bufferedshape = QgsVectorLayer(GFRBUFFER_OUTPUT_LOCATION, "gfr_buffered", "ogr")


# Exit applications
QgsApplication.exitQgis()
QApplication.exit()
#1 osm 2 gfr_buffered
general.runalg('qgis:difference',osmshape,gfr_bufferedshape,False,"/home/rideaway/rideaway-data/src/qgis_Scripts/finaloutput.shp")
outputLayer2 = QgsVectorLayer("/home/rideaway/rideaway-data/src/qgis_Scripts/finaloutput.shp", "gfrshape", "ogr")

#output as geojson
QgsVectorFileWriter.writeAsVectorFormat(outputLayer2,'/home/rideaway/rideaway-data/src/qgis_Scripts/output/output.geojson', 'utf-8', None, 'GeoJSON')
