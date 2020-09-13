from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QDialog, QTableWidgetItem, QStatusBar, QGridLayout
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, Qt
from ctx_pubsub import Ctx_PubSub
from variable_manager import VariableManager
from symbol_select_dialog import SelectSymbol

#import widgets.display_monitored_variables_simple as monitorDisplay
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
    #   Menu item strings
    #
    #####
    _fileMenuName = 'File'
    _openElfFileMenuName = 'Open ELF File'
    _closeElfFileMenuName = 'Close Elf File'
    _exitMenuName = 'Exit'
    #
    _editMenuName = 'Edit'
    _addVariableMenuName = 'Add Variable ...'
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
    _addVariableTip = 'Add variable(s) to monitor'
    ##
    #
    #   Help menu item tips
    #
    ##
    _aboutTip = 'Show application properties'
    #
    _variables = dict({})  # The symbols read from the ELF file
    _monitored_variables = dict({})
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
        # Get the VariableManger instance
        #
        variableManager = VariableManager.getInstance()

        self.setWindowTitle('CtxMonitor by Sid Price')
        self.resize(800, 600)

        self._menuBar = QMenuBar(self)
        self._statusBar = QStatusBar(self)
        self.setStatusBar(self._statusBar)

        self._menu_items = self._menu_setup({
            self._fileMenuName: {
                self._openElfFileMenuName: self._openElf,
                self._closeElfFileMenuName: self._closeElf,
                self._exitMenuName: self.close,
            },
            self._editMenuName: {
                self._addVariableMenuName: self._newVariable,
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
        self._add_variable_menu = self._menu_items[self._editMenuName][self._addVariableMenuName]
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
        self._monitored = VariableDisplay(self)
        self.layout.addWidget(self._monitored, 0, 0)

        self.show()
        
        ##################################################
        #                                                #
        # Ready to roll!                                 #
        #                                                #
        ##################################################

        self._pubSub.subscribe_monitored_database(self._listener_monitored)
        self._pubSub.subscribe_loaded_elf_file(self._listener_elf_loaded)
        

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

    def _openElf(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Select the debug ELF file')
        dialog.setNameFilter('ELF Files (*.elf)')
        dialog.setFileMode(QFileDialog.ExistingFiles)
        if dialog.exec() == QDialog.Accepted:
            elfName = str(dialog.selectedFiles()[0])
            self._pubSub.send_load_elf_file(elf_filename=elfName)
            self.statusBar().showMessage(elfName + ' ... Loading', 2000)
            

        self.activateWindow()

    def _closeElf(self):
        self._pubSub.send_close_elf_file()

    def _newVariable(self):
        dialog = SelectSymbol(self._variables, self._monitored_variables)
        dialog.exec()

    def _listener_elf_loaded(self, symbols):
        print('main got elf loaded')
        self._close_elf_file_menu.setEnabled(True)
        self._variables = symbols
        if symbols != None:
            self._add_variable_menu.setEnabled(True)
        else:
            self._add_variable_menu.setEnabled(False)
            self._close_elf_file_menu.setEnabled(False)
            self._monitored.clear()

    def _listener_monitored(self, monitored):
        self._monitored_variables = monitored
        self._monitored.init(monitored)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #
    #   TODO create the ProbeManager here
    #
    window = MainWindow()
    app.exec_()
