# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ParcelsFromPolygonDialog
                                 A QGIS plugin
 Splits a polygon into smaller polygons based on area and direction
                             -------------------
        begin                : 2018-08-05
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Nicu Tofan/Advaita SRL
        email                : advaita.brasov@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import math
from PyQt4 import QtGui, uic
from .maptool_select_angle import MapToolSelectAngle
from osgeo import ogr

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),
    'parcels_splitter_dialog_base.ui'),
    resource_suffix='')


class ParcelsFromPolygonDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, plugin, parent=None):
        """Constructor."""
        super(ParcelsFromPolygonDialog, self).__init__(parent)
        self.plugin = plugin
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.angle_picker = None

        self.pushButton_PickFirstDir.clicked.connect(self.pickFirstDirection)
        self.counter_Radians.editingFinished.connect(self.updateAngleFromRadians)
        self.counter_Degrees.editingFinished.connect(self.updateAngleFromDegrees)
        self.counter_Gradians.editingFinished.connect(self.updateAngleFromGradians)

    def updateAngleFromRadians(self):
        angle = self.counter_Radians.value()
        self.counter_Degrees.setValue(angle * 180 / math.pi)
        self.counter_Gradians.setValue(angle * 200 / math.pi)

    def updateAngleFromGradians(self):
        angle = self.counter_Gradians.value()
        self.counter_Degrees.setValue(angle * 180 / 200)
        self.counter_Radians.setValue(angle * math.pi / 200)

    def updateAngleFromDegrees(self):
        angle = self.counter_Degrees.value()
        self.counter_Gradians.setValue(angle * 200 / 180)
        self.counter_Radians.setValue(angle * math.pi / 180)

    def pickFirstDirection(self):
        """Allows  the user to pick a direction on the map. """

        def anglePicked(angle):
            self.counter_Radians.setValue(angle)

        if self.angle_picker is None:
            self.angle_picker = MapToolSelectAngle(
                self.plugin.iface.mapCanvas(), anglePicked)
        self.plugin.iface.mapCanvas().setMapTool(self.angle_picker)

    def first_angle(self):
        """ get the direction by which we will split the polygon. """
        return self.counter_Radians.value()

    def get_angle_by_selection(self, value):
        """ Converts the angle to radians from whatever the user selected. """
        if self.radioButton_Radians.isChecked():
            return value
        elif self.radioButton_Gradians.isChecked():
            return value * math.pi / 200
        elif self.radioButton_Degrees.isChecked():
            return value * math.pi / 180
        else:
            raise NotImplementedError

    def last_angle(self):
        """ Get the angle for the last parcel in radians. """
        return self.get_angle_by_selection(self.counter_PostProportional.value())

    def const_angle(self):
        """ Get the angle for the last parcel in radians. """
        return self.get_angle_by_selection(self.counter_PostConst.value())

    def advanceMode(self):
        """ What to do for parcels after first one? """
        if self.radioButton_PostKeepConstant.isChecked():
            return 'same', None
        elif self.radioButton_PostConst.isChecked():
            return 'const', self.const_angle()
        elif self.radioButton_PostProportional.isChecked():
            return 'gradual', self.last_angle()
        else:
            raise NotImplementedError

    def parcelForTheRest(self):
        """ Should we create a parcel for whatever is not covered in the list of areas? """
        return self.checkBox_ParcelForRest.isChecked()

    def areas(self):
        """ The list of areas to create parcels from. """
        try:
            result = [float(val)
                    for val in unicode(
                    self.plainTextEdit_Areas.toPlainText()).split('\n')]
            if len(result) == 0:
                self.sayError(self.plugin.tr("At least one area expected"))
        except ValueError:
            self.sayError(self.plugin.tr("Values on each line must be numeric"))
            result = []
        return result

    def sayError(self, message):
        print(message)
        raise ValueError(message)

    def targetPolygon(self):
        """ Get the polygon to split. """

        active_layer = self.plugin.iface.activeLayer()
        if active_layer is None:
            self.sayError(self.plugin.tr("No active layer"))
            return None
        sel_features = active_layer.selectedFeatures()
        if len(sel_features) == 0:
            self.sayError(self.plugin.tr("No polygon selected"))
        elif len(sel_features) > 1:
            self.sayError(self.plugin.tr("Please select a single polygon"))
        else:
            poly_geom = sel_features[0].geometry()
            if poly_geom.wkbType() != ogr.wkbPolygon:
                self.sayError(self.plugin.tr("The feature is not a polygon"))
            else:
                return poly_geom, sel_features[0]
        return None
