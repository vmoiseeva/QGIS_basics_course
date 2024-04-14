# custom expressions
from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='MyNewFuunctions')
def my_func(value1, value2, feature, parent):
    return value1 + value2


# to work with geometry
@qgsfunction(args='auto', group='MyNewFunctions', usesgeometry= True)

#processing.algorithmHelp("qgis:polygonize")
#processing.algorithmHelp("qgis:selectbylocation")
outputFolder = '/Users/tomsawyer/Documents/students/euro/lesson_3/temp/'

layers = QgsProject.instance().mapLayersByName('USA_roads')
line_layer = layers[0]

processing.runAndLoadResults('qgis:polygonize', {'INPUT': line_layer, 'KEEP_FIELDS': True, 'OUTPUT': outputFolder + 'polygons.shp'})

layers = QgsProject.instance().mapLayersByName('polygons')
polygons_layer = layers[0]
#удаление объектов из слоя
polygons_layer.dataProvider().deleteFeatures([f.id() for f in polygons_layer.getSelectedFeatures()])

topo_list = []

polys_diss = processing.run("native:dissolve", {'INPUT': polygons_layer, 'OUTPUT': outputFolder + 'polygons_dissolve.shp'})["OUTPUT"]
border = processing.run("native:polygonstolines", {'INPUT': polys_diss, 'OUTPUT':outputFolder + 'border.shp'})["OUTPUT"]
processing.run("qgis:selectbylocation", {'INPUT': polygons_layer, 'PREDICATE': 0, 'INTERSECT': border, 'METHOD': 0 })

topo_list.append(outputFolder + f'topoyarus_{i}.shp')

# console output
#QgsMessageLog.logMessage(str(polygons_layer.featureCount()), "console")
# merge layers into 1
processing.runAndLoadResults("qgis:mergevectorlayers", {'LAYERS': topo_list, 'CRS': polygons_layer.crs(), 'OUTPUT': outputFolder + 'topoyarusi.shp'})

# remove layers from the file system
for ty in topo_list:
    QgsVectorFileWriter.deleteShapeFile(ty)

# colour by unique values
from random import randrange
layers = QgsProject.instance().mapLayersByName('topoyarusi')
topo_layer = layers[0]

findex = topo_layer.dataProvider().fields().indexFromName('layer')
unique_values = topo_layer.uniqueValues(findex)

    # fill categories
categories = []
for unique_value in unique_values:
    # initialize the default symbol for this geometry type
    symbol = QgsSymbol.defaultSymbol(topo_layer.geometryType())

    # configure a symbol layer
    layer_style = {}
    layer_style['color'] = '%d, %d, %d' % (randrange(0, 256), randrange(0, 256), randrange(0, 256))
    layer_style['outline'] = '#000000'
    symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)

    # replace default symbol layer with the configured one
    if symbol_layer is not None:
        symbol.changeSymbolLayer(0, symbol_layer)

    # create renderer object
    category = QgsRendererCategory(unique_value, symbol, str(unique_value))
    # entry for the list of category items
    categories.append(category)

    # create renderer object
renderer = QgsCategorizedSymbolRenderer('layer', categories)

    # assign the created renderer to the layer
if renderer is not None:
    topo_layer.setRenderer(renderer)

topo_layer.triggerRepaint()
