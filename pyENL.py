#!/usr/bin/env python3

'''
Programa principal que abre la interfaz gráfica de pyENL
'''
import sys
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("GUI/MainWindow.ui")[0]

class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def solve():
        pass

app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
