from PySide2 import QtWidgets, QtCore
from gui.form import Form

from database.file_handler import FileHandler
class Model(QtCore.QAbstractTableModel):
    def __init__(self, data_list, filtered_data=None, parent=None):
        super().__init__(parent)
        self.data_list = data_list
        self.filtered_data = filtered_data

        
        # test

    def get_element(self, index):
        # dodato filter
        if self.filtered_data is not None:
            return self.filtered_data[index.row()]
        # 
        return self.data_list.get_all()[index.row()]

    # def get_element(self, index):
    #     return self.data_list.get_all()[index.row()]

    def rowCount(self, index):
        # dodato filter
        if self.filtered_data is not None:
            return len(self.filtered_data)
        # 
        return len(self.data_list.get_all())




    def columnCount(self, index):
        return len(self.data_list.metadata["collumns"])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        self.selected_data = self.get_element(index)
        for i in range(len(self.data_list.metadata["collumns"])):
            if index.column() == i and role == QtCore.Qt.DisplayRole:
                return getattr(self.selected_data, (self.data_list.metadata["collumns"][i]))

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        for i in range(len(self.data_list.metadata["collumns"])):
            if section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole: # dodati proveru ako je collumns tipa list nemoj ga kreirati !!!!!
                return self.data_list.metadata["collumns"][i].replace("_"," ").capitalize()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        self.selected_data = self.get_element(index)
        if value == "":
            return False
        for i in range(len(self.data_list.metadata["collumns"])):
            if index.column() == i and role == QtCore.Qt.EditRole:
                self.data_list.edit(self.selected_data, self.data_list.metadata["collumns"][i], value)
                return True
        return False

    def removeRows(self, row, rows, index=QtCore.QModelIndex()):
        selected_data = self.get_element(index)
        # zabrana za brisanje povezanih objekata
        connected_tables = []
        for i in self.data_list.metadata["linked_files"]:
            c_model = FileHandler(i).get_handler()
            connected_tables.append(c_model)
        for i in connected_tables:
            for d in range(len(i.data)):
                current = ""
                filter_sel = ""
                for j in range(len(i.metadata["key"])):
                    for k in range(len(self.data_list.metadata["key"])):
                        if i.metadata["key"][j] == self.data_list.metadata["key"][k]:
                            current += str(getattr(i.data[d], i.metadata["key"][j]))
                            filter_sel += str(getattr(selected_data, self.data_list.metadata["key"][k]))
                if (current == filter_sel) and (len(current) != 0 or len(filter_sel) != 0):
                    message_box = QtWidgets.QMessageBox()
                    message_box.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
                    message_box.setText("Ovaj podatak je povezan sa drugim podatkom!")
                    message_box.exec()
                    return False
        # 
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + rows - 1)
        self.data_list.delete_one(self.get_element(index))
        self.endRemoveRows()
        return True

    def insertRows(self, row, rows, index=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(), row, row + rows-1)
        forma = Form(self.data_list)
        obj = forma.get_object()
        if obj is None:
            return False
        self.data_list.insert(obj)
        # dodato filter 
        if self.filtered_data is not None:
            self.filtered_data.append(obj)
        # 
        self.endInsertRows()
        return True

    def flags(self, index):
        for i in range(len(self.data_list.metadata["collumns"])):
            for j in range(len(self.data_list.metadata["key"])):
                if self.data_list.metadata["collumns"][i] == self.data_list.metadata["key"][j]:
                    if index.column() == i:
                        return ~QtCore.Qt.ItemIsEditable
        return super().flags(index) | QtCore.Qt.ItemIsEditable



