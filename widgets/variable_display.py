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

from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem

class VariableDisplay(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._display = QTableWidget()
        self._display.accessibleName = 'displayTableWidget'
        # self._display.setRowCount(1)
        self._display.setColumnCount(4)
        self._display.setHorizontalHeaderItem(0, QTableWidgetItem('Name'))
        self._display.setHorizontalHeaderItem(1, QTableWidgetItem('Address'))
        self._display.setHorizontalHeaderItem(2, QTableWidgetItem('Content'))
        self._display.setHorizontalHeaderItem(3, QTableWidgetItem('Period'))
        self._layout.addWidget(self._display)
        self.setLayout(self._layout)

    def init(self, variables):
        pass