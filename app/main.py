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
#   Main module for ctxMonitor
#
##########################################################################import ctypes

import ctypes
from PySide2.QtGui import QIcon
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QDialog, QTableWidgetItem,  QGridLayout
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, Qt
from ctx_pubsub import Ctx_PubSub
from variable_manager import VariableManager
from probe_manager import ProbeManager
from widgets.symbol_select_dialog import SelectSymbol
from widgets.preferences_dialog import UserPreferences
from preferences import Preferences
from ctx_StatusBar import CTX_StatusBar
from widgets.variable_display import VariableDisplay
import sys
import os


class MainWindow(QMainWindow):
    ##########
    #
    #   String constants used in MainWindow
    #
    ##########

    #####
    #
    #   Main Window Title
    #
    #####
    _mainWindowTitle = 'CtxMonitor by Sid Price'
    #####
    #
    #   Menu item strings
    #
    #####
    _fileMenuName = 'File'
    _openElfFileMenuName = 'Open ELF File'
    _closeElfFileMenuName = 'Close Elf File'
    _exitMenuName = 'Exit'
    #
    _editMenuName = 'Edit'
    _editVariablesMenuName = 'Edit Variables ...'
    _editPreferencesMenuName = 'Edit Preferences ...'
    #
    _helpMenuName = 'Help'
    _aboutMenuName = 'About'
    #####
    #
    #   Statusbar tips
    #
    #####
    ##
    #
    #   File menu item tips
    #
    ##
    _openElfFileTip = 'Open an ELF file'
    _closeElfFileTip = 'Close current Elf file'
    _exitTip = 'Close the application'
    ##
    #
    #   Edit menu item tips
    #
    ##
    _addVariableTip = 'Add/Edit variable(s) to monitor'
    ##
    #
    #   Help menu item tips
    #
    ##
    _aboutTip = 'Show application properties'
    #
    _variables = dict({})  # The symbols read from the ELF file
    _pubsub = None

    def __init__(self):
        super().__init__()

        self.window = QWidget()
        self.layout = QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        #
        # create an instance of the Ctx_PubSub class for this window
        #
        self._pubSub = Ctx_PubSub.getInstance()
        #
        # Get the ProbeManger instance, this will create the manager
        #
        self._probeManager = ProbeManager.getInstance()
        #
        # Get the VariableManger instance, this will create the manager
        #
        self._variableManager = VariableManager.getInstance()

        self.setWindowTitle(self._mainWindowTitle)
        self.setWindowIcon(QIcon('./icons/ctxMonitor_32x32.png'))
        self.resize(800, 600)

        self._menuBar = QMenuBar(self)
        self._statusBar = CTX_StatusBar(self)
        self._menu_items = self._menu_setup({
            self._fileMenuName: {
                self._openElfFileMenuName: self._openElf,
                self._closeElfFileMenuName: self._closeElf,
                self._exitMenuName: self.close,
            },
            self._editMenuName: {
                self._editVariablesMenuName: self._editMonitoredVariables,
                self._editPreferencesMenuName: self._editPreferences,
            },
            self._helpMenuName: {
                self._aboutMenuName: None,
            }
        }, self._menuBar)
        self.setMenuBar(self._menuBar)
        #
        # File menu items
        #
        self._open_elf_file_menu = self._menu_items[self._fileMenuName][self._openElfFileMenuName]
        self._open_elf_file_menu.setStatusTip(self._openElfFileTip)
        #
        self._close_elf_file_menu = self._menu_items[self._fileMenuName][self._closeElfFileMenuName]
        self._close_elf_file_menu.setEnabled(False)
        self._close_elf_file_menu.setStatusTip(self._closeElfFileTip)
        #
        self._exit_menu = self._menu_items[self._fileMenuName][self._exitMenuName]
        self._exit_menu.setStatusTip(self._exitTip)
        #
        #   Edit menu items
        #
        self._add_variable_menu = self._menu_items[self._editMenuName][self._editVariablesMenuName]
        self._add_variable_menu.setEnabled(False)
        self._add_variable_menu.setStatusTip(self._addVariableTip)
        #
        #   Help menu items
        #
        self._about_menu = self._menu_items[self._helpMenuName][self._aboutMenuName]
        self._about_menu.setStatusTip(self._aboutTip)

        ####
        #
        #   Add the custom widget that shows monitored variables
        #
        #   Note:
        #       A custom widget is used so that the display may be
        #       updated to a more advanced version by designing a
        #       new widget
        #
        ####
        self._display = VariableDisplay(self)
        self.layout.addWidget(self._display, 0, 0)

        self.show()

        ##################################################
        #                                                #
        # Ready to roll!                                 #
        #                                                #
        ##################################################

        self._pubSub.subscribe_loaded_elf_file(self._listener_elf_loaded)

        #####
        #
        #   Check we have the minimum preferences set in order to run, if
        #   not, open the preferences dialog to get them set.
        #
        #####

        self._settings = Preferences.getInstance()
        comPort = self._settings.preferences_probe_port()
        if ( comPort == ''):    # must have a comm port
            self._editPreferences()
        #####
        #
        #   If we have previously loaded an ELF file, load it again
        #
        #####
        elf_file = self._settings.elf_file()
        if (elf_file != None):
            self._pubSub.send_load_elf_file(elf_filename=elf_file)
            self.setWindowTitle(self._mainWindowTitle + '  -  ' + os.path.basename(elf_file))
            self._statusBar.ShowMessage(elf_file + ' ... Loading', 2000)
        #####
        #
        #   Time to connect to the probe
        #
        #####
        #self._probeManager.connect_to_probe()
        self._pubSub.subscribe_probe_connected(self._listener_probe_connected)
        self._settings = Preferences.getInstance()
        comPort = self._settings.preferences_probe_port()
        if ( comPort == ''):    # must have a comm port
            return
        self._pubSub.send_probe_connect()


    def _menu_setup(self, d, parent=None):
        k = {}
        for name, value in d.items():
            name_safe = name.replace('&', '')
            if isinstance(value, dict):
                wroot = QMenu(parent)
                wroot.setTitle(name)
                parent.addAction(wroot.menuAction())
                w = self._menu_setup(value, wroot)
                w['__root__'] = wroot
            else:
                w = QAction(parent)
                w.setText(name)
                if callable(value):
                    w.triggered.connect(value)
                parent.addAction(w)
            k[name_safe] = w
        return k

    def closeEvent(self, event):
        variableManager = VariableManager.getInstance()
        variableManager.close()
        return super().closeEvent(event)

    def _openElf(self):
        dialog = QFileDialog(self)
        initial_dir = self._settings.elf_path()
        if (initial_dir != None):
            dialog.setDirectory(initial_dir)
        dialog.setWindowTitle('Select the debug ELF file')
        dialog.setNameFilter('ELF Files (*.elf)')
        dialog.setFileMode(QFileDialog.ExistingFiles)
        
        if dialog.exec() == QDialog.Accepted:
            initial_dir = dialog.directory()
            self._settings.set_elf_path(initial_dir)
            elfName = str(dialog.selectedFiles()[0])
            self._settings.set_elf_file(elfName)
            self._settings.sync()
            self.setWindowTitle(self._mainWindowTitle + '  -  ' + os.path.basename(elfName))
            self._pubSub.send_load_elf_file(elf_filename=elfName)
            self._statusBar.showMessage(elfName + ' ... Loading', 2000)

        self.activateWindow()

    def _closeElf(self):
        self._settings.remove_elf_file()
        self._pubSub.send_close_elf_file()

    def _editMonitoredVariables(self):
        dialog = SelectSymbol(self._variables)
        dialog.exec()

    def _editPreferences(self):
        dialog = UserPreferences()
        dialog.exec()
        if dialog.result() == QDialog.Accepted:
            #
            #   User may have changed the target power, so update the probe
            #
            tpwr_enable = self._settings.preferences_probe_power_target()
            self._pubSub.send_probe_target_control_power(enable=tpwr_enable)
      
    def _listener_elf_loaded(self, symbols):
        self._close_elf_file_menu.setEnabled(True)
        self._variables = symbols
        if symbols != None:
            self._add_variable_menu.setEnabled(True)
            
        else:
            self._add_variable_menu.setEnabled(False)
            self._close_elf_file_menu.setEnabled(False)
        self._display.init()

    def _listener_probe_connected(self, connectState):
        message = 'Connected to probe'
        if not connectState:
            message = 'Failed to connect to probe'
        self._statusBar.ShowMessage(message, 5000)   
        self._statusBar.ShowProbeState(connectState)    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./icons/ctxMonitor_32x32.png'))
    QCoreApplication.setOrganizationName('Sid Price Design')
    QCoreApplication.setApplicationName('ctxMonitor v1.0')
    QCoreApplication.setOrganizationDomain('sidprice.com')
    myappid = 'SidPriceDesign.ctx.ctxMonitor.0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    window = MainWindow()
    app.exec_()
