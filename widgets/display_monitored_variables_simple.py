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

from PySide2.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel

class DisplayMonitoredVariables_Simple(QWidget):
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.layout = QGridLayout()
            self.setLayout(self.layout)

            self.textbox = QLineEdit()
            self.echo_label = QLabel('')

            self.textbox.textChanged.connect(self.textbox_text_changed)

            self.layout.addWidget(self.textbox, 0, 0)
            self.layout.addWidget(self.echo_label, 1, 0)

    def textbox_text_changed(self): 
        self.echo_label.setText(self.textbox.text()) 
  

