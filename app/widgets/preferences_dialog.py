##########################################################################
#
#   User Preferences Dialog, subclassed from QDialog
#
##########################################################################

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit, QComboBox

# from ctx_timing import CtxTiming

class UserPreferences(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('User Preferences')
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
        self._tabs = QTabWidget()
        self._ok_button = QPushButton('OK')
        self._ok_button.setFixedWidth(70)
        self._ok_button.clicked.connect(self._okButtonPressed)
        self._cancel_button = QPushButton('Cancel')
        self._cancel_button.setFixedWidth(70)
        self._cancel_button.clicked.connect(self._cancelButtonPressed)
        ###
        #   Options TAB controls
        ###

        #   Default radix label

        optionDefaultRadixLabel = QLabel()
        optionDefaultRadixLabel.setFixedWidth(100)
        optionDefaultRadixLabel.setAlignment(Qt.AlignRight)
        optionDefaultRadixLabel.setText('Default display radix:')

        #   Default radix Combobox

        optionDefaultRadixCombobox = QComboBox()
        optionDefaultRadixCombobox.setStyleSheet('font-size:12px')

        #   Default radix layout widget

        radixWidget = QHBoxLayout()
        radixWidget.setAlignment(Qt.AlignLeft)
        radixWidget.addWidget(optionDefaultRadixLabel)
        radixWidget.addWidget(optionDefaultRadixCombobox)

        #   Default period label

        optionDefaultPeriodLabel = QLabel()
        optionDefaultPeriodLabel.setFixedWidth(100)
        optionDefaultPeriodLabel.setAlignment(Qt.AlignRight)
        optionDefaultPeriodLabel.setText('Default monitor period:')

        #   Default period Combobox

        optionDefaultPeriodCombobox = QComboBox()
        optionDefaultPeriodCombobox.setStyleSheet('font-size:12px')
        #optionDefaultPeriodCombobox.addItems(CtxTiming.Periods)

        #   Default period layout widget

        periodWidget = QHBoxLayout()
        periodWidget.setAlignment(Qt.AlignLeft)
        periodWidget.addWidget(optionDefaultPeriodLabel)
        periodWidget.addWidget(optionDefaultPeriodCombobox)

        #   Place options into vertical box

        optionsWidget = QVBoxLayout()
        wrapper = QWidget()
        wrapper.setLayout(radixWidget)
        optionsWidget.addWidget(wrapper)
        #
        wrapper = QWidget()
        wrapper.setLayout(periodWidget)
        optionsWidget.addWidget(wrapper)

        buttonsWidget = QHBoxLayout()
        
        #   Layout buttons

        buttonsWidget.setAlignment(Qt.AlignRight)
        buttonsWidget.addWidget(self._ok_button)
        buttonsWidget.addWidget(self._cancel_button)

        rootWidget = QVBoxLayout()
        wrapper = QWidget()
        wrapper.setLayout(optionsWidget)
        rootWidget.addWidget(wrapper)
        #
        wrapper = QWidget()
        wrapper.setLayout(buttonsWidget)
        rootWidget.addWidget(wrapper)

        tabWidget = QWidget()
        tabWidget.setLayout(rootWidget)

        self._tabs.addTab(tabWidget, 'Options')
        wrapper = QHBoxLayout()
        wrapper.addWidget(self._tabs)
        self.setLayout(wrapper)

    def _okButtonPressed(self):
        pass

    def _cancelButtonPressed(self):
        pass

    def _optionsTabUi(self):
        pass

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UserPreferences()
    window.exec()
