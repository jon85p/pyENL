#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
from PyQt4 import QtCore, QtGui, uic
from utils import *
from entrada import pyENL_variable

form_class = uic.loadUiType("GUI/MainWindow.ui")[0]


class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # self.solve_button.clicked.connect(self.prueba)
        # Variables en el programa:
        self.variables = []
        self.tabWidget.currentChanged.connect(self.actualizaVars)
        self.cajaTexto.textChanged.connect(self.actualizaInfo)
        # print(dir(self.varsTable))
        # print(dir(self.tabWidget))

    def solve():
        pass

    def actualizaVars(self):
        '''
        Al cambiar a la pestaña de variables esta debe actualizarse con las
        variables en la caja de texto.
        '''
        # print([obj.name for obj in self.variables])
        # Si se cambia justo a la segunda pestaña...
        if self.tabWidget.currentIndex() == 1:
            texto = self.cajaTexto.toPlainText()
            self.varsTable.resizeColumnsToContents()
            self.varsTable.resizeRowsToContents()
            # La cantidad de filas es pues igual a la cantidad de variables.
            self.varsTable.setRowCount(len(self.variables))
            # Muestra seis columnas, una para cada parámetro de la variable.
            self.varsTable.setColumnCount(6)
            horHeaders = ['Variable', 'Valor Inicial',
                          'Inf', 'Sup', 'Unidades', 'Comentario']
            for i, var in enumerate(self.variables):
                # Por cada variable ahora a llenar la tabla!
                #Empezamos con el nombre de variable:
                lista_items = []
                newitem = QtGui.QTableWidgetItem(var.name)
                self.varsTable.setItem(i, 0, newitem)
                newitem = QtGui.QTableWidgetItem(str(var.guess))
                self.varsTable.setItem(i, 1, newitem)
                newitem = QtGui.QTableWidgetItem(str(var.lowerlim))
                self.varsTable.setItem(i, 2, newitem)
                newitem = QtGui.QTableWidgetItem(str(var.upperlim))
                self.varsTable.setItem(i, 3, newitem)
                newitem = QtGui.QTableWidgetItem(var.units)
                self.varsTable.setItem(i, 4, newitem)
                newitem = QtGui.QTableWidgetItem(var.comment)
                self.varsTable.setItem(i, 5, newitem)
                # for m, item in enumerate(data[key]):
                #     newitem = QtGui.QTableWidgetItem(item)
                #     self.varsTable.setItem(m, n, newitem)
            self.varsTable.setHorizontalHeaderLabels(horHeaders)
            # print(dir(newitem))
            # self.varsTable.show()
            # self.infoLabel.setText('Pollo')

    def actualizaInfo(self):
        '''
        Actualiza la información del label inferior y de la lista interna de
        variables con respecto al sistema de ecuaciones que el usuario está
        ingresando
        '''
        texto = self.cajaTexto.toPlainText()
        texto = texto.splitlines()
        # self.infoLabel.setText((len(texto)))
        # Ahora definir la cantidad de ecuaciones y de variables en la caja
        try:
            cantidad_eqn, var_reco = cantidadEqnVar(texto)
            cantidad_var = len(var_reco)
            a_mostrar = str(cantidad_eqn) + ' ecuaciones / ' + \
                str(cantidad_var) + ' variables'
            self.infoLabel.setText(a_mostrar)
            # Ahora actualizar la lista de variables si es necesario
            # Recordar que var_reco contiene las variables reconocidas en la
            # actualización.
            varsSelf = [obj.name for obj in self.variables]
            for varGUI in var_reco:
                if varGUI not in varsSelf:
                    # Si no está entonces agregar!
                    new_var = pyENL_variable(varGUI)
                    self.variables.append(new_var)
            # Si no está en var_reco pero está en self.variables...
            for i, varSelf in enumerate(self.variables):
                if varSelf.name not in var_reco:
                    self.variables.pop(i)
        except Exception as e:
            self.infoLabel.setText(
                'Error encontrando cantidad de variables y de ecuaciones')

app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
