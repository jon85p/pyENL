#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
import os
import ast
import subprocess
import threading
from PyQt5 import QtCore, uic, QtGui, QtWidgets
# import qdarkstyle
# import qdarkgraystyle
from utils import *
from entrada import pyENL_variable, entradaTexto
from translations import translations
from copy import deepcopy
from functools import partial
from zipfile import ZipFile
import tempfile
from expimp import sols2odt, sols2tex
from pint import _DEFAULT_REGISTRY as u
u.load_definitions("units.txt")
from CoolProp.CoolProp import FluidsList, get_parameter_index, get_parameter_information, is_trivial_parameter
from pyENL_fcns.functions import dicc_coolprop
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
from GUI.props import Ui_Dialog as prop_class
from GUI.settings import Ui_Dialog as settings_class


def quitaComentarios(eqns):
    '''
    Elimina los comentarios de la lista de ecuaciones para solucionar problema
    de que se muestren en la lista de residuos
    '''
    b = []
    for eqn in eqns:
        if ('<<' not in eqn) and not (eqn.replace(' ','').replace('\t', '') == ''):
            b.append(eqn)
    return b


class MyWindowClass(QtWidgets.QMainWindow, form_class):
    '''
    Clase para generar objeto aplicación, que contiene todas las rutinas a usar
    por la interfaz gráfica.
    Cada una de los métodos de esta clase corresponden a acciones que llevan a
    modificar parámetros de la interfaz gráfica.
    '''

    def __init__(self, parent, theme):
        '''
        Inicialización del objeto ventana principal; contiene lo que se lleva a
        cabo para cargar la ventana principal.
        '''
        QtWidgets.QMainWindow.__init__(self, parent)
        opciones_ = configFile("config.txt")
        self.format = opciones_.format
        self.opt_method = opciones_.method
        self.lang = opciones_.lang
        self.traduccion = translations(self.lang)
        self.opt_tol = opciones_.tol
        self.timeout = opciones_.timeout
        self.cuDir = opciones_.cuDir
        self.theme = theme
        self.sizeFont = 12
        self.fontUI = QtGui.QFont()
        if opciones_.sFontUI:
            self.fontUI.fromString(opciones_.sFontUI)
            self.sizeFont = int(opciones_.sFontUI.split(",")[1])
        self.setupUi(self)
        # self.solve_button.clicked.connect(self.prueba)
        # Dejar en una sola línea el texto
        self.cajaTexto.setLineWrapMode(0)
        # Variables en el programa:
        self.cajaTexto.setFocus()
        self.variables = []
        self.solucion = None
        self.tabWidget.currentChanged.connect(self.actualizaVars)
        self.cajaTexto.textChanged.connect(self.actualizaInfo)
        self.cajaTexto.updateRequest.connect(self.actualizarNumeroLinea)
        self.cleanVarButton.clicked.connect(self.showVarsTable)
        self.Actualizar_Button.clicked.connect(self.actualizaVarsTable)
        self.solve_button.clicked.connect(self.solve)
        self.actionTermodinamicas.triggered.connect(self.propWindow)
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
        self.actionTermodinamicas.setShortcut('Ctrl+T')
        self.actionCerrar.setShortcut('Ctrl+W')
        self.home_dir = os.path.expanduser('~')
        # TODO En lugar de salir de una vez, crear función que verifique que
        # se han guardado los cambios y así
        self.actionSalir.triggered.connect(self.cerrarPyENL)
        self.actionAyuda_NumPy.triggered.connect(partial(self.open_url,'https://docs.scipy.org/doc/numpy/reference/'))
        self.actionAyuda_CoolProp.triggered.connect(partial(self.open_url,'http://www.coolprop.org/coolprop/HighLevelAPI.html'))
        self.actionAyuda_pyENL.triggered.connect(partial(self.open_url,'https://jon85p.github.io/pyENL/help'))
        self.actionLicencias.triggered.connect(partial(self.open_url,'https://raw.githubusercontent.com/jon85p/pyENL/master/COPYING'))

        # TODO En Información incluir la máxima desviación
        # print(dir(self))
        # print(dir(self.actionSalir))
        # self.tabWidget.setCurrentIndex(2)
        # self.cargarUnidades()
        #
        # Fuente, prueba
        self.fontUI.setPointSize(self.sizeFont)
        self.cajaTexto.setFont(self.fontUI)
        # self.cajaNumeracion.setEnabled(True)
        self.cajaNumeracion.setFont(self.fontUI)
        # self.cajaNumeracion.setEnabled(False)

        # eliminar márgenes superiores:
        doc1 = self.cajaNumeracion.document()
        doc1.setDocumentMargin(0)
        doc2 = self.cajaTexto.document()
        doc2.setDocumentMargin(0)


        # ACA van las cosas que luego se activarán
        self.actionUnidades.setEnabled(False)
        self.actionPor_agregar.setEnabled(False)
        self.menuFunciones_de_usuario.setEnabled(False)
        self.actionImprimir.setEnabled(False)
        self.actionArchivo_EES.setEnabled(False)

    def settingsWindow(self):
        langs = {"es": 0, "en": 1, "fr": 2, "pt": 3}
        methods = {'hybr':0, 'lm':1, 'broyden1':2, 'broyden2':3, 'anderson':4,
                   'linearmixing':5, 'diagbroyden':6, 'excitingmixing':7, 'krylov':8, 'df-sane':9}
        temas = {"Default":0, "DarkBlack":1,"Dracula":2,"Blue":3,"BreezeDark":4, "BreezeLight":5,
                 "Gray":6,"GrayDark":7}
        dialog = QtWidgets.QDialog()
        dialog.ui = settings_class()
        dialog.ui.setupUi(dialog, self.traduccion)
        # Hay que conectar ANTES de que se cierre la ventana de diálogo
        dialog.ui.buttonBox.accepted.connect(partial(self.saveSettings, dialog.ui))
        dialog.ui.comboBox.setCurrentIndex(langs[self.lang])
        dialog.ui.temas.setCurrentIndex(temas[self.theme])
        dialog.ui.format_line.setText(self.format)
        dialog.ui.method_opt.setCurrentIndex(methods[self.opt_method])
        dialog.ui.tol_line.setText(str(self.opt_tol))
        dialog.ui.timeout_spin.setValue(self.timeout)
        dialog.ui.sizeFont.setValue(self.sizeFont)
        dialog.ui.fontText.setCurrentFont(self.fontUI)
        dialog.exec_()
        dialog.show()
        # dialog.ui.buttonBox.accepted.connect(self.pruebaprint)
        # print(dir(dialog.ui.comboBox))

    def saveSettings(self, ui):
        langs = {0: "es", 1: "en", 2: "fr", 3:"pt"}
        methods = {0:'hybr', 1:'lm', 2:'broyden1', 3:'broyden2', 4:'anderson',
                   5:'linearmixing', 6:'diagbroyden', 7:'excitingmixing', 8:'krylov', 9:'df-sane'}
        temas = {0:"Default", 1:"DarkBlack",2:"Dracula",3:"Blue",4:"BreezeDark",5:"BreezeLight",
                 6:"Gray",7:"GrayDark"}
        self.lang = langs[ui.comboBox.currentIndex()]
        self.theme = temas[ui.temas.currentIndex()]
        self.opt_method = methods[ui.method_opt.currentIndex()]
        self.timeout = ui.timeout_spin.value()
        self.fontUI = ui.fontText.currentFont()
        self.sizeFont = ui.sizeFont.value()
        self.fontUI.setPointSize(self.sizeFont)
        self.cajaTexto.setFont(self.fontUI)
        # self.cajaNumeracion.setEnabled(True)
        self.cajaNumeracion.setFont(self.fontUI)
        fontString = self.fontUI.toString()
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
            bufferr = bufferr + 'theme=' + self.theme + '\n'
            bufferr = bufferr + 'method=' + self.opt_method + '\n'
            bufferr = bufferr + 'format=' + self.format + '\n'
            bufferr = bufferr + 'tol=' + str(self.opt_tol) + '\n'
            bufferr = bufferr + 'timeout=' + str(self.timeout) + '\n'
            bufferr = bufferr + 'font=' + fontString + '\n'
            bufferr = bufferr + 'cuDir=' + str(self.cuDir) + '\n'
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
        actualizar_directorio(self.cuDir)

        if self.archivoModificado:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(self.traduccion["El documento se ha modificado"])
            msgBox.setInformativeText(self.traduccion["¿Desea guardar los cambios?"]);
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
            msgBox.setText(self.traduccion["El documento se ha modificado"])
            msgBox.setInformativeText(self.traduccion["¿Desea guardar los cambios?"]);
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
        self.variables = []
        self.solucion = []
        self.imprimeSol(self.format)

    def guardaArchivoComo(self):
        try:
            self.output_save = QtWidgets.QFileDialog.getSaveFileName(filter="pyENL (*.enl)", directory=self.cuDir)[0]
            if self.output_save!='': #si no se guardó nada se almacena un '' entonces no acutalizar el cuDir
                self.cuDir = '/'.join(self.output_save.split('/')[0:-1]) #se elimina el nombreArchivo.enl de la ruta
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
            # Crear el archivo vars/vars1.txt
            f = open(tmp_route + 'vars/vars1.txt', 'wb')
            dict_vars = {}
            for var in self.variables:
                lista_a_guardar = []
                lista_a_guardar.append('{:.50}'.format(var.guess))
                lista_a_guardar.append('{:.50}'.format(var.lowerlim))
                lista_a_guardar.append('{:.50}'.format(var.upperlim))
                lista_a_guardar.append(var.comment)
                lista_a_guardar.append(str(var.units))
                dict_vars[var.name] = lista_a_guardar
            texto_dicc = dict_vars.__repr__()
            texto_dicc_b = texto_dicc.encode('utf-8')
            f.write(texto_dicc_b)
            f.close()
            # Guardar index.txt (solamente eqns1.txt y vars1.dat
            f = open(tmp_route + 'index.txt', 'wb')
            indice = ['src/eqns1.txt\n','vars/vars1.txt\n']
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
            msgBox.setText(self.traduccion["El documento se ha modificado"])
            msgBox.setInformativeText(self.traduccion["¿Desea guardar los cambios?"]);
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


    def abreArchivoAccion(self,file2Open=None):
        self.variables = []
        self.solucion = []
        self.imprimeSol(self.format)
        try:
            if file2Open == None:
                self.open_file = QtWidgets.QFileDialog.getOpenFileName(filter="pyENL (*.enl)", directory=self.cuDir)[0]
            else:
                self.open_file =file2Open
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
            g = open(tmp_route + os.sep + 'vars/vars1.txt')
            dic_str_var = g.read()
            g.close()
            # Diccionario con las variables del archivo guardado
            dic_var = ast.literal_eval(dic_str_var)
            self.variables = []
            for var in dic_var.keys():
                lista = dic_var[var]
                var_a_lista = pyENL_variable(var)
                var_a_lista.guess = float(lista[0])
                var_a_lista.lowerlim = float(lista[1])
                var_a_lista.upperlim = float(lista[2])
                var_a_lista.comment = lista[3]
                var_a_lista.units = u.parse_units(lista[4])
                var_a_lista.dim = var_a_lista.units.dimensionality
                self.variables.append(var_a_lista)
            # Borrado de carpeta temporal
            tmp_dir.cleanup()
            # Esto es para que use el nombre de abierto para sobreescribir el archivo luego
            self.output_save = self.open_file
            self.setWindowTitle('pyENL: ' + self.output_save.split('/')[-1])
            self.archivoModificado = False
            #El archivo que se abrió esta OK then se alamacena la nueva direccion de la carpeta
            self.cuDir = '/'.join(self.output_save.split('/')[0:-1]) # se elimina el "nombreArchivo.enl" de la ruta a guardar
        except IOError: # si no se abre ningun archivo que no muestre ningun mensaje
            pass
        except:
            QtWidgets.QMessageBox.about(self, "Error", "No se abrió bien el archivo")

    def open_url(self, url):

        if "win" in sys.platform:
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                QtWidgets.QMessageBox.about(self, "Error", "Open: " + url)

    def actualizaFuncionTermo(self, dialog, items_no_rep,args_no_rep):
        '''
        Actualiza el texto a copiar para la llamada de la función termodinámica asociada
        '''
        dialog.listWidget_4.setEnabled(True)
        id_fluido = dialog.listWidget.currentRow()
        id_prop_busc = dialog.listWidget_2.currentRow()
        id_arg1 = dialog.listWidget_3.currentRow()
        id_arg2 = dialog.listWidget_4.currentRow()
        fluido = dialog.lista_fluidos[id_fluido]
        prop_busc = get_parameter_information(items_no_rep[id_prop_busc], "short")
        arg_1 = get_parameter_information(args_no_rep[id_arg1], "short")
        unit1 = get_parameter_information(args_no_rep[id_arg1], "units")
        arg_2 = get_parameter_information(args_no_rep[id_arg2], "short")
        unit2 = get_parameter_information(args_no_rep[id_arg2], "units")
        cadena = 'prop("' + prop_busc + '","'+ arg_1+ '",0['+ unit1 +'],"'+ arg_2+'",0['+ unit2 +'],"' + fluido + '")'
        if is_trivial_parameter(items_no_rep[id_prop_busc]):
            cadena = 'prop("' + prop_busc + '","' + fluido + '")'
        cadena = prop_busc + "_1 = " + cadena
        dialog.textEdit.setText(cadena)
        # Este atributo enmarca el texto a agregar que hace referencia a la llamada de
        # función termodinámica
        self.texto_termo_a_agregar = cadena

    def propWindow(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = prop_class()
        dialog.ui.setupUi(dialog, self.traduccion)
        dialog.ui.buttonBox.accepted.connect(partial(self.insertProp, dialog.ui))
        lista1 = sorted(FluidsList())
        # Lista de fluidos
        for item in lista1:
            dialog.ui.listWidget.addItem(item)
        # Lista de propiedades
        #props_l =

        lista2 = dicc_coolprop.keys()
        dialog.ui.lista_fluidos = lista1
        # Items no repetidos
        items_no_rep = []
        args_no_rep = []
        descriptions = []
        unit_items = []
        # Lista de propiedades
        for item in lista2:
            indice = get_parameter_index(item)
            if indice not in items_no_rep:
                items_no_rep.append(indice)
                # Long se refiere a la descripción larga de la propiedad
                description = get_parameter_information(indice, "long")
                descriptions.append(description)
                unidad_item = get_parameter_information(indice, "units")
                unit_items.append(unidad_item)
                # Ordenar por descripción y añadir los siguientes en ese orden
                # dialog.ui.listWidget_2.addItem(description + ' [' + unidad_item + ']')
                # Agregar parámetros de entrada
                # IO = get_parameter_information(indice, "IO")
                # if IO == 'IO':
                    # args_no_rep.append(indice)
                    # dialog.ui.listWidget_3.addItem(description + ' [' + unidad_item + ']')
                    # dialog.ui.listWidget_4.addItem(description + ' [' + unidad_item + ']')
        # Orden alfabético
        # Hay que ordenar, unit_items, descriptions, items_no_rep
        unit_items = sorted(unit_items, key= lambda x: descriptions[unit_items.index(x)])
        items_no_rep = sorted(items_no_rep, key =  lambda x: descriptions[items_no_rep.index(x)])
        descriptions = sorted(descriptions, key= lambda x:x)

        for i, item in enumerate(items_no_rep):
            description = descriptions[i]
            unidad_item = unit_items[i]
            dialog.ui.listWidget_2.addItem(description + ' [' + unidad_item + ']')
            IO = get_parameter_information(item, "IO")
            if IO == 'IO':
                args_no_rep.append(item)
                dialog.ui.listWidget_3.addItem(description + ' [' + unidad_item + ']')
                dialog.ui.listWidget_4.addItem(description + ' [' + unidad_item + ']')

        dialog.ui.listWidget.currentItemChanged.connect(partial(self.actualizaFuncionTermo,
                                                                dialog.ui,items_no_rep,args_no_rep))
        dialog.ui.listWidget_2.currentItemChanged.connect(partial(self.actualizaFuncionTermo,
                                                                dialog.ui,items_no_rep,args_no_rep))
        dialog.ui.listWidget_3.currentItemChanged.connect(partial(self.actualizaFuncionTermo,
                                                                dialog.ui,items_no_rep,args_no_rep))
        dialog.ui.listWidget_4.currentItemChanged.connect(partial(self.actualizaFuncionTermo,
                                                                dialog.ui,items_no_rep,args_no_rep))
        dialog.exec_()
        dialog.show()
        # window = PropWindow(self)
        # if window.exec_():
         #    print("Listo!")

    def insertProp(self, ui):
        # Inserta texto con llamado a función prop()
        # este texto está almacenado en self.texto_termo_a_agregar
        # print("Holaaa")
        posicion = self.cajaTexto.textCursor()
        self.cajaTexto.insertPlainText(self.texto_termo_a_agregar)

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
        # self.actualizaInfo()
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
            #newitem.setFlags(QtCore.Qt.ItemIsEditable)
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
            #Inicialmente se revisa que no la hayan embarrado repitiendo Variables
            #Ojalá se encuentre una mejor manera de hacer esto , y no con un for repetido xD
            list_names = []
            # se guarda en una lista todas los nombres de las variables de la tabla
            for i, var in enumerate(self.variables):
                list_names.append(self.varsTable.item(i,0).text())
            #si el # de elementos de ambas listas son diferentes entonces habian variables repetidas
            if len(list_names) !=len(set(list_names)): # set() elimina duplicados
                raise Exception(self.traduccion["Hay nombres de variables repetidos"])

            for i, var in enumerate(self.variables):
                # print(self.varsTable.item(i, 1).text())
                new_name = self.varsTable.item(i,0).text()
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

                # lo dentro del sig if salió de : https://stackoverflow.com/questions/13981824/how-can-i-find-a-substring-and-highlight-it-in-qtextedit
                # si se cambió el nombre de la variable se debe reemplazar en la ventana de ecuaciones
                actual_name = self.variables[i].name
                if actual_name != new_name:
                    cursor = self.cajaTexto.textCursor() #crea el objeto cursor
                    #texto a buscar en self.cajaTexto
                    toFind = "\\b"+self.variables[i].name + "\\b"   #el "\\b" para que solo busque palabras completas
                    regex = QtCore.QRegExp(toFind) #ni idea el porqué, toca crear el objeto
                    # posicion inicial (en la caja de texto se va contando cada caracter como una posicion (los saltos de linea ocupan dos posicion al ser :"\n"))
                    pos= 0
                    # index da la posicion donde está el primer elemento "toFind" en self.cajaTexto
                    index = regex.indexIn(self.cajaTexto.toPlainText(),pos)
                    while(index != -1): #si indexIn  no encuentra nada retorna un -1

                        cursor.setPosition(index)
                        cursor.movePosition(QtGui.QTextCursor.EndOfWord,1) #selecciona la variable
                        cursor.insertText(new_name) # sobreescribe lo seleccionado
                        #la siguiente linea será útil para ventana de buscar variables en el texto
                        #pos = index + regex.matchedLength()
                        #Por ahora al ir reemplazando la palabra cada vez que la encuentra no es necesario cambiar la poscion de busqueda
                        pos= 0
                        index = regex.indexIn(self.cajaTexto.toPlainText(),pos)
                    #si todo funka entonces se reemplaza el nombre en el objeto variable
                    self.variables[i].name =new_name

                # Ya que se recogieron los valores de la tabla, ahora a
                # actualizar la lista de variables del programa:
                self.variables[i].guess = guess
                self.variables[i].lowerlim = lowerlim
                self.variables[i].upperlim = upperlim
                temp_unit = eval('u.parse_units("' + units + '")')
                self.variables[i].dim = temp_unit.dimensionality
                self.variables[i].units = temp_unit
                # print(self.variables[i].units)
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

    def actualizarNumeroLinea(self):
        '''
        Actualiza cada cierto tiempo la numeración de las lineas
        de la caja de texto de ecuaciones
        '''
        #Quizá no es la mejor manera de hacerlo pero funciona! tómalo!
        #Se define los cursores de la caja de ecuaciones y el de la
        #caja de numeración
        cursor = self.cajaTexto.textCursor()
        cursor_nume = self.cajaNumeracion.textCursor()
        #se mueve a la primera linea visible de la caja de numeracion
        cursor_nume.movePosition(QtGui.QTextCursor.Start,1)
        self.cajaNumeracion.clear() #Se borra todo
        # se define el objeto bloque
        bloque = self.cajaTexto.firstVisibleBlock()
        numFirstLine = bloque.firstLineNumber() #first line visible
        numEndLine = self.cajaTexto.blockCount() #numero de la ultima linea
        #Se lee la fuente del texto
        fuente = QtGui.QFontMetrics(self.fontUI)
        width=fuente.width('0') #ancho en pixeles del caracter 0
        #numero de caracteres por linea
        nucaporli = 50//width #50 : ancho predefinido de cadaNumeracion
        #Se barre desde el start(firstline) hasta el total de lineas (endline)
        for i in range(numFirstLine,numEndLine):
            # se suma el 1 ya que la numeracion de las lineas start in 0
            cursor_nume.insertText((str(i +1)).rjust(nucaporli) )
            cursor_nume.insertBlock()

    def actualizaInfo(self):
        '''
        Actualiza la información del label inferior y de la lista interna de
        variables con respecto al sistema de ecuaciones que el usuario está
        ingresando
        '''
        #solo se actualiza si se está modificando directamente en la caja de texto
        if self.tabWidget.currentIndex() != 0: #si no esta en la pestaña de la caja de texto
            return #vemos loca
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



def main():
    '''
    Una vez se arranca el script, se llama esta función que crea una instancia
    de la aplicación con un objeto de ventana principal, la muestra y ejecuta
    el aplicativo
    '''
    theme = 'Default'
    themes = {'Default':None, 'DarkBlack':'Dark.qss', 'Blue':'Style_Blue.qss',
              'BreezeDark':'BreezeDark.qss','Dracula':'dracula.qss' ,'Gray':'Style_Gray.qss',
              'BreezeLight':'BreezeLight.qss','GrayDark':'GrayDark.qss'}
    # Leer archivo de configuración para encontrar el tema
    try:
        with open('config.txt', 'rb') as f:
            lineas = f.read().decode('utf-8').splitlines()

        for linea in lineas:
            if 'theme' in linea:
                theme = linea.split('=')[1]
    except:
        pass
    app = QtWidgets.QApplication(sys.argv)
    theme_file = themes[theme]
    if theme_file:
        f = open("themes/" + theme_file, "rb")
        qss = f.read().decode("utf-8")
        f.close()
        app.setStyleSheet(qss)

    MyWindow = MyWindowClass(None, theme)
    # Si se comienza abriendo un archivo especifico:
    if len(sys.argv) == 2 :
        file2Open = sys.argv[1]
        currentDir_open = os.path.dirname(os.path.abspath(__file__)) + os.sep + file2Open
        MyWindow.abreArchivoAccion(currentDir_open)
    MyWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
