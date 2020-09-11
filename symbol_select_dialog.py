##########################################################################
#
#   Symbol Selection Dialog, subclassed from QDialog
#
##########################################################################

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtWidgets import QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QCheckBox, QWidget
import sys

from variables import Variables
from variable import Variable


class SelectSymbol(QtWidgets.QDialog):
    def __init__(self, variables, monitored_variables):
        super().__init__()

        self._variables = variables
        self._monitored_variables = monitored_variables

        self.setWindowTitle('Select Symbol')
        #
        #   Limit the size of the dialog
        #
        self.setMaximumWidth(550)
        self.setMinimumWidth(550)
        self.setMaximumHeight(300)
        self.setMinimumHeight(300)
        #
        #   Create the controls
        #
        self._variables_view = QTableWidget()
        self._variables_view.setColumnCount(4)
        self._variables_view.setHorizontalHeaderItem(0, QTableWidgetItem('Enable'))
        self._variables_view.setHorizontalHeaderItem(1, QTableWidgetItem('Name'))
        self._variables_view.setHorizontalHeaderItem(2, QTableWidgetItem('Address'))
        self._variables_view.setHorizontalHeaderItem(3, QTableWidgetItem('Update Period'))
        self._variables_view.setColumnWidth(0, 60)
        otherWidth = (self.width() - 60) / 3
        self._variables_view.setColumnWidth(1, otherWidth)
        self._variables_view.setColumnWidth(2, otherWidth)
        self._variables_view.horizontalHeader().setStretchLastSection(True)
        self._variables_view.verticalHeader().hide()
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
        layout.addWidget(self._variables_view)
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
        row = 0
        for name, var in self._variables.items():
            self._variables_view.setRowCount(row + 1)
            ###
            #
            #   Build the enable/disable checkbox
            #
            ###            
            checkboxWidget = QWidget()
            checkBox = QCheckBox(checkboxWidget)
            #
            #   If the variable is in the monitored list
            #   check the checkbox
            #
            isMonitored = False
            if (self._monitored_variables != None):
                if (self._monitored_variables[name]):
                    isMonitored = True
            if (isMonitored):
                checkBox.setCheckState(Qt.CheckState.Checked)
            else:
                checkBox.setCheckState(Qt.CheckState.Unchecked)

            layoutCheckbox = QHBoxLayout(checkboxWidget)
            layoutCheckbox.addWidget(checkBox)
            layoutCheckbox.setAlignment(Qt.AlignCenter)
            layoutCheckbox.setContentsMargins(0, 0, 0, 0)
            self._variables_view.setCellWidget(row,0, checkboxWidget)
            
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self._variables_view.setItem(row, 1, item)

            item = QTableWidgetItem(f'0x{var.address}')
            item.setTextAlignment(Qt.AlignCenter)
            self._variables_view.setItem(row, 2, item)
            # item = QTableWidgetItem('0')
            # item.setTextAlignment(Qt.AlignCenter)
            # self._variables_view.setItem(row, 2, item)
            row += 1

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectSymbol({ 'one': 'two', 'three': 'three'})
    window.exec()
    print(window.result)
    # app.exec_()
