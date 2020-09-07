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

        self._symbols = symbols
        uic.loadUi('symbol_select_dialog.ui', self)

        self._symbols_view = self.findChild(QtWidgets.QTableView, 'tblViewSymbols')
        self._ok_button = self.findChild(QtWidgets.QPushButton, 'btnOk')
        self._ok_button.clicked.connect(self._okButtonPressed)
        self._cancel_button = self.findChild(QtWidgets.QPushButton, 'btnCancel')
        self._cancel_button.clicked.connect(self._cancelButtonPressed)

        self._displaySymbols()

    def _okButtonPressed(self):
        self.result = 'OK'
        self.close()

    def _cancelButtonPressed(self):
        self.result = 'Cancel'
        self.close()

    def _displaySymbols(self):
        row = 0
        # for name, value in self._symbols.items():
        #     item = QTableWidgetItem(name)
        #     item.setTextAlignment(Qt.AlignCenter)
        #     self.symbolTableView.setItem(row, 0, item)
        #     item = QTableWidgetItem(f'0x{value}')
        #     item.setTextAlignment(Qt.AlignCenter)
        #     self.symbolTableView.setItem(row, 1, item)
        #     row += 1
        #     self.symbolTableView.setRowCount(row+1)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectSymbol({ 'one': 'two', 'three': 'three'})
    window.exec()
    print(window.result)
    # app.exec_()
