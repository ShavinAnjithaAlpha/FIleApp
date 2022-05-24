from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QDockWidget, QTabWidget, QTabBar, QDesktopWidget, QScrollArea,
                             QInputDialog, QAction, QToolBar, QComboBox, QFileDialog, QLineEdit, QGroupBox,
                             QActionGroup, QGraphicsEffect, QGraphicsDropShadowEffect)
from PyQt5.QtCore import QSize, Qt, QDate, QTime, pyqtSignal, QPropertyAnimation
from PyQt5.QtGui import QFont, QColor, QIcon, QCursor, QPixmap
from util.file_engine import FileEngine
from util.db_manager import db_manager

from widgets.folder_widget import FolderWidget
from widgets.image_widget import ImageWidget
from widgets.file_widget import FileWidget
from widgets.path_bar import PathBar


class FileArea(QWidget):

    folder_status_signal = pyqtSignal(list)
    image_status_signal = pyqtSignal(list)
    file_status_signal = pyqtSignal(list)

    def __init__(self, db_manager : db_manager ,parent = None):
        super(FileArea, self).__init__(parent)
        # declare the attributes
        self.file_engine = FileEngine(db_manager, self)
        self.folders = []
        self.files = []
        self.selected_widget = None

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

        # create the search and path widget area
        search_bar = self.setUpSearchBar()
        # main layout
        main_lyt = QVBoxLayout()
        main_lyt.setContentsMargins(0, 0, 0, 0)
        main_lyt.setSpacing(0)

        main_lyt.addWidget(tool_bar)
        main_lyt.addLayout(search_bar)
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

        tool_bar.addWidget(self.navigationBox())

        tool_bar.addSeparator()

        tool_bar.addWidget(self.newBox())

        tool_bar.addSeparator()

        tool_bar.addWidget(self.viewBox())

        tool_bar.addSeparator()

        tool_bar.addWidget(self.actionBox())

        return tool_bar

    def navigationBox(self):
         # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("Navigations")

        # create the actions
        home_action = self.action_button("", QIcon("img/sys/home.png"), self.home)

        back_action = self.action_button("", QIcon("img/sys/back.png"), self.goBackward)

        forward_action = self.action_button("", QIcon("img/sys/right-arrow.png"), self.goForward)


        hbox = QHBoxLayout()
        hbox.addWidget(home_action)
        hbox.addWidget(back_action)
        hbox.addWidget(forward_action)

        gr_box.setLayout(hbox)
        return gr_box


    def viewBox(self):

        # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("View Options")

        # add the view changed combo box
        self.viewChangedBox = QComboBox()
        self.viewChangedBox.addItem(QIcon("img/sys/list.png"), "List View", 0)
        self.viewChangedBox.addItem(QIcon("img/sys/blocks.png"), "Grid View", 1)
        self.viewChangedBox.currentIndexChanged.connect(self.changeFolderMode)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Item View"))
        vbox.addWidget(self.viewChangedBox)
        vbox.addStretch()

        gr_box.setLayout(vbox)
        return gr_box

    def newBox(self):

        # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("Add File Or Folder")
        # new folder action
        new_folder_action = self.action_button("New Folder", QIcon("img/sys/add-folder.png"), self.newFolder)
        # add file action
        add_files_action =self.action_button("Add Files", QIcon("img/sys/add-file.png"), self.addFiles)

        # create the h box
        hbox = QHBoxLayout()
        hbox.addWidget(new_folder_action)
        hbox.addWidget(add_files_action)

        gr_box.setLayout(hbox)
        return gr_box

    def actionBox(self):

        # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("Actions")

        open_action = self.action_button("Open", QIcon("img/sys/open-folder.png"), self.openSelectFolder)
        rename_action = self.action_button("Rename", QIcon("img/sys/rename.png"), self.renameSeletedFolder)
        delete_action = self.action_button("Delete", QIcon("img/sys/delete.png"), lambda : None)
        copy_action = self.action_button("Copy", QIcon("img/sys/copy.png"), lambda : None)
        move_action = self.action_button("Move", QIcon("img/sys/forward.png"), lambda : None)

        self.actions = [open_action, rename_action, delete_action, copy_action, move_action]
        [action.setDisabled(True) for action in self.actions]

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(open_action, 0, 0)
        grid.addWidget(rename_action, 0, 1)
        grid.addWidget(delete_action, 0, 2)
        grid.addWidget(copy_action, 1, 0)
        grid.addWidget(move_action, 1, 1)

        gr_box.setLayout(grid)
        return gr_box

    def action_button(self, text, icon, func):

        button = QPushButton(text)
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))
        button.setObjectName("action_button")
        # button.setLayoutDirection(Qt.RightToLeft)
        # set the signal slot function
        button.pressed.connect(func)

        return button

    def showAndHideSearchBar(self):

        if self.search_bar.isVisible():
            self.search_bar.hide()
        else:
            self.search_bar.show()

            animation = QPropertyAnimation(self.search_bar, b"fixedWidth")
            animation.setStartValue(0)
            animation.setEndValue(300)
            animation.setDuration(1000)

            animation.start()


    def setUpSearchBar(self):

        # create the widget
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10, 20, 10, 20)

        searchButton = QPushButton("")
        searchButton.setIcon(QIcon("img/sys/search-icon.png"))
        searchButton.setIconSize(QSize(40, 40))
        searchButton.pressed.connect(self.showAndHideSearchBar)
        searchButton.setObjectName("search-bar-button")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Anything")
        self.search_bar.setObjectName("search-bar")
        self.search_bar.resize(QSize(300, 30))
        self.search_bar.hide()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(40, 40, 40))
        shadow.setXOffset(-10)
        # set the shadow
        self.search_bar.setGraphicsEffect(shadow)

        # create the path bar
        self.path_bar = PathBar(self.file_engine.getStringPath(self.file_engine.current_path), self.file_engine.current_path)
        self.path_bar.path_signal.connect(self.pathBarClicked)


        hbox.addWidget(searchButton)
        hbox.addWidget(self.search_bar)
        hbox.addWidget(self.path_bar)
        hbox.addStretch()

        return hbox

    def pathBarClicked(self, path  :str):

        self.openFolder(path)

    def openFolder(self, path , back = False):

        # first clean the file area
        self.cleanArea()

        folder_widgets, files_widgets = self.file_engine.open_folder(path, back = back)
        for i, widget in enumerate(folder_widgets):
            self.folders.append(widget)
        for widget in files_widgets:
            self.files.append(widget)

        self.changeFolderMode(self.viewChangedBox.currentIndex())
        # disabled the actions
        [a.setDisabled(True) for a in self.actions]
        # update the path bar

        self.path_bar.setPath(self.file_engine.getStringPath(self.file_engine.current_path), self.file_engine.current_path)

    def openSelectFolder(self):

        if self.selected_widget and isinstance(self.selected_widget, FolderWidget):
            self.openFolder(self.selected_widget.path)

        elif self.selected_widget and isinstance(self.selected_widget, ImageWidget) or isinstance(self.selected_widget, FileWidget):
            pass
        else:
            pass

    def renameSeletedFolder(self):

        if self.selected_widget and isinstance(self.selected_widget, FolderWidget):
            self.selected_widget.rename()


    def newFolder(self):

        name, ok = QInputDialog.getText(self, "New Folder", "Folder Name:", text="New Folder")
        if ok:
            folder_widget = self.file_engine.new_folder(name)
            self.folders.append(folder_widget)

            folder_widget.changeView(self.viewChangedBox.currentIndex())
            count = len([*self.folders, *self.files])

            # add folder widget upon the view mode
            if self.viewChangedBox.currentIndex() == 0:
                self.grid.addWidget(folder_widget, count, 0)
            elif self.viewChangedBox.currentIndex() == 1:
                [self.grid.removeWidget(w) for w in self.temp_labels]
                [w.deleteLater() for w in self.temp_labels]

                self.temp_labels.clear()
                self.grid.addWidget(folder_widget, (count-1)//6, (count-1)%6)

                x = len([*self.folders , *self.files]) - 1
                if x % 6 != 0:
                    while x % 6 != 0:
                        x += 1
                        label = QLabel()
                        self.temp_labels.append(label)
                        self.grid.addWidget(label, x // 6, x % 6)

    def addFiles(self):

        files, ok = QFileDialog.getOpenFileNames(self, "Add Files", "", "All File(*.*)")
        if ok:
            file_widgets = self.file_engine.add_files(files)

            count = len([*self.files, *self.folders])
            for w in file_widgets:
                self.files.append(w)
                w.changeView(self.viewChangedBox.currentIndex())

            # add to the grid view this files
            if self.viewChangedBox.currentIndex() == 0:
                for i, w in enumerate(file_widgets):
                    self.grid.addWidget(w, i + count, 0)

            elif self.viewChangedBox.currentIndex() == 1:
                [w.deleteLater() for w in self.temp_labels]
                self.temp_labels.clear()

                for i, w in enumerate(file_widgets):
                    self.grid.addWidget(w,  (i + count)// 6, (i + count)%6)

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

        if self.file_engine.count() > 1 and self.file_engine.path_stack.index(self.file_engine.current_path) != 0:
            index = self.file_engine.backward() #- 1
            # open the last position
            self.openFolder(self.file_engine.path(index), back = True)

    def goForward(self):

        if self.file_engine.count() > 1 and self.file_engine.path_stack.index(self.file_engine.current_path) != self.file_engine.count() - 1:
            index = self.file_engine.forward()
            # open the folder
            self.openFolder(self.file_engine.path(index), back=True)

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
        [a.setDisabled(False) for a in self.actions]

        # fire the status signal
        self.folder_status_signal.emit([self.selected_widget.name, self.selected_widget.path, self.selected_widget.time, self.selected_widget.fav])

    def selectFile(self, file_widget):

        for w in [*self.folders, *self.files]:
            if w == file_widget:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = file_widget
        [a.setDisabled(False) for a in self.actions]

        if isinstance(file_widget, ImageWidget):
            self.image_status_signal.emit([file_widget.file, file_widget.path, file_widget.time, file_widget.fav])
        elif isinstance(file_widget, FileWidget):
            self.file_status_signal.emit([file_widget.file, file_widget.path, file_widget.time, file_widget.fav])

    def home(self):

        self.openFolder(".")

