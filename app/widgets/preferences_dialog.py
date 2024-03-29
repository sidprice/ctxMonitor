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
#   User Preferences Dialog, subclassed from QDialog
#
##########################################################################

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox

#from ctx_timing import CtxTiming
from ctx_pubsub import Ctx_PubSub

from preferences import Preferences

from probe import Probes, Reconnect

class UserPreferences(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('User Preferences')
        #
        #   Limit the size of the dialog
        #
        self.setMaximumWidth(400)
        self.setMinimumWidth(400)
        self.setMaximumHeight(200)
        self.setMinimumHeight(200)
        #
        #   Create the controls
        #
        self._createDialogButtons()
        self._createOptionsTabUi()
        self._createProbeTabUi()

        self._combineTabs()

        rootWidget = QVBoxLayout()
        rootWidget.addWidget(self._tabs)
        wrapper = QWidget()
        wrapper.setLayout(self._buttonsWidget)
        rootWidget.addWidget(wrapper)

        self.setLayout(rootWidget)

        self._settings = Preferences.getInstance()
        self._pubSub = Ctx_PubSub.getInstance()

        self._getCurrentPreferences()

    def _getCurrentPreferences(self):
        self._tabs.setCurrentIndex(self._settings.preferences_last_tab())  # select last used TAB
        self._probeDevice = self._settings.preferences_probe_port()
        if self._probeDevice != "":
            selindex = self._portCombo.findText(self._probeDevice)
            self._portCombo.setCurrentIndex(selindex)
        if self._settings.preferences_probe_power_target() == 0:
            state = Qt.CheckState.Unchecked
        else:
            state = Qt.CheckState.Checked
        self._probeTpwrCheckbox.setCheckState(state)
        

    def _saveCurrentPreferences(self):
        self._settings.set_preferences_last_tab(self._tabs.currentIndex())  # last TAB
        self._settings.set_preferences_probe_port(self._portCombo.currentText())  # probe port
        #
        # If the port changed then reconnect to new port
        #
        if self._probeDevice != self._portCombo.currentText():
            Reconnect(self._portCombo.currentText())
        self._settings.set_preferences_probe_power_target(self._probeTpwrCheckbox.isChecked())

        self._settings.sync()

    def _okButtonPressed(self):
        self._saveCurrentPreferences()
        self._pubSub.send_probe_connect()
        self.accept()

    def _cancelButtonPressed(self):
        self.reject()

    def _createDialogButtons(self):
        self._ok_button = QPushButton('OK')
        self._ok_button.setFixedWidth(70)
        self._ok_button.clicked.connect(self._okButtonPressed)
        self._cancel_button = QPushButton('Cancel')
        self._cancel_button.setFixedWidth(70)
        self._cancel_button.clicked.connect(self._cancelButtonPressed)
        self._buttonsWidget = QHBoxLayout()
        self._buttonsWidget.setAlignment(Qt.AlignRight)
        self._buttonsWidget.addWidget(self._ok_button)
        self._buttonsWidget.addWidget(self._cancel_button)

    def _createProbeTabUi(self):
        self._probePortLabel = QLabel()  # Probe port label
        self._probePortLabel.setFixedWidth(100)
        self._probePortLabel.setAlignment(Qt.AlignRight)
        self._probePortLabel.setText('Probe port:')

        # self._probePortText = QLineEdit()
        # self._probePortText.setFixedWidth(100)
        # self._probePortText.setAlignment(Qt.AlignRight)

        #
        #   Create a ComboBox to display/enter comm ports
        #
        self._portCombo = QComboBox()
        probes = Probes()
        for probe in probes:
            self._portCombo.addItem(probe)
        self._portCombo.setCurrentIndex(1)
        self._portWidget = QHBoxLayout()  # port layout widget
        self._portWidget.setAlignment(Qt.AlignLeft)
        self._portWidget.addWidget(self._probePortLabel)
        self._portWidget.addWidget(self._portCombo)
        # self._portWidget.addWidget(self._probePortText)

        self._probeTpwrCheckbox = QCheckBox()  # Probe Power Target checkbox
        self._probeTpwrCheckbox.setFixedWidth(225)
        self._probeTpwrCheckbox.setText('Power target')

        self._probeTpwrWidget = QHBoxLayout()
        self._probeTpwrWidget.setAlignment(Qt.AlignRight)
        self._probeTpwrWidget.addWidget(self._probeTpwrCheckbox)

        self._probeOptionsWidget = QVBoxLayout()  # Place probe settings into vertical box
        wrapper = QWidget()
        wrapper.setLayout(self._portWidget)
        self._probeOptionsWidget.addWidget(wrapper)
        wrapper = QWidget()
        wrapper.setLayout(self._probeTpwrWidget)
        self._probeOptionsWidget.addWidget(wrapper)

    def _createOptionsTabUi(self):
        self._optionDefaultRadixLabel = QLabel()  # default radix label
        self._optionDefaultRadixLabel.setFixedWidth(120)
        #self._optionDefaultRadixLabel.setFixedHeight(60)
        self._optionDefaultRadixLabel.setAlignment(Qt.AlignRight)
        self._optionDefaultRadixLabel.setText('Default display radix:')

        self._optionDefaultRadixCombobox = QComboBox()  # default radix combobox
        #self._optionDefaultRadixCombobox.setFixedHeight(60)
        self._optionDefaultRadixCombobox.setStyleSheet('font-size:12px')

        self._radixWidget = QHBoxLayout()  # default radix layout widget
        self._radixWidget.setAlignment(Qt.AlignLeft)
        self._radixWidget.addWidget(self._optionDefaultRadixLabel)
        self._radixWidget.addWidget(self._optionDefaultRadixCombobox)

        self._optionDefaultPeriodLabel = QLabel()  # default period label
        self._optionDefaultPeriodLabel.setFixedWidth(120)
        self._optionDefaultPeriodLabel.setFixedHeight(60)
        self._optionDefaultPeriodLabel.setAlignment(Qt.AlignRight)
        self._optionDefaultPeriodLabel.setText('Default monitor period:')

        self._optionDefaultPeriodCombobox = QComboBox()  # default period combobox
        self._optionDefaultPeriodCombobox.setStyleSheet('font-size:12px')
        #self._optionDefaultPeriodCombobox.addItems(CtxTiming.Periods)

        self._periodWidget = QHBoxLayout()  # default period layout widget
        self._periodWidget.setAlignment(Qt.AlignLeft)
        self._periodWidget.addWidget(self._optionDefaultPeriodLabel)
        self._periodWidget.addWidget(self._optionDefaultPeriodCombobox)

        self._optionsWidget = QVBoxLayout()  # Place options into vertical box
        wrapper = QWidget()
        wrapper.setLayout(self._radixWidget)
        self._optionsWidget.addWidget(wrapper)
        #
        wrapper = QWidget()
        wrapper.setLayout(self._periodWidget)
        self._optionsWidget.addWidget(wrapper)


    def _combineTabs(self):
        self._tabs = QTabWidget()
        self._tabs.setTabShape(QTabWidget.Triangular)
        wrapper = QWidget()
        wrapper.setLayout(self._optionsWidget)
        self._tabs.addTab(wrapper, 'Options')
        wrapper = QWidget()
        wrapper.setLayout(self._probeOptionsWidget)
        self._tabs.addTab(wrapper, 'Probe')


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UserPreferences()
    window.exec()
