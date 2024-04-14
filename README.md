# QGIS basics course

The repository contains a collection of Python scripts for basic level geospatial analysis and QGIS plugin development. The scripts were written as part of an introductory course in geospatial data processing and visualisation using QGIS and Python. 

## 1. Basic Operations

- **1_basic_operations.py** script demonstrates the basics of working with basic geospatial analysis operations. It covers various tasks such as accessing vector and raster layers, manipulating layer attributes and styles, performing selections, exporting data to shapefiles, and creating map layouts with titles, legends, attribute tables, and scale bars. The script demonstrates different practices including error handling, modularization, and documentation.
- **1_basic_operations_extra.py** script expands the list of basic operations and presents additional practice on the topic. It adds a numeric field representing population differences between genders, exports subsets based on these differences to separate shapefiles, creates and populates columns with feature coordinates, and exports features meeting longitude criteria

## 2. Geoprocessing tools for buffering, dissolving, clipping, and creating grids

- **2_geoprocessing_tools.py** script showcases core functionalities, including accessing vector layers, performing geoprocessing tasks like buffering, dissolving, and clipping, and calculating fractal dimensions for spatial datasets. Additionally, it illustrates the creation and usage of custom expressions for spatial data manipulation.

## 3. V**ector processing**

- **3_vector_processing.py** script focuses on leveraging custom expressions and working with vector layers in QGIS. The main operations include polygonization, dissolve, and selection by location. The script then merges the results into a single layer and applies a categorized symbol renderer to visualize the data based on unique values.
- **3_vector_processing_extra.py** script extends the practice of vector processing tools by introducing custom expressions for selecting objects within a specified rectangular extent, within a particular UTM zone, based on area size, and by hemisphere.

## 4. Topological levels basics

- **4_topological_levels_basics.py** script demonstrates the implementation of a custom QGIS Processing algorithm for creating topological levels from a line layer. It defines an algorithm class inheriting from QgsProcessingAlgorithm and specifies the input parameters and outputs. The algorithm processes the input layer by polygonizing it, dissolving polygons, and creating border lines. It then selects features based on their intersection with the border lines and saves them as separate shapefiles. Finally, it merges these shapefiles into a single layer and adds the resulting layer to the QGIS project.

## 5. Combobox basics

- **5_combobox_basics.py** script provides functionality for a QGIS plugin, focusing on user interface interaction and event handling. It clears, populates, and tracks changes in a combobox widget (**`myComboBox`**) and updates a label widget (**`myLabel`**) with text. Additionally, it tracks button clicks (**`myButton`**) and layer manipulation events within the QGIS project, such as layer addition and removal. The script also includes instructions for incorporating external resources like icons and images using **`pyrcc5`**. Platform-specific instructions for setting up PyQt5 on Mac and Windows environments are provided as comments.
