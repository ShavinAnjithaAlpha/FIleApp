from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QGridLayout, QTabWidget,
                             QTabBar, QToolBar, QDesktopWidget, QScrollArea, QLabel, QSplitter, QPushButton)
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon

from widgets.file_area import FileArea
from widgets.status_widget_factory import WidgetFactory
from widgets.favorite_panel import FavoritePanel
from widgets.folder_tree_widget import FolderTreeWidget
from widgets.about_dialog import AboutDialog

from apps.photo_viewer import PhotoViewer
from apps.video_player import VideoPlayer

from util.db_manager import db_manager
from util.clipboard import ClipBoard, CopiedItem

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
        self.db_manager = db_manager() # initialize the db manager instance globally for handle database side
        self.clipboard = ClipBoard(self.db_manager) # initialize clipboard instance for store copied items globally

        self.setWindowTitle("File App ~beta version 1.0")
        self.setWindowIcon(QIcon("img/sys/FileAppIcon.png"))
        self.resize(self.full_size) # resize the window to the size of desktop
        # set up the toolbar
        self.setUpToolBar()
        # set up the dock area
        # self.setUpDock()
        # set up the central widget
        self.setUpCentral()

        self.show() # shoe window on the screen

    def setUpDock(self, splitter : QGridLayout):
        # declare the dock widgets list
        self.docks_widgets = []

        # create the scroll area for dock widget
        scroll_area = QScrollArea()
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


        # create the vbox for the dock widget
        self.dock_vbox = QVBoxLayout()
        self.dock_vbox.setContentsMargins(0, 0, 0, 0)
        self.dock_vbox.setSpacing(0)

        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.dock_vbox)
        scroll_area.setWidget(widget)
        # self.dock.setWidget(scroll_area)

        hideButton = QPushButton()
        hideButton.setObjectName("hide-button")
        hideButton.setIcon(QIcon("img/sys/arrow_forward.png"))
        hideButton.pressed.connect(lambda e = scroll_area, b = hideButton : self.hideStatusPanel(e, b))

        # splitter.addWidget(hideButton)
        splitter.addWidget(scroll_area, 0, 2)
        splitter.addWidget(hideButton, 0, 1, alignment=Qt.AlignTop)
        scroll_area.setMaximumWidth(int(self.width() * 0.21))


        self.addTreeView() # set up the tree view in the dock widget area

    def addTreeView(self):

        self.tree = FolderTreeWidget(self.db_manager)
        self.docks_widgets.append(self.tree)
        self.dock_vbox.addWidget(QLabel())
        self.dock_vbox.insertWidget(1, self.tree)

        self.tree.doubleClicked.connect(self.openFolder)

    def hideStatusPanel(self, scroll_area : QScrollArea, button : QPushButton):

        self.statusPanelAnimation = QPropertyAnimation(scroll_area, b'maximumWidth')
        self.statusPanelAnimation.setStartValue(scroll_area.width())
        self.statusPanelAnimation.setEasingCurve(QEasingCurve.OutCubic)
        self.statusPanelAnimation.setDuration(600)

        if scroll_area.width() > 0:
            self.statusPanelAnimation.setEndValue(0)
            self.statusPanelAnimation.start()
            button.setIcon(QIcon("img/sys/arrow_back.png"))
        else:
            self.statusPanelAnimation.setEndValue(int(self.width() * 0.21))
            self.statusPanelAnimation.start()
            button.setIcon(QIcon("img/sys/arrow_forward.png"))


    def setUpToolBar(self):

        # create the toolbar
        self.tool_bar = QToolBar("Tool Bar")
        self.tool_bar.setIconSize(QSize(30, 30))
        # self.tool_bar.setFixedHeight(int(self.full_size.height() * 0.09))
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)



        self.tool_bar.addAction(QIcon("img/sys/trash-free-icon-font.png"), "Recycle Bin",
                                self.openRecycleBin)
        self.tool_bar.addAction(QIcon("img/sys/heart-free-icon-font (1).png"), "Favorites",
                                self.openFavorites)
        self.tool_bar.addAction(QIcon("img/sys/info-free-icon-font.png"), "About",
                                self.openAbout)
        self.tool_bar.addAction(QIcon("img/sys/off.png"), "Exit",
                                lambda : QApplication.exit(0))



    def setUpCentral(self):

        # create the tab bar widget
        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setTabShape(QTabWidget.Rounded)

        # set the tab closed request slots for close the tab
        self.tab_bar.tabCloseRequested.connect(self.closeTab)
        # set the add tab bar button
        newTabButton = self.tab_bar.tabBar().addTab("+")
        self.tab_bar.tabBar().setTabButton(newTabButton, QTabBar.RightSide, None)
        self.tab_bar.tabBar().tabBarClicked.connect(self.addNewFileTab)



        # create the main tab widget
        self.current_file_area = FileArea(self.db_manager, self, clipboard=self.clipboard)
        # bind the file area to signal slots
        self.current_file_area.folder_status_signal.connect(self.createFolderStatus)
        self.current_file_area.image_status_signal.connect(self.createImageStatus)
        self.current_file_area.file_status_signal.connect(self.createFileStatus)

        self.tab_bar.addTab(self.current_file_area , "Home")
        self.tab_bar.setCurrentIndex(0)


        central_widget = QWidget()
        central_widget.setContentsMargins(0, 0, 0, 0)
        # create the splitter
        splitter_box = QGridLayout()
        splitter_box.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(splitter_box)
        splitter_box.addWidget(self.tab_bar, 0, 0)
        self.setUpDock(splitter_box)

        self.setCentralWidget(central_widget)

    def addNewFileTab(self, event):

        if event == self.tab_bar.tabBar().count() - 1:
            self.current_file_area = FileArea(self.db_manager, self ,clipboard=self.clipboard)
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
            "favorite" : data[3],
            "type" : data[4]
        }

        status_widget = WidgetFactory.FolderStatusWidget(data[1], info)
        if len(self.docks_widgets) == 1:
            self.dock_vbox.insertWidget(0, status_widget)
            self.dock_vbox.addStretch()
            self.docks_widgets.insert(0, status_widget)

        else:
            # first remove the status widget
            self.dock_vbox.removeWidget(self.docks_widgets[0])
            self.docks_widgets[0].deleteLater()
            # update the list
            self.docks_widgets.insert(0, status_widget)
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
            self.docks_widgets.insert(0, status_widget)

        else:
            # first remove the status widget
            self.dock_vbox.removeWidget(self.docks_widgets[0])
            self.docks_widgets[0].deleteLater()
            # update the list
            self.docks_widgets.insert(0, status_widget)
            self.dock_vbox.insertWidget(0, status_widget)

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
            self.docks_widgets.insert(0, status_widget)

        else:
            # first remove the status widget
            self.dock_vbox.removeWidget(self.docks_widgets[0])
            self.docks_widgets[0].deleteLater()
            # update the list
            self.docks_widgets.insert(0, status_widget)
            self.dock_vbox.insertWidget(0, status_widget)

    def openRecycleBin(self):

        self.current_file_area = FileArea(self.db_manager, self)
        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.current_file_area, "Recycle Bin")

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)

        pass

    def openFavorites(self):

        self.favorite_area = FavoritePanel(self.db_manager, self, clipboard=self.clipboard)
        self.favorite_area.folder_status_signal.connect(self.createFolderStatus)
        self.favorite_area.image_status_signal.connect(self.createImageStatus)
        self.favorite_area.file_status_signal.connect(self.createFileStatus)
        self.favorite_area.folder_open_signal.connect(self.openFavoriteFolder)
        self.tab_bar.insertTab(self.tab_bar.tabBar().count() - 1, self.favorite_area, "Favorite")

        self.tab_bar.setCurrentIndex(self.tab_bar.tabBar().count() - 2)


    def openFavoriteFolder(self, path : str):

        self.current_file_area = FileArea(self.db_manager, self, path = path, clipboard=self.clipboard)
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

    def openAbout(self):

        aboutDialog = AboutDialog()
        aboutDialog.exec_()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(style_sheet)
    window = FileApp()
    app.exec_()

