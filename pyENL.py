#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
from PyQt4 import QtCore, QtGui, uic
from utils import *
from entrada import pyENL_variable, entradaTexto

form_class = uic.loadUiType("GUI/MainWindow.ui")[0]


class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # self.solve_button.clicked.connect(self.prueba)
        # Variables en el programa:
        self.cajaTexto.setFocus()
        self.variables = []
        self.solucion = None
        self.tabWidget.currentChanged.connect(self.actualizaVars)
        self.cajaTexto.textChanged.connect(self.actualizaInfo)
        self.cleanVarButton.clicked.connect(self.showVarsTable)
        self.Actualizar_Button.clicked.connect(self.actualizaVarsTable)
        self.solve_button.clicked.connect(self.solve)
        # print(dir(self.varsTable))
        # print(dir(self.tabWidget))
        # self.tabWidget.setCurrentIndex(2)

    def solve(self):
        '''
        Pasa el contenido de la caja de texto y de la tabla de variables al
        solver principal y calcula.
        '''
        # 10 segundos de espera
        self.actualizaInfo()
        try:
            pyENL_timeout = 10
            ecuaciones = self.cajaTexto.toPlainText().splitlines()
            self.solucion = entradaTexto(
                ecuaciones, pyENL_timeout, pyENL_varsObjects=self.variables)
            tiempo = self.solucion[1]
            variables = self.solucion[0][0]
            residuos = self.solucion[0][1]
            solved = self.solucion[0][2]
            QtGui.QMessageBox.about(self, "Información", 'Solucionado en ' +
                                    str(tiempo) + ' segundos')
            # Ahora a enfocar la última pestaña de la aplicación:
            self.tabWidget.setCurrentIndex(2)
            # Ahora a imprimir la respuesta en la tabla si solved es True
            if solved is True:
                # Imprimir
                self.solsTable.resizeColumnsToContents()
                self.solsTable.resizeRowsToContents()
                # La cantidad de filas es pues igual a la cantidad de variables.
                self.solsTable.setRowCount(len(self.variables))
                # Muestra cuatro columnas, una para cada parámetro de la solución.
                self.solsTable.setColumnCount(4)
                horHeaders = ['Variable', 'Solución', 'Unidades', 'Comentario']
                for i, var in enumerate(variables):
                    # Por cada variable ahora a llenar la tabla!
                    # Empezamos con el nombre de variable:
                    lista_items = []
                    newitem = QtGui.QTableWidgetItem(var.name)
                    # Nada se puede editar
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)
                    self.solsTable.setItem(i, 0, newitem)

                    newitem = QtGui.QTableWidgetItem(str(var.guess))
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)
                    color = QtGui.QColor(255, 255, 0, 40)
                    newitem.setBackgroundColor(color)
                    self.solsTable.setItem(i, 1, newitem)

                    newitem = QtGui.QTableWidgetItem(var.units)
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)
                    self.solsTable.setItem(i, 2, newitem)

                    newitem = QtGui.QTableWidgetItem(var.comment)
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)
                    self.solsTable.setItem(i, 3, newitem)

                self.solsTable.setHorizontalHeaderLabels(horHeaders)
                pass
            else:
                QtGui.QMessageBox.about(
                    self, "Problema", "No hubo convergencia a solución...")
        except Exception as e:
            QtGui.QMessageBox.about(self, "Error", str(e))

    def actualizaVars(self):
        '''
        Al cambiar a la pestaña de variables esta debe actualizarse con las
        variables en la caja de texto.
        '''
        # print([obj.name for obj in self.variables])
        # Si se cambia justo a la segunda pestaña...
        self.actualizaInfo()
        if self.tabWidget.currentIndex() == 1:
            self.showVarsTable()

    def showVarsTable(self):
        '''
        Imprime en tabla las variables del programa.
        '''
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
            # Empezamos con el nombre de variable:
            lista_items = []
            newitem = QtGui.QTableWidgetItem(var.name)
            # color = QtGui.QColor(240,100,100)
            # newitem.setBackgroundColor(color)
            # Esto es para que no se pueda editar el nombre de la variable
            # desde la tabla de variables:
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.varsTable.setItem(i, 0, newitem)

            newitem = QtGui.QTableWidgetItem(str(var.guess))
            color = QtGui.QColor(255, 255, 0, 40)
            newitem.setBackgroundColor(color)
            self.varsTable.setItem(i, 1, newitem)

            newitem = QtGui.QTableWidgetItem(str(var.lowerlim))
            color = QtGui.QColor(0, 255, 0, 40)
            newitem.setBackgroundColor(color)
            self.varsTable.setItem(i, 2, newitem)

            newitem = QtGui.QTableWidgetItem(str(var.upperlim))
            color = QtGui.QColor(255, 0, 0, 40)
            newitem.setBackgroundColor(color)
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

    def actualizaVarsTable(self):
        '''
        Al darle al botón de Actualizar en la pestaña de variables, actualizar
        los parámetros de las variables de programa.
        '''
        try:
            for i, var in enumerate(self.variables):
                # print(self.varsTable.item(i, 1).text())
                guess = float(self.varsTable.item(i, 1).text())
                lowerlim = float(self.varsTable.item(i, 2).text())
                upperlim = float(self.varsTable.item(i, 3).text())
                units = self.varsTable.item(i, 4).text()
                comment = self.varsTable.item(i, 5).text()
                if lowerlim >= upperlim:
                    raise Exception('El número ' + str(lowerlim) +
                                    ' es mayor a ' + str(upperlim) +
                                    ' en la variable ' + var.name)
                if (guess < lowerlim) or (guess > upperlim):
                    raise Exception('El valor inicial de ' + str(var.name) +
                                    ' debe estar entre los dos límites.')
                # Ya que se recogieron los valores de la tabla, ahora a
                # actualizar la lista de variables del programa:
                self.variables[i].guess = guess
                self.variables[i].lowerlim = lowerlim
                self.variables[i].upperlim = upperlim
                self.variables[i].units = units
                self.variables[i].comment = comment
        except Exception as e:
            QtGui.QMessageBox.about(self, "Error", str(e))
        self.showVarsTable()

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
