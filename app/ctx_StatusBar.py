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
#   Class that provides the UI Status Bar for ctxMonitor
#
##########################################################################

from multiprocessing import connection
from PySide2.QtWidgets import QWidget, QStatusBar, QLabel
from PySide2.QtGui import QIcon, QPixmap


class CTX_StatusBar():
    def __init__(self, parent=None):
        self._parent = parent
        self._statusBar = QStatusBar(parent)

        self._parent.setStatusBar(self._statusBar)
        self._statusBarSetup()

    #
    #   Set up the status bar controls
    #
    def _statusBarSetup(self):
        self._statusBar.setStyleSheet(
            'padding-top: 10px; padding-bottom: 15px')
        self._connectionStatus = QLabel()
        self._connectionStatus.setStyleSheet('border: 5; color: blue ;')
        self._connectionStatus.setText("Status")

        self._connectionIcon = QLabel()
        connectionIcon = QPixmap('icons/disconnected.png')
        self._connectionIcon.setPixmap(connectionIcon)
        self._connectionIcon.setToolTip("Probe is disconnected")

        self._statusBar.reformat()
        self._statusBar.addPermanentWidget(self._connectionStatus)
        self._statusBar.addPermanentWidget(self._connectionIcon)

    def ShowMessage(self, message, timeout):
        self._statusBar.showMessage(message, timeout)
    #
    #   Display an icon in the statusbar that reflects the passed state
    # of the probe. (Connected/Disconnected)
    #

    def ShowProbeState(self, probeState):
        
        if ( probeState == True):
            connectionIcon = QPixmap('icons/connected.png')
            toolTip = 'Probe is connected'
        else:
            connectionIcon = QPixmap('icons/disconnected.png')  
            self._connectionIcon.setToolTip("Probe is disconnected")
        self._connectionIcon.setPixmap(connectionIcon)
        self._connectionIcon.setToolTip(toolTip)
