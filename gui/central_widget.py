from PySide2 import QtWidgets, QtGui, QtCore
from gui.model import Model

from gui.form import Form

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent, data_list):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.data_list = data_list
        self.subtables = []
        self.tab_widget = None
        # self.create_tab_widget()

        for i in range(len(self.data_list.metadata["linked_files"])):
            self.subtables.append(QtWidgets.QTableView(self.tab_widget))


        self.model = Model(self.data_list)
        self.table = QtWidgets.QTableView(self.tab_widget)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # subtable test
        self.table.clicked.connect(self.show_tabs)


    
        self.tool_bar = QtWidgets.QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.setFloatable(False)
        tool_bar_add = QtWidgets.QAction("ADD", self.tool_bar)
        tool_bar_add.triggered.connect(lambda : self.table.model().insertRows(1, 1, QtCore.QModelIndex()))
        self.tool_bar.addAction(tool_bar_add)
        tool_bar_delete = QtWidgets.QAction("DELETE", self.tool_bar)
        tool_bar_delete.triggered.connect(lambda : self.remove_one())
        self.tool_bar.addAction(tool_bar_delete)


        # test za context
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.handle_header_menu)


        # self.subtable = QtWidgets.QTableView(self.tab_widget)
        # self.subtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.subtable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # self.table.clicked.connect(self.data_object_selected)

        # self.subtable2 = QtWidgets.QTableView(self.tab_widget)

        # self.dodaj_studenta = StudentForma(self.model.students)
        # self.tab_widget.addTab(self.dodaj_studenta,"Dodaj studenta")

        # self.tab_widget.addTab(self.subtable, QtGui.QIcon("icons8-edit-file-64.png"), "Polozeni predmeti")
        # self.tab_widget.addTab(self.subtable2, QtGui.QIcon("icons8-edit-file-64.png"), "Nepolozeni predmeti")
    
        self.main_layout.addWidget(self.tool_bar)
        self.main_layout.addWidget(self.table)
        if len(self.subtables) > 0:
            self.create_tab_widget()
            self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def data_object_selected(self, index):
        model = self.table.model(self.data_list)
        selected_object_model = model.get_element(index)
        # polozeni_predmeti_model = self.create_polozeni_predmeti_model(student)
        # self.subtable.setModel(polozeni_predmeti_model)

        # self.tab_widget.addTab(self.subtable, QtGui.QIcon("icons8-edit-file-64.png"), "Polozeni predmeti")

        
    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    # def create_polozeni_predmeti_model(self, student):
    #     polozeni_predmeti_model = PolozeniPredmetModel(self.model.students)
    #     polozeni_predmeti_model.polozeni_predmeti = student.polozeni_predmeti

    #     return polozeni_predmeti_model

    def show_tabs(self):
        for i in self.subtables:
            self.tab_widget.addTab(i, QtGui.QIcon("icons8-edit-file-64.png"), "Polozeni predmeti")

    def remove_one(self):
        indexes = self.table.selectionModel().selectedIndexes()
        for index in indexes:
            self.table.model().removeRows(index.row(), 1, index)
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
    

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = None
        self.create_tab_widget()

        self.subtable1 = QtWidgets.QTableView(self.tab_widget)
        self.subtable2 = QtWidgets.QTableView(self.tab_widget)  
    
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def student_selected(self, index):
        model = self.table1.model()
        selected_student = model.get_element(index)

        polozeni_predmeti_model = PolozeniPredmetModel()
        polozeni_predmeti_model.polozeni_predmeti = selected_student.polozeni_predmeti

        nepolozeni_predmeti_model = NepolozeniPredmetModel()
        nepolozeni_predmeti_model.nepolozeni_predmeti = selected_student.nepolozeni_predmeti

        self.subtable1.setModel(polozeni_predmeti_model)
        self.subtable2.setModel(nepolozeni_predmeti_model)
