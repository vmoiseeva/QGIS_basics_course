### Task 1. Add a numeric field to the USA_Major_Cities layer

layer = iface.activeLayer()
layer.name()
'USA_Major_Cities'
dir(QgsField)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
 '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
 '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
 'alias', 'comment', 'constraints', 'convertCompatible', 'defaultValueDefinition', 'displayName',
 'displayNameWithAlias', 'displayString', 'displayType', 'editorWidgetSetup', 'friendlyTypeString', 'isDateOrTime',
 'isNumeric', 'isReadOnly', 'length', 'name', 'precision', 'setAlias', 'setComment', 'setConstraints',
 'setDefaultValueDefinition', 'setEditorWidgetSetup', 'setLength', 'setName', 'setPrecision', 'setReadOnly',
 'setSplitPolicy', 'setSubType', 'setType', 'setTypeName', 'splitPolicy', 'staticMetaObject', 'subType', 'type',
 'typeName']

# create field object
myField = QgsField('NewField', QVariant.Int)
layer.startEditing()
True
layer.addAttribute(myField)
True
layer.commitChanges()
True

### Task 2. Fill the created numeric field with a value representing the difference between the values in the MALES and FEMALES columns

layer.startEditing()

for feature in layer.getFeatures():
    feature['NewField'] = feature['MALES'] - feature['FEMALES']
    layer.updateFeature(feature)

layer.commitChanges()

### Task 3. Export 3 shp files from the USA_Major_Cities file.

import os

os.mkdir('/Users/valeriiamoiseeva/Documents/Studies/PANDAN/QGIS/task_1/selected_shps')

output_folder = '/Users/valeriiamoiseeva/Documents/Studies/PANDAN/QGIS/task_1/selected_shps'

layer.selectByExpression('"NewField" > 0')
QgsVectorFileWriter.writeAsVectorFormat(layer, os.path.join(output_folder, 'more_male.shp'), "utf-8", layer.crs(),
                                        "ESRI Shapefile", onlySelected=True)
layer.removeSelection()

layer.selectByExpression('"NewField" < 0')
QgsVectorFileWriter.writeAsVectorFormat(layer, os.path.join(output_folder, 'more_female.shp'), "utf-8", layer.crs(),
                                        "ESRI Shapefile", onlySelected=True)
(0, '')
layer.removeSelection()

layer.selectByExpression('"NewField" = 0')
QgsVectorFileWriter.writeAsVectorFormat(layer, os.path.join(output_folder, 'both_the_same.shp'), "utf-8", layer.crs(),
                                        "ESRI Shapefile", onlySelected=True)
(0, '')

### Задача 4. Export only those objects from the USA_Major_Cities file to a shp file longitude > -98

# create new columns
x = QgsField('x', QVariant.Int)
y = QgsField('y', QVariant.Int)

# starting to edit the layer
layer.startEditing()

# add new columns
layer.addAttribute(x)

layer.addAttribute(y)

layer.commitChanges()

# get coordinates of objects, write them to the columns created earlier

layer.startEditing()

for feature in layer.getFeatures():
    feature['x'] = feature.geometry().asPoint().x()
    feature['y'] = feature.geometry().asPoint().y()
    layer.updateFeature(feature)

layer.commitChanges()

# select only objects that match the specified condition

layer.selectByExpression('"x" > -98')

# write the selected objects to a separate layer

QgsVectorFileWriter.writeAsVectorFormat(layer, os.path.join(output_folder, 'longitude_separation.shp'), "utf-8",
                                        layer.crs(), "ESRI Shapefile", onlySelected=True)

layer.removeSelection()