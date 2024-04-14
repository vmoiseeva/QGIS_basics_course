# clear combobox
self.dockwidget.myComboBox.clear()
# add items to the combobox
self.dockwidget.myComboBox.addItems(список)
# current combobox index
self.dockwidget.myComboBox.currentIndex()
# track changes of the selected combobox item
self.dockwidget.myComboBox.currentIndexChanged.connect(self.functionname)

self.dockwidget.myLabel.setText("текст")
# get a list of project layers
list(QgsProject.instance().mapLayers().values())

# track button presses
self.dockwidget.myButton.clicked.connect(self.functionname)

# track the addition of a layer to the list of project layers
QgsProject.instance().legendLayersAdded.connect(self.functionname)
# track deletion of a layer from the list of project layers
QgsProject.instance().layersRemoved.connect(self.functionname)

# include external resources like icons, images, or UI files in the QGIS plugin
pyrcc5 -o resources.py resources.qrc

# Mac
#brew install pyqt@5
# Windows
# @echo off
# call "C:\OSGeo4W64\bin\o4w_env.bat"
# call "C:\OSGeo4W64\bin\qt5_env.bat"
# call "C:\OSGeo4W64\bin\py3_env.bat"
#
# @echo on
# pyrcc5 -o resources.py resources.qrc