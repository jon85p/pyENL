# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Props.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class prop_class(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(499, 428)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 0, 1, 2)
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setObjectName("listWidget_2")
        self.gridLayout.addWidget(self.listWidget_2, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 1)
        self.listWidget_3 = QtWidgets.QListWidget(Dialog)
        self.listWidget_3.setObjectName("listWidget_3")
        self.gridLayout.addWidget(self.listWidget_3, 4, 0, 1, 2)
        self.listWidget_4 = QtWidgets.QListWidget(Dialog)
        self.listWidget_4.setObjectName("listWidget_4")
        self.gridLayout.addWidget(self.listWidget_4, 4, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setEnabled(False)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 2, 2, 1)
        self.listWidget_5 = QtWidgets.QListWidget(Dialog)
        self.listWidget_5.setEnabled(False)
        self.listWidget_5.setObjectName("listWidget_5")
        self.gridLayout.addWidget(self.listWidget_5, 6, 0, 2, 2)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 7, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 1, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Propiedades fluido"))
        self.label.setText(_translate("Dialog", "Uso de propiedades de fluidos"))
        self.label_2.setText(_translate("Dialog", "Fluido:"))
        self.label_3.setText(_translate("Dialog", "Propiedad"))
        self.label_4.setText(_translate("Dialog", "Propiedad 1"))
        self.label_5.setText(_translate("Dialog", "Propiedad 2"))
        self.label_6.setText(_translate("Dialog", "Propiedad 3"))
        self.label_7.setText(_translate("Dialog", "Salida"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Props.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(499, 428)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(6, 6, 186, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(6, 30, 41, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(247, 30, 63, 18))
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(6, 54, 235, 87))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setGeometry(QtCore.QRect(247, 54, 246, 87))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(6, 147, 74, 18))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(247, 147, 74, 18))
        self.label_5.setObjectName("label_5")
        self.listWidget_3 = QtWidgets.QListWidget(Dialog)
        self.listWidget_3.setGeometry(QtCore.QRect(6, 171, 235, 88))
        self.listWidget_3.setObjectName("listWidget_3")
        self.listWidget_4 = QtWidgets.QListWidget(Dialog)
        self.listWidget_4.setGeometry(QtCore.QRect(247, 171, 246, 88))
        self.listWidget_4.setObjectName("listWidget_4")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setEnabled(False)
        self.label_6.setGeometry(QtCore.QRect(6, 265, 74, 18))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(247, 265, 37, 18))
        self.label_7.setObjectName("label_7")
        self.listWidget_5 = QtWidgets.QListWidget(Dialog)
        self.listWidget_5.setEnabled(False)
        self.listWidget_5.setGeometry(QtCore.QRect(6, 289, 235, 93))
        self.listWidget_5.setObjectName("listWidget_5")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(247, 295, 246, 87))
        self.textEdit.setObjectName("textEdit")
        self.reject = QtWidgets.QPushButton(Dialog)
        self.reject.setGeometry(QtCore.QRect(247, 388, 88, 34))
        self.reject.setObjectName("reject")
        self.accept = QtWidgets.QPushButton(Dialog)
        self.accept.setGeometry(QtCore.QRect(127, 388, 88, 34))
        self.accept.setObjectName("accept")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Propiedades fluido"))
        self.label.setText(_translate("Dialog", "Uso de propiedades de fluidos"))
        self.label_2.setText(_translate("Dialog", "Fluido:"))
        self.label_3.setText(_translate("Dialog", "Propiedad"))
        self.label_4.setText(_translate("Dialog", "Propiedad 1"))
        self.label_5.setText(_translate("Dialog", "Propiedad 2"))
        self.label_6.setText(_translate("Dialog", "Propiedad 3"))
        self.label_7.setText(_translate("Dialog", "Salida"))
        self.reject.setText(_translate("Dialog", "Cancelar"))
        self.accept.setText(_translate("Dialog", "Aceptar"))

