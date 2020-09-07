##########################################################################
#
#   Custom Widget to display monitored variables.
#
#   Note:
#       This is a simplistic display to continue the proff of concept. By
#       having a custom widget a more sophisticated display may be weasily
#       added later.
#
##########################################################################

from PySide2.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QHeader
from PySide2 import QtCore


class DisplayMonitoredVariables_Simple(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #
        self._variableTable = QTableWidget(self)
        self._variableTable.setColumnCount = 4
        self._variableTable.setRowCount = 1

        self._header = QHeader(QtCore.Qt.Orientation.Horizontal)
        self._variableTable.setHorizontalHeader(self._header)
        #
        self._variableTable.setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self._variableTable.setHorizontalHeaderItem(1, QTableWidgetItem('Address'))
        self._variableTable.setHorizontalHeaderItem(2, QTableWidgetItem('Content'))
        self._variableTable.setHorizontalHeaderItem(3, QTableWidgetItem('Period'))
        self.layout.addWidget(self._variableTable, 0, 0)
        item = QTableWidgetItem('')
        self._variableTable.setItem(0, 0, item)
        # self.textbox = QLineEdit()
        # self.echo_label = QLabel('')

        # self.textbox.textChanged.connect(self.textbox_text_changed)

        # self.layout.addWidget(self.textbox, 0, 0)
        # self.layout.addWidget(self.echo_label, 1, 0)

    def init(self, variables):
        self._variables = variables
        print(self._variables)

    def clear(self):
        self._variables = None
        print('Clear variable display')
