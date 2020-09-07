##########################################################################
#
#   Symbol Selection Dialog, subclassed from QDialog
#
##########################################################################

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtWidgets import QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget
import sys


class SelectSymbol(QtWidgets.QDialog):
    def __init__(self, symbols):
        super().__init__()

        self._symbols = symbols

        self.setWindowTitle('Select Symbol')
        #
        #   Create the controls
        #
        self._symbols_view = QTableWidget()
        self._ok_button = QPushButton('OK')
        self._ok_button.clicked.connect(self._okButtonPressed)
        self._cancel_button = QPushButton('Cancel')
        self._cancel_button.clicked.connect(self._cancelButtonPressed)
        #
        #   Layout the controls
        #
        vBox = QVBoxLayout()
        hBox = QHBoxLayout()

        hBox.addWidget(self._ok_button)
        hBox.addWidget(self._cancel_button)

        layout = vBox
        layout.addWidget(self._symbols_view)
        layout.addLayout(hBox)

        self.setLayout(vBox)
        

        # self._window.show()
        self._displaySymbols()

    def _okButtonPressed(self):
        self.result = 'OK'
        self.close()

    def _cancelButtonPressed(self):
        self.result = 'Cancel'
        self.close()

    def _displaySymbols(self):
        self._symbols_view.setColumnCount(2)
        row = 0
        for name, value in self._symbols.items():
            self._symbols_view.setRowCount(row+1)
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self._symbols_view.setItem(row, 0, item)
            item = QTableWidgetItem(f'0x{value}')
            item.setTextAlignment(Qt.AlignCenter)
            self._symbols_view.setItem(row, 1, item)
            row += 1

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectSymbol({ 'one': 'two', 'three': 'three'})
    window.exec()
    print(window.result)
    # app.exec_()
