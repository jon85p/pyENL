# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setWindowTitle("pyENL")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("GUI/imgs/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.eqnTab = QtWidgets.QWidget()
        self.eqnTab.setObjectName("eqnTab")
        self.gridLayout = QtWidgets.QGridLayout(self.eqnTab)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.cajaTexto = QtWidgets.QPlainTextEdit(self.eqnTab)
        self.cajaTexto.setObjectName("cajaTexto")
        self.gridLayout.addWidget(self.cajaTexto, 0, 1, 1, 1)
        self.solve_button = QtWidgets.QPushButton(self.eqnTab)
        self.solve_button.setObjectName("solve_button")
        self.gridLayout.addWidget(self.solve_button, 1, 1, 1, 1)
        self.cajaNumeracion = QtWidgets.QTextEdit(self.eqnTab)
        self.cajaNumeracion.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cajaNumeracion.sizePolicy().hasHeightForWidth())
        self.cajaNumeracion.setSizePolicy(sizePolicy)
        self.cajaNumeracion.setMaximumSize(QtCore.QSize(50, 16777215))
        self.cajaNumeracion.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.cajaNumeracion.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cajaNumeracion.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cajaNumeracion.setObjectName("cajaNumeracion")
        self.gridLayout.addWidget(self.cajaNumeracion, 0, 0, 1, 1)
        self.tabWidget.addTab(self.eqnTab, "")
        self.varTab = QtWidgets.QWidget()
        self.varTab.setObjectName("varTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.varTab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.varsTable = QtWidgets.QTableWidget(self.varTab)
        self.varsTable.setObjectName("varsTable")
        self.varsTable.setColumnCount(0)
        self.varsTable.setRowCount(0)
        self.verticalLayout.addWidget(self.varsTable)
        self.Actualizar_Button = QtWidgets.QPushButton(self.varTab)
        self.Actualizar_Button.setObjectName("Actualizar_Button")
        self.verticalLayout.addWidget(self.Actualizar_Button)
        self.cleanVarButton = QtWidgets.QPushButton(self.varTab)
        self.cleanVarButton.setObjectName("cleanVarButton")
        self.verticalLayout.addWidget(self.cleanVarButton)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.varTab, "")
        self.solTab = QtWidgets.QWidget()
        self.solTab.setObjectName("solTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.solTab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.solsTable = QtWidgets.QTableWidget(self.solTab)
        self.solsTable.setObjectName("solsTable")
        self.solsTable.setColumnCount(0)
        self.solsTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.solsTable)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem)
        self.info_button = QtWidgets.QPushButton(self.solTab)
        self.info_button.setObjectName("info_button")
        self.verticalLayout_3.addWidget(self.info_button)
        self.tabWidget.addTab(self.solTab, "")
        self.resTab = QtWidgets.QWidget()
        self.resTab.setObjectName("resTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.resTab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.resTable = QtWidgets.QTableWidget(self.resTab)
        self.resTable.setObjectName("resTable")
        self.resTable.setColumnCount(0)
        self.resTable.setRowCount(0)
        self.gridLayout_4.addWidget(self.resTable, 0, 0, 1, 1)
        self.tabWidget.addTab(self.resTab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel.setObjectName("infoLabel")
        self.gridLayout_2.addWidget(self.infoLabel, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuExportar_reporte = QtWidgets.QMenu(self.menuArchivo)
        self.menuExportar_reporte.setObjectName("menuExportar_reporte")
        self.menuImportar = QtWidgets.QMenu(self.menuArchivo)
        self.menuImportar.setObjectName("menuImportar")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuOpciones = QtWidgets.QMenu(self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuHerramientas = QtWidgets.QMenu(self.menubar)
        self.menuHerramientas.setObjectName("menuHerramientas")
        self.menuFunciones_Ingenieria = QtWidgets.QMenu(self.menuHerramientas)
        self.menuFunciones_Ingenieria.setObjectName("menuFunciones_Ingenieria")
        self.menuFunciones_de_usuario = QtWidgets.QMenu(self.menuHerramientas)
        self.menuFunciones_de_usuario.setObjectName("menuFunciones_de_usuario")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setWhatsThis("")
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_Como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_Como.setObjectName("actionGuardar_Como")
        self.actionCerrar = QtWidgets.QAction(MainWindow)
        self.actionCerrar.setObjectName("actionCerrar")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionComentario = QtWidgets.QAction(MainWindow)
        self.actionComentario.setObjectName("actionComentario")
        self.actionSeleccionar_todo = QtWidgets.QAction(MainWindow)
        self.actionSeleccionar_todo.setObjectName("actionSeleccionar_todo")
        self.actionDeshacer = QtWidgets.QAction(MainWindow)
        self.actionDeshacer.setObjectName("actionDeshacer")
        self.actionRehacer = QtWidgets.QAction(MainWindow)
        self.actionRehacer.setObjectName("actionRehacer")
        self.actionCopiar = QtWidgets.QAction(MainWindow)
        self.actionCopiar.setObjectName("actionCopiar")
        self.actionPegar = QtWidgets.QAction(MainWindow)
        self.actionPegar.setObjectName("actionPegar")
        self.actionPegar_2 = QtWidgets.QAction(MainWindow)
        self.actionPegar_2.setObjectName("actionPegar_2")
        self.actionAyuda_pyENL = QtWidgets.QAction(MainWindow)
        self.actionAyuda_pyENL.setObjectName("actionAyuda_pyENL")
        self.actionAyuda_NumPy = QtWidgets.QAction(MainWindow)
        self.actionAyuda_NumPy.setObjectName("actionAyuda_NumPy")
        self.actionAyuda_CoolProp = QtWidgets.QAction(MainWindow)
        self.actionAyuda_CoolProp.setObjectName("actionAyuda_CoolProp")
        self.actionSobre_pyENL = QtWidgets.QAction(MainWindow)
        self.actionSobre_pyENL.setObjectName("actionSobre_pyENL")
        self.actionLicencias = QtWidgets.QAction(MainWindow)
        self.actionLicencias.setObjectName("actionLicencias")
        self.actionTermodinamicas = QtWidgets.QAction(MainWindow)
        self.actionTermodinamicas.setObjectName("actionTermodinamicas")
        self.actionPor_agregar = QtWidgets.QAction(MainWindow)
        self.actionPor_agregar.setObjectName("actionPor_agregar")
        self.actionDisponibles = QtWidgets.QAction(MainWindow)
        self.actionDisponibles.setObjectName("actionDisponibles")
        self.actionAgregar = QtWidgets.QAction(MainWindow)
        self.actionAgregar.setObjectName("actionAgregar")
        self.actionUnidades = QtWidgets.QAction(MainWindow)
        self.actionUnidades.setObjectName("actionUnidades")
        self.actionConfiguracion = QtWidgets.QAction(MainWindow)
        self.actionConfiguracion.setObjectName("actionConfiguracion")
        self.actionImprimir = QtWidgets.QAction(MainWindow)
        self.actionImprimir.setObjectName("actionImprimir")
        self.actionLibreOffice = QtWidgets.QAction(MainWindow)
        self.actionLibreOffice.setObjectName("actionLibreOffice")
        self.actionTeX = QtWidgets.QAction(MainWindow)
        self.actionTeX.setObjectName("actionTeX")
        self.actionArchivo_EES = QtWidgets.QAction(MainWindow)
        self.actionArchivo_EES.setObjectName("actionArchivo_EES")
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
        self.menuHerramientas.addAction(self.menuFunciones_Ingenieria.menuAction())
        self.menuHerramientas.addAction(self.menuFunciones_de_usuario.menuAction())
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
        _translate = QtCore.QCoreApplication.translate
        self.solve_button.setText(_translate("MainWindow", "Resolver"))
        self.cajaNumeracion.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.eqnTab), _translate("MainWindow", "Ecuaciones"))
        self.Actualizar_Button.setText(_translate("MainWindow", "Actualizar"))
        self.cleanVarButton.setText(_translate("MainWindow", "Limpiar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.varTab), _translate("MainWindow", "Variables"))
        self.info_button.setText(_translate("MainWindow", "Información"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.solTab), _translate("MainWindow", "Soluciones"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resTab), _translate("MainWindow", "Residuos"))
        self.infoLabel.setText(_translate("MainWindow", "x Ecuaciones/y Variables"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuExportar_reporte.setTitle(_translate("MainWindow", "Exportar reporte"))
        self.menuImportar.setTitle(_translate("MainWindow", "Importar"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Opciones"))
        self.menuHerramientas.setTitle(_translate("MainWindow", "Herramientas"))
        self.menuFunciones_Ingenieria.setTitle(_translate("MainWindow", "Funciones Ingeniería"))
        self.menuFunciones_de_usuario.setTitle(_translate("MainWindow", "Funciones de usuario"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_Como.setText(_translate("MainWindow", "Guardar Como..."))
        self.actionCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))
        self.actionComentario.setText(_translate("MainWindow", "Comentario"))
        self.actionSeleccionar_todo.setText(_translate("MainWindow", "Seleccionar todo"))
        self.actionDeshacer.setText(_translate("MainWindow", "Deshacer"))
        self.actionRehacer.setText(_translate("MainWindow", "Rehacer"))
        self.actionCopiar.setText(_translate("MainWindow", "Copiar"))
        self.actionPegar.setText(_translate("MainWindow", "Cortar"))
        self.actionPegar_2.setText(_translate("MainWindow", "Pegar"))
        self.actionAyuda_pyENL.setText(_translate("MainWindow", "Ayuda pyENL"))
        self.actionAyuda_NumPy.setText(_translate("MainWindow", "Ayuda NumPy"))
        self.actionAyuda_CoolProp.setText(_translate("MainWindow", "Ayuda CoolProp"))
        self.actionSobre_pyENL.setText(_translate("MainWindow", "Sobre pyENL"))
        self.actionLicencias.setText(_translate("MainWindow", "Licencias"))
        self.actionTermodinamicas.setText(_translate("MainWindow", "Termodinámicas"))
        self.actionPor_agregar.setText(_translate("MainWindow", "Por agregar..."))
        self.actionDisponibles.setText(_translate("MainWindow", "Disponibles"))
        self.actionAgregar.setText(_translate("MainWindow", "Agregar..."))
        self.actionUnidades.setText(_translate("MainWindow", "Unidades"))
        self.actionConfiguracion.setText(_translate("MainWindow", "Configuración"))
        self.actionImprimir.setText(_translate("MainWindow", "Imprimir"))
        self.actionLibreOffice.setText(_translate("MainWindow", "Open Document Text"))
        self.actionTeX.setText(_translate("MainWindow", "Archivo LaTeX"))
        self.actionArchivo_EES.setText(_translate("MainWindow", "Archivo EES"))
