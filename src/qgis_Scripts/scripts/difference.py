import processing
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorFileWriter
from time import sleep
from qgis.core import *
from qgis.utils import *

buffer=None
osm=None
outputLayer=None

for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
   
    if lyr.source() == "/Users/moustapharamachi/osm/osm.shp":
        osm = lyr

    if lyr.source() == "/Users/moustapharamachi/osm/bufferedGFR.shp":
        buffer = lyr
    break
       

outputLayer2 = processing.runalg('qgis:difference',osm,buffer, outputLayer,None)
QgsVectorFileWriter.writeAsVectorFormat(outputLayer,r"/Users/moustapharamachi/osm/hopen.shp","utf-8",None,"ESRI Shapefile")
QgsVectorFileWriter.writeAsVectorFormat(outputLayer2,r"/Users/moustapharamachi/osm/hopen2.shp","utf-8",None,"ESRI Shapefile")

QgsVectorFileWriter.writeAsVectorFormat(outputLayer,r"/Users/moustapharamachi/osm/hopen3.shp","utf-8",None,"ESRI Shapefile",True)
QgsVectorFileWriter.writeAsVectorFormat(outputLayer2,r"/Users/moustapharamachi/osm/hopen4.shp","utf-8",None,"ESRI Shapefile",True)


QgsGeometryAnalyzer().buffer(outputLayer, "/Users/moustapharamachi/osm/hopppper.shp", 0.0003, False, False, -1)
QgsGeometryAnalyzer().buffer(outputLayer2, "/Users/moustapharamachi/osm/hopper22.shp", 0.0003, False, False, -1)
#cLayer =iface.mapCanvas().currentLayer()
#provider = cLayer.dataProvider()
#provider = outputLayer.dataProvider()
#writer = QgsVectorFileWriter( "/Users/moustapharamachi/osm/output_path_and_name2.shp", provider.encoding(), provider.fields(),QGis.WKBPolygon, provider.crs() )


#QgsMapLayerRegistry.instance().addMapLayer(outputLayer)

#QgsVectorFileWriter.writeAsVectorFormat(outputLayer,"/Users/moustapharamachi/osm/differenceFromScript.shp","utf-8",None,"ESRI Shapefile") #does not work on mac



_writer = QgsVectorFileWriter.writeAsVectorFormat(outputLayer,r"/Users/moustapharamachi/osm/hopen2.shp","utf-8",None,"ESRI Shapefile", True)
