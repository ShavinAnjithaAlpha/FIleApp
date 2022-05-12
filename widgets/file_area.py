from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout ,QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QDockWidget, QTabWidget, QTabBar, QDesktopWidget, QScrollArea,
                             QInputDialog)
from PyQt5.QtCore import QSize, Qt, QDate, QTime
from PyQt5.QtGui import QFont, QColor
from util.file_engine import FileEngine
from util.db_manager import db_manager

class FileArea(QScrollArea):
    def __init__(self, db_manager : db_manager):
        super(FileArea, self).__init__()
        # declare the attributes
        self.file_engine = FileEngine(db_manager, self)
        self.folders = []
        self.files = []

        self.initializeUI()

    def initializeUI(self):

        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # create the main widget
        self.mainWidget = QWidget()
        self.mainWidget.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.mainWidget) # append the widget to scroll area

        # create the grid layout for widget
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.mainWidget.setLayout(self.grid)

        # open the current folder
        self.openFolder(self.file_engine.current_path)

    def openFolder(self, path , back = False):

        # first clean the file area
        self.cleanArea()

        folder_widgets = self.file_engine.open_folder(path, back = back)
        for i, widget in enumerate(folder_widgets):
            self.grid.addWidget(widget, i, 0)
            self.folders.append(widget)


    def newFolder(self):

        name, ok = QInputDialog.getText(self, "New Folder", "Folder Name:")
        if ok:
            folder_widget = self.file_engine.new_folder(name)
            self.folders.append(folder_widget)

            self.grid.addWidget(folder_widget , len(self.folders) , 0)

    def cleanArea(self):

        for widget in self.folders:
            widget.deleteLater()

        for widget in self.files:
            widget.deleteLater()

        self.folders = []
        self.files = []

    def removeWidgetsFromGrid(self):

        for widget in [*self.folders , *self.files]:
            self.grid.removeWidget(widget)

    def goBackward(self):
        # print(self.file_engine.path_stack)
        if self.file_engine.count() > 1:
            index = self.file_engine.backward() - 1
            # open the last position
            self.openFolder(self.file_engine.path(index), back = True)

    def changeFolderMode(self, index):

        if index == 0:
            print("list")
        elif index == 1:
            print("grid")
        else:
            print("None")

    def home(self):

        self.openFolder(".")

