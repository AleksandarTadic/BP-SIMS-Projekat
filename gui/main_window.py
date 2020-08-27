import os
import json
import datetime
from PySide2 import QtWidgets, QtGui, QtCore
from gui.central_widget import CentralWidget
from gui.appearence.appearence import *
from gui.help import Help
from database.file_handler import FileHandler


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,app):
        super(MainWindow, self).__init__()
        self.resize(1000, 600)
        self.setWindowTitle("Editor generickih podataka")
        self.setWindowIcon(QtGui.QIcon())

        self.central_widget = QtWidgets.QTabWidget(self)
        self.central_widget.setTabsClosable(True)
        self.central_widget.tabCloseRequested.connect(self.delete_tab)

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.view_menu = QtWidgets.QMenu("View", self.menu_bar)
        self.help_menu = QtWidgets.QAction("Help", self.menu_bar)
        self.help_menu.triggered.connect(Help)

        self.full_screen = QtWidgets.QAction("FullScreen", checkable=True)
        self.full_screen.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.FullScreen))
        self.full_screen.triggered.connect(lambda : self.full_screen_check(self.full_screen))
        self.view_menu.addAction(self.full_screen)

        #theme menubar
        theme = QtWidgets.QMenu("Theme", self.view_menu)
        theme.addSection("Dark Theme")
        dark = QtWidgets.QAction("Dark", theme)
        dark.triggered.connect(lambda : dark_theme(app))
        theme.addAction(dark)
        dark_moon = QtWidgets.QAction("Midnight Blue", theme)
        dark_moon.triggered.connect(lambda : dark_moon_theme(app))
        theme.addAction(dark_moon)
        theme.addSection("Light Theme")
        light_gray = QtWidgets.QAction("Light Gray", theme)
        light_gray.triggered.connect(lambda : light_gray_theme(app))
        theme.addAction(light_gray)
        self.view_menu.addMenu(theme)

        self.menu_bar.addMenu(self.view_menu)
        self.menu_bar.addAction(self.help_menu)

        structure_dock = QtWidgets.QDockWidget("Local Files Dock", self)

        file_system_model = QtWidgets.QFileSystemModel()
        file_system_model.setRootPath(QtCore.QDir.currentPath())

        tree_view = QtWidgets.QTreeView()
        tree_view.setModel(file_system_model)
        tree_view.setRootIndex(file_system_model.index(QtCore.QDir.currentPath() + "/database/data"))
        tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) #prosirena kolona naspram sadrzaja

        structure_dock.setWidget(tree_view)
        structure_dock.setMaximumWidth(250)

        # db dock
        with open("database/metadata/db_metadata.json", "r") as f:
            db = json.load(f)
        db = db["database"]
        database_dock = QtWidgets.QDockWidget("Database Dock", self)
        database_dock.setMaximumWidth(250)
        db_list = QtWidgets.QListWidget()
        for i in range(len(db)):
            item = QtWidgets.QListWidgetItem(db[i])
            item.setIcon(QtGui.QIcon("icons/db-icon.png"))
            db_list.addItem(item)
        database_dock.setWidget(db_list)

        toggle_database_dock_action = database_dock.toggleViewAction()
        self.view_menu.addAction(toggle_database_dock_action)

        toggle_structure_dock_action = structure_dock.toggleViewAction()
        self.view_menu.addAction(toggle_structure_dock_action)

        def open_database(index):
            tree_view.clearSelection()
            metadata_path = index.text() + "_metadata.json"        
            data_list = FileHandler(metadata_path, True).get_handler()
            status_bar.showMessage("Otvorili ste " + data_list.metadata["title"].lower() + "!          Tip: " + "Database")
            central_workspace = CentralWidget(self.central_widget, data_list)
            central_workspace.setProperty("tab_path", index.text())
            if self.check_tabs(index.text()):
                return
            self.central_widget.addTab(central_workspace, QtGui.QIcon("icons/tab_icon.png"), data_list.metadata["title"].capitalize()+"_db")
            self.setCentralWidget(self.central_widget)

        db_list.itemClicked.connect(open_database)

        def file_clicked(index):
            db_list.clearSelection()
            file_path = os.path.basename(file_system_model.filePath(index)).replace(".txt", "")
            metadata_path = file_path + "_metadata.json"
            data_list = FileHandler(metadata_path).get_handler()
            status_bar.showMessage("Otvorili ste " + data_list.metadata["title"].lower() + "!          Tip: " + data_list.metadata["type"].capitalize())
            central_workspace = CentralWidget(self.central_widget, data_list)
            central_workspace.setProperty("tab_path", file_system_model.filePath(index))
            if self.check_tabs(file_system_model.filePath(index)):
                return
            self.central_widget.addTab(central_workspace, QtGui.QIcon("icons/tab_icon.png"), data_list.metadata["title"].capitalize())
            self.setCentralWidget(self.central_widget)

        tree_view.clicked.connect(file_clicked)

        status_bar = QtWidgets.QStatusBar(self)
        status_bar.showMessage("Status bar je prazan!")

        self.setMenuBar(self.menu_bar)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, structure_dock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, database_dock)
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(status_bar)

    def full_screen_check(self, full_screen):
        if self.full_screen.isChecked():
            return self.showFullScreen()
        return self.showNormal()

    def check_tabs(self, new_tab):
        for i in range(self.central_widget.count()):
            if self.central_widget.widget(i).property("tab_path") == new_tab:
                self.central_widget.setCurrentIndex(i)
                return True


    def delete_tab(self, index):
        widget = self.central_widget.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.central_widget.removeTab(index)