from qgis.utils import iface
from qgis.analysis import QgsGeometryAnalyzer 
from qgis.core import QgsMapLayerRegistry
#mc = iface.mapCanvas() 
#layer = mc.currentLayer()

layer=None
for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
    if lyr.source() == "/Users/moustapharamachi/osm/GFR.shp":
        layer = lyr
        break

QgsGeometryAnalyzer().buffer(layer, "/Users/moustapharamachi/osm/bufferFromScript.shp", 0.0003, False, False, -1)