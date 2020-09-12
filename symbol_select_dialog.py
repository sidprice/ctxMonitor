##########################################################################
#
#   Symbol Selection Dialog, subclassed from QDialog
#
##########################################################################

from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt, QPoint
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
        self._variables_view.setSelectionMode(QTableWidget.NoSelection)
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
            checkBox.clicked.connect(self._check_changed)
            #
            #   If the variable is in the monitored list
            #   check the checkbox and save the period
            #   for display later
            #
            isMonitored = False
            if (self._monitored_variables != None):
                if ( name in self._monitored_variables):
                    isMonitored = True
            if (isMonitored):
                checkBox.setCheckState(Qt.CheckState.Checked)
                period = self._monitored_variables[name].period
            else:
                checkBox.setCheckState(Qt.CheckState.Unchecked)
                period = None

            layoutCheckbox = QHBoxLayout(checkboxWidget)
            layoutCheckbox.addWidget(checkBox)
            layoutCheckbox.setAlignment(Qt.AlignCenter)
            layoutCheckbox.setContentsMargins(0, 0, 0, 0)
            self._variables_view.setCellWidget(row, 0, checkboxWidget)

            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
            self._variables_view.setItem(row, 1, item)

            item = QTableWidgetItem(f'0x{var.address}')
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
            item.setTextAlignment(Qt.AlignCenter)
            self._variables_view.setItem(row, 2, item)

            # item = QTableWidgetItem(f'{period}')
            # item.setTextAlignment(Qt.AlignCenter)
            # item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
            # self._variables_view.setItem(row, 3, item)
            if (period != None):
                item = QTableWidgetItem(f'{period}')
            else:
                item = QTableWidgetItem('')
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            self._variables_view.setItem(row, 3, item)

            row += 1

    def _check_changed(self, thisBox):
        cb = self.sender()
        gl = cb.mapToGlobal(QPoint())
        lp = self._variables_view.viewport().mapFromGlobal(gl)

        ix = self._variables_view.indexAt(lp)
        print(ix.row(), ix.column(), cb.isChecked())
        #
        name = (self._variables_view.item(ix.row(), 1)).text()
        period = (self._variables_view.item(ix.row(), 3)).text()
        if (cb.isChecked()):
            address = self._variables[name].address
            ##
            #
            #   Update or create a monitor entry
            #
            ##
            if ( name in self._monitored_variables):
                var = self._monitored_variables[name]
                var.period = period
            else:
                var = Variable(name, address, period)
            self._monitored_variables[name] = var
        else:
            ##
            #
            #   Remove the variable from the monitored list
            #
            ##
            del self._monitored_variables[name]
        
        print(self._monitored_variables)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectSymbol({'one': 'two', 'three': 'three'})
    window.exec()
    print(window.result)
    # app.exec_()
