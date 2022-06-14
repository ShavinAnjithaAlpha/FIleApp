from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QDockWidget, QTabWidget,
                             QTabBar, QToolBar, QDesktopWidget, QScrollArea, QLabel)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

from widgets.file_area import FileArea
from widgets.status_widget_factory import WidgetFactory
from widgets.favorite_panel import FavoritePanel
from widgets.folder_tree_widget import FolderTreeWidget

from apps.photo_viewer import PhotoViewer
from apps.video_player import VideoPlayer

from util.db_manager import db_manager

from style_sheets.main_style_sheet import style_sheet

class FileApp(QMainWindow):
    def __init__(self):
        super(FileApp, self).__init__()
        # view mode index
        self.view_mode_index = 0
        self.initializeUI()


    def initializeUI(self):

        self.full_size = QDesktopWidget().screenGeometry(-1).size()
        # declare the main current file area object
        self.current_file_area = None
        self.db_manager = db_manager()

        self.setWindowTitle("Files Manager")
        self.resize(self.full_size) # resize the window to the size of desktop
        # set up the toolbar
        self.setUpToolBar()
        # set up the dock area
        self.setUpDock()
        # set up the central widget
        self.setUpCentral()

        self.show() # shoe window on the screen

    def setUpDock(self):
        # declare the dock widgets list
        self.docks_widgets = []

        # create the dock area
        self.dock = QDockWidget("Status Bar", self)
        self.dock.setMinimumWidth(int(self.full_size.width() * 0.2))
        self.dock.setAllowedAreas(Qt.RightDockWidgetArea)

        self.dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)


        # create the scroll area for dock widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        # create the vbox for the dock widget
        self.dock_vbox = QVBoxLayout()
        self.dock_vbox.setContentsMargins(0, 0, 0, 0)
        self.dock_vbox.setSpacing(0)

        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.dock_vbox)
        scroll_area.setWidget(widget)
        self.dock.setWidget(scroll_area)

        self.addTreeView() # set up the tree view in the dock widget area

    def addTreeView(self):

        self.tree = FolderTreeWidget(self.db_manager)
        self.docks_widgets.append(self.tree)
        self.dock_vbox.addWidget(QLabel())
        self.dock_vbox.insertWidget(1, self.tree)

        self.tree.doubleClicked.connect(self.openFolder)


    def setUpToolBar(self):

        # create the toolbar
        self.tool_bar = QToolBar("Tool Bar")
        self.tool_bar.setIconSize(QSize(20, 20))
        self.tool_bar.setFixedHeight(int(self.full_size.height() * 0.09))
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)



        self.tool_bar.addAction(QIcon("img/sys/trash.png"), "Recycle Bin",
                                self.openRecycleBin)
        self.tool_bar.addAction(QIcon("img/sys/star.png"), "Favorites",
                                self.openFavorites)



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
        self.current_file_area = FileArea(self.db_manager, self)
        # bind the file area to signal slots
        self.current_file_area.folder_status_signal.connect(self.createFolderStatus)
        self.current_file_area.image_status_signal.connect(self.createImageStatus)
        self.current_file_area.file_status_signal.connect(self.createFileStatus)

        self.tab_bar.addTab(self.current_file_area , "Home")
        self.tab_bar.setCurrentIndex(0)

    def addNewFileTab(self, event):

        if event == self.tab_bar.tabBar().count() - 1:
            self.current_file_area = FileArea(self.db_manager, self)
            self.current_file_area.folder_status_signal.connect(self.createFolderStatus)
            self.current_file_area.image_status_signal.connect(self.createImageStatus)
            self.current_file_area.file_status_signal.connect(self.createFileStatus)

            self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.current_file_area, "Home({})".format(self.tab_bar.count()))

            self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

    def closeTab(self, event):

        if self.tab_bar.tabBar().count() == 2:
            QApplication.quit()

        widget = self.tab_bar.widget(event)
        self.tab_bar.tabBar().removeTab(event)

    def changeFolderView(self, index : int):

        self.view_mode_index = index
        for i in range(self.tab_bar.tabBar().count() - 1):
            self.tab_bar.widget(i).changeFolderMode(index)

    def viewModeIndex(self):
        return self.view_mode_index

    def createFolderStatus(self, data : list):

        info = {
            "Name" : data[0],
            "Path" : data[1],
            "Created at" : data[2].__str__(),
            "favorite" : data[3]
        }

        status_widget = WidgetFactory.FolderStatusWidget(data[1], info)
        if len(self.docks_widgets) == 1:
            self.dock_vbox.insertWidget(0, status_widget)
            self.dock_vbox.addStretch()
            self.docks_widgets.append(status_widget)

        else:
            # first remove the status widget
            self.dock_vbox.removeWidget(self.docks_widgets[1])
            self.docks_widgets[1].deleteLater()
            # update the list
            self.docks_widgets.insert(1, status_widget)
            self.dock_vbox.insertWidget(0, status_widget)

    def createImageStatus(self, data : list):

        info = {
            "File" : data[0],
            "Path" : data[1],
            "Added at" : data[2],
            "Favorite" : data[3]
        }

        status_widget = WidgetFactory.ImageStatusWidget(info)

        if len(self.docks_widgets) == 1:
            self.dock_vbox.insertWidget(0, status_widget)
            self.dock_vbox.addStretch()
            self.docks_widgets.append(status_widget)

        else:
            # first remove the status widget
            self.dock_vbox.removeWidget(self.docks_widgets[1])
            self.docks_widgets[1].deleteLater()
            # update the list
            self.docks_widgets.insert(0, status_widget)
            self.dock_vbox.insertWidget(1, status_widget)

    def createFileStatus(self, data : list):

        info = {
            "File" : data[0],
            "Path" : data[1],
            "Added at" : data[2],
            "Favorite" : data[3]
        }

        status_widget = WidgetFactory.FileStatusWidget(info)
        if len(self.docks_widgets) == 1:
            self.dock_vbox.insertWidget(0, status_widget)
            self.dock_vbox.addStretch()
            self.docks_widgets.append(status_widget)

        else:
            # first remove the status widget
            self.dock_vbox.removeWidget(self.docks_widgets[1])
            self.docks_widgets[1].deleteLater()
            # update the list
            self.docks_widgets.insert(0, status_widget)
            self.dock_vbox.insertWidget(1, status_widget)

    def openRecycleBin(self):

        self.current_file_area = FileArea(self.db_manager, self)
        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.current_file_area, "Recycle Bin")

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

        pass

    def openFavorites(self):

        self.favorite_area = FavoritePanel(self.db_manager, self)
        self.favorite_area.folder_open_signal.connect(self.openFavoriteFolder)
        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.favorite_area, "Favorite")

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)


    def openFavoriteFolder(self, path : str):

        self.current_file_area = FileArea(self.db_manager, self, path = path)
        # self.current_file_area.openFolder(path)
        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.current_file_area, "Home(%d)".format(self.tab_bar.count()))

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

    def openImages(self, images : list[str], index : int):

        # create the photo viewer widget
        photoViewer = PhotoViewer(images, index)

        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, photoViewer,
                               "Image Viewer")

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

    def openVideo(self, video_list : list[str], index : int):

        # create the photo viewer widget
        videoViewer = VideoPlayer(video_list, index)

        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, videoViewer,
                               "Image Viewer")

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

    def openFolder(self, index):

        path = self.tree.model.item(index.row(), 0).item[1]
        if self.current_file_area:
            self.current_file_area.openFolder(path)

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(style_sheet)
    window = FileApp()
    app.exec_()

