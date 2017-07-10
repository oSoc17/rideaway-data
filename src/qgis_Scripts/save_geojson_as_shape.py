vlayer = QgsVectorLayer("/Users/moustapharamachi/osm/GFR.geojson","mygeojson","ogr")
#QgsMapLayerRegistry.instance().addMapLayer(vlayer)
writer = QgsVectorFileWriter.writeAsVectorFormat(vlayer,r"Users/moustapharamachi/osm/GFR2.shp","utf-8",None,"ESRI Shapefile")
