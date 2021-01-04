# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setWindowTitle(_fromUtf8("pyENL"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("GUI/imgs/icon.ico")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.eqnTab = QtGui.QWidget()
        self.eqnTab.setObjectName(_fromUtf8("eqnTab"))
        self.gridLayout = QtGui.QGridLayout(self.eqnTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cajaTexto = QtGui.QPlainTextEdit(self.eqnTab)
        self.cajaTexto.setObjectName(_fromUtf8("cajaTexto"))
        self.gridLayout.addWidget(self.cajaTexto, 0, 0, 1, 1)
        self.solve_button = QtGui.QPushButton(self.eqnTab)
        self.solve_button.setObjectName(_fromUtf8("solve_button"))
        self.gridLayout.addWidget(self.solve_button, 1, 0, 1, 1)
        self.tabWidget.addTab(self.eqnTab, _fromUtf8(""))
        self.varTab = QtGui.QWidget()
        self.varTab.setObjectName(_fromUtf8("varTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.varTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.varsTable = QtGui.QTableWidget(self.varTab)
        self.varsTable.setObjectName(_fromUtf8("varsTable"))
        self.varsTable.setColumnCount(0)
        self.varsTable.setRowCount(0)
        self.verticalLayout.addWidget(self.varsTable)
        self.Actualizar_Button = QtGui.QPushButton(self.varTab)
        self.Actualizar_Button.setObjectName(_fromUtf8("Actualizar_Button"))
        self.verticalLayout.addWidget(self.Actualizar_Button)
        self.cleanVarButton = QtGui.QPushButton(self.varTab)
        self.cleanVarButton.setObjectName(_fromUtf8("cleanVarButton"))
        self.verticalLayout.addWidget(self.cleanVarButton)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.varTab, _fromUtf8(""))
        self.solTab = QtGui.QWidget()
        self.solTab.setObjectName(_fromUtf8("solTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.solTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.solsTable = QtGui.QTableWidget(self.solTab)
        self.solsTable.setObjectName(_fromUtf8("solsTable"))
        self.solsTable.setColumnCount(0)
        self.solsTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.solsTable)
        spacerItem = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem)
        self.info_button = QtGui.QPushButton(self.solTab)
        self.info_button.setObjectName(_fromUtf8("info_button"))
        self.verticalLayout_3.addWidget(self.info_button)
        self.tabWidget.addTab(self.solTab, _fromUtf8(""))
        self.resTab = QtGui.QWidget()
        self.resTab.setObjectName(_fromUtf8("resTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.resTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.resTable = QtGui.QTableWidget(self.resTab)
        self.resTable.setObjectName(_fromUtf8("resTable"))
        self.resTable.setColumnCount(0)
        self.resTable.setRowCount(0)
        self.gridLayout_4.addWidget(self.resTable, 0, 0, 1, 1)
        self.tabWidget.addTab(self.resTab, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.infoLabel = QtGui.QLabel(self.centralwidget)
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.gridLayout_2.addWidget(self.infoLabel, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArchivo = QtGui.QMenu(self.menubar)
        self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
        self.menuExportar_reporte = QtGui.QMenu(self.menuArchivo)
        self.menuExportar_reporte.setObjectName(
            _fromUtf8("menuExportar_reporte"))
        self.menuImportar = QtGui.QMenu(self.menuArchivo)
        self.menuImportar.setObjectName(_fromUtf8("menuImportar"))
        self.menuEditar = QtGui.QMenu(self.menubar)
        self.menuEditar.setObjectName(_fromUtf8("menuEditar"))
        self.menuOpciones = QtGui.QMenu(self.menubar)
        self.menuOpciones.setObjectName(_fromUtf8("menuOpciones"))
        self.menuHerramientas = QtGui.QMenu(self.menubar)
        self.menuHerramientas.setObjectName(_fromUtf8("menuHerramientas"))
        self.menuFunciones_Ingenieria = QtGui.QMenu(self.menuHerramientas)
        self.menuFunciones_Ingenieria.setObjectName(
            _fromUtf8("menuFunciones_Ingenieria"))
        self.menuFunciones_de_usuario = QtGui.QMenu(self.menuHerramientas)
        self.menuFunciones_de_usuario.setObjectName(
            _fromUtf8("menuFunciones_de_usuario"))
        self.menuAyuda = QtGui.QMenu(self.menubar)
        self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir = QtGui.QAction(MainWindow)
        self.actionAbrir.setWhatsThis(_fromUtf8(""))
        self.actionAbrir.setObjectName(_fromUtf8("actionAbrir"))
        self.actionGuardar = QtGui.QAction(MainWindow)
        self.actionGuardar.setObjectName(_fromUtf8("actionGuardar"))
        self.actionGuardar_Como = QtGui.QAction(MainWindow)
        self.actionGuardar_Como.setObjectName(_fromUtf8("actionGuardar_Como"))
        self.actionCerrar = QtGui.QAction(MainWindow)
        self.actionCerrar.setObjectName(_fromUtf8("actionCerrar"))
        self.actionSalir = QtGui.QAction(MainWindow)
        self.actionSalir.setObjectName(_fromUtf8("actionSalir"))
        self.actionComentario = QtGui.QAction(MainWindow)
        self.actionComentario.setObjectName(_fromUtf8("actionComentario"))
        self.actionSeleccionar_todo = QtGui.QAction(MainWindow)
        self.actionSeleccionar_todo.setObjectName(
            _fromUtf8("actionSeleccionar_todo"))
        self.actionDeshacer = QtGui.QAction(MainWindow)
        self.actionDeshacer.setObjectName(_fromUtf8("actionDeshacer"))
        self.actionRehacer = QtGui.QAction(MainWindow)
        self.actionRehacer.setObjectName(_fromUtf8("actionRehacer"))
        self.actionCopiar = QtGui.QAction(MainWindow)
        self.actionCopiar.setObjectName(_fromUtf8("actionCopiar"))
        self.actionPegar = QtGui.QAction(MainWindow)
        self.actionPegar.setObjectName(_fromUtf8("actionPegar"))
        self.actionPegar_2 = QtGui.QAction(MainWindow)
        self.actionPegar_2.setObjectName(_fromUtf8("actionPegar_2"))
        self.actionAyuda_pyENL = QtGui.QAction(MainWindow)
        self.actionAyuda_pyENL.setObjectName(_fromUtf8("actionAyuda_pyENL"))
        self.actionAyuda_NumPy = QtGui.QAction(MainWindow)
        self.actionAyuda_NumPy.setObjectName(_fromUtf8("actionAyuda_NumPy"))
        self.actionAyuda_CoolProp = QtGui.QAction(MainWindow)
        self.actionAyuda_CoolProp.setObjectName(
            _fromUtf8("actionAyuda_CoolProp"))
        self.actionSobre_pyENL = QtGui.QAction(MainWindow)
        self.actionSobre_pyENL.setObjectName(_fromUtf8("actionSobre_pyENL"))
        self.actionLicencias = QtGui.QAction(MainWindow)
        self.actionLicencias.setObjectName(_fromUtf8("actionLicencias"))
        self.actionTermodinamicas = QtGui.QAction(MainWindow)
        self.actionTermodinamicas.setObjectName(
            _fromUtf8("actionTermodinamicas"))
        self.actionPor_agregar = QtGui.QAction(MainWindow)
        self.actionPor_agregar.setObjectName(_fromUtf8("actionPor_agregar"))
        self.actionDisponibles = QtGui.QAction(MainWindow)
        self.actionDisponibles.setObjectName(_fromUtf8("actionDisponibles"))
        self.actionAgregar = QtGui.QAction(MainWindow)
        self.actionAgregar.setObjectName(_fromUtf8("actionAgregar"))
        self.actionUnidades = QtGui.QAction(MainWindow)
        self.actionUnidades.setObjectName(_fromUtf8("actionUnidades"))
        self.actionConfiguracion = QtGui.QAction(MainWindow)
        self.actionConfiguracion.setObjectName(
            _fromUtf8("actionConfiguracion"))
        self.actionImprimir = QtGui.QAction(MainWindow)
        self.actionImprimir.setObjectName(_fromUtf8("actionImprimir"))
        self.actionLibreOffice = QtGui.QAction(MainWindow)
        self.actionLibreOffice.setObjectName(_fromUtf8("actionLibreOffice"))
        self.actionTeX = QtGui.QAction(MainWindow)
        self.actionTeX.setObjectName(_fromUtf8("actionTeX"))
        self.actionArchivo_EES = QtGui.QAction(MainWindow)
        self.actionArchivo_EES.setObjectName(_fromUtf8("actionArchivo_EES"))
        self.menuExportar_reporte.addAction(self.actionLibreOffice)
        self.menuExportar_reporte.addAction(self.actionTeX)
        self.menuImportar.addAction(self.actionArchivo_EES)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addAction(self.actionGuardar_Como)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.menuExportar_reporte.menuAction())
        self.menuArchivo.addAction(self.menuImportar.menuAction())
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionCerrar)
        self.menuArchivo.addAction(self.actionSalir)
        self.menuEditar.addAction(self.actionComentario)
        self.menuEditar.addAction(self.actionSeleccionar_todo)
        self.menuEditar.addSeparator()
        self.menuEditar.addAction(self.actionDeshacer)
        self.menuEditar.addAction(self.actionRehacer)
        self.menuEditar.addSeparator()
        self.menuEditar.addAction(self.actionCopiar)
        self.menuEditar.addAction(self.actionPegar)
        self.menuEditar.addAction(self.actionPegar_2)
        self.menuOpciones.addAction(self.actionUnidades)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.actionConfiguracion)
        self.menuFunciones_Ingenieria.addAction(self.actionTermodinamicas)
        self.menuFunciones_Ingenieria.addAction(self.actionPor_agregar)
        self.menuFunciones_de_usuario.addAction(self.actionDisponibles)
        self.menuFunciones_de_usuario.addAction(self.actionAgregar)
        self.menuHerramientas.addAction(
            self.menuFunciones_Ingenieria.menuAction())
        self.menuHerramientas.addAction(
            self.menuFunciones_de_usuario.menuAction())
        self.menuHerramientas.addAction(self.actionImprimir)
        self.menuAyuda.addAction(self.actionAyuda_pyENL)
        self.menuAyuda.addAction(self.actionAyuda_NumPy)
        self.menuAyuda.addAction(self.actionAyuda_CoolProp)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionSobre_pyENL)
        self.menuAyuda.addAction(self.actionLicencias)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        # Texto traducido:
        self.solve_button.setText(_translate(
            "MainWindow", self.traduccion["Resolver"], None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.eqnTab), _translate(
            "MainWindow", self.traduccion["Ecuaciones"], None))
        self.Actualizar_Button.setText(_translate(
            "MainWindow", self.traduccion["Actualizar"], None))
        self.cleanVarButton.setText(_translate(
            "MainWindow", self.traduccion["Limpiar"], None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.varTab), _translate(
            "MainWindow", self.traduccion["Variables"], None))
        self.info_button.setText(_translate(
            "MainWindow", self.traduccion["Información"], None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.solTab), _translate(
            "MainWindow", self.traduccion["Soluciones"], None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resTab), _translate(
            "MainWindow", self.traduccion["Residuos"], None))
        self.infoLabel.setText(_translate("MainWindow", self.traduccion[
                               "x Ecuaciones/y Variables"], None))
        self.menuArchivo.setTitle(_translate(
            "MainWindow", self.traduccion["Archivo"], None))
        self.menuExportar_reporte.setTitle(_translate(
            "MainWindow", self.traduccion["Exportar reporte"], None))
        self.menuImportar.setTitle(_translate(
            "MainWindow", self.traduccion["Importar"], None))
        self.menuEditar.setTitle(_translate(
            "MainWindow", self.traduccion["Editar"], None))
        self.menuOpciones.setTitle(_translate(
            "MainWindow", self.traduccion["Opciones"], None))
        self.menuHerramientas.setTitle(_translate(
            "MainWindow", self.traduccion["Herramientas"], None))
        self.menuFunciones_Ingenieria.setTitle(_translate(
            "MainWindow", self.traduccion["Funciones Ingeniería"], None))
        self.menuFunciones_de_usuario.setTitle(_translate(
            "MainWindow", self.traduccion["Funciones de usuario"], None))
        self.menuAyuda.setTitle(_translate(
            "MainWindow", self.traduccion["Ayuda"], None))
        self.actionAbrir.setText(_translate(
            "MainWindow", self.traduccion["Abrir"], None))
        self.actionGuardar.setText(_translate(
            "MainWindow", self.traduccion["Guardar"], None))
        self.actionGuardar_Como.setText(_translate(
            "MainWindow", self.traduccion["Guardar Como..."], None))
        self.actionCerrar.setText(_translate(
            "MainWindow", self.traduccion["Cerrar"], None))
        self.actionSalir.setText(_translate(
            "MainWindow", self.traduccion["Salir"], None))
        self.actionComentario.setText(_translate(
            "MainWindow", self.traduccion["Comentario"], None))
        self.actionSeleccionar_todo.setText(_translate(
            "MainWindow", self.traduccion["Seleccionar todo"], None))
        self.actionDeshacer.setText(_translate(
            "MainWindow", self.traduccion["Deshacer"], None))
        self.actionRehacer.setText(_translate(
            "MainWindow", self.traduccion["Rehacer"], None))
        self.actionCopiar.setText(_translate(
            "MainWindow", self.traduccion["Copiar"], None))
        self.actionPegar.setText(_translate(
            "MainWindow", self.traduccion["Cortar"], None))
        self.actionPegar_2.setText(_translate(
            "MainWindow", self.traduccion["Pegar"], None))
        self.actionAyuda_pyENL.setText(_translate(
            "MainWindow", self.traduccion["Ayuda pyENL"], None))
        self.actionAyuda_NumPy.setText(_translate(
            "MainWindow", self.traduccion["Ayuda NumPy"], None))
        self.actionAyuda_CoolProp.setText(_translate(
            "MainWindow", self.traduccion["Ayuda CoolProp"], None))
        self.actionSobre_pyENL.setText(_translate(
            "MainWindow", self.traduccion["Sobre pyENL"], None))
        self.actionLicencias.setText(_translate(
            "MainWindow", self.traduccion["Licencias"], None))
        self.actionTermodinamicas.setText(_translate(
            "MainWindow", self.traduccion["Termodinámicas"], None))
        self.actionPor_agregar.setText(_translate(
            "MainWindow", self.traduccion["Por agregar..."], None))
        self.actionDisponibles.setText(_translate(
            "MainWindow", self.traduccion["Disponibles"], None))
        self.actionAgregar.setText(_translate(
            "MainWindow", self.traduccion["Agregar..."], None))
        self.actionUnidades.setText(_translate(
            "MainWindow", self.traduccion["Unidades"], None))
        self.actionConfiguracion.setText(_translate(
            "MainWindow", self.traduccion["Configuración"], None))
        self.actionImprimir.setText(_translate(
            "MainWindow", self.traduccion["Imprimir"], None))
        self.actionLibreOffice.setText(_translate(
            "MainWindow", self.traduccion["Open Document Text"], None))
        self.actionTeX.setText(_translate(
            "MainWindow", self.traduccion["Archivo LaTeX"], None))
        self.actionArchivo_EES.setText(_translate(
            "MainWindow", self.traduccion["Archivo EES"], None))
