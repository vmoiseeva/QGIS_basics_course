# path to the interpreter
import sys
print(sys.executable)
# package path
import os
print(os.path.abspath(os.__file__))


# get active layer
layer = iface.activeLayer()
layer.name()
layer.type()

# get objects
features = layer.getFeatures()
for f in features:
	attrs = f.attributes()
	print(attrs)
    print(f.id())

# sample management
layer.selectAll()
layer.removeSelection()
layer.selectByExpression('"Type" = \'State\'')
layer.selectByExpression('"UID" > 5')
iface.mapCanvas().setSelectionColor( QColor("green") )

selected = layer.getSelectedFeatures()
for sF in selected:
    print(sF.attributes()[5])

# writing to a vector file
import os
os.mkdir('/путь к файлу/euro/lesson_1/test')
QgsVectorFileWriter.writeAsVectorFormat(layer, '/путь к файлу/euro/lesson_1/feature_1.shp', "utf-8", layer.crs(), "ESRI Shapefile", onlySelected=True)



layer = QgsVectorLayer('/путь к файлу/euro/layers/aus_centroids.shp', "myFirstLayer", "ogr")
QgsProject.instance().addMapLayer(layer)

# get fields
for f in lyr.fields():
    print(f)

# create a new feature
layer = iface.activeLayer()
feat = QgsFeature(layer.fields())
feat.setAttribute('Name', 'New_State')
feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(143, -5)))
layer.dataProvider().addFeatures([feat])
layer.triggerRepaint()
layer.dataProvider().deleteFeatures([11]) #remove object by id

# raster manipulation
path_to_tif = os.path.join(QgsProject.instance().homePath(), "layers", "Australia_rast.tif")
iface.addRasterLayer(path_to_tif, "Austr_rasstr")
rlayer.renderer().type()
rlayer = QgsProject.instance().mapLayersByName('Australia_rast')[0]
rlayer.renderer().setOpacity(0.5)
rlayer.triggerRepaint()
rlayer.renderer().gradient()
rlayer.renderer().setGradient(1)
rlayer.triggerRepaint()


lyr = iface.activeLayer()
iface.showAttributeTable(lyr)
# layer styling
lyr.opacity()
lyr.setOpacity(0.35)
lyr.triggerRepaint()
lyr.setOpacity(1)
lyr.triggerRepaint()

lyr.renderer().type()
s = lyr.renderer().symbol()
s.setColor(QColor.fromRgb(255,0,0))
lyr.triggerRepaint()
ns = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'blue'})
lyr.renderer().setSymbol(ns)
lyr.triggerRepaint()

# create and export a map
aus_points = iface.activeLayer()
aus_polys = iface.activeLayer()


project = QgsProject.instance() # get the current qgis project
manager = project.layoutManager() # layout management
layoutName = 'MyLayout'
layouts_list = manager.printLayouts()
layout = QgsPrintLayout(project) # create layout
layout.initializeDefaults()  # create an empty list
layout.setName(layoutName)
pc = layout.pageCollection()
pc.pages()[0].setPageSize('A4', QgsLayoutItemPage.Orientation.Landscape) #Portrait
manager.addLayout(layout)

# add a map
myMap = QgsLayoutItemMap(layout)
myMap.setRect(1, 1, 1, 1)

ms = QgsMapSettings() # map properties
ms.setLayers([aus_points, aus_polys]) # layer mapping
rect = QgsRectangle(ms.fullExtent())
rect.scale(1.0)
ms.setExtent(rect)
myMap.setExtent(rect)
layout.addLayoutItem(myMap)
# map dimensions
myMap.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
myMap.attemptResize(QgsLayoutSize(200, 200, QgsUnitTypes.LayoutMillimeters))

# add a name
title = QgsLayoutItemLabel(layout)
title.setText("Карта Австралии")
title.setFont(QFont('Arial', 24))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))

# add a legend
legend = QgsLayoutItemLegend(layout)
legend.setTitle("Условные обозначения")
layerTree = QgsLayerTree()
layerTree.addLayer(aus_points)
layerTree.addLayer(aus_polys)
legend.model().setRootGroup(layerTree)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(230, 15, QgsUnitTypes.LayoutMillimeters))

# add an attribute table
table = QgsLayoutItemAttributeTable(layout)
table.setVectorLayer(aus_polys)
table.setDisplayedFields(["Name", "Type"])
frame1 = QgsLayoutFrame(layout, table)
table.addFrame(frame1)
frame1.attemptResize(QgsLayoutSize(20, 500), True)
frame1.attemptMove(QgsLayoutPoint(230,45, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(frame1)

# add scale
scalebar = QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Numeric')
scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
scalebar.setNumberOfSegments(4)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(0.5)
scalebar.setLinkedMap(myMap)
scalebar.setUnitLabel('км')
scalebar.setFont(QFont('Arial', 14))
scalebar.update()
layout.addLayoutItem(scalebar)
scalebar.attemptMove(QgsLayoutPoint(230, 180, QgsUnitTypes.LayoutMillimeters))

exporter = QgsLayoutExporter(layout)

fileName = '/путь к файлу/euro/lesson_1/outPdf1.pdf'

exporter.exportToPdf(fileName, QgsLayoutExporter.PdfExportSettings())