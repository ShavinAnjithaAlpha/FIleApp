from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap
import datetime

from util.Folder import Folder

from style_sheets.folder_style_sheet import style_sheet

class FolderWidget(Folder, QWidget):
    def __init__(self, name, path, time, fav, parent = None):
        super(FolderWidget, self).__init__(name, path, time, fav)
        QWidget.__init__(self, parent)
        self.parent = parent

        # create the folder name text , create date and time and icon
        self.name_label = QLabel(self.name)
        self.name_label.setObjectName("name-label")

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(QSize(150, 120))
        icon = QPixmap("img/sys/folder (1).png").scaled(self.icon_label.size() , Qt.KeepAspectRatio, Qt.FastTransformation)
        self.icon_label.setPixmap(icon)

        self.time_label = QLabel(self.time)
        self.time_label.setObjectName("time-label")

        self.favorite_button = QPushButton()
        self.favorite_button.setObjectName("fav-button")
        self.favorite_button.setIcon(QIcon("img/sys/star.png"))

        # create the grid
        grid = QGridLayout()
        grid.addWidget(self.favorite_button, 0, 2)
        grid.addWidget(self.icon_label, 1, 0, 2, 1)
        grid.addWidget(self.name_label, 1, 1)
        grid.addWidget(self.time_label, 2, 2)

        # create the base widget
        baseWidget = QWidget()
        baseWidget.setObjectName("folder-base")
        baseWidget.setLayout(grid)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(baseWidget)
        self.setStyleSheet(style_sheet)

    def contextMenuEvent(self, event : QContextMenuEvent) -> None:

        # create the context menu for folder
        folderMenu = QMenu(self)
        folderMenu.setTitle("Folder Actions")

        # create the folder actions here
        open_action = QAction(QIcon("img/sys/open-folder (1).png"),"Open", self)
        open_action.triggered.connect(lambda e : self.parent.openFolder(self.path))
        folderMenu.addAction(open_action)

        rename_action = QAction(QIcon("img/sys/rename.png"), "Rename", self)
        folderMenu.addAction(rename_action)

        lock_action = QAction(QIcon("img/sys/lock.png"), "Lock", self)
        folderMenu.addAction(lock_action)

        fav_action = QAction(QIcon("img/sys/star.png") , "Set Favorite", self)
        folderMenu.addAction(fav_action)

        delete_action = QAction(QIcon("img/sys/delete.png"),"Delete", self)
        folderMenu.addAction(delete_action)


        folderMenu.exec_(self.mapToGlobal(event.pos()))

    def mouseDoubleClickEvent(self,event : QMouseEvent) -> None:

        self.parent.openFolder(self.path)
        # stop propagate the signal
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    w = FolderWidget("shavin", ".0", "2022.12.12", False)
    w.show()
    print()
    app.exec_()