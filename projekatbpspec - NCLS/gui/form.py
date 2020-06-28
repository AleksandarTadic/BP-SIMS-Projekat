from PySide2 import QtWidgets, QtCore, QtGui

class Form(QtWidgets.QDialog):
    def __init__(self, data_type, parent=None):
        super(Form, self).__init__(parent)
        self.data_type = data_type
        self.new_object = None
        self.setWindowIcon(QtGui.QIcon("icons/angry.ico"))
        self.setWindowTitle(data_type.metadata["title"] + " dodavanje")
        self.layout = QtWidgets.QFormLayout()
        self.dodaj = QtWidgets.QPushButton("Dodaj")
        self.dodaj.clicked.connect(lambda : self.add_class())
        self.dodaj.setFixedSize(200,40)
        self.q_line_edit_list = []
        for i in range(len(data_type.metadata["collumns"])):
            self.line_edit = QtWidgets.QLineEdit()
            self.line_edit.setFixedSize(200,40)
            self.layout.addRow(QtWidgets.QLabel(self.data_type.metadata["collumns"][i].replace("_"," ").capitalize() + ": "),self.line_edit)
            self.q_line_edit_list.append(self.line_edit)
        self.layout.addWidget(self.dodaj)
        self.setLayout(self.layout)
        self.display()
    
    def add_class(self):
        self.new_object = {}
        for i in range(len(self.q_line_edit_list)):
            if self.q_line_edit_list[i].text() == "":
                self.message_box("Sva polja moraju biti popunjena!")
                self.new_object = None
                return
            self.new_object[self.data_type.metadata["collumns"][i]] = self.q_line_edit_list[i].text()
        for i in self.data_type.data:
            if self.data_type.concat(i) == self.data_type.concat(self.new_object):
                self.message_box("Kljuc je zauzet!")
                self.new_object = None
                return
            # /\
        self.close()

    def message_box(self, text):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
        message_box.setText(text)
        message_box.exec()

    def get_object(self):
        return self.new_object

    def display(self):
        self.exec_()