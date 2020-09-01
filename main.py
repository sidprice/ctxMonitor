from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice
from ctx_pubsub import Ctx_PubSub
from variable_manager import VariableManager
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #
        # create an instance of the Ctx_PubSub class for this window
        #
        pubSub = Ctx_PubSub.getInstance()
        #
        # Get the VariableManger instance
        #
        variableManager = VariableManager.getInstance()

        self.setWindowTitle('CtxMonitor by Sid Price')
        self.resize(800, 600)

        self._menuBar = QMenuBar(self)
        self._menu_items = self._menu_setup({
            '&File': {
                '&Open ELF File': self._openElf,
                'E&xit': self.close,
            },
            'Help': {
                'About': None,
            }
        }, self._menuBar)

        self.show()
        #
        # Ready to roll! subscribe to the database topic
        #
        pubSub.subscribe_variable_database(self._listener_database)
        

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
            pubSub = Ctx_PubSub.getInstance()
            pubSub.send_load_elf_file(elf_filename=elfName)
            # myVariables = variables.Variables()
            # symbols = myVariables.Load(str(dialog.selectedFiles()[0]))
            # if symbols != None:
            #     row = 0
            #     for name, value in symbols.items():
            #         item = QTableWidgetItem(name)
            #         item.setTextAlignment(Qt.AlignCenter)
            #         self.symbolTableView.setItem(row, 0, item)
            #         item = QTableWidgetItem(f'0x{value}')
            #         item.setTextAlignment(Qt.AlignCenter)
            #         self.symbolTableView.setItem(row, 1, item)
            #         row += 1
            #         self.symbolTableView.setRowCount(row+1)

    def _listener_database(self, symbols):
        print(symbols)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #
    #   TODO create the ProbeManager here
    #
    window = MainWindow()
    app.exec_()
