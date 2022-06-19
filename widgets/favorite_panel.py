import os

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QScrollArea,
                            QComboBox, QLineEdit)
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QIcon

from util.db_manager import db_manager
from util.clipboard import ClipBoard

from widgets.folder_widget import FolderWidget
from widgets.image_widget import ImageWidget
from widgets.file_widget import FileWidget
from widgets.file_area import FileArea

class FavoritePanel(FileArea):

    # signal for open the folder
    folder_open_signal = pyqtSignal(str)

    def __init__(self, db_manager : db_manager, parent = None, * , clipboard : ClipBoard):
        super(FavoritePanel, self).__init__(db_manager, parent, clipboard=clipboard)

    def initializeUI(self):

        self.temp_labels = []

        # create the scroll area and setUp it
        scroll_area = QScrollArea()

        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # create the main widget
        self.mainWidget = QWidget()
        self.mainWidget.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(self.mainWidget) # append the widget to scroll area

        # create the grid layout for widget
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(self.grid)
        vbox.addLayout(hbox)
        self.mainWidget.setLayout(vbox)

        # # create the toolbar and add to the main layout
        # tool_bar = self.setUpToolBar()

        # create the search and path widget area
        search_bar = self.setUpSearchBar()
        # main layout
        main_lyt = QVBoxLayout()
        main_lyt.setContentsMargins(0, 0, 0, 0)
        main_lyt.setSpacing(0)

        # main_lyt.addWidget(tool_bar)
        main_lyt.addLayout(search_bar, 1)
        main_lyt.addWidget(scroll_area)
        self.setLayout(main_lyt)

        # open the current folder
        self.initializePanel()

    def showAndHideSearchBar(self):

        self.searchBarAnimation = QPropertyAnimation(self.search_bar, b"maximumWidth")
        self.searchBarAnimation.setStartValue(self.search_bar.width())
        self.searchBarAnimation.setDuration(250)
        self.searchBarAnimation.setEasingCurve(QEasingCurve.OutCubic)

        if self.search_bar.width() <= 10:
            self.searchBarAnimation.setEndValue(450)
        else:
            self.searchBarAnimation.setEndValue(0)
            # self.search_bar.show()

        self.searchBarAnimation.start()

    def setUpSearchBar(self):

        # create the widget
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 20, 0, 20)

        searchButton = QPushButton("")
        searchButton.setIcon(QIcon("img/sys/search-free-icon-font.png"))
        searchButton.setIconSize(QSize(40, 40))
        searchButton.pressed.connect(self.showAndHideSearchBar)
        searchButton.setObjectName("search-bar-button")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Anything")
        self.search_bar.setObjectName("search-bar")
        self.search_bar.setMaximumWidth(0)
        # implement the search method
        self.search_bar.textChanged.connect(self.searchFolderFiles)


        # create the sort combo box
        self.sortComboBox = QComboBox()
        self.sortComboBox.setObjectName("sort-box")
        for name, index in {"Name":  0, "Date added" : 1, "Size": 2}.items():
            self.sortComboBox.addItem(name, index)
        self.sortComboBox.currentIndexChanged.connect(self.sortWidgets)

        self.reverseSortBox = QComboBox()
        self.reverseSortBox.setObjectName("sort-box2")
        self.reverseSortBox.addItems(["Asc", "Desc"])
        self.reverseSortBox.currentIndexChanged.connect(self.sortWidgets)

        hbox.addWidget(searchButton)
        hbox.addWidget(self.search_bar)
        hbox.addStretch()
        hbox.addWidget(QLabel("Sort by"))
        hbox.addWidget(self.sortComboBox)
        hbox.addWidget(self.reverseSortBox)

        return hbox

    def initializePanel(self):

        # first clean the file area
        self.cleanArea()

        folder_widgets, files_widgets = self.file_engine.open_favorites()

        for i, widget in enumerate(folder_widgets):
            self.folders.append(widget)
        for widget in files_widgets:
            self.files.append(widget)

        self.changeFolderMode(1)

    def selected(self, folder_widget : FolderWidget):

        for w in [*self.folders, *self.files]:
            if w == folder_widget:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = folder_widget

        # fire the status signal
        self.folder_status_signal.emit([self.selected_widget.name, self.selected_widget.path, self.selected_widget.time, self.selected_widget.fav, self.selected_widget.type])

    def selectFile(self, file_widget):

        for w in [*self.folders, *self.files]:
            if w == file_widget:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = file_widget

        if isinstance(file_widget, ImageWidget):
            self.image_status_signal.emit([file_widget.file, file_widget.path, file_widget.time, file_widget.fav])
        elif isinstance(file_widget, FileWidget):
            self.file_status_signal.emit([file_widget.file, file_widget.path, file_widget.time, file_widget.fav])

    def openFolder(self, path , back = False):

        # send the signal
        self.folder_open_signal.emit(path)

    def openSelectFolder(self):

        if self.selected_widget:
            self.folder_open_signal.emit(self.selected_widget.path)

    def sortWidgets(self, index):

        i = self.sortComboBox.currentData()
        reverse = self.reverseSortBox.currentIndex()

        if i == 0:
            self.folders.sort(key=lambda e: e.name, reverse=reverse)
            self.files.sort(key=lambda e: e.getName(), reverse=reverse)
        elif i == 1:
            self.folders.sort(key=lambda e: e.time, reverse=reverse)
            self.files.sort(key=lambda e: e.time, reverse=reverse)

        elif i == 2:
            self.files.sort(key=lambda e: os.stat(e.file).st_size, reverse=reverse)
            self.folders.sort(key=lambda e : self.file_engine.db_manager.folder_count(e.path), reverse=reverse)
        # change view
        self.changeFolderMode(1)

