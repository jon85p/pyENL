#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
import os
import threading
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from utils import *
from entrada import pyENL_variable, entradaTexto
from translations import translations
from copy import deepcopy
import pint
from functools import partial
from zipfile import ZipFile
import tempfile
from expimp import sols2odt, sols2tex
u = pint.UnitRegistry()
u.load_definitions("units.txt")
# Cargar ahora interfaz desde archivo .py haciendo conversión con:
# $ pyuic4 GUI/MainWindow.ui -o GUI/MainWindow.py
# Icono: QtWidgets.QPixmap(_fromUtf8("GUI/imgs/icon.png")
# Esto para efectos de traducciones!
# NOTE
# Cada vez que se actualice MainWindow.ui se debe actualizar MainWindow.py

#TODO
# Cuando salga error de no convergencia, no mostrar ventana de tiempo de solución

# form_class = uic.loadUiType("GUI/MainWindow.ui")[0]
from GUI.MainWindow5 import Ui_MainWindow as form_class
from GUI.props import prop_class
from GUI.settings import Ui_Dialog as settings_class


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


class MyWindowClass(QtWidgets.QMainWindow, form_class):
    '''
    Clase para generar objeto aplicación, que contiene todas las rutinas a usar
    por la interfaz gráfica.
    Cada una de los métodos de esta clase corresponden a acciones que llevan a
    modificar parámetros de la interfaz gráfica.
    '''

    def __init__(self, parent=None):
        '''
        Inicialización del objeto ventana principal; contiene lo que se lleva a
        cabo para cargar la ventana principal.
        '''
        QtWidgets.QMainWindow.__init__(self, parent)
        # TODO Opciones del programa:
        opciones_ = configFile("config.txt")
        self.format = opciones_.format
        self.opt_method = opciones_.method
        self.lang = opciones_.lang
        self.traduccion = translations(self.lang)
        self.opt_tol = opciones_.tol
        self.timeout = opciones_.timeout
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
        # self.actionTermodinamicas.triggered.connect(self.propWindow)
        self.actionConfiguracion.triggered.connect(self.settingsWindow)
        self.actionComentario.triggered.connect(self.agregaComentario)
        self.actionSeleccionar_todo.triggered.connect(self.cajaTexto.selectAll)
        self.actionCopiar.triggered.connect(self.cajaTexto.copy)
        # actionPegar es del botón cortar y pegar_2 del botón pegar
        self.actionPegar.triggered.connect(self.cajaTexto.cut)
        self.actionPegar_2.triggered.connect(self.cajaTexto.paste)
        # Guardar archivo
        self.actionGuardar.triggered.connect(self.guardaArchivo)
        self.actionGuardar_Como.triggered.connect(self.guardaArchivoComo)
        self.actionAbrir.triggered.connect(self.abreArchivo)
        self.actionCerrar.triggered.connect(self.cierraArchivo)
        self.actionLibreOffice.triggered.connect(self.exportaODT)
        self.actionTeX.triggered.connect(self.exportaTex)
        self.output_save = None
        # Para saber si el archivo se ha modificado sin guardarse
        self.archivoModificado = False
        # self.actionSalir.connect(self.salir)
        # Atajo para resolver el sistema
        self.solve_button.setShortcut('Ctrl+R')
        self.actionSalir.setShortcut('Ctrl+Q')
        self.actionGuardar.setShortcut('Ctrl+S')
        self.actionAbrir.setShortcut('Ctrl+O')
        self.actionCerrar.setShortcut('Ctrl+W')
        self.home_dir = os.path.expanduser('~')
        # TODO En lugar de salir de una vez, crear función que verifique que
        # se han guardado los cambios y así
        self.actionSalir.triggered.connect(self.cerrarPyENL)

        # TODO En Información incluir la máxima desviación
        # print(dir(self))
        # print(dir(self.actionSalir))
        # self.tabWidget.setCurrentIndex(2)
        # self.cargarUnidades()
        
    def settingsWindow(self):
        langs = {"es": 0, "en": 1, "fr": 2, "pt": 3}
        methods = {'hybr':0, 'lm':1, 'broyden1':2, 'broyden2':3, 'anderson':4,
                   'linearmixing':5, 'diagbroyden':6, 'excitingmixing':7, 'krylov':8, 'df-sane':9}
        dialog = QtWidgets.QDialog()
        dialog.ui = settings_class()
        dialog.ui.setupUi(dialog)
        # Hay que conectar ANTES de que se cierre la ventana de diálogo
        dialog.ui.buttonBox.accepted.connect(partial(self.saveSettings, dialog.ui))
        dialog.ui.comboBox.setCurrentIndex(langs[self.lang])
        dialog.ui.format_line.setText(self.format)
        dialog.ui.method_opt.setCurrentIndex(methods[self.opt_method])
        dialog.ui.tol_line.setText(str(self.opt_tol))
        dialog.ui.timeout_spin.setValue(self.timeout)
        dialog.exec_()
        dialog.show()
        # dialog.ui.buttonBox.accepted.connect(self.pruebaprint)
        # print(dir(dialog.ui.comboBox))
    
    def saveSettings(self, ui):
        langs = {0: "es", 1: "en", 2: "fr", 3:"pt"}
        methods = {0:'hybr', 1:'lm', 2:'broyden1', 3:'broyden2', 4:'anderson',
                   5:'linearmixing', 6:'diagbroyden', 7:'excitingmixing', 8:'krylov', 9:'df-sane'}
        self.lang = langs[ui.comboBox.currentIndex()]
        self.opt_method = methods[ui.method_opt.currentIndex()]
        try:
            self.opt_tol = float(str(ui.tol_line.text()))
        except Exception as e: 
            QtWidgets.QMessageBox.about(self, "Error", "No se entiende el formato de la tolerancia")
            self.settingsWindow()
        try:
            format_str = str(ui.format_line.text())
            if '{' not in format_str or '}' not in format_str:
                raise Exception("Error")
            pi_test = format_str.format(3.141592)
            self.format = format_str
        except:
            QtWidgets.QMessageBox.about(self, "Error", "No se entiende el formato de presentación de números")
            self.settingsWindow()
        "Actualizar fichero"
        try:
            bufferr = 'lang=' + self.lang + '\n'
            bufferr = bufferr + 'method=' + self.opt_method + '\n'
            bufferr = bufferr + 'format=' + self.format + '\n'
            bufferr = bufferr + 'tol=' + str(self.opt_tol) + '\n'
            bufferr = bufferr + 'timeout=' + str(self.timeout) + '\n'
            g = open("config.txt", 'wb')
            g.write(bufferr.encode('utf-8'))
            g.close()
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error", "No se pudo almacenar la configuración en archivo 'config.txt'")
            print(str(e))
	
    def exportaTex(self):
        try:
            tex_out = QtWidgets.QFileDialog.getSaveFileName(filter="TeX (*.tex)", directory=self.home_dir)[0]
            sols2tex(self.variables, tex_out, self.cajaTexto.toPlainText().splitlines(), "John Doe")
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error", "No se pudo exportar")
            #print("ERROOOOOOR-------")
            #print(str(e))

    def exportaODT(self):
        try:
            odt_out = QtWidgets.QFileDialog.getSaveFileName(filter="Open Document Format (*.odt)", directory=self.home_dir)[0]
            sols2odt(self.variables, odt_out, self.cajaTexto.toPlainText().splitlines())
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error", "No se pudo exportar")
            #print("EROOOOOOR------------")
            # print(str(e))
        
    def agregaComentario(self):
        # QtWidgets.QMessageBox.about(self, "Prueba", "Se ha activado la alarma")
        posicion = self.cajaTexto.textCursor()
        self.cajaTexto.insertPlainText("<< >>")
        hint = self.traduccion["Acá va el comentario"]
        self.cajaTexto.moveCursor(posicion.Left, posicion.MoveAnchor)
        self.cajaTexto.moveCursor(posicion.Left, posicion.MoveAnchor)
        self.cajaTexto.insertPlainText(hint)
        for i in range(len(hint)):
            self.cajaTexto.moveCursor(posicion.Left, posicion.KeepAnchor)
        # posicion.movePosition(posicion.Left, posicion.MoveAnchor, 2)
        
    def cerrarPyENL(self, event=None):
        # QtWidgets.QMessageBox.about(self, "Advertencia", "Estoy saliendo")
        if self.archivoModificado:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("El documento se ha modificado")
            msgBox.setInformativeText("¿Desea guardar los cambios?");
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.guardaArchivo()
                QtWidgets.qApp.quit()
            elif ret == QtWidgets.QMessageBox.Discard:
                QtWidgets.qApp.quit()
            elif ret == QtWidgets.QMessageBox.Cancel:
                if event:
                    event.ignore()
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Esto no debería salir")
        else:
            QtWidgets.qApp.quit()
        
    def closeEvent(self, event):
        # Modifica la acción de salir con el botón X para que pase por la función cerrarPyENL()
        self.cerrarPyENL(event)
        
    def cierraArchivo(self):
        if self.archivoModificado:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("El documento se ha modificado")
            msgBox.setInformativeText("¿Desea guardar los cambios?");
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.guardaArchivo()
                self.limpiaTrasCierre()
            elif ret == QtWidgets.QMessageBox.Discard:
                self.limpiaTrasCierre()
            elif ret == QtWidgets.QMessageBox.Cancel:
                pass
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Esto no debería salir")
        else:
            self.limpiaTrasCierre()
        
    def limpiaTrasCierre(self):
        self.output_save = None
        self.cajaTexto.setPlainText('')
        self.setWindowTitle('pyENL')
        self.archivoModificado = False
        
    def guardaArchivoComo(self):
        try:
            self.output_save = QtWidgets.QFileDialog.getSaveFileName(filter="pyENL (*.enl)", directory=self.home_dir)[0]
        except:
            pass
        # print(self.output_save)
        if self.output_save != '':
            self.guardaArchivo()
        
    def guardaArchivo(self):
        # Guarda un archivo, ya pasándole el nombre por self.output_save
        # Si no está, guardar como
        if not self.output_save:
            self.guardaArchivoComo()
        else:
            # Guarda el archivo como tal
            # Pasar texto a fichero para comprimirlo, al igual que vars1.dat
            # Creación de carpeta temporal
            tmp_dir = tempfile.TemporaryDirectory(prefix="pyENL")
            tmp_route = str(tmp_dir).split("'")[1] + os.sep # Cuidado con el "/", comprobar en Windows
            # Crea carpetas a usar:
            folders = ['src', 'vars', 'imgs', 'tables', 'graphs']
            for folder in folders:
                os.makedirs(tmp_route + folder)
            # Ahora guarda el texto en src/eqns1.txt
            f = open(tmp_route + 'src/eqns1.txt', 'wb')
            texto = self.cajaTexto.toPlainText()
            texto_b = texto.encode('utf-8')
            f.write(texto_b)
            f.close()
            # Guardar index.txt (solamente eqns1.txt y vars1.dat
            f = open(tmp_route + 'index.txt', 'wb')
            indice = ['src/eqns1.txt\n']
            for archivo in indice:
                f.write(archivo.encode('utf-8'))
            f.close()
            # Listo por ahora para comprimir
            archivo_zip = ZipFile(self.output_save, 'w')
            for folder in folders:
                archivo_zip.write(tmp_route + folder, folder)
            for archivo in indice:
                archivo_zip.write(tmp_route + archivo[0:-1], archivo[0:-1])
            # Por último añadir el índice
            archivo_zip.write(tmp_route + 'index.txt', 'index.txt')
            archivo_zip.close()
            # Ya no hay cambios por guardar
            self.archivoModificado = False
            # Listo, ahora a borrar la carpeta temporal
            tmp_dir.cleanup()
            self.setWindowTitle("pyENL: " +  self.output_save.split('/')[-1])
    
    def abreArchivo(self):
        if self.archivoModificado:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("El documento se ha modificado")
            msgBox.setInformativeText("¿Desea guardar los cambios?");
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.guardaArchivo()
                self.abreArchivoAccion()
            elif ret == QtWidgets.QMessageBox.Discard:
                self.abreArchivoAccion()
            elif ret == QtWidgets.QMessageBox.Cancel:
                pass
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Esto no debería salir")
        else:
            self.abreArchivoAccion()
        
        
    def abreArchivoAccion(self):
        try:
            self.open_file = QtWidgets.QFileDialog.getOpenFileName(filter="pyENL (*.enl)", directory=self.home_dir)[0]
            # Open stuff
            # De momento que muestre el texto y cargue a vars1.dat
            # Generación de la carpeta temporal para la descompresión de archivos
            tmp_dir = tempfile.TemporaryDirectory(prefix="pyENL")
            tmp_route = str(tmp_dir).split("'")[1] + os.sep # Cuidado con el "/", comprobar en Windows
            zipAbrir = ZipFile(self.open_file)
            zipAbrir.extractall(tmp_route)
            zipAbrir.close()
            # Lee eqns1.txt (De momento)
            f = open(tmp_route + os.sep + 'src/eqns1.txt')
            texto_a = f.read()
            f.close()
            self.cajaTexto.setPlainText(texto_a)
            # Borrado de carpeta temporal
            tmp_dir.cleanup()
            # Esto es para que use el nombre de abierto para sobreescribir el archivo luego
            self.output_save = self.open_file
            self.setWindowTitle('pyENL: ' + self.output_save.split('/')[-1])
            self.archivoModificado = False
        except:
            QtWidgets.QMessageBox.about(self, "Error", "No se abrió un archivo")
        
    def propWindow(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = prop_class()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()
        # window = PropWindow(self)
        # if window.exec_():
         #    print("Listo!")

    def solve(self):
        '''
        Pasa el contenido de la caja de texto y de la tabla de variables al
        solver principal y calcula.
        '''
        # 10 segundos de espera
        #self.solve_button.setDisabled()
        self.actualizaInfo()
        backup_var = deepcopy(self.variables)
        try:
            pyENL_timeout = self.timeout
            ecuaciones = self.cajaTexto.toPlainText().splitlines()
            # Para poder soportar variables tipo texto
            ecuaciones = variables_string(ecuaciones)
            # Quitar los comentarios de las ecuaciones:
            self.ecuaciones_s = quitaComentarios(ecuaciones)
            self.solucion = entradaTexto(
                ecuaciones, pyENL_timeout, varsObj=self.variables, tol = self.opt_tol, method=self.opt_method)
            tiempo = self.solucion[1]
            tiempo = '{:,.4}'.format(tiempo)
            self.variables = self.solucion[0][0]
            self.residuos = self.solucion[0][1]
            solved = self.solucion[0][2]
            if not solved:
                raise Exception("No hubo convergencia a la solución")
            QtWidgets.QMessageBox.about(self, self.traduccion["Información"], self.traduccion['Solucionado en '] + \
              tiempo + self.traduccion[' segundos.\nMayor desviación de '] + str(max(self.residuos)))
            # Ahora a enfocar la última pestaña de la aplicación:
            self.tabWidget.setCurrentIndex(2)
            # Ahora a imprimir la respuesta en la tabla si solved es True
            if solved is True:
                # Imprimir
                self.imprimeSol(self.format)

            else:
                QtWidgets.QMessageBox.about(
                    self, self.traduccion["Problema", "No hubo convergencia a solución..."])
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error", str(e))
            # Restaurar acá las variables copiadas
            self.variables = backup_var
        #self.solve_button.setEnabled()
            
    def imprimeSol(self, formateo):
        '''
        Imprime en la pestaña de soluciones, las respuestas al sistema de
        ecuaciones ingresado por el usuario en la caja de texto que se usa para
        tal fin.
        '''
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

        for i, var in enumerate(self.variables):
            # Por cada variable ahora a llenar la tabla!
            # Empezamos con el nombre de variable:
            lista_items = []
            newitem = QtWidgets.QTableWidgetItem(var.name)
            # Nada se puede editar
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.solsTable.setItem(i, 0, newitem)

            # Acá se modificará el formato de la salida
            newitem = QtWidgets.QTableWidgetItem(formateo.format(var.guess))
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            # color = QtGui.QColor(255, 255, 0, 40)
            # newitem.setBackgroundColor(color)
            self.solsTable.setItem(i, 1, newitem)

            newitem = QtWidgets.QTableWidgetItem(str(var.units))
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.solsTable.setItem(i, 2, newitem)

            newitem = QtWidgets.QTableWidgetItem(var.comment)
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.solsTable.setItem(i, 3, newitem)

            # Residuos:
            newitem = QtWidgets.QTableWidgetItem(self.ecuaciones_s[i])
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.resTable.setItem(i, 0, newitem)
            newitem = QtWidgets.QTableWidgetItem(str(self.residuos[i]))
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.resTable.setItem(i, 1, newitem)

        self.solsTable.setHorizontalHeaderLabels(horHeaders)
        self.resTable.setHorizontalHeaderLabels(resHeaders)

    def actualizaVars(self):
        '''
        Al cambiar a la pestaña de variables esta debe actualizarse con las
        variables en la caja de texto.
        '''
        # print([obj.name for obj in self.variables])
        # Si se cambia justo a la segunda pestaña...
        self.variables.sort(key=lambda x: x.name.lower())
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
            newitem = QtWidgets.QTableWidgetItem(var.name)
            # color = QtWidgets.QColor(240,100,100)
            # newitem.setBackgroundColor(color)
            # Esto es para que no se pueda editar el nombre de la variable
            # desde la tabla de variables:
            newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.varsTable.setItem(i, 0, newitem)

            newitem = QtWidgets.QTableWidgetItem(str(var.guess))
            # color = QtWidgets.QColor(255, 255, 0, 40)
            # newitem.setBackgroundColor(color)
            self.varsTable.setItem(i, 1, newitem)

            newitem = QtWidgets.QTableWidgetItem(str(var.lowerlim))
            # color = QtWidgets.QColor(0, 255, 0, 40)
            # newitem.setBackgroundColor(color)
            self.varsTable.setItem(i, 2, newitem)

            newitem = QtWidgets.QTableWidgetItem(str(var.upperlim))
            # color = QtWidgets.QColor(255, 0, 0, 40)
            # newitem.setBackgroundColor(color)
            self.varsTable.setItem(i, 3, newitem)
            newitem = QtWidgets.QTableWidgetItem(str(var.units))
            # Cambiar cuando las unidades estén listas
            #TODO
            # newitem.setFlags(QtCore.Qt.ItemIsEditable)
            self.varsTable.setItem(i, 4, newitem)

            newitem = QtWidgets.QTableWidgetItem(var.comment)
            self.varsTable.setItem(i, 5, newitem)

            # for m, item in enumerate(data[key]):
            #     newitem = QtWidgets.QTableWidgetItem(item)
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
                temp_unit = eval('u.parse_units("' + units + '")')
                self.variables[i].dim = temp_unit.dimensionality
                self.variables[i].units = temp_unit
                print(self.variables[i].units)
                #if self.variables[i].units != units:
                    #self.variables[i].units = units
                    ## Se barre dimension por dimension hasta encontrar
                    ## la que contenga la unidad asignada
                    #for dim in self.dimension_list:
                        #if units in self.Dicc_dimen[dim]:
                            #self.variables[i].dim= dim
                            #break
                    #print(self.variables[i].dim)
                    
                self.variables[i].comment = comment
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error", str(e))
        self.showVarsTable()
        self.archivoModificado = True

    def actualizaInfo(self):
        '''
        Actualiza la información del label inferior y de la lista interna de
        variables con respecto al sistema de ecuaciones que el usuario está
        ingresando
        '''
        # Se modificó ya el archivo
        self.archivoModificado = True
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

    def cargarUnidades(self):
        ''' Se carga la base de datos de unidades que se encuentra en el
        archivo unidades.txt '''
        self.Dicc_dimen = {}
        self.dimension_list = []
        archivo = open("units.txt")
        texto= archivo.read()
        dimensiones= texto.split('%') #separamos el txt en una lista donde cada elemento sea la dimension
        del dimensiones[0] # el primer elemento es un espacio en blanco asi que se debe borrar
        for indicador in dimensiones:

            datos = indicador.splitlines()#convertir cada conversion en un elemento de una lista
            datos.pop(-1) #Se elimina el espacio que hay entre dimensiones en el txt
            key_dimension = datos.pop(0) #La primera linea indica la dimension asi que se remueve
            self.dimension_list.append(key_dimension)

            Dicc_unid= {}
            for equivalencia in datos: #equivalencia va a tomar cada linea que contiene la unidad y la relacion de conversion

                (key_unidad, conversion) = equivalencia.split()
                Dicc_unid[key_unidad] = conversion
            #Una vez terminado el diccionario de conversiones para una dimensión dada se agrega al Diccionario de dimensiones
            self.Dicc_dimen[key_dimension]= Dicc_unid

class PropWindow(QtWidgets.QMainWindow, prop_class):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


def main():
    '''
    Una vez se arranca el script, se llama esta función que crea una instancia
    de la aplicación con un objeto de ventana principal, la muestra y ejecuta
    el aplicativo
    '''
    app = QtWidgets.QApplication(sys.argv)
    MyWindow = MyWindowClass(None)
    MyWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
