import os

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QScrollArea,
                             QInputDialog, QToolBar, QComboBox, QFileDialog, QLineEdit, QGroupBox,
                             QGraphicsEffect, QGraphicsDropShadowEffect)
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QIcon, QDragEnterEvent, QDropEvent

from util.file_engine import FileEngine
from util.db_manager import db_manager

from widgets.folder_widget import FolderWidget
from widgets.image_widget import ImageWidget
from widgets.file_widget import FileWidget
from widgets.path_bar import PathBar


class FileArea(QWidget):

    COLUMNS = 7

    folder_status_signal = pyqtSignal(list)
    image_status_signal = pyqtSignal(list)
    file_status_signal = pyqtSignal(list)

    FOLDER_TYPES = {"Normal" : "N", "Image Folder" : "I", "Video Folder" : "V","Document Folder" : "D",
                    "System Folder" : "S", "Red" : "RED", "Green" : "GREEN", "Blue" : "BLUE"}

    def __init__(self, db_manager : db_manager ,parent = None, * , path = ""):
        super(FileArea, self).__init__(parent)
        # declare the attributes
        self.parent = parent
        self.db_manager = db_manager
        self.file_engine = FileEngine(db_manager, self)
        if path:
            self.file_engine.current_path = path
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
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(self.grid)
        vbox.addLayout(hbox)
        self.mainWidget.setLayout(vbox)

        # create the toolbar and add to the main layout
        tool_bar = self.setUpToolBar()

        # create the search and path widget area
        search_bar = self.setUpSearchBar()
        # main layout
        main_lyt = QVBoxLayout()
        main_lyt.setContentsMargins(0, 0, 0, 0)
        main_lyt.setSpacing(0)

        main_lyt.addWidget(tool_bar)
        main_lyt.addLayout(search_bar, 1)
        main_lyt.addWidget(scroll_area)
        self.setLayout(main_lyt)


        # open the current folder
        self.openFolder(self.file_engine.current_path)

    def setUpToolBar(self):

        # create the grid
        self.tool_bar = QToolBar()
        self.tool_bar.setObjectName("file-area-tool-bar")
        self.tool_bar.setContentsMargins(0, 0, 0, 0)
        # tool_bar.setIconSize(QSize(50, 50))
        self.tool_bar.setMaximumHeight(220)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.tool_bar.addWidget(self.navigationBox())

        self.tool_bar.addSeparator()

        self.tool_bar.addWidget(self.newBox())

        self.tool_bar.addSeparator()

        self.tool_bar.addWidget(self.viewBox())

        self.tool_bar.addSeparator()

        self.tool_bar.addWidget(self.actionBox())

        return self.tool_bar

    def navigationBox(self):
         # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("Navigations")

        # create the actions
        home_action = self.action_button("", QIcon("img/sys/home.png"), self.home)

        back_action = self.action_button("", QIcon("img/sys/back.png"), self.goBackward)

        forward_action = self.action_button("", QIcon("img/sys/right-arrow.png"), self.goForward)


        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        grid.addWidget(home_action, 0, 0)
        grid.addWidget(back_action, 1, 0)
        grid.addWidget(forward_action, 1 ,1)


        gr_box.setLayout(grid)
        return gr_box


    def viewBox(self):

        # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("View Options")

        # add the view changed combo box
        self.viewChangedBox = QComboBox()
        self.viewChangedBox.setIconSize(QSize(35, 35))
        self.viewChangedBox.addItem(QIcon("img/sys/list_view.png"), "List", 0)
        self.viewChangedBox.addItem(QIcon("img/sys/grid_view.png"), "Grid", 1)
        self.viewChangedBox.currentIndexChanged.connect(self.changeFolderMode)

        refresh_button = self.action_button("", QIcon("img/sys/refresh-arrow.png"), self.refresh)

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(QLabel("Item View"), 0, 0)
        grid.addWidget(self.viewChangedBox, 1, 0)
        grid.addWidget(refresh_button, 0, 1, 2, 1, alignment=Qt.AlignVCenter)

        gr_box.setLayout(grid)
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
        hbox = QGridLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(new_folder_action, 0, 0)
        hbox.addWidget(add_files_action, 1, 0)

        gr_box.setLayout(hbox)
        return gr_box

    def actionBox(self):

        # create the group box
        gr_box = QGroupBox()
        gr_box.setTitle("Actions")

        open_action = self.action_button("Open", QIcon("img/sys/open-folder.png"), self.openSelectFolder)
        rename_action = self.action_button("Rename", QIcon("img/sys/rename.png"), self.renameSeletedFolder)
        delete_action = self.action_button("Delete", QIcon("img/sys/delete.png"), self.deleteSelected)
        permant_delete_action = self.action_button("Remove", QIcon("img/sys/close.png"), self.removeSelected)
        copy_action = self.action_button("Copy", QIcon("img/sys/copy.png"), lambda : None)
        move_action = self.action_button("Move", QIcon("img/sys/forward.png"), lambda : None)

        self.actions = [open_action, rename_action, delete_action, copy_action, move_action, permant_delete_action]
        [action.setDisabled(True) for action in self.actions]

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(open_action, 0, 0)
        grid.addWidget(rename_action, 0, 1)
        grid.addWidget(delete_action, 0, 2)
        grid.addWidget(copy_action, 1, 0)
        grid.addWidget(move_action, 1, 1)
        grid.addWidget(permant_delete_action, 1, 2)

        gr_box.setLayout(grid)
        return gr_box

    def action_button(self, text, icon, func):

        button = QPushButton(text)
        button.setIcon(icon)
        button.setIconSize(QSize(35, 35))
        button.setObjectName("action_button")
        # button.setLayoutDirection(Qt.RightToLeft)
        # set the signal slot function
        button.pressed.connect(func)

        return button

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

    def showAndHideToolPanel(self, button : QPushButton):

        # create the animation for toolbar
        self.toolBarAnimation = QPropertyAnimation(self.tool_bar, b'maximumHeight')
        self.toolBarAnimation.setStartValue(self.tool_bar.height())
        self.toolBarAnimation.setDuration(500)

        if self.tool_bar.maximumHeight() >= 220:
            self.toolBarAnimation.setEndValue(0)
            self.toolBarAnimation.setEasingCurve(QEasingCurve.OutCubic)
            # set the button mew icon
            button.setIcon(QIcon("img/sys/expand_more.png"))
        else:
            self.toolBarAnimation.setEndValue(220)
            self.toolBarAnimation.setEasingCurve(QEasingCurve.OutCubic)
            # set the button new icon
            button.setIcon(QIcon("img/sys/expand_less.png"))

        self.toolBarAnimation.start()


    def setUpSearchBar(self):

        # create the widget
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 20, 0, 20)

        searchButton = QPushButton("")
        searchButton.setIcon(QIcon("img/sys/search.png"))
        searchButton.setIconSize(QSize(25, 25))
        searchButton.pressed.connect(self.showAndHideSearchBar)
        searchButton.setObjectName("search-bar-button")


        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Anything")
        self.search_bar.setObjectName("search-bar")
        # self.search_bar.resize(QSize(450, 25))
        self.search_bar.setMaximumWidth(0)
        # self.search_bar.hide()
        # set the action for search bar
        self.search_bar.textChanged.connect(self.searchFolderFiles)

        # create the path bar
        self.path_bar = PathBar(self.file_engine.getStringPath(self.file_engine.current_path), self.file_engine.current_path)
        self.path_bar.path_signal.connect(self.pathBarClicked)

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

        # create the button for hide and show the tool panel
        toolPanelHideShowButton = QPushButton()
        toolPanelHideShowButton.setObjectName("hide-button")
        toolPanelHideShowButton.setIcon(QIcon("img/sys/expand_more.png"))
        toolPanelHideShowButton.pressed.connect(lambda e= toolPanelHideShowButton : self.showAndHideToolPanel(e))

        hbox.addWidget(searchButton)
        hbox.addWidget(self.search_bar)
        hbox.addWidget(self.path_bar)
        hbox.addStretch()
        hbox.addWidget(QLabel("Sort by"))
        hbox.addWidget(self.sortComboBox)
        hbox.addWidget(self.reverseSortBox)
        hbox.addSpacing(15)
        hbox.addWidget(toolPanelHideShowButton)

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
            # set the signal slots
            if isinstance(widget , ImageWidget):
                widget.image_open_signal.connect(self.loadToPhotoViwer)
            elif widget.isVideoFile():
                widget.video_play_singal.connect(self.loadToVideoPlayer)
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

    def refresh(self):

        self.openFolder(self.file_engine.current_path)

    def renameSeletedFolder(self):

        if self.selected_widget and isinstance(self.selected_widget, FolderWidget):
            self.selected_widget.rename()

    def deleteSelected(self):

        self.selected_widget.delete()

    def removeSelected(self):

        self.selected_widget.remove()

    def newFolder(self):

        name, ok = QInputDialog.getText(self, "New Folder", "Folder Name:", text="New Folder")
        if ok:
            type_, ok = QInputDialog.getItem(self, "Folder Type", "Select Folder Type", self.FOLDER_TYPES.keys(), 0)
            if ok:
                folder_widget = self.file_engine.new_folder(name, type_)
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
                    self.grid.addWidget(folder_widget, (count - 1) // FileArea.COLUMNS, (count - 1) % FileArea.COLUMNS)

                    x = len([*self.folders, *self.files]) - 1
                    if x % FileArea.COLUMNS != 0:
                        while x % FileArea.COLUMNS != 0:
                            x += 1
                            label = QLabel()
                            self.temp_labels.append(label)
                            self.grid.addWidget(label, x // FileArea.COLUMNS, x % FileArea.COLUMNS)

    def addFiles(self):

        files, ok = QFileDialog.getOpenFileNames(self, "Add Files", "", "All File(*.*)")
        if ok:
            file_widgets = self.file_engine.add_files(files)

    def populateFileWidgets(self, file_widgets : list):

        count = len([*self.files, *self.folders])
        for w in file_widgets:
            self.files.append(w)
            w.changeView(self.viewChangedBox.currentIndex())

            # connect signal slots
            if isinstance(w, ImageWidget):
                w.image_open_signal.connect(self.loadToPhotoViwer)
            elif w.isVideoFile():
                w.video_play_singal.connect(self.loadToVideoPlayer)

        # add to the grid view this files
        if self.viewChangedBox.currentIndex() == 0:
            for i, w in enumerate(file_widgets):
                self.grid.addWidget(w, i + count, 0)

        elif self.viewChangedBox.currentIndex() == 1:
            [w.deleteLater() for w in self.temp_labels]
            self.temp_labels.clear()

            for i, w in enumerate(file_widgets):
                self.grid.addWidget(w, (i + count) // FileArea.COLUMNS, (i + count) % FileArea.COLUMNS)

            x = len([*self.folders, *self.files]) - 1
            if x % FileArea.COLUMNS != 0:
                while x % FileArea.COLUMNS != 0:
                    x += 1
                    label = QLabel()
                    self.temp_labels.append(label)
                    self.grid.addWidget(label, x // FileArea.COLUMNS, x % FileArea.COLUMNS)

    def cleanArea(self):

        for widget in [*self.folders, *self.files, *self.temp_labels]:
            widget.deleteLater() # delete the all widgets in the file area


        self.folders.clear()
        self.files.clear()
        self.temp_labels.clear()

    def removeWidgetsFromGrid(self):

        [w.deleteLater() for w in self.temp_labels] # delete the temp labels
        for widget in [*self.folders , *self.files]:
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
                self.grid.addWidget(w, i//FileArea.COLUMNS, i%FileArea.COLUMNS)

            if x % FileArea.COLUMNS != 0:
                while x%FileArea.COLUMNS != 0:
                    x += 1
                    label = QLabel()
                    self.temp_labels.append(label)
                    self.grid.addWidget(label, x//FileArea.COLUMNS, x % FileArea.COLUMNS)



        else:
            print("None")

    def selected(self, folder_wigdet : FolderWidget):

        for w in [*self.folders, *self.files]:
            if w == folder_wigdet and w is not None:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = folder_wigdet
        [a.setDisabled(False) for a in self.actions]
        #
        # fire the status signal
        self.folder_status_signal.emit([self.selected_widget.name, self.selected_widget.path, self.selected_widget.time, self.selected_widget.fav])

    def selectFile(self, file_widget):

        for w in [*self.folders, *self.files]:
            if w == file_widget and w is not None:
                w.selected()
            else:
                w.unselected()

        self.selected_widget = file_widget
        [a.setDisabled(False) for a in self.actions]

        if self.selected_widget:
            if isinstance(file_widget, ImageWidget):
                self.image_status_signal.emit([file_widget.file, file_widget.path, file_widget.time, file_widget.fav])
            elif isinstance(file_widget, FileWidget):
                self.file_status_signal.emit([file_widget.file, file_widget.path, file_widget.time, file_widget.fav])


    def home(self):

        self.openFolder(".")

    def getViewIndex(self):

        return self.viewChangedBox.currentIndex()

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
        self.changeFolderMode(self.getViewIndex())

    def searchFolderFiles(self, text: str):

        for widget in self.folders:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

        for widget in self.files:
            if text.lower() in widget.file.lower():
                widget.show()
            else:
                widget.hide()

    def loadToPhotoViwer(self, current_file : str):

        image_files = []
        for w in self.files:
            if isinstance(w, ImageWidget):
                image_files.append(w.file)

        self.parent.openImages(image_files, image_files.index(current_file))

    def loadToVideoPlayer(self, current_file  : str):

        video_files = []
        for w in self.files:
            if w.isVideoFile():
                video_files.append(w.file)

        # call to the parent load video player method
        self.parent.openVideo(video_files, video_files.index(current_file))

    def dragEnterEvent(self, event : QDragEnterEvent) -> None:

        if event.mimeData().hasUrls():
            event.accept() # accept the dragged data
            event.setDropAction(Qt.CopyAction) # mark as the copy action
            return
        event.ignore()

    def dropEvent(self, event : QDropEvent) -> None:

        if event.mimeData().hasUrls():
            event.accept()
            # get the urls and convert it to the local file paths
            local_files = list(map(lambda e : e.toLocalFile() , event.mimeData().urls()))
            # call to the file engine add file method
            file_widgets = self.file_engine.add_files(local_files)
            # place widgets in the file area
            self.populateFileWidgets(file_widgets)
            return
        event.ignore()



