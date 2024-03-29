##########################################################################
#
#   COPYRIGHT Sid Price 2022
#
#   This file is part of ctxMonitor
#
#       ctxMonitor is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Nersion 3 as published
#   by the Free Software Foundation .
#
#       ctxMonitor is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along with Foobar.
#               If not, see <https://www.gnu.org/licenses/>.
#
#   Symbol Selection Dialog, subclassed from QDialog
#
##########################################################################

from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt, QPoint
from PySide2.QtWidgets import QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QCheckBox, QWidget, QComboBox
import sys

from variables import Variables
from variable import Variable
from ctx_pubsub import Ctx_PubSub
from ctx_timing import CtxTiming


class SelectSymbol(QtWidgets.QDialog):

    def __init__(self, variables):
        super().__init__()

        self._variables = variables

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
        self._displaySymbols()

    def _okButtonPressed(self):
        ###
        #
        #   Broadcast the monitored variables
        #
        ###
        pubSub = Ctx_PubSub.getInstance()
        for name, var in self._variables.items():
            pubSub.send_variable_changed(var)
        self.close()

    def _cancelButtonPressed(self):
        self.close()

    def _displaySymbols(self):
        self._variables_view.blockSignals(True)
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
            #   If the variable is monitored
            #   check the checkbox and save the period
            #   for display later
            #
            isMonitored = False
            if name in self._variables:
                if self._variables[name].monitored:
                    isMonitored = True



            if (isMonitored):
                checkBox.setCheckState(Qt.CheckState.Checked)
                period = self._variables[name].period
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

            item = QComboBox()
            item.setStyleSheet('font-size:12px')
            item.addItems(CtxTiming.Periods)
            if (isMonitored):
                item.setEnabled(True)
                index = item.findText(CtxTiming.text_from_period(self._variables[name].period))
                item.setCurrentIndex(index)
            else:
                item.setEnabled(False)
            item.currentIndexChanged.connect(self._combobox_changed)
            self._variables_view.setCellWidget(row, 3, item)

            row += 1
        self._variables_view.blockSignals(False)

    def _combobox_changed(self):
        cb = self.sender()
        gl = cb.mapToGlobal(QPoint())
        lp = self._variables_view.viewport().mapFromGlobal(gl)

        ix = self._variables_view.indexAt(lp)
        row = ix.row()
        column = ix.column()
        name = (self._variables_view.item(row, 1)).text()
        comboBox = self._variables_view.cellWidget(row, column)
        self._variables[name].period = CtxTiming.period_from_text(comboBox.currentText())

    def _check_changed(self):
        cb = self.sender()
        gl = cb.mapToGlobal(QPoint())
        lp = self._variables_view.viewport().mapFromGlobal(gl)

        ix = self._variables_view.indexAt(lp)
        #
        row = ix.row()
        name = (self._variables_view.item(row, 1)).text()
        comboBox = self._variables_view.cellWidget(row, 3)
        period = CtxTiming.period_from_text(comboBox.currentText())
        self._variables[name].monitored = cb.isChecked()
        self._variables_view.cellWidget(row, 3).setEnabled(True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectSymbol({'one': 'two', 'three': 'three'})
    window.exec()
    # app.exec_()
