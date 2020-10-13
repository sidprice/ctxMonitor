##########################################################################
#
#   Custom Widget to display monitored variables.
#
#   Note:
#       This is a simplistic display to continue the proof of concept. By
#       having a custom widget a more sophisticated display may be easily
#       added later.
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

        self._variables = {}
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
        #   Subscribe to variable database changes
        #
        ###
        pubSub = Ctx_PubSub.getInstance()
        pubSub.subscribe_variable_changed(self._listener_variable_changed)
        pubSub.subscribe_variable_content_changed(self._listener_variable_content_changed)
        pubSub.subscribe_closed_elf_file(self._listener_elf_closed)

    def init(self):

        self._display.blockSignals(True)
        self._display.clearContents()
        row = 0
        for name, var in self._variables.items():
            if var.monitored == True:
                self._displayVariable(row, var)
                row += 1

    def _displayVariable(self, row, var, update=False):
        if not update:
            self._display.setRowCount(row + 1)
        
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

    def _listener_variable_changed(self, var):
        self._variables[var.name] = var.copy()

        if var.monitored:
            result = self._display.findItems(var.name, Qt.MatchExactly)
            if len(result):
                item = result[0]
                row = item.row()
                update = True
            else:
                row = self._display.rowCount()
                update = False
            self._displayVariable(row, self._variables[var.name], update)

    def _listener_variable_content_changed(self, var):
        result = self._display.findItems(var.name, Qt.MatchExactly)
        item = result[0]
        self._show_content(item.row(), var)

    def _listener_elf_closed(self):
        self._display.setRowCount(0)
        self._variables.clear()

    def _play_pause_clicked(self):
        button = self.sender()
        gl = button.mapToGlobal(QPoint())
        lp = self._display.viewport().mapFromGlobal(gl)

        ix = self._display.indexAt(lp)
        #
        row = ix.row()
        name = (self._display.item(row, 1)).text()
        enable = not self._variables[name].enable
        self._variables[name].enable = enable
        if (enable):
            icon = QIcon('icons/pause.png')
        else:
            icon = QIcon('icons/run.png')
        button.setIcon(icon)
        pubsub = Ctx_PubSub.getInstance()
        pubsub.send_variable_changed(self._variables[name])
