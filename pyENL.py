#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
from PyQt4 import QtCore, QtGui, uic
from utils import *
from entrada import pyENL_variable, entradaTexto
from translations import translations

# Cargar ahora interfaz desde archivo .py haciendo conversión con:
# $ pyuic4 GUI/MainWindow.ui -o GUI/MainWindow.py
# Esto para efectos de traducciones!
# NOTE
# Cada vez que se actualice MainWindow.ui se debe actualizar MainWindow.py

# form_class = uic.loadUiType("GUI/MainWindow.ui")[0]
from GUI.MainWindow import Ui_MainWindow as form_class


def quitaComentarios(eqns):
    '''
    Elimina los comentarios de la lista de ecuaciones para solucionar problema
    de que se muestren en la lista de residuos
    '''
    b = []
    for eqn in eqns:
        if '<<' not in eqn:
            b.append(eqn)
    return b


class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        # TODO Opciones del programa:
        opciones_ = configFile("config.txt")
        self.opt_method = opciones_.method
        self.lang = opciones_.lang
        self.traduccion = translations(self.lang)
        self.opt_tol = None
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
        # self.actionSalir.connect(self.salir)
        # Atajo para resolver el sistema
        self.solve_button.setShortcut('Ctrl+R')
        self.actionSalir.setShortcut('Ctrl+Q')
        # TODO En lugar de salir de una vez, crear función que verifique que
        # se han guardado los cambios y así
        self.actionSalir.triggered.connect(QtGui.qApp.quit)

        # TODO En Información incluir la máxima desviación
        # print(dir(self))
        # print(dir(self.actionSalir))
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
            # Para poder soportar variables tipo texto
            ecuaciones = variables_string(ecuaciones)
            # Quitar los comentarios de las ecuaciones:
            ecuaciones_s = quitaComentarios(ecuaciones)
            self.solucion = entradaTexto(
                ecuaciones, pyENL_timeout, varsObj=self.variables, method='hybr')
            tiempo = self.solucion[1]
            variables = self.solucion[0][0]
            residuos = self.solucion[0][1]
            solved = self.solucion[0][2]
            QtGui.QMessageBox.about(self, self.traduccion["Información"], self.traduccion['Solucionado en '] +
                                    str(tiempo) + self.traduccion[' segundos.\nMayor desviación de '] + str(max(residuos)))
            # Ahora a enfocar la última pestaña de la aplicación:
            self.tabWidget.setCurrentIndex(2)
            # Ahora a imprimir la respuesta en la tabla si solved es True
            if solved is True:
                # Imprimir
                self.solsTable.resizeColumnsToContents()
                self.solsTable.resizeRowsToContents()
                # La cantidad de filas es pues igual a la cantidad de
                # variables.
                self.solsTable.setRowCount(len(self.variables))
                # Muestra cuatro columnas, una para cada parámetro de la
                # solución.
                self.solsTable.setColumnCount(4)
                horHeaders = [self.traduccion['Variable'], self.traduccion['Solución'],
                              self.traduccion['Unidades'], self.traduccion['Comentario']]
                # Ahora para la pestaña de residuos:
                self.resTable.resizeColumnsToContents()
                self.resTable.resizeRowsToContents()
                self.resTable.setRowCount(len(self.variables))
                self.resTable.setColumnCount(2)
                resHeaders = [self.traduccion['Ecuación'],
                              self.traduccion['Residuo']]

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

                    # Residuos:
                    newitem = QtGui.QTableWidgetItem(ecuaciones_s[i])
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)
                    self.resTable.setItem(i, 0, newitem)
                    newitem = QtGui.QTableWidgetItem(str(residuos[i]))
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)
                    self.resTable.setItem(i, 1, newitem)

                self.solsTable.setHorizontalHeaderLabels(horHeaders)
                self.resTable.setHorizontalHeaderLabels(resHeaders)

            else:
                QtGui.QMessageBox.about(
                    self, self.traduccion["Problema", "No hubo convergencia a solución..."])
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
        horHeaders = [self.traduccion['Variable'], self.traduccion['Valor Inicial'],
                      self.traduccion['Inferior'], self.traduccion['Superior'], self.traduccion['Unidades'], self.traduccion['Comentario']]
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
            # Cambiar cuando las unidades estén listas
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
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
                    raise Exception(self.traduccion['El número '] + str(lowerlim) +
                                    self.traduccion[' es mayor a '] + str(upperlim) +
                                    self.traduccion[' en la variable '] + var.name)
                if (guess < lowerlim) or (guess > upperlim):
                    raise Exception(self.traduccion['El valor inicial de '] + str(var.name) +
                                    self.traduccion[' debe estar entre los dos límites.'])
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
            a_mostrar = str(cantidad_eqn) + self.traduccion[' ecuaciones / ' ] + \
                str(cantidad_var) + self.traduccion[' variables']
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
                self.traduccion['Error encontrando cantidad de variables y de ecuaciones'])


def main():
    app = QtGui.QApplication(sys.argv)
    MyWindow = MyWindowClass(None)
    MyWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
