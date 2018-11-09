#!/usr/bin/env python3

import sys
from PyQt5 import QtCore, uic, QtGui, QtWidgets
import numpy as np
from time import sleep
Qt = QtCore.Qt

try:
    sys.path.append('/home/travis/build/jon85p/pyENL')
except:
    pass

from pyENL import MyWindowClass

#app = QtWidgets.QApplication(sys.argv)
#MyWindow = MyWindowClass(None, theme)
#MyWindow.show()
#app.exec_()

def test_init(qtbot):
    widget = MyWindowClass(None, 'Default')
    qtbot.addWidget(widget)
    assert widget.infoLabel.text() == '0 equations /0 variables'
    assert widget.actionAbrir.text() == 'Open'
    QtWidgets.qApp.quit()
    
def test_reco_vars(qtbot):
    widget = MyWindowClass(None, 'Default')
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.cajaTexto, 'a = 3 + c - pi/pi + 1')
    qtbot.keyPress(widget.cajaTexto, Qt.Key_Return)
    qtbot.keyClicks(widget.cajaTexto, 'b = 2')
    widget.tabWidget.setCurrentIndex(1)
    assert len(widget.variables) == 3
    assert widget.varsTable.item(0,0).text() == 'a'
    assert widget.varsTable.item(1,0).text() == 'b'
    assert widget.varsTable.item(2,0).text() == 'c'
    widget.tabWidget.setCurrentIndex(0)
    qtbot.keyPress(widget.cajaTexto, Qt.Key_Return)
    qtbot.keyClicks(widget.cajaTexto, 'c = 2 + b')
    qtbot.mouseClick(widget.solve_button, Qt.LeftButton)
    assert np.isclose(widget.variables[0].guess, 7, atol=widget.opt_tol)
    assert np.isclose(widget.variables[1].guess, 2, atol=widget.opt_tol)
    assert np.isclose(widget.variables[2].guess, 4, atol=widget.opt_tol)
    widget.tabWidget.setCurrentIndex(0)
    widget.cajaTexto.setPlainText("")
    assert widget.cajaTexto.toPlainText() == ''
    qtbot.keyClicks(widget.cajaTexto, 'x = y^2 - 10')
    qtbot.keyPress(widget.cajaTexto, Qt.Key_Return)
    qtbot.keyClicks(widget.cajaTexto, 'y = 3*z - x')
    qtbot.keyPress(widget.cajaTexto, Qt.Key_Return)
    qtbot.keyClicks(widget.cajaTexto, 'z = 2*x + pi')
    qtbot.keyPress(widget.cajaTexto, Qt.Key_Return)
    qtbot.keyClicks(widget.cajaTexto, 'd = 4')
    widget.tabWidget.setCurrentIndex(1)
    assert len(widget.variables) == 4
    assert widget.varsTable.item(0,0).text() == 'd'
    assert widget.varsTable.item(1,0).text() == 'x'
    assert widget.varsTable.item(2,0).text() == 'y'
    assert widget.varsTable.item(3,0).text() == 'z'
    widget.tabWidget.setCurrentIndex(0)
    qtbot.mouseClick(widget.solve_button, Qt.LeftButton)
    assert np.isclose(widget.variables[0].guess, 4, atol=widget.opt_tol)
    assert np.isclose(widget.variables[1].guess, -1.294866, atol=widget.opt_tol)
    assert np.isclose(widget.variables[2].guess, 2.950446, atol=widget.opt_tol)
    assert np.isclose(widget.variables[3].guess, 0.55186, atol=widget.opt_tol)
    QtWidgets.qApp.quit()
