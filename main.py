import sys
import os
import json
import datetime
from PySide2 import QtWidgets, QtGui, QtCore

from database.serial_handler import SerialHandler
from database.sequential_handler import SequentialHandler

from gui.central_widget import CentralWidget
from gui.appearence.appearence import *

if __name__ == "__main__":
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
                return SequentialHandler(file_path, metadata_path)
            else:
                status_bar.showMessage("Otvorili ste " + file_path.replace("_data", "e") + "!          Tip: " + temp_metadata["type"])
                return SerialHandler(file_path, metadata_path)
  
        central_widget = QtWidgets.QTabWidget(main_window)
        data_list = get_file_handler(file_path, metadata_path)
        central_workspace = CentralWidget(central_widget, data_list)
        central_widget.addTab(central_workspace, QtGui.QIcon("icons/tab_icon.png"), file_path.replace("_data", "").capitalize())
        central_widget.setTabsClosable(True)
        central_widget.tabCloseRequested.connect(delete_tab)
        main_window.setCentralWidget(central_widget)


    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    main_window = QtWidgets.QMainWindow()
    main_window.resize(800, 500)
    main_window.setWindowTitle("Editor generickih podataka")
    main_window.setWindowIcon(QtGui.QIcon("icons/angry.ico"))
    # poziv pocetne teme po vremenu
    set_theme_by_current_time(app)


    def full_screen_check(full_screen):
        if full_screen.isChecked():
            return main_window.showFullScreen()
        return main_window.showNormal()

    menu_bar = QtWidgets.QMenuBar(main_window)
    file_menu = QtWidgets.QMenu("File", menu_bar)
    edit_menu = QtWidgets.QMenu("Edit", menu_bar)
    view_menu = QtWidgets.QMenu("View", menu_bar)
    help_menu = QtWidgets.QAction("Help", menu_bar) # promenjeno u QAction 
    def get_help():
        help_me = QtWidgets.QDialog()
        help_me.setMinimumSize(200, 100)
        help_me.setWindowTitle("Help")
        help_me.setWindowIcon(QtGui.QIcon("icons/angry.ico"))
        help_layout = QtWidgets.QVBoxLayout()
        help_text = QtWidgets.QLabel('''
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
        help_text.setFont(QtGui.QFont("Times", 11))
        help_layout.addWidget(help_text)
        # help_me.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
        # help_me.setText("Otvaranje datoteke: levim klikom na fajl iz leve tabele.\n\nFullScreen: View/Fullscreen ili F11\n")
        help_me.setLayout(help_layout)
        help_me.exec()

    help_menu.triggered.connect(lambda : get_help())


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

    # menu_bar.addMenu(file_menu)
    # menu_bar.addMenu(edit_menu)
    menu_bar.addMenu(view_menu)
    # dodato help i about action
    menu_bar.addAction(help_menu)

    # tool_bar = QtWidgets.QToolBar(main_window)

    central_widget = QtWidgets.QTabWidget(main_window)

    structure_dock = QtWidgets.QDockWidget("Structure dock", main_window)

    file_system_model = QtWidgets.QFileSystemModel()
    file_system_model.setRootPath(QtCore.QDir.currentPath())

    tree_view = QtWidgets.QTreeView()
    tree_view.setModel(file_system_model)
    tree_view.setRootIndex(file_system_model.index(QtCore.QDir.currentPath() + "/database/data"))
    tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) #prosirena kolona naspram sadrzaja

    structure_dock.setWidget(tree_view)
    structure_dock.setMaximumWidth(250) # maximalna velicina strukture docka

    toggle_structure_dock_action = structure_dock.toggleViewAction()
    view_menu.addAction(toggle_structure_dock_action)

    tree_view.clicked.connect(file_clicked)

    status_bar = QtWidgets.QStatusBar(main_window)
    status_bar.showMessage("Status bar je prazan!")

    # set
    main_window.setMenuBar(menu_bar)
    # main_window.addToolBar(tool_bar)
    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, structure_dock)
    main_window.setCentralWidget(central_widget)
    main_window.setStatusBar(status_bar)
    main_window.show()
    # menu_bar.setParent(main_window)
    sys.exit(app.exec_())

    

