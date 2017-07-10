import processing   # utilize the Processing Framework
 
input = '/Users/moustapharamachi/osm/GFRSHAPE.shp'  # input layer to split
field = 'icr'                      # attribute with values to use for splitting
operator = 0                        # enumerator for equals (=)
value = '2'                     # value to use for extracting to new layer
output = '/Users/moustapharamachi/osm/shapefiles/SHAPE_2.geojson'        # output layer created by extract tool
 
# run the <span class="element">Extract by attribute</span> tool
processing.runalg('qgis:extractbyattribute', input, field, operator, value, output)