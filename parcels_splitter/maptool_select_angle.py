# -*- coding: utf-8 -*-
"""
"""
import math
from qgis.gui import QgsMapTool, QgsMapMouseEvent
from PyQt4.QtCore import Qt


class MapToolSelectAngle(QgsMapTool):
    def __init__(self, canvas, ok_callback):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.point1 = None
        self.point2 = None
        self.ok_callback = ok_callback

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.snapPoint(QgsMapMouseEvent.SnapAllLayers).x()
        y = event.snapPoint(QgsMapMouseEvent.SnapAllLayers).y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        if self.point1 is None:
            self.point1 = point
        else:
            self.point2 = point
            self.angle = self.getAngle()
            self.ok_callback(self.angle)
            self.canvas.unsetMapTool(self)

    def getAngle(self):
        return math.atan2(
            self.point2.y() - self.point1.y(),
            self.point2.x() - self.point1.x())

    def activate(self):
        self.stdCursor = self.parent().cursor()
        self.parent().setCursor(Qt.CrossCursor)

    def deactivate(self):
        self.parent().setCursor(self.stdCursor)

    def isZoomTool(self):
        return False

    def isTransient(self):
        return True

    def isEditTool(self):
        return False
