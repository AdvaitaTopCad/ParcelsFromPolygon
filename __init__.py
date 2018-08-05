# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ParcelsFromPolygon
                                 A QGIS plugin
 Splits a polygon into smaller polygons based on area and direction
                             -------------------
        begin                : 2018-08-05
        copyright            : (C) 2018 by Nicu Tofan/Advaita SRL
        email                : advaita.brasov@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ParcelsFromPolygon class from file ParcelsFromPolygon.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .parcels_splitter import ParcelsFromPolygon
    return ParcelsFromPolygon(iface)
