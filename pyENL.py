#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
from PyQt4 import QtCore, QtGui, uic
from utils import *

form_class = uic.loadUiType("GUI/MainWindow.ui")[0]


class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # self.solve_button.clicked.connect(self.prueba)
        self.tabWidget.currentChanged.connect(self.actualizaVars)
        self.cajaTexto.textChanged.connect(self.actualizaInfo)
        # print(dir(self.infoLabel))
        # print(dir(self.tabWidget))

    def solve():
        pass

    def actualizaVars(self):
        '''
        Al cambiar a la pestaña de variables esta debe actualizarse con las
        variables en la caja de texto.
        '''
        if self.tabWidget.currentIndex() == 1:
            texto = self.cajaTexto.toPlainText()
            # self.infoLabel.setText('Pollo')

    def actualizaInfo(self):
        '''
        Actualiza la información del label inferior con respecto al sistema de
        ecuaciones que el usuario está ingresando
        '''
        texto = self.cajaTexto.toPlainText()
        texto = texto.splitlines()
        # self.infoLabel.setText((len(texto)))
        # Ahora definir la cantidad de ecuaciones y de variables en la caja
        try:
            cantidad_eqn, cantidad_var = cantidadEqnVar(texto)
            a_mostrar = str(cantidad_eqn) + ' ecuaciones / ' + \
                str(cantidad_var) + ' variables'
            self.infoLabel.setText(a_mostrar)
        except Exception as e:
            self.infoLabel.setText(
                'Error encontrando cantidad de variables y de ecuaciones')

app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
