from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout ,QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QDockWidget, QTabWidget, QTabBar, QDesktopWidget, QToolBar)
from PyQt5.QtCore import QSize, Qt, QDate, QTime
from PyQt5.QtGui import QFont, QColor, QIcon

from widgets.file_area import FileArea

from util.db_manager import db_manager

from style_sheets.main_style_sheet import style_sheet

class FileApp(QMainWindow):
    def __init__(self):
        super(FileApp, self).__init__()
        self.initializeUI()

    def initializeUI(self):

        self.full_size = QDesktopWidget().screenGeometry(-1).size()
        # declare the main current file area object
        self.current_file_area = None
        self.db_manager = db_manager()

        self.setWindowTitle("Files Manager")
        self.resize(self.full_size) # resize the window to the size of desktop
        # set up the dock area
        self.setUpDock()
        # set up the central widget
        self.setUpCentral()

        self.setStyleSheet(style_sheet)
        self.show() # shoe window on the screen

    def setUpDock(self):
        # create the dock area
        self.dock = QDockWidget("Status Bar", self)
        self.dock.setMinimumWidth(int(self.full_size.width() * 0.15))
        self.dock.setAllowedAreas(Qt.RightDockWidgetArea)

        self.dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        # create the tool bar
        self.tool_bar = QToolBar("Tool Bar")
        self.tool_bar.setMinimumHeight(int(self.full_size.height() * 0.10))
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)

        self.tool_bar.addAction(QIcon("img/sys/new_folder.png") , "New Folder",
                                lambda  : self.tab_bar.currentWidget().newFolder())



    def setUpCentral(self):

        # create the tab bar widget
        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True)
        self.setCentralWidget(self.tab_bar)


        # create the main tab widget
        self.current_file_area = FileArea(self.db_manager)
        self.tab_bar.addTab(self.current_file_area , "Home")



if __name__ == "__main__":
    app = QApplication([])
    window = FileApp()
    app.exec_()

