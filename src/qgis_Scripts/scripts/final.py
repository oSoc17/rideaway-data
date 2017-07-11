from qgis.core import *
from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
from qgis.core import QgsMapLayerRegistry
# read location
OSM_INPUT_LOCATION="/Users/moustapharamachi/osm/datasources/osm.geojson"
GFR_INPUT_LOCATION="/Users/moustapharamachi/osm/datasources/gfr.geojson"

#output location
OSM_OUTPUT_LOCATION="/Users/moustapharamachi/osm/osm.geojson" #not used
GFR_OUTPUT_LOCATION="/Users/moustapharamachi/osm/GFR.geojson" #not used
GFRBUFFER_OUTPUT_LOCATION="/Users/moustapharamachi/osm/buffered_gfr.shp"


#load GFR data and osm data
osmlayer = QgsVectorLayer(OSM_INPUT_LOCATION,"osmgeojson","ogr")
gfrlayer = QgsVectorLayer(GFR_INPUT_LOCATION,"gfrgeojson","ogr")

#write output
writer = QgsVectorFileWriter.writeAsVectorFormat(osmlayer,r"Users/moustapharamachi/osm/osm.shp","utf-8",None,"ESRI Shapefile")
writer = QgsVectorFileWriter.writeAsVectorFormat(gfrlayer,r"Users/moustapharamachi/osm/gfr.shp","utf-8",None,"ESRI Shapefile")

#read shape files
osmshape = QgsVectorLayer("/Users/moustapharamachi/osm/osm.shp", "osmshape", "ogr")
gfrshape = QgsVectorLayer("/Users/moustapharamachi/osm/gfr.shp", "gfrshape", "ogr")

#buffer
QgsGeometryAnalyzer().buffer(gfrshape, GFRBUFFER_OUTPUT_LOCATION, 0.0003, False, False, -1)
gfr_bufferedshape = QgsVectorLayer(GFRBUFFER_OUTPUT_LOCATION, "gfr_buffered", "ogr")



#1 osm 2 gfr_buffered
 processing.runalg('qgis:difference',osmshape,gfr_bufferedshape,False,"/Users/moustapharamachi/osm/finaloutput.shp")
outputLayer2 = QgsVectorLayer("/Users/moustapharamachi/osm/finaloutput.shp", "gfrshape", "ogr")

#output as geojson
QgsVectorFileWriter.writeAsVectorFormat(outputLayer2,'/Users/moustapharamachi/osm/output/output.geojson', 'utf-8', None, 'GeoJSON')