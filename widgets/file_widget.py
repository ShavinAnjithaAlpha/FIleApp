import os.path

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt, QSize, QTime, QDate
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap
import datetime

from util.File import File

from style_sheets.image_style_sheet import style_sheet

class FileWidget(File, QWidget):

    MAX_FILE_NAME_LENGTH = 20

    icon_dict = {
        ".pdf": "img/sys/pdf.png",
        ".txt": "img/sys/text-format.png",
        ".html": "img/sys/html-5.png",
        ".js": "img/sys/js.png",
        ".css": "img/sys/css-3.png",
        ".docx": "img/sys/doc.png",
        ".zip": "img/sys/zip (1).png",
        ".rar": "img/sys/rar.png",
        ".py": "img/sys/python.png",
        ".java": "img/sys/java.png"
    }

    def __init__(self, file, path, time, fav = False, parent = None):
        super(FileWidget, self).__init__(file, path, time, fav)
        QWidget.__init__(self, parent)
        self.parent = parent

        self.initilizeUI()

    def initilizeUI(self):

        self.imageView = QLabel()
        self.imageView.setFixedHeight(120)
        # self.imageView.adjustSize()
        # fill the appropriate file icon for imageView label
        self.fillIcon()

        self.file_name_label = QLabel()
        if len(self.filterFileName()) > FileWidget.MAX_FILE_NAME_LENGTH:
            self.file_name_label.setText("{}...".format(self.filterFileName()[:50]))
        else:
            self.file_name_label.setText(self.filterFileName())

        self.file_name_label.setWordWrap(True)
        self.file_name_label.setObjectName("name-label")

        self.size_label = QLabel(self.size())
        self.size_label.setObjectName("size-label")

        self.time_label = QLabel(self.formatTime(f"{self.time}"))
        self.time_label.setObjectName("time-label")

        self.setUpFavoriteButton()

        # create the grid
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.base = QWidget()
        self.base.setObjectName("image-base")
        self.base.setLayout(self.grid)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0 , 0)
        hbox.addWidget(self.base)

        self.setLayout(hbox)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(style_sheet)

    def fillIcon(self):

        ext = self.getExtension()
        self.imageView.setPixmap(
            QPixmap(FileWidget.icon_dict.get(ext, "img/sys/file.png")).scaledToHeight(self.imageView.height()))

    def setUpFavoriteButton(self):

        self.fav_button = QPushButton()
        # self.fav_button.setContentsMargins(25, 25, 25, 25)
        self.fav_button.setFixedSize(QSize(30, 30))
        self.fav_button.setObjectName("fav-button")
        self.fav_button.setIconSize(QSize(25, 25))
        self.fav_button.pressed.connect(self.changeFav)

        if self.fav:
            self.fav_button.setIcon(QIcon("img/sys/star.png"))
        else:
            self.fav_button.setIcon(QIcon("img/sys/star (1).png"))

    def changeFav(self):

        self.fav = not self.fav
        self.parent.file_engine.db_manager.change_favorite_file(self.path , self.file, self.fav)
        if self.fav:
            self.fav_button.setIcon(QIcon("img/sys/star.png"))
        else:
            self.fav_button.setIcon(QIcon("img/sys/star (1).png"))


    def changeView(self, index):

        for w in [self.imageView, self.file_name_label, self.time_label, self.fav_button, self.size_label]:
            self.grid.removeWidget(w)

        if index == 0:
            self.file_name_label.setMaximumWidth(1500)

            self.grid.addWidget(self.imageView, 0, 0, alignment=Qt.AlignVCenter)
            self.grid.addWidget(self.file_name_label, 0, 1, alignment=Qt.AlignLeft)
            self.grid.addWidget(self.size_label, 0, 2)
            self.grid.addWidget(self.time_label, 0, 3)
            self.grid.addWidget(self.fav_button, 0, 4, alignment=Qt.AlignRight|Qt.AlignRight)

            self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum))
            self.setMaximumWidth(2000)

        elif index == 1:
            self.file_name_label.setMaximumWidth(230)

            self.size_label.hide() # hide the size label from grid view
            self.grid.addWidget(self.fav_button, 0, 0, alignment=Qt.AlignRight)
            self.grid.addWidget(self.imageView, 1, 0, alignment=Qt.AlignCenter)
            self.grid.addWidget(self.file_name_label, 2, 0, alignment=Qt.AlignCenter)

            self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        else:
            pass




    def filterFileName(self):

        return os.path.split(self.file)[1]

    def mousePressEvent(self, event : QMouseEvent) -> None:

        self.parent.selectFile(self)
        event.accept()

    def contextMenuEvent(self, event : QContextMenuEvent) -> None:

        # create the cntext menu
        menu = QMenu()

        # create the actions
        open_action = QAction(QIcon("img/sys/photo.png"),"Open", self)
        open_action.triggered.connect(lambda : print("opened"))
        menu.addAction(open_action)

        menu.addSeparator()

        copy_action = QAction(QIcon("img/sys/copy.png"), "Copy", self)
        menu.addAction(copy_action)

        move_action = QAction(QIcon("img/sys/forward.png"), "Move", self)
        menu.addAction(move_action)

        menu.addSeparator()

        delete_action = QAction(QIcon("img/sys/delete.png"), "delete", self)
        delete_action.triggered.connect(self.delete)
        menu.addAction(delete_action)

        remove_action = QAction(QIcon("img/sys/close.png"), "remove", self)
        remove_action.triggered.connect(self.remove)
        menu.addAction(remove_action)

        menu.exec_(self.mapToGlobal(event.pos()))

    def selected(self):

        self.base.setObjectName("selected-image-base")
        self.setStyleSheet(style_sheet)

    def unselected(self):

        self.base.setObjectName("image-base")
        self.setStyleSheet(style_sheet)

    def formatTime(self, text : str):

        date, time = text.split(" ")
        time_ , date_ = QTime.fromString(time.split(".")[0], "hh:mm:ss") , QDate.fromString(date, "yyyy-MM-dd")

        formatted_date, formatted_time = date_.toString("yyyy MMM dd"), time_.toString("hh:mm A")

        return f"added on {formatted_date} {formatted_time}"


    def size(self):

        try:
            size = os.stat(self.file).st_size

            if size < 1024:
                return f"{size} Bytes"
            elif size < 1024 *1024:
                return "{:.2f} KB".format(size/1024)
            else:
                return "{:.2f} MB".format(size/1024/1024)

        except:
            return "None"

    def getExtension(self):

        return os.path.splitext(self.file)[1]

    def getName(self):

        return os.path.split(self.file)[1]

    def delete(self):

        # ask first for confirmation
        button = QMessageBox.warning(self, "Delete File", "Are you sure to delete\n '{}' file".format(self.getName()),
                                     QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

        if button == QMessageBox.StandardButton.Yes:
            # remove the folder to the recycle bin
            x = self.parent.db_manager.deleteFile(self.path, self.file)
            if x:
                # remove from the file area folder list
                self.parent.files.remove(self)
                # delete the folder widget
                self.deleteLater()

    def remove(self):

        # ask first for confirmation
        button = QMessageBox.warning(self, "Remove File", "Are you sure to permanant remove\n '{}' file".format(self.getName()),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if button == QMessageBox.StandardButton.Yes:
            # remove the folder to the recycle bin
            x = self.parent.db_manager.removeFile(self.path)
            if x:
                # remove from the file area folder list
                self.parent.folders.remove(self)
                # delete the folder widget
                self.deleteLater()

