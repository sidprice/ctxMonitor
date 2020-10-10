##########################################################################
#
#   Custom Widget to display monitored variables.
#
#   Note:
#       This is a simplistic display to continue the proof of concept. By
#       having a custom widget a more sophisticated display may be easily
#       added later.
#
#   Icons -> https://material.io/resources/icons/?style=baseline
#
##########################################################################

from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QToolButton
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtCore import Qt, QPoint
from ctx_pubsub import Ctx_PubSub
from variable import Variable


class VariableDisplay(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self._monitored_variables = {}
        self._layout = QHBoxLayout()
        self._display = QTableWidget()
        self._display.accessibleName = 'displayTableWidget'

        self._display.setColumnCount(4)
        self._display.setHorizontalHeaderItem(0, QTableWidgetItem(' '))
        self._display.setHorizontalHeaderItem(1, QTableWidgetItem('Name'))
        self._display.setHorizontalHeaderItem(2, QTableWidgetItem('Address'))
        self._display.setHorizontalHeaderItem(3, QTableWidgetItem('Content'))
        self._display.horizontalHeader().setStretchLastSection(True)

        self._display.setColumnWidth(0, 40)

        self._display.verticalHeader().hide()
        self._layout.addWidget(self._display)
        self.setLayout(self._layout)
        ###
        #
        #   Subscribe to variable content changes
        #
        ###
        pubSub = Ctx_PubSub.getInstance()
        pubSub.subscribe_variable_change(self._variable_change)
        pubSub.subscribe_monitor_variable(self._listener_monitor_variable)

    def _listener_monitor_variable(self, monitor):
        row = self._display.rowCount()
        try:
            test = self._monitored_variables[monitor.name]  # already in the list?
            ##
            #
            #  If we get here the variable is already being displayed so just update it
            #
            ##
            self._variable_change(monitor)
        except:
            ##
            #
            #   If we get here the variable is not displayed yet
            #
            ##
            self._monitored_variables[monitor.name] = Variable( name=monitor.name, address=monitor.address, period=monitor.period, enable=monitor.enable)
            self._displayVariable(row, monitor)

    def init(self, monitored_variables):
        self._monitored_variables = dict(monitored_variables)

        self._display.blockSignals(True)
        self._display.clearContents()
        row = 0
        for name, var in self._monitored_variables.items():
            self._displayVariable(row, var)
            row += 1

    def _displayVariable(self, row, var):
        self._display.setRowCount(row+1)
        icon_widget = QWidget()
        layout_icon = QHBoxLayout(icon_widget)

        button = QToolButton()
        if (var.enable):
            icon = QIcon('icons/pause.png')
        else:
            icon = QIcon('icons/run.png')
        button.setIcon(icon)

        layout_icon.addWidget(button)
        layout_icon.setAlignment(Qt.AlignCenter)
        layout_icon.setContentsMargins(0, 0, 0, 0)
        button.clicked.connect(self._play_pause_clicked)

        self._display.setCellWidget(row, 0, icon_widget)

        item = QTableWidgetItem(var.name)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
        self._display.setItem(row, 1, item)

        item = QTableWidgetItem(f'0x{var.address}')
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
        self._display.setItem(row, 2, item)
        ###
        #
        #   Show content of variable
        #
        ###
        self._show_content(row, var)

    def _show_content(self, row, var):
        item = QTableWidgetItem(var.content)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
        self._display.setItem(row, 3, item)

    def _variable_change(self, var):
        result = self._display.findItems(var.name, Qt.MatchExactly)
        item = result[0]
        self._show_content(item.row(), var)

    def _play_pause_clicked(self):
        button = self.sender()
        gl = button.mapToGlobal(QPoint())
        lp = self._display.viewport().mapFromGlobal(gl)

        ix = self._display.indexAt(lp)
        #
        row = ix.row()
        name = (self._display.item(row, 1)).text()
        enable = not self._monitored_variables[name].enable
        self._monitored_variables[name].enable = enable
        if (enable):
            icon = QIcon('icons/pause.png')
        else:
            icon = QIcon('icons/run.png')
        button.setIcon(icon)
        pubsub = Ctx_PubSub.getInstance()
        #pubsub.send_monitored_database(database=self._monitored_variables)
        pubsub.send_monitor_variable(self._monitored_variables[name])
