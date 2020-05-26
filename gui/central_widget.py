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

        # subtable test
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
            toolbar_add.triggered.connect(lambda : self.subtables[self.get_current_widget()].model().insertRows(1, 1, QtCore.QModelIndex()))
        self.toolbar.addAction(toolbar_add)
        toolbar_delete = QtWidgets.QAction("DELETE", self.toolbar)
        if table is not None:
            toolbar_delete.triggered.connect(lambda : self.remove_one(table, model))
        else:
            toolbar_delete.triggered.connect(lambda : self.remove_one(self.subtables[self.get_current_widget()], self.subtables[self.get_current_widget()].model()))
        self.toolbar.addAction(toolbar_delete)
        layout.addWidget(self.toolbar)
        

    # def data_object_selected(self, index):
    #     model = self.table.model(self.data_list)
    #     selected_object_model = model.get_element(index)

    def get_current_widget(self):
        return self.tab_widget.currentIndex()
        
    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def show_tabs(self):
        for i in range(len(self.subtables)):
            self.subhandler = FileHandler(self.data_list.metadata["linked_files"][i]).get_handler()
            self.model = Model(self.subhandler)
            self.subtables[i].setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.subtables[i].setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.subtables[i].horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.subtables[i].setModel(self.model)
            self.tab_widget.addTab(self.subtables[i], QtGui.QIcon("icons8-edit-file-64.png"), self.data_list.metadata["linked_files"][i].replace("_metadata.json","").capitalize())

    def remove_one(self, table, model):
        indexes = table.selectionModel().selectedIndexes()
        for index in indexes:
            model.removeRows(index.row(), 1, index)
            break
        # index = self.table.selectionModel().currentIndex()
        # self.table.model().removeRows(index.row(), 1, index)

    def handle_header_menu(self):
        menu = QtWidgets.QMenu(self)
        delete = QtWidgets.QAction("Delete", menu)
        delete.triggered.connect(lambda : self.remove_one())
        menu.addAction(delete)
        add = QtWidgets.QAction("Add", menu)
        add.triggered.connect(lambda : self.table.model().insertRows(1, 1, QtCore.QModelIndex()))
        menu.addAction(add)
        menu.exec_(QtGui.QCursor.pos())
