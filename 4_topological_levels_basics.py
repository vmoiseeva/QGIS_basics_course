from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayer,
                       QgsVectorFileWriter,
                       QgsProcessing,
                       QgsProcessingContext,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFolderDestination)
from qgis import processing
import os
import shutil


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    IN_LINES = 'INPUT_LINES'
    OUT_FOLDER = 'OUTPUT_FOLDER'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'topological_levels'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Topological levels')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Topology')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'topology'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Create topological levels from line layer")

    # добавление параметров
    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # add a layer parameter
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_LINES,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine]
            )
        )

        # add a text parameter
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUT_FOLDER,
                self.tr('Temporary folder')
            )
        )

    # code for the tool itself
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # read input parameters into variables
        in_layer = self.parameterAsString(
            parameters,
            self.IN_LINES,
            context
        )

        in_folder = self.parameterAsString(
            parameters,
            self.OUT_FOLDER,
            context
        )

        # error output in case the input parameter was not counted
        if in_layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.IN_LINES))
        if in_folder is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUT_FOLDER))

        feedback.pushInfo(in_layer)
        feedback.pushInfo(in_folder)

        # console output
        # feedback.pushInfo('CRS is {}'.format(in_layer.sourceCrs().authid()))
        feedback.pushInfo('Input layer name is {}'.format(in_layer))

        temp_dir = in_folder + '/temp'
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        polygons_layer_path = processing.run('qgis:polygonize', {'INPUT': in_layer, 'KEEP_FIELDS': True,
                                                                 'OUTPUT': temp_dir + '/polygons.shp'})["OUTPUT"]
        topo_list = []
        polygons_layer = QgsVectorLayer(polygons_layer_path, "polygons_layer", "ogr")

        total = polygons_layer.featureCount()

        i = 0
        while polygons_layer.featureCount() > 0:
            # stop the process by pressing the Cancel button
            if feedback.isCanceled():
                break
            polys_diss = \
            processing.run("native:dissolve", {'INPUT': polygons_layer, 'OUTPUT': temp_dir + '/polygons_dissolve.shp'})[
                "OUTPUT"]
            border_layer = \
            processing.run("native:polygonstolines", {'INPUT': polys_diss, 'OUTPUT': temp_dir + '/border.shp'})[
                "OUTPUT"]
            processing.run("qgis:selectbylocation",
                           {'INPUT': polygons_layer, 'PREDICATE': 0, 'INTERSECT': border_layer, 'METHOD': 0})
            QgsVectorFileWriter.writeAsVectorFormat(polygons_layer, temp_dir + f'/topoyarus_{i}.shp', "utf-8",
                                                    polygons_layer.crs(), "ESRI Shapefile", onlySelected=True)
            topo_list.append(temp_dir + f'/topoyarus_{i}.shp')
            polygons_layer.dataProvider().deleteFeatures([f.id() for f in polygons_layer.getSelectedFeatures()])
            # progress bar update
            feedback.setProgress(int(((total - polygons_layer.featureCount()) / total) * 100))
            i += 1
        topoyarusi_path = processing.run("qgis:mergevectorlayers", {'LAYERS': topo_list, 'CRS': polygons_layer.crs(),
                                                                    'OUTPUT': in_folder + '/topoyarusi.shp'})['OUTPUT']

        # folder deletion
        shutil.rmtree(temp_dir)

        topoyarusi_layer = QgsVectorLayer(topoyarusi_path, "topoyarusi", "ogr")
        context.temporaryLayerStore().addMapLayer(topoyarusi_layer)
        context.addLayerToLoadOnCompletion(
            topoyarusi_layer.id(),
            QgsProcessingContext.LayerDetails('Test',
                                              context.project(),
                                              'LAYER'))

        # result output
        return {}