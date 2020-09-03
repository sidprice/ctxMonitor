##########################################################################
#
#   Symbol Selection Dialog, subclassed from QDialog
#
##########################################################################

from PyQt5 import QtWidgets, uic
import sys


class SelectSymbol(QtWidgets.QDialog):
    def __init__(self, symbols):
        super().__init__()

        self.symbols = symbols
        uic.loadUi('symbol_select_dialog.ui', self)

        self.symbols_view = self.findChild(QtWidgets.QTreeView, 'tblViewSymbols')
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'btnOk')
        self.ok_button.clicked.connect(self._okButtonPressed)
        self.cancel_button = self.findChild(QtWidgets.QPushButton, 'btnCancel')
        self.cancel_button.clicked.connect(self._cancelButtonPressed)

    def _okButtonPressed(self):
        self.result = 'OK'
        self.close()

    def _cancelButtonPressed(self):
        self.result = 'Cancel'
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectSymbol({ 'one': 'two', 'three': 'three'})
    window.exec()
    print(window.result)
    # app.exec_()
