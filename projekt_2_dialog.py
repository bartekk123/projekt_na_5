# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Projekt_2Dialog
                                 A QGIS plugin
 Wtyczka pozwala obliczyć różnice wysokości pomiędzy punktami oraz pole powierzchni dowolengo poligonu.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Bartłomiej Cabaj, Igor Dudek
        email                : bartekc2003@gmail.com
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

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'projekt_2_dialog_base.ui'))


class Projekt_2Dialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Projekt_2Dialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.pushButton_dh.clicked.connect(self.calculate_dh)
        
    def calculate_dh(self):
        selected_layer = self.mMapLayerComboBox.currentLayer()
        features = selected_layer.selectedFeatures()
        h_1 = float(features[0]['wysokosc'])
        h_2 = float(features[1]['wysokosc'])
        dh = h_2 - h_1 
        self.label_dh_result.setText(f'{dh}m')
