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

    def get_class(self, kls):
        parts = kls.split(".")
        module = ".".join(parts[:-1])
        my_class = __import__(module)
        for comp in parts[1:]:
            my_class = getattr(my_class, comp)
        return my_class
    
    def add_class(self):
        path_to_class = ("database.klase" + "." + self.data_type.metadata["path_to_file"].lower().replace("_data","") + "." + self.data_type.metadata["class"])
        new_class = self.get_class(path_to_class)
        self.new_object = new_class()
        for i in range(len(self.q_line_edit_list)):
            if self.q_line_edit_list[i].text() == "":
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
                message_box.setText("Sva polja moraju biti popunjena!")
                message_box.exec()
                self.new_object = None
                return
            setattr(self.new_object, self.data_type.metadata["collumns"][i], self.q_line_edit_list[i].text())
        for i in self.data_type.data:
            if self.data_type.concat(i) == self.data_type.concat(self.new_object):
                message_box = QtWidgets.QMessageBox()
                message_box.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
                message_box.setText("Kljuc je zauzet!")
                message_box.exec()
                self.new_object = None
                return
        self.close()

    def get_object(self):
        return self.new_object

    def display(self):
        self.exec_()