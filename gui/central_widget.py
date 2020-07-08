from PySide2 import QtWidgets, QtGui, QtCore
from gui.model import Model

from gui.form import Form

from database.file_handler import FileHandler

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent, data_list):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.data_list = data_list
        self.subtables = []
        self.tab_widget = None

        for i in range(len(self.data_list.metadata["linked_files"])):
            self.subtables.append(QtWidgets.QTableView(self.tab_widget))

        self.model = Model(self.data_list)
        self.table = QtWidgets.QTableView(self.tab_widget)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.setModel(self.model)

        # subtable
        self.table.clicked.connect(self.show_tabs)

        # test za context
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handle_header_menu)
    
        self.set_toolbar(self.main_layout, self.table, self.table.model())
        self.main_layout.addWidget(self.table)
        if len(self.subtables) > 0:
            self.create_tab_widget()
            self.set_toolbar(self.main_layout)
            self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def set_toolbar(self, layout, table=None, model=None):
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        toolbar_add = QtWidgets.QAction("ADD", self.toolbar)
        if table is not None:
            toolbar_add.triggered.connect(lambda : model.insertRows(1, 1, QtCore.QModelIndex()))
        else:
            # toolbar_add.triggered.connect(lambda : self.subtables[self.get_current_widget()].model().insertRows(1, 1, QtCore.QModelIndex()))
            toolbar_add.triggered.connect(lambda : self.insert_one(self.insert_one(self.subtables[self.get_current_widget()].model())))
        self.toolbar.addAction(toolbar_add)
        toolbar_delete = QtWidgets.QAction("DELETE", self.toolbar)
        if table is not None:
            toolbar_delete.triggered.connect(lambda : self.remove_one(table, model))
        else:
            toolbar_delete.triggered.connect(lambda : self.remove_one(self.subtables[self.get_current_widget()], self.subtables[self.get_current_widget()].model()))
        self.toolbar.addAction(toolbar_delete)
        layout.addWidget(self.toolbar)
        
    def get_current_widget(self):
        return self.tab_widget.currentIndex()
        
    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def show_tabs(self, index):    
        selected_object_model = self.data_list.get_all()[index.row()]
        for i in range(len(self.subtables)):
            self.subhandler = FileHandler(self.data_list.metadata["linked_files"][i], self.data_list.is_database()).get_handler()

            filtered_data = []
            for d in range(len(self.subhandler.get_all())):
                current = ""
                filter_sel = ""

                if self.data_list.metadata["linked_keys"] != False:
                    linked_keys = self.data_list.metadata["linked_keys"]
                    for j in range(len(linked_keys)):
                        if linked_keys[j]["name"] == self.subhandler.metadata["class"]:
                            for k in range(len(linked_keys[j]["fk"])):
                                current += str(self.subhandler.get_all()[d][linked_keys[j]["fk"][k]])
                                filter_sel += str(selected_object_model[linked_keys[j]["k"][k]])
                if (current == filter_sel) and (len(current) != 0 or len(filter_sel) != 0):
                    filtered_data.append(self.subhandler.data[d])
            
            self.model = Model(self.subhandler, filtered_data)
            self.subtables[i].setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.subtables[i].setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.subtables[i].horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.subtables[i].setModel(self.model)
            self.tab_widget.addTab(self.subtables[i], QtGui.QIcon("icons/tab_icon.png"), self.model.data_list.metadata["title"])

    def remove_one(self, table, model):
        if model is not None:
            indexes = table.selectionModel().selectedIndexes()
            for index in indexes:
                model.removeRows(index.row(), 1, index)
                break
        # index = self.table.selectionModel().currentIndex()
        # self.table.model().removeRows(index.row(), 1, index)

    def insert_one(self, model):
        if model is not None:
            model.insertRows(1, 1, QtCore.QModelIndex())
        
    def handle_header_menu(self):
        menu = QtWidgets.QMenu(self)
        delete = QtWidgets.QAction("Delete", menu)
        delete.triggered.connect(lambda : self.remove_one(self.table, self.table.model()))
        menu.addAction(delete)
        add = QtWidgets.QAction("Add", menu)
        add.triggered.connect(lambda : self.table.model().insertRows(1, 1, QtCore.QModelIndex()))
        menu.addAction(add)
        menu.exec_(QtGui.QCursor.pos())
