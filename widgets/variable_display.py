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

class VariableDisplay(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
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

    def init(self, monitored_variables):
        self._monitored_variables = monitored_variables

        self._display.blockSignals(True)
        row = 0
        for name, var in self._monitored_variables.items():
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

            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
            self._display.setItem(row, 1, item)

            item = QTableWidgetItem(f'0x{var.address}')
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
            self._display.setItem(row, 2, item)

            row += 1
    
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
        pubsub.send_monitored_database(database = self._monitored_variables)





