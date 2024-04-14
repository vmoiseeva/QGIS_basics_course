import sys
print(sys.executable)
import os
print(os.path.abspath(os.__file__))


# Get the project extent (QgsRectangle class object)
layer = iface.activeLayer()
ext = iface.mapCanvas().extent()
# Obtain object geometry
feature.geometry()
# Check if a point is in the extent
ext.contains(feature.geometry().asPoint())

ids = []
layer.selectByIds(ids)

# work with geoprocessing tools
from qgis import processing
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())

# tool reference
processing.algorithmHelp("native:buffer")

in_shp = '/путь/к файлу/lesson_2/layers/USA_Major_Cities.shp'
out_shp = '/путь/к файлу/lesson_2/temp/USA_Major_Cities_buff.shp'

# tool start
processing.run("native:buffer", {'INPUT': in_shp, 'DISTANCE': 0.5, 'SEGMENTS': 10, 'DISSOLVE': False, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 10, 'OUTPUT': out_shp})
iface.addVectorLayer(out_shp, "buffer", "ogr")
# or add it right away
processing.runAndLoadResults("native:buffer", {'INPUT': in_shp, 'DISTANCE': 0.5, 'SEGMENTS': 10, 'DISSOLVE': False, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 10, 'OUTPUT': out_shp})

# you can save the result of the geoprocessing tool to qgis temporary memory instead of to disc
processing.runAndLoadResults("native:buffer", {'INPUT': in_shp, 'DISTANCE': 1.0, 'SEGMENTS': 10, 'DISSOLVE': False, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 10, 'OUTPUT': 'memory:test_layer'})


# fractal dimension calculation
outputFolder = '/путь/к файлу/temp/'
cells = iface.activeLayer() # cell layer
rails = iface.activeLayer() # road layer

# all roads together
processing.runAndLoadResults("native:dissolve", {'INPUT': rails, 'OUTPUT': outputFolder + 'rails_dissolve.shp'})


# select an object by id
sFeatures = cells.getSelectedFeatures()
for sf in sFeatures:
    print(sf.geometry().boundingBox())
    ext = sf.geometry().boundingBox()
    xMax = ext.xMaximum()
    xMin = ext.xMinimum()
    yMax = ext.yMaximum()
    yMin = ext.yMinimum()
extent = str(xMin)+ ',' + str(xMax)+ ',' + str(yMin)+ ',' + str(yMax)


processing.runAndLoadResults('native:creategrid',  {'EXTENT': extent, 'HSPACING': (xMax-xMin)/1, 'VSPACING': (yMax-yMin)/1, 'CRS': cells.crs(),  'TYPE': 2, 'OUTPUT': outputFolder + 'GridCell_1.shp'})
# road trimming on the selected cell (this is done once for 1 cell)
processing.runAndLoadResults("native:clip", {'INPUT': outputFolder + 'rails_dissolve.shp', 'OVERLAY': outputFolder + 'GridCell_1.shp', 'OUTPUT': outputFolder + 'rails_clipped_cell_1.shp'})


layers = QgsProject.instance().mapLayersByName('rails_clipped_cell_1')
rails_cell_layer = layers[0]

layers = QgsProject.instance().mapLayersByName('GridCell_1')
cell_layer = layers[0]

results = {1: 0, 0.5: 0, 0.25: 0, 0.125: 0, 0.0625: 0}

# go through each cell and count how many intersected the roads.
for r in rails_cell_layer.getFeatures():
    for cell in cell_layer.getFeatures():
        if cell.geometry().intersects(r.geometry()):
            results[1] += 1

# Find the degree
from numpy import log
from scipy import optimize
fitfunc = lambda p, x: (p[0] + p[1] * x)
errfunc = lambda p, x, y: (y - fitfunc(p, x))

results_edges = [1, 0.5, 0.25, 0.125, 0.0625]
results_values = list(results.values())

logx = log(results_edges)
logy = log(results_values)

qout,success = optimize.leastsq(errfunc, [0,0], args=(logx, logy),maxfev=30000)
print(qout[1]) # required degree




# custom expressions
from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='MyNewFunctions')
def my_func(value1, value2, feature, parent):
    return value1 + value2