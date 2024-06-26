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
from PyQt5.QtCore import Qt
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, iface

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
        self.pushButton_pole.clicked.connect(self.oblicz_pole)
        self.checkBox_m2.stateChanged.connect(self.onCheckBoxChanged)
        self.checkBox_ary.stateChanged.connect(self.onCheckBoxChanged)
        self.checkBox_ha.stateChanged.connect(self.onCheckBoxChanged)
        self.pushButton_clear.clicked.connect(self.wyczysc_wyniki)
        self.pushButton_poligon.clicked.connect(self.stworz_poligon)
        
    def calculate_dh(self):
        selected_layer = self.mMapLayerComboBox.currentLayer()
        features = selected_layer.selectedFeatures()
        if len(features) != 2:
            self.label_h_error.setText("Wybierz dokładnie dwa punkty!")
            return
        
        h_1 = float(features[0]['wysokosc'])
        h_2 = float(features[1]['wysokosc'])
        nr1 = features[0]['nr_punktu']
        nr2 = features[1]['nr_punktu']
        dh = h_2 - h_1 
        self.label_dh_result.setText(f'Roznica wysokosci miedzy punktami {nr2} a {nr1} wynosi {dh} m')
        
        
    def pole_powierzchni(self):
        selected_layer = self.mMapLayerComboBox.currentLayer()
        features = selected_layer.selectedFeatures()
        if len(features) < 3:
            self.label_pole_error.setText("Wybierz przynajmiej 3 punkty!")
            return
        n = len(features)
        suma = 0
        for i in range(n):
            xi = float(features[i]['x'])
            yi = float(features[i]['y'])
            xi_plus_1 = float(features[(i + 1) % n]['x'])
            yi_plus_1 = float(features[(i + 1) % n]['y'])
            suma += xi * yi_plus_1 - xi_plus_1 * yi

       
        pole_m2 = 0.5 * abs(suma)  # Pole w metrach kwadratowych
        pole_a = pole_m2 / 100  # Pole w arach
        pole_ha = pole_m2 / 10000  # Pole w hektarach

        return pole_m2, pole_a, pole_ha

    def oblicz_pole(self, state):
        if state == Qt.Checked:
            pole_m2, pole_a, pole_ha = self.pole_powierzchni()  
            wybrane_punkty = self.mMapLayerComboBox.currentLayer().selectedFeatures()
            punkty_str = ", ".join(f"({p['x']}, {p['y']})" for p in wybrane_punkty)
            if self.checkBox_m2.isChecked():
                self.label_pole_result.setText(f'{pole_m2} m² ({punkty_str})')
            elif self.checkBox_a.isChecked():
                self.label_pole_result.setText(f'{pole_a} akr ({punkty_str})')
            elif self.checkBox_ha.isChecked():
                self.label_pole_result.setText(f'{pole_ha} hektarów ({punkty_str})')
    def wyczysc_wyniki(self):
        self.label_dh_result_result.clear()
        self.label_pole_result.clear()
        self.checkBox_m2.setChecked(False)
        self.checkBox_a.setChecked(False)
        self.checkBox_ha.setChecked(False)
        self.label_h_error.clear()
        self.label_pole_error.clear()
        self.mMapLayerComboBox.clear()
        
        

    
    def stworz_poligon(self): 
        layer_name = "Nowy Poligon"
        crs = QgsProject.instance().crs()
        polygon_layer = QgsVectorLayer("Polygon?crs={}".format(crs.authid()), layer_name, "memory")
        QgsProject.instance().addMapLayer(polygon_layer)
    
   
        punkt1 = QgsPointXY(0, 0)  
        punkt2 = QgsPointXY(1, 0) 
        punkt3 = QgsPointXY(1, 1)  
        punkt4 = QgsPointXY(0, 1) 

        polygon_feature = QgsFeature()
        polygon_geometry = QgsGeometry.fromPolygonXY([[punkt1, punkt2, punkt3, punkt4]])
        polygon_feature.setGeometry(polygon_geometry)
        polygon_layer.dataProvider().addFeatures([polygon_feature])

        
        iface.mapCanvas().refresh()

