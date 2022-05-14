from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QDockWidget, QTabWidget, QTabBar, QDesktopWidget, QScrollArea,
                             QInputDialog, QAction, QToolBar, QComboBox, QFileDialog)
from PyQt5.QtCore import QSize, Qt, QDate, QTime
from PyQt5.QtGui import QFont, QColor, QIcon, QCursor
from util.file_engine import FileEngine
from util.db_manager import db_manager

from widgets.folder_widget import FolderWidget

class FileArea(QWidget):
    def __init__(self, db_manager : db_manager):
        super(FileArea, self).__init__(None)
        # declare the attributes
        self.file_engine = FileEngine(db_manager, self)
        self.folders = []
        self.files = []
        self.selected_folder = None

        self.initializeUI()

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

        # create the tool bar and add to the main layout
        tool_bar = self.setUpToolBar()
        # main layout
        main_lyt = QVBoxLayout()
        main_lyt.setContentsMargins(0, 0, 0, 0)
        main_lyt.setSpacing(0)

        main_lyt.addWidget(tool_bar)
        main_lyt.addWidget(scroll_area)
        self.setLayout(main_lyt)


        # open the current folder
        self.openFolder(self.file_engine.current_path)

    def setUpToolBar(self):

        # create the grid
        tool_bar = QToolBar()
        tool_bar.setObjectName("file-area-tool-bar")
        tool_bar.setContentsMargins(0, 0, 0, 0)
        tool_bar.setIconSize(QSize(50, 50))
        tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # create the actions
        home_action = QAction(QIcon("img/sys/home.png"),"Home", self)
        home_action.triggered.connect(self.home)
        tool_bar.addAction(home_action)

        back_action = QAction(QIcon("img/sys/back.png"), "" ,self)
        back_action.triggered.connect(self.goBackward)
        tool_bar.addAction(back_action)

        forward_action = QAction(QIcon("img/sys/right-arrow.png"), "",self)
        forward_action.triggered.connect(self.goForward)
        tool_bar.addAction(forward_action)

        tool_bar.addSeparator()

        open_action = QAction(QIcon("img/sys/open-folder.png"), "Open", self)
        open_action.triggered.connect(self.openSelectFolder)
        tool_bar.addAction(open_action)

        new_folder_action = QAction(QIcon("img/sys/add-folder.png"), "New Folder", self)
        new_folder_action.triggered.connect(self.newFolder)
        tool_bar.addAction(new_folder_action)

        add_files_action = QAction(QIcon("../img/sys/clipboard.png"), "Add Files", self)
        add_files_action.triggered.connect(self.addFiles)
        tool_bar.addAction(add_files_action)

        tool_bar.addSeparator()

        # add the view changed combo box
        self.viewChangedBox = QComboBox()
        self.viewChangedBox.addItem(QIcon("img/sys/list.png"), "List View", 0)
        self.viewChangedBox.addItem(QIcon("img/sys/blocks.png"), "Grid View", 1)
        self.viewChangedBox.currentIndexChanged.connect(self.changeFolderMode)
        # add to the toolbar
        tool_bar.addWidget(self.viewChangedBox)



        return tool_bar

    def openFolder(self, path , back = False):

        # first clean the file area
        self.cleanArea()

        folder_widgets, files_widgets = self.file_engine.open_folder(path, back = back)
        for i, widget in enumerate(folder_widgets):
            self.folders.append(widget)
        for widget in files_widgets:
            self.files.append(widget)

        self.changeFolderMode(self.viewChangedBox.currentIndex())

    def openSelectFolder(self):

        if self.selected_folder:
            self.openFolder(self.selected_folder.path)

    def newFolder(self):

        name, ok = QInputDialog.getText(self, "New Folder", "Folder Name:", text="New Folder")
        if ok:
            folder_widget = self.file_engine.new_folder(name)
            self.folders.append(folder_widget)

            folder_widget.changeView(self.viewChangedBox.currentIndex())
            # add folder widget upon the view mode
            if self.viewChangedBox.currentIndex() == 0:
                self.grid.addWidget(folder_widget, len(self.folders), 0)
            elif self.viewChangedBox.currentIndex() == 1:
                [w.deleteLater() for w in self.temp_labels]
                self.temp_labels.clear()
                self.grid.addWidget(folder_widget, (len(self.folders)-1)//6, (len(self.folders)-1)%6)

                x = len([*self.folders , *self.files]) - 1
                if x % 6 != 0:
                    while x % 6 != 0:
                        x += 1
                        label = QLabel()
                        self.temp_labels.append(label)
                        self.grid.addWidget(label, x // 6, x % 6)

    def addFiles(self):

        files, ok = QFileDialog.getOpenFileNames(self, "Add Files", "", "JPEG Files(*.jpg);;PNG Files(*.png)")
        if ok:
            file_widgets = self.file_engine.add_files(files)
            print("file_widget")
            for w in file_widgets:
                self.files.append(w)
                w.changeViewMode(self.viewChangedBox.currentIndex())
            print("chanheMode")
            # add to the grid view this files
            for w in file_widgets:
                # add upon the view mode index
                if self.viewChangedBox.currentIndex() == 0:
                    self.grid.addWidget(w, len(self.folders), 0)
                elif self.viewChangedBox.currentIndex() == 1:
                    [w.deleteLater() for w in self.temp_labels]
                    self.temp_labels.clear()
                    self.grid.addWidget(w, (len(self.folders) - 1) // 6, (len(self.folders) - 1) % 6)

                    x = len([*self.folders, *self.files]) - 1
                    if x % 6 != 0:
                        while x % 6 != 0:
                            x += 1
                            label = QLabel()
                            self.temp_labels.append(label)
                            self.grid.addWidget(label, x // 6, x % 6)

    def cleanArea(self):

        for widget in self.folders:
            widget.deleteLater()

        for widget in self.files:
            widget.deleteLater()

        self.folders.clear()
        self.files.clear()
        self.temp_labels.clear()

    def removeWidgetsFromGrid(self):

        for widget in [*self.folders , *self.files, *self.temp_labels]:
            self.grid.removeWidget(widget)

        self.temp_labels.clear()

    def goBackward(self):
        # print(self.file_engine.path_stack)
        if self.file_engine.count() > 1:
            index = self.file_engine.backward() - 1
            # open the last position
            self.openFolder(self.file_engine.path(index), back = True)

    def goForward(self):

        pass

    def changeFolderMode(self, index):

        [w.changeView(index) for w in [*self.folders, *self.files]]

        if index == 0:
            # arrange the widget again
            self.removeWidgetsFromGrid()

            for i, w in enumerate([*self.folders , *self.files]):
                self.grid.addWidget(w, i, 0)

        elif index == 1:
            # arrange the widget as the grid
            self.removeWidgetsFromGrid()

            x = len([*self.folders, *self.files]) - 1
            for i, w in enumerate([*self.folders, *self.files]):
                self.grid.addWidget(w, i//6, i%6)

            if x%6 != 0:
                while x%6 != 0:
                    x += 1
                    label = QLabel()
                    self.temp_labels.append(label)
                    self.grid.addWidget(label, x//6, x%6)



        else:
            print("None")

    def selected(self, folder_wigdet : FolderWidget):

        for w in [*self.folders, *self.files]:
            if w == folder_wigdet:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = folder_wigdet

    def selectFile(self, file_widget):

        for w in [*self.folders, *self.files]:
            if w == file_widget:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = file_widget

    def home(self):

        self.openFolder(".")

