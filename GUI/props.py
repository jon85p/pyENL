# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/Props.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog, traduccion):
        Dialog.setObjectName("Dialog")
        Dialog.resize(499, 428)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 0, 1, 2)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 6, 0, 1, 3)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setObjectName("listWidget_2")
        self.gridLayout.addWidget(self.listWidget_2, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 1)
        self.listWidget_3 = QtWidgets.QListWidget(Dialog)
        self.listWidget_3.setObjectName("listWidget_3")
        self.gridLayout.addWidget(self.listWidget_3, 4, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.listWidget_4 = QtWidgets.QListWidget(Dialog)
        self.listWidget_4.setEnabled(False)
        self.listWidget_4.setObjectName("listWidget_4")
        self.gridLayout.addWidget(self.listWidget_4, 4, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 2, 1, 1)

        self.retranslateUi(Dialog, traduccion)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

    def retranslateUi(self, Dialog, traduccion):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Propiedades fluido"))
        self.label.setText(_translate("Dialog", "Uso de propiedades de fluidos"))
        self.label_4.setText(_translate("Dialog", "Primer argumento"))
        self.label_3.setText(_translate("Dialog", "Propiedad buscada"))
        self.label_7.setText(_translate("Dialog", "Salida"))
        self.label_5.setText(_translate("Dialog", "Segundo Argumento"))
        self.label_2.setText(_translate("Dialog", "Fluido:"))

