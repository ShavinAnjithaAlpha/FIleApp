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
        self.imageView.setFixedSize(QSize(400, 250))
        self.imageView.setPixmap(QPixmap(self.file).scaled(
            self.imageView.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))

        self.image_name_label = QLabel(self.filterImageName())
        self.image_name_label.setWordWrap(True)

        self.time_label = QLabel(self.formatTime(self.time))
        self.time_label.setObjectName("time-label")

        self.fav_label = QPushButton(QIcon("img/sys/star.png"), "")
        self.fav_label.setObjectName("fav_button")

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


    def changeView(self, index):

        for w in [self.imageView, self.image_name_label, self.time_label, self.fav_label]:
            self.grid.removeWidget(w)

        if index == 0:
            self.grid.addWidget(self.imageView, 0, 0, 3, 1)
            self.grid.addWidget(self.image_name_label, 1, 1)
            self.grid.addWidget(self.fav_label , 0, 2)
            self.grid.addWidget(self.time_label, 1, 2)
        elif index == 1:
            self.grid.addWidget(self.imageView, 0, 0)
            self.grid.addWidget(self.fav_label, 0, 0)


    def filterImageName(self):

        return os.path.split(self.file)[1]

    def mousePressEvent(self, event : QMouseEvent) -> None:

        self.parent.selectFile(self)
        event.accept()


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

        return f"created on {formatted_date} {formatted_time}"
