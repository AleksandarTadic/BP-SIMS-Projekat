import os
import json
import datetime
from PySide2 import QtWidgets, QtGui, QtCore
from database.serial_handler import SerialHandler
from database.sequential_handler import SequentialHandler
from gui.central_widget import CentralWidget
from gui.appearence.appearence import *
from gui.help import Help

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,app):
        super(MainWindow, self).__init__()
        self.resize(800, 500)
        self.setWindowTitle("Editor generickih podataka")
        self.setWindowIcon(QtGui.QIcon("icons/angry.ico"))

        menu_bar = QtWidgets.QMenuBar(self)
        view_menu = QtWidgets.QMenu("View", menu_bar)
        help_menu = QtWidgets.QAction("Help", menu_bar)
        help_menu.triggered.connect(Help)

        full_screen = QtWidgets.QAction("FullScreen", checkable=True)
        full_screen.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.FullScreen))
        full_screen.triggered.connect(lambda : full_screen_check(full_screen))
        view_menu.addAction(full_screen)

        #theme menubar
        theme = QtWidgets.QMenu("Theme", view_menu)
        theme.addSection("Dark Theme")
        dark = QtWidgets.QAction("Dark", theme)
        dark.triggered.connect(lambda : dark_theme(app))
        theme.addAction(dark)
        dark_moon = QtWidgets.QAction("Dark Moon", theme)
        dark_moon.triggered.connect(lambda : dark_moon_theme(app))
        theme.addAction(dark_moon)
        theme.addSection("Light Theme")
        light_gray = QtWidgets.QAction("Light Gray", theme)
        light_gray.triggered.connect(lambda : light_gray_theme(app))
        theme.addAction(light_gray)
        view_menu.addMenu(theme)

        menu_bar.addMenu(view_menu)
        menu_bar.addAction(help_menu)

        central_widget = QtWidgets.QTabWidget(self)

        structure_dock = QtWidgets.QDockWidget("Structure dock", self)

        file_system_model = QtWidgets.QFileSystemModel()
        file_system_model.setRootPath(QtCore.QDir.currentPath())

        tree_view = QtWidgets.QTreeView()
        tree_view.setModel(file_system_model)
        tree_view.setRootIndex(file_system_model.index(QtCore.QDir.currentPath() + "/database/data"))
        tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) #prosirena kolona naspram sadrzaja

        structure_dock.setWidget(tree_view)
        structure_dock.setMaximumWidth(250)

        toggle_structure_dock_action = structure_dock.toggleViewAction()
        view_menu.addAction(toggle_structure_dock_action)

        def full_screen_check(full_screen):
            if full_screen.isChecked():
                return self.showFullScreen()
            return self.showNormal()

        def file_clicked(index):
            file_path = os.path.basename(file_system_model.filePath(index))
            metadata_path = file_path.replace("_data","_metadata.json")

            def delete_tab(index):
                central_widget.removeTab(index)
                status_bar.showMessage("Zatvorili ste " + file_path.replace("_data", "e") + "!")
            
            def get_file_handler(file_path, metadata_path):
                temp_metadata = None
                try:
                    with open("database/metadata/" + metadata_path, "rb") as temp_meta_file:
                        temp_metadata = json.load(temp_meta_file)
                except FileNotFoundError:
                    print("Metadata file nije pronadjen!")
                if temp_metadata["type"] == "sequential":
                    status_bar.showMessage("Otvorili ste " + file_path.replace("_data", "e") + "!          Tip: " + temp_metadata["type"])
                    return SequentialHandler(metadata_path, file_path)
                else:
                    status_bar.showMessage("Otvorili ste " + file_path.replace("_data", "e") + "!          Tip: " + temp_metadata["type"])
                    return SerialHandler(metadata_path, file_path)
    
            central_widget = QtWidgets.QTabWidget(self)
            data_list = get_file_handler(file_path, metadata_path)
            central_workspace = CentralWidget(central_widget, data_list)
            central_widget.addTab(central_workspace, QtGui.QIcon("icons/tab_icon.png"), file_path.replace("_data", "").capitalize())
            # central_widget.setTabsClosable(True)
            central_widget.tabCloseRequested.connect(delete_tab)
            self.setCentralWidget(central_widget)

        tree_view.clicked.connect(file_clicked)

        status_bar = QtWidgets.QStatusBar(self)
        status_bar.showMessage("Status bar je prazan!")

        self.setMenuBar(menu_bar)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, structure_dock)
        self.setCentralWidget(central_widget)
        self.setStatusBar(status_bar)
