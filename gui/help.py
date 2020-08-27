from PySide2 import QtWidgets, QtGui, QtCore


class Help(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setter()


    def setter(self):
        self.setMinimumSize(200, 100)
        self.setWindowTitle("Help")
        self.setWindowIcon(QtGui.QIcon("icons/angry.ico"))
        self.help_layout = QtWidgets.QVBoxLayout()
        self.help_text = QtWidgets.QLabel('''
        Otvaranje datoteke: levim klikom na fajl iz leve tabele. 
            
        Dodavanje: desni klik van tabele/add.

        Brisanje: desni klik u red tabele/delete.

        Izmena: dupli klik na polje u redu/potvrda na enter.

        ---------------------------------------------------------------
        FullScreen: View/FullScreen ili F11.

        Izgled: View/Theme.

        Stablo datoteka: View/Structure dock.

        ---------------------------------------------------------------
        Kontakt: 
            Aleksandar Tadic - 2018271033
            Miroljub Brkic - 2018270676
        
        ''')
        self.help_text.setFont(QtGui.QFont("Times", 11))
        self.help_layout.addWidget(self.help_text)
        self.setLayout(self.help_layout)
        self.exec()