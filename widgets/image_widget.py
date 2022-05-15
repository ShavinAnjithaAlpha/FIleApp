import os.path

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout
from PyQt5.QtCore import Qt, QSize, QTime, QDate
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap
import datetime

from util.File import File

from style_sheets.image_style_sheet import style_sheet

class ImageWidget(File, QWidget):
    def __init__(self, file, path, time, fav = False, parent = None):
        super(ImageWidget, self).__init__(file, path, time, fav)
        QWidget.__init__(self, parent)
        self.parent = parent

        self.initilizeUI()

    def initilizeUI(self):

        self.imageView = QLabel()
        self.imageView.setFixedSize(QSize(250, 220))
        try:
            self.imageView.setPixmap(QPixmap(self.file).scaled(
                self.imageView.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))
        except:
            self.imageView.setPixmap(QPixmap("img/sys/picture.png").scaled(self.imageView.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))

        self.image_name_label = QLabel(self.filterImageName())
        self.image_name_label.setWordWrap(True)
        self.image_name_label.setObjectName("name-label")

        self.time_label = QLabel(self.formatTime(f"{self.time}"))
        self.time_label.setObjectName("time-label")

        self.size_label = QLabel(self.size())
        self.size_label.setObjectName("size-label")

        self.setUpFavoriteButton()

        # create the grid
        self.grid = QGridLayout()
        # self.grid.setContentsMargins(0, 0, 0, 0)

        self.base = QWidget()
        self.base.setObjectName("image-base")
        self.base.setLayout(self.grid)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0 , 0)
        hbox.addWidget(self.base)

        self.setLayout(hbox)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(style_sheet)

    def setUpFavoriteButton(self):

        self.fav_button = QPushButton()
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

        for w in [self.imageView, self.image_name_label, self.time_label, self.fav_button, self.size_label]:
            self.grid.removeWidget(w)

        if index == 0:
            self.grid.addWidget(self.imageView, 0, 0, 3, 1)
            self.grid.addWidget(self.image_name_label, 1, 1)
            self.grid.addWidget(self.fav_button , 0, 3)
            self.grid.addWidget(self.time_label, 2, 2)
            self.grid.addWidget(self.size_label, 2, 1)

            self.setFixedHeight(230)
            self.setMaximumWidth(2000)

        elif index == 1:
            self.grid.addWidget(self.imageView, 1, 0)
            self.grid.addWidget(self.fav_button, 0, 0)

            self.setFixedSize(QSize(250, 230))

        else:
            pass


    def filterImageName(self):

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

        open_os_action = QAction(QIcon("img/sys/picture.png"), "Open By OS", self)
        open_os_action.triggered.connect(lambda : os.startfile(self.file))
        menu.addAction(open_os_action)

        menu.addSeparator()

        copy_action = QAction(QIcon("img/sys/copy.png"), "Copy", self)
        menu.addAction(copy_action)

        move_action = QAction(QIcon("img/sys/forward.png"), "Move", self)
        menu.addAction(move_action)

        menu.addSeparator()

        delete_action = QAction(QIcon("img/sys/delete.png"), "delete", self)
        delete_action.triggered.connect(self.delete)
        menu.addAction(delete_action)

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

    def delete(self):

        pass

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
