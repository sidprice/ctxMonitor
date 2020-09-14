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

from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem

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
        self._layout.addWidget(self._display)
        self.setLayout(self._layout)

    def init(self, variables):
        pass
