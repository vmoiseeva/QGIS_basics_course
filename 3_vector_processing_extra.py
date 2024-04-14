# Task 1. Custom expression that takes 4 coordinates (xMax, xMin, yMax, yMin) as input and selects objects inside a rectangle,
# # bounded by the given extent

from qgis.core import *
from qgis.gui import *
from qgis.utils import *


@qgsfunction(args='auto', group='CustomFunctions', usesgeometry=True)
def bounding_box(x_max, x_min, y_max, y_min, feature, parent):
    extent = QgsRectangle(float(x_min), float(y_min), float(x_max), float(y_max))
    geometry = feature.geometry()

    if geometry.intersects(extent):
        return True
    else:
        return False


# Task 2. Custom expression that takes the UTM zone number as input and selects all objects in this zone

from qgis.core import *
from qgis.gui import *
from qgis.utils import *


@qgsfunction(args='auto', group='CustomFunctions', usesgeometry=True)
def inside_UTM(zone_number, feature, parent):
    geometry = feature.geometry()

    if geometry is not None:
        point = geometry.centroid().asPoint()
        zone = int((point.x() + 180) / 6) + 1

        if zone == int(zone_number):
            return True

    return False


# Task 3. Expression that selects by numeric parameter only those objects with area larger than a specified parameter

from qgis.core import *
from qgis.gui import *
from qgis.utils import *


@qgsfunction(args='auto', group='CustomFunctions', usesgeometry=True)
def select_objects_by_area_2(area_given, feature, parent):
    geometry = feature.geometry()

    if geometry is not None:
        area = geometry.area()

        if area > area_given:
            return True

    return False


# Task 4. Expression selecting objects in the northern or southern hemisphere by "North" or "South" parameters, respectively

from qgis.core import *
from qgis.gui import *
from qgis.utils import *


@qgsfunction(args='auto', group='CustomFunctions', usesgeometry=True)
def by_hemisphere(hemisphere, feature, parent):
    geometry = feature.geometry()

    if geometry is not None:
        latitude_list = [vertex.y() for vertex in geometry.vertices()]

        if (hemisphere.lower() == 'north' and all(lat >= 0 for lat in latitude_list)) or \
                (hemisphere.lower() == 'south' and all(lat < 0 for lat in latitude_list)):
            return True

    return False