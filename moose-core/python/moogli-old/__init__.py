from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
from PyQt4 import QtOpenGL
import operator

# from PyQt4.QtGui import *
import _moogli
from _moogli import MorphologyViewerWidget
from _moogli import MorphologyViewer
from main import *

class DynamicMorphologyViewerWidget(_moogli.MorphologyViewerWidget):
    _timer = QtCore.QTimer()

    def set_callback(self,callback, idletime = 0):
        self.callback = callback
        self.idletime = idletime
        self._timer.timeout.connect(self.start_cycle)
        self.start_cycle()

    def start_cycle(self):
        if self.isVisible():
            if self.callback(self.get_morphology(), self):
                self._timer.start(self.idletime)
            else:
                self._timer.timeout.disconnect(self.start_cycle)
            self.update()
        else:
            self._timer.start(self.idletime)


class Morphology(_moogli.Morphology):
    def __init__(self, name = "", points = 10):
        _moogli.Morphology.__init__(self, name, 1, 50.0, points, 2)
        self._groups = {}

    def create_group(self, group_id, compartment_ids, base_value = None, peak_value = None, base_color = None, peak_color = None):
        self._groups[group_id] = (compartment_ids, base_value, peak_value, base_color, peak_color)

    def set_color(self, group_id, values):
        (compartment_ids, base_value, peak_value, base_color, peak_color) = self._groups[group_id]
        for compartment_id, value in zip(compartment_ids, values):
            normalized_value = (value - base_value) / (peak_value - base_value)
            if normalized_value > 1.0 : normalized_value = 1.0
            if normalized_value < 0.0 : normalized_value = 0.0
            if peak_color is None:
                color = base_color(normalized_value)
            else:
                color = map(operator.add, base_color, [ normalized_value * x for x in map(operator.sub, peak_color, base_color)])
            self.set_compartment_color(compartment_id, color)

    def set_diameter(self, group_id, values):
        compartment_ids = self._groups[group_id][0]
        # print zip(compartment_ids, values)
        for (compartment_id, diameter) in zip(compartment_ids, values):
            diameter = diameter * 10000000.0
            # print diameter
            # print compartment_id
            self.set_compartment_diameter(compartment_id, diameter)
        # [self.set_compartment_diameter(values[0], values[1] * 10e7) for values in zip(compartment_ids, values)]

__all__ = [ "Morphology"
          , "MorphologyViewer"
          , "MorphologyViewerWidget"
          , "DynamicMorphologyViewerWidget"
          ]
