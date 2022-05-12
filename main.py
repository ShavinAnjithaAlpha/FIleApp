from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QDockWidget, QTabWidget, QTabBar, QDesktopWidget, QToolBar, QComboBox)
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
        # set up the tool  bar
        self.setUpToolBar()
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

    def setUpToolBar(self):

        # create the tool bar
        self.tool_bar = QToolBar("Tool Bar")
        self.tool_bar.setIconSize(QSize(50, 50))
        self.tool_bar.setMinimumHeight(int(self.full_size.height() * 0.13))
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)


        self.tool_bar.addAction(QIcon("img/sys/home.png"), "Home",
                                lambda : self.tab_bar.currentWidget().home())

        self.tool_bar.addAction(QIcon("img/sys/back.png"), "",
                                lambda: self.tab_bar.currentWidget().goBackward())

        self.tool_bar.addAction(QIcon("img/sys/right-arrow.png"), "",
                                lambda: print("forward"))

        self.tool_bar.addSeparator()

        self.tool_bar.addAction(QIcon("img/sys/open-folder.png"), "Open",
                                lambda : print("open"))

        self.tool_bar.addAction(QIcon("img/sys/add-folder.png"), "New Folder",
                                lambda: self.tab_bar.currentWidget().newFolder())



        self.tool_bar.addSeparator()
        # add the view changed combo box
        self.viewChangedBox = QComboBox()
        self.viewChangedBox.addItem(QIcon("img/sys/list.png"), "List View",0)
        self.viewChangedBox.addItem(QIcon("img/sys/blocks.png"), "Grid View",1)
        self.viewChangedBox.currentIndexChanged.connect(self.changeFolderView)
        # add to the tool bar
        self.tool_bar.addWidget(self.viewChangedBox)



    def setUpCentral(self):

        # create the tab bar widget
        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setTabShape(QTabWidget.Rounded)
        self.setCentralWidget(self.tab_bar)

        # set the tab closed request slots for close the tab
        self.tab_bar.tabCloseRequested.connect(self.closeTab)
        # set the add tab bar button
        newTabButton = self.tab_bar.tabBar().addTab("+")
        self.tab_bar.tabBar().setTabButton(newTabButton, QTabBar.RightSide, None)
        self.tab_bar.tabBar().tabBarClicked.connect(self.addNewFileTab)



        # create the main tab widget
        self.current_file_area = FileArea(self.db_manager)
        self.tab_bar.addTab(self.current_file_area , "Home")
        self.tab_bar.setCurrentIndex(0)

    def addNewFileTab(self, event):

        if event == self.tab_bar.tabBar().count() - 1:
            self.current_file_area = FileArea(self.db_manager)
            self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.current_file_area, "Home")

            self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

    def closeTab(self, event):

        if self.tab_bar.tabBar().count() == 2:
            QApplication.quit()

        widget = self.tab_bar.widget(event)
        self.tab_bar.tabBar().removeTab(event)

    def changeFolderView(self, index : int):

        for i in range(self.tab_bar.tabBar().count() - 1):
            self.tab_bar.widget(i).changeFolderMode(index)


if __name__ == "__main__":
    app = QApplication([])
    window = FileApp()
    app.exec_()

