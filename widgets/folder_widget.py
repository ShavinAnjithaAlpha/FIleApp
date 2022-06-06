from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt, QSize, QTime, QDate
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap
import datetime

from util.Folder import Folder

from style_sheets.folder_style_sheet import style_sheet

class FolderWidget(Folder, QWidget):
    def __init__(self, name, path, time, fav, type = 'N' , pw = None ,parent = None):
        super(FolderWidget, self).__init__(name, path, time, fav)
        QWidget.__init__(self, parent)
        self.parent = parent
        self.password = pw

        # create the folder name text , create date and time and icon
        self.name_label = QLabel(self.name)
        self.name_label.setObjectName("name-label")

        self.icon_label = QLabel()
        self.icon_label.setFixedHeight(120)
        self.setFolderIcon(type)

        self.time_label = QLabel(self.formatTime(f"{self.time}"))
        self.time_label.setObjectName("time-label")

        self.setUpFavoriteButton()

        # create the grid
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        # self.changeView(0)

        # create the base widget
        self.baseWidget = QWidget()
        self.baseWidget.setContentsMargins(0, 0, 0, 0)
        self.baseWidget.setObjectName("folder-base")
        self.baseWidget.setLayout(self.grid)

        self.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.layout().addWidget(self.baseWidget)
        self.setStyleSheet(style_sheet)

    def setUpFavoriteButton(self):

        self.favorite_button = QPushButton()
        self.favorite_button.setFixedSize(QSize(30, 30))
        self.favorite_button.setObjectName("fav-button")
        self.favorite_button.setIconSize(QSize(25, 25))
        self.favorite_button.pressed.connect(self.changeFav)

        if self.fav:
            self.favorite_button.setIcon(QIcon("img/sys/star.png"))
        else:
            self.favorite_button.setIcon(QIcon("img/sys/star (1).png"))

    def changeFav(self):

        self.fav = not self.fav
        self.parent.file_engine.db_manager.change_favorite_folder(self.path ,self.fav)
        if self.fav:
            self.favorite_button.setIcon(QIcon("img/sys/star.png"))
        else:
            self.favorite_button.setIcon(QIcon("img/sys/star (1).png"))

    def changeView(self, index):

        # first remove the widget from grid
        for w in [self.name_label, self.time_label, self.icon_label, self.favorite_button]:
            self.grid.removeWidget(w)

        if index == 0:
            self.name_label.setWordWrap(False)
            self.grid.addWidget(self.favorite_button, 0, 3, alignment=Qt.AlignRight|Qt.AlignTop)
            self.grid.addWidget(self.icon_label, 0, 0, 1, 1)
            self.grid.addWidget(self.name_label, 0, 1, alignment=Qt.AlignLeft)
            self.grid.addWidget(self.time_label, 0, 2)

            self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum))
            self.setMaximumWidth(2000)

        elif index == 1:
            self.name_label.setWordWrap(True)
            self.grid.addWidget(self.favorite_button, 0, 0)
            self.grid.addWidget(self.icon_label, 1, 0, 1, 1)
            self.grid.addWidget(self.name_label, 2, 0, 1, 1)
            # adjust th size of the  widget
            self.setFixedWidth(230)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum))

        else:
            pass

    def contextMenuEvent(self, event : QContextMenuEvent) -> None:

        # create the context menu for folder
        folderMenu = QMenu(self)
        folderMenu.setTitle("Folder Actions")

        # create the folder actions here
        open_action = QAction(QIcon("img/sys/open-folder (1).png"),"Open", self)
        open_action.triggered.connect(lambda e : self.parent.openFolder(self.path))
        folderMenu.addAction(open_action)

        rename_action = QAction(QIcon("img/sys/rename.png"), "Rename", self)
        rename_action.triggered.connect(self.rename)
        folderMenu.addAction(rename_action)

        typeChangedAction = QMenu("Changed Folder Color")
        typeChangedAction.setIcon(QIcon("img/sys/widget.png"))
        folderMenu.addMenu(typeChangedAction)

        for color, icon in {"Red" : QIcon("img/sys/circle.png"), "Green" : QIcon("../img/sys/circle (1).png"),
                            "Blue" : QIcon("img/sys/circle (1).png"), "Orange" : QIcon("img/sys/circle (2).png"), "Yellow": QIcon(),
                            "Image Folder": QIcon("img/sys/image_folder.png"),
                            "Video Folder" : QIcon("img/sys/video_folder.png"),
                            "Document Folder" : QIcon("img/sys/doc_folder.png"),
                            "Normal Folder": QIcon("img/sys/folder (1).png")}.items():
            action = QAction(icon, color, self)
            typeChangedAction.addAction(action)

        lock_action = QAction(QIcon("img/sys/lock.png"), "Lock", self)
        folderMenu.addAction(lock_action)

        fav_action = QAction(QIcon("img/sys/star.png") , "Change Favorite", self)
        fav_action.triggered.connect(self.changeFav)
        folderMenu.addAction(fav_action)

        folderMenu.addSeparator()

        copy_action = QAction(QIcon("img/sys/copy.png"), "Copy", self)
        folderMenu.addAction(copy_action)

        move_action = QAction(QIcon("img/sys/forward.png"), "Move", self)
        folderMenu.addAction(move_action)

        folderMenu.addSeparator()

        delete_action = QAction(QIcon("img/sys/delete.png"),"Delete", self)
        delete_action.triggered.connect(self.delete)
        folderMenu.addAction(delete_action)

        remove_action = QAction(QIcon("img/sys/delete.png"), "Remove", self)
        remove_action.triggered.connect(self.remove)
        folderMenu.addAction(remove_action)


        folderMenu.exec_(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, event : QMouseEvent) -> None:

        self.parent.selected(self)
        event.accept()


    def mouseDoubleClickEvent(self,event : QMouseEvent) -> None:

        self.parent.openFolder(self.path)
        # stop propagate the signal
        event.accept()

    def selected(self):

        self.baseWidget.setObjectName("selected-folder-base")
        self.setStyleSheet(style_sheet)

    def unselected(self):

        self.baseWidget.setObjectName("folder-base")
        self.setStyleSheet(style_sheet)

    def formatTime(self, text : str):

        date, time = text.split(" ")
        time_ , date_ = QTime.fromString(time.split(".")[0], "hh:mm:ss") , QDate.fromString(date, "yyyy-MM-dd")

        formatted_date, formatted_time = date_.toString("yyyy MMM dd"), time_.toString("hh:mm A")

        return f"created on {formatted_date} {formatted_time}"

    def rename(self):

        name, ok = QInputDialog.getText(self, "Rename Folder", "Folder New Name:", text=self.name)
        if ok:
            self.parent.file_engine.db_manager.rename_folder(self.path, name)
            # set the label name
            self.name = name
            self.name_label.setText(name)

    def delete(self):

        # ask first for confirmation
        button = QMessageBox()
        button.setIconPixmap(
            QPixmap("img/sys/delete.png").scaled(QSize(60, 60), Qt.KeepAspectRatio, Qt.FastTransformation))
        button.setText("Are you sure to delete\n '{}' folder?".format(self.name))
        button.setWindowTitle("Remove Folder")
        button.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if button.exec() == QMessageBox.StandardButton.Yes:
            # remove the folder to the recycle bin
            x = self.parent.db_manager.deleteFolder(self.path)
            if x:
                # remove from the file area folder list
                self.parent.folders.remove(self)
                # delete the folder widget
                self.deleteLater()

    def remove(self):

        # ask first for confirmation
        button = QMessageBox()
        button.setIconPixmap(QPixmap("img/sys/close.png").scaled(QSize(60, 60), Qt.KeepAspectRatio, Qt.FastTransformation))
        button.setText("Are you sure to remove permantly\n '{}' folder?".format(self.name))
        button.setWindowTitle("Remove Folder")
        button.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

        if button.exec() == QMessageBox.StandardButton.Yes:
            # remove the folder to the recycle bin
            x = self.parent.db_manager.removeFolder(self.path)
            if x:
                # remove from the file area folder list
                self.parent.folders.remove(self)
                # delete the folder widget
                self.deleteLater()

    def setFolderIcon(self, type : str):

        if type == "N":
            icon = QPixmap("img/sys/folder (1).png").scaledToHeight(self.icon_label.height())
        elif type == "I":
            icon = QPixmap("img/sys/image_folder.png").scaledToHeight(self.icon_label.height())
        elif type == "V":
            icon = QPixmap("img/sys/video_folder.png").scaledToHeight(self.icon_label.height())
        elif type == "D":
            icon = QPixmap("img/sys/doc_folder.png").scaledToHeight(self.icon_label.height())
        elif type == "GREEN":
            icon = QPixmap("img/sys/green_folder.png").scaledToHeight(self.icon_label.height())
        elif type == "YELLOW":
            icon = QPixmap("img/sys/yellow_folder.png").scaledToHeight(self.icon_label.height())
        self.icon_label.setPixmap(icon)


if __name__ == "__main__":
    app = QApplication([])
    w = FolderWidget("shavin", ".0", "2022.12.12", False)
    w.show()
    print()
    app.exec_()