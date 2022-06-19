from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy, QGraphicsBlurEffect
from PyQt5.QtCore import Qt, QSize, QTime, QDate, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap

from util.Folder import Folder
from util.File import File

from style_sheets.folder_style_sheet import style_sheet

class FolderWidget(Folder, QWidget):

    FOLDER_TYPES = {"Normal": "N", "Image Folder": "I", "Video Folder": "V", "Document Folder": "D",
                    "System Folder": "S", "Code Folder" : "C", "Music Folder" : "M", "User Folder" : "U",
                    "Red": "RED", "Green": "GREEN", "Blue": "BLUE"}

    FOLDER_MENU_ICONS = {
        "Red": "img/sys/red_oval.png",
        "Green": "img/sys/green_oval.png",
        "Blue": "img/sys/blue_oval.png",
        "Orange": "img/sys/orange_oval.png",
        "Yellow": "img/sys/yellow_oval.png",
        "Image Folder": "img/sys/folder_icons/folder (9).png",
        "Video Folder": "img/sys/folder_icons/video-folder.png",
        "Document Folder": "img/sys/folder_icons/file-storage.png",
        "Normal Folder": "img/sys/folder_icons/yellow_folder.png",
        "System Folder" : "img/sys/folder_icons/folder (10).png",
        "Music Folder" : "img/sys/folder_icons/music-folder (1).png",
        "Code Folder" : "img/sys/folder_icons/folder (4).png",
        "User Folder" : "img/sys/folder_icons/folder (6).png"
    }

    FOLDER_ICONS = {
        "N" : "img/sys/folder_icons/yellow_folder.png",
        "I" : "img/sys/folder_icons/folder (9).png",
        "V" : "img/sys/folder_icons/video-folder.png",
        "D" : "img/sys/folder_icons/file-storage.png",
        "S" : "img/sys/folder_icons/folder (10).png",
        "C" : "img/sys/folder_icons/folder (4).png",
        "M" : "img/sys/folder_icons/music-folder (1).png",
        "U" : "img/sys/folder_icons/folder (6).png",
        "RED" : "img/sys/folder_icons/empty-folder (1).png",
        "GREEN" : "img/sys/folder_icons/green_folder.png",
        "BLUE" : "img/sys/folder_icons/blue_folder.png",
        "ORANGE" : "img/sys/folder_icons/orange_folder.png",
        "YELLOW" : "img/sys/folder_icons/yellow_folder.png"
    }


    ICON_HEIGHT = 80

    # declare custom signals for folder widget
    copy_signal = pyqtSignal([Folder, File])

    def __init__(self, name, path, time, fav, type = 'N' , pw = None ,parent = None):
        super(FolderWidget, self).__init__(name, path, time, fav, type)
        QWidget.__init__(self, parent)
        self.parent = parent
        self.password = pw

        # create the folder name text , create date and time and icon
        self.name_label = QLabel(self.name)
        self.name_label.setObjectName("name-label")
        self.name_label.adjustSize()

        self.icon_label = QLabel()
        # self.icon_label.setFixedHeight(self.ICON_HEIGHT)
        self.setFolderIcon(type)

        self.time_label = QLabel(self.formatTime(f"{self.time}"))
        self.time_label.setObjectName("time-label")

        self.setUpFavoriteButton()

        # create the grid
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(0)
        self.grid.setSpacing(0)
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
            self.favorite_button.setIcon(QIcon("img/sys/heart-free-icon-font (1).png"))
        else:
            self.favorite_button.setIcon(QIcon("img/sys/heart-free-icon-font.png"))

    def changeFav(self):

        self.fav = not self.fav
        self.parent.file_engine.db_manager.change_favorite_folder(self.path ,self.fav)
        if self.fav:
            self.favorite_button.setIcon(QIcon("img/sys/heart-free-icon-font (1).png"))
        else:
            self.favorite_button.setIcon(QIcon("img/sys/heart-free-icon-font.png"))


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

            # self.setMaximumHeight(300)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum))
            self.setMaximumWidth(2000)

        elif index == 1:
            self.name_label.setWordWrap(True)
            self.grid.addWidget(self.favorite_button, 0, 0, alignment=Qt.AlignLeft)
            self.grid.addWidget(self.icon_label, 1, 0, alignment=Qt.AlignCenter)
            self.grid.addWidget(self.name_label, 2, 0, alignment=Qt.AlignHCenter)
            # adjust th size of the  widget
            # self.setFixedWidth(230)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

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

        for color, icon in self.FOLDER_MENU_ICONS.items():
            action = QAction(QIcon(icon), color, self)
            action.triggered.connect(lambda e, x = color : self.changeColor(x)) # add the event slots to action
            typeChangedAction.addAction(action)

        lock_action = QAction(QIcon("img/sys/lock.png"), "Lock", self)
        folderMenu.addAction(lock_action)

        fav_action = QAction(QIcon("img/sys/star.png") , "Change Favorite", self)
        fav_action.triggered.connect(self.changeFav)
        folderMenu.addAction(fav_action)

        folderMenu.addSeparator()

        copy_action = QAction(QIcon("img/sys/copy.png"), "Copy", self)
        copy_action.triggered.connect(lambda e, x = True : self.copyFolder(x))
        folderMenu.addAction(copy_action)

        move_action = QAction(QIcon("img/sys/forward.png"), "Move", self)
        move_action.triggered.connect(lambda e , x = False : self.copyFolder(x))
        folderMenu.addAction(move_action)

        paste_action = QAction(QIcon("img/sys/file.png"), "Paste", self)
        paste_action.triggered.connect(self.pasteItem)
        folderMenu.addAction(paste_action)

        folderMenu.addSeparator()

        delete_action = QAction(QIcon("img/sys/delete.png"),"Delete", self)
        delete_action.triggered.connect(self.delete)
        folderMenu.addAction(delete_action)

        remove_action = QAction(QIcon("img/sys/close.png"), "Remove", self)
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
        button.setText("Are you sure to remove permanantly\n '{}' folder?".format(self.name))
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

        self.icon_label.setPixmap(QPixmap(self.FOLDER_ICONS.get(type, "img/sys/folder (3).png"))
                                  .scaledToHeight(self.ICON_HEIGHT))
        self.icon_label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        # adjust the image label size
        self.icon_label.adjustSize()

    def changeColor(self, type : str):

        # get color code
        code = self.FOLDER_TYPES.get(type, "N")
        # call to the db manager and save the changes
        self.parent.db_manager.change_folder_color(self.path, code)
        # change the current folder icon
        self.setFolderIcon(code)

    def copyFolder(self, copy_flag : bool):
        # copied the item to global clipboard instance
        self.parent.clipboard.copyItem(Folder(self.name, self.path, self.time, self.fav, self.type), copy_flag)

        if not copy_flag:
            blurEffect = QGraphicsBlurEffect()
            self.icon_label.setGraphicsEffect(blurEffect)


    def pasteItem(self):
        # access the parent clipboard item
        state = self.parent.clipboard.paste(self.path)
        if not state:
            QMessageBox.warning(self, "Paste items warning", "Error occured in paste mechnism!",
                                QMessageBox.StandardButton.Ok)



if __name__ == "__main__":
    app = QApplication([])
    w = FolderWidget("shavin", ".0", "2022.12.12", False)
    w.show()
    print()
    app.exec_()