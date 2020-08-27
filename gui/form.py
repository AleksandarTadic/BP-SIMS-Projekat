from PySide2 import QtWidgets, QtCore, QtGui
import datetime

class Form(QtWidgets.QDialog):
    def __init__(self, data_type, parent=None):
        super(Form, self).__init__(parent)
        self.data_type = data_type
        self.new_object = None
        self.setWindowIcon(QtGui.QIcon())
        self.setWindowTitle(self.data_type.metadata["title"] + " dodavanje")
        self.layout = QtWidgets.QFormLayout()
        self.dodaj = QtWidgets.QPushButton("Dodaj")
        self.dodaj.clicked.connect(lambda : self.add_class())
        self.dodaj.setFixedSize(200,40)
        self.q_line_edit_list = []
        for i in range(len(self.data_type.metadata["collumns"])):
            if self.data_type.metadata["attr_type"][i] == "str":
                self.line_edit = QtWidgets.QLineEdit()
                self.line_edit.setMaxLength(self.data_type.metadata["attr_max"][i])
            elif self.data_type.metadata["attr_type"][i] == "int":
                self.line_edit = QtWidgets.QSpinBox()
                max_len = ""
                for n in range(self.data_type.metadata["attr_max"][i]):
                    max_len += "9"
                max_len = int(max_len)
                self.line_edit.setRange(0, max_len)
            elif self.data_type.metadata["attr_type"][i] == "date":
                self.line_edit = QtWidgets.QDateEdit()
            self.line_edit.setFixedSize(200,40)
            self.layout.addRow(QtWidgets.QLabel(self.data_type.metadata["collumns"][i].replace("_"," ").capitalize() + ": "),self.line_edit)
            self.q_line_edit_list.append(self.line_edit)
        self.layout.addWidget(self.dodaj)
        self.setLayout(self.layout)
        self.display()
    
    def add_class(self):
        self.new_object = {}
        for i in range(len(self.q_line_edit_list)):
            if self.data_type.metadata["attr_type"][i] == "str":
                if self.q_line_edit_list[i].text() == "":
                    self.message_box("Sva polja moraju biti popunjena!")
                    self.new_object = None
                    return
                self.new_object[self.data_type.metadata["collumns"][i]] = self.q_line_edit_list[i].text()
            elif self.data_type.metadata["attr_type"][i] == "int":
                self.new_object[self.data_type.metadata["collumns"][i]] = str(self.q_line_edit_list[i].value())
            elif self.data_type.metadata["attr_type"][i] == "date":
                value = self.q_line_edit_list[i].date().toString(QtCore.Qt.ISODate)
                date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                if self.data_type.is_database():
                    date = date.strftime("%d-%m-%Y")
                else:
                    date = date.strftime("%d.%m.%Y")
                self.new_object[self.data_type.metadata["collumns"][i]] = date
        if self.data_type.metadata["type"] != "serial":
            for i in self.data_type.get_all():
                if self.data_type.concat(i) == self.data_type.concat(self.new_object):
                    self.message_box("Kljuc je zauzet!")
                    self.new_object = None
                    return

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