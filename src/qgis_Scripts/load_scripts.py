import  core
from qgis.core import *
layer = QgsVectorLayer("/Users/moustapharamachi/osm/GFRSHAPE.shp", "GFRSHAPE2", "ogr")
if not layer:
  print "Layer failed to load!"
QgsMapLayerRegistry.instance().addMapLayer(layer)

