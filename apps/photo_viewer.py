import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy, QScrollArea, QScrollBar, QSlider
from PyQt5.QtCore import Qt, QSize, QTime, QDate
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap

from util.Folder import Folder

from style_sheets.photo_viewer_style_sheet import style_sheet

class PhotoViewer(QWidget):
    HEIGHT = 850

    def __init__(self, images : list[str], index = 0,parent = None):
        super(PhotoViewer, self).__init__(parent)
        self.imageList = images
        self.index = index
        # initialize UI
        self.initializeUI()

    def initializeUI(self):

        # create the scroll area for add the image view
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setSizePolicy(QSizePolicy(QSizePolicy.Expanding , QSizePolicy.Expanding))
        self.scroll_area.setFixedSize(QSize(1500, 800))

        # create the image view label
        self.imageViewLabel = QLabel()
        self.scroll_area.setWidget(self.imageViewLabel)

        # create the forward and backward buttons
        self.back_btn = QPushButton("<")
        self.back_btn.pressed.connect(self.goBackward)
        self.back_btn.setObjectName("backward-button")

        self.forward_btn = QPushButton(">")
        self.forward_btn.pressed.connect(self.goForward)
        self.forward_btn.setObjectName("forward-button")

        # create the toolbar
        toolBarLyt = QHBoxLayout()
        self.setUpToolBar(toolBarLyt)

        # create the main grid
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(self.scroll_area, 0, 0, 1, 3, alignment=Qt.AlignHCenter)
        grid.addWidget(self.back_btn, 0, 0, alignment=Qt.AlignLeft)
        grid.addWidget(self.forward_btn, 0, 2, alignment=Qt.AlignRight)
        grid.addLayout(toolBarLyt, 1, 0, 1, 3, alignment=Qt.AlignHCenter)

        self.setLayout(grid)
        self.setStyleSheet(style_sheet)

        # load the image to the image view
        self.loadImage()

    def setUpToolBar(self, hbox : QHBoxLayout):

        hbox.setSpacing(15)

        # create the zoom bar
        self.zoom_bar = QSlider(Qt.Horizontal)
        self.zoom_bar.setMinimum(100)
        self.zoom_bar.setMaximum(800)
        self.zoom_bar.setValue(100)
        self.zoom_bar.setMaximumWidth(250)
        self.zoom_bar.setTracking(True)
        self.zoom_bar.valueChanged.connect(self.zoom)

        plus_button = QPushButton("+")
        plus_button.pressed.connect(self.zoomIn)

        minus_button = QPushButton("-")
        minus_button.pressed.connect(self.zoomOut)

        open_with_button = QPushButton()
        open_with_button.setIcon(QIcon("img/sys/photo.png"))
        open_with_button.setIconSize(QSize(60, 60))
        open_with_button.pressed.connect(lambda : os.startfile((self.imageList[self.index])))

        hbox.addWidget(self.zoom_bar)
        hbox.addWidget(plus_button)
        hbox.addWidget(minus_button)
        hbox.addSpacing(25)
        hbox.addWidget(open_with_button)
        hbox.addStretch()


    def loadImage(self):

        try:
            self.imageViewLabel.setPixmap(QPixmap(self.imageList[self.index]).scaled(self.scroll_area.size(),
                                                                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.imageViewLabel.adjustSize()
            self.zoom_bar.setEnabled(True)
            self.zoom_bar.setValue(100)

        except:
            self.imageViewLabel.setText("Nothing Here")
            self.imageViewLabel.setAlignment(Qt.AlignCenter)
            self.zoom_bar.setDisabled(True)

    def addImages(self, images : list[str]):

        self.imageList = [*self.imageList , images]

    def goForward(self):

        # update the image index
        self.index += 1
        # set the new image view
        self.imageViewLabel.setPixmap(QPixmap(self.imageList[self.index]).scaledToHeight(self.HEIGHT))
        # update the button status
        self.updateNavigateButtons()
        self.zoom_bar.setValue(100)

    def goBackward(self):

        # update the image index
        self.index -= 1
        # set the new image view
        self.imageViewLabel.setPixmap(QPixmap(self.imageList[self.index]).scaledToHeight(self.HEIGHT))
        self.updateNavigateButtons()
        self.zoom_bar.setValue(100)

    def addImages(self, image : str):

        self.imageList.append(image)

    def updateNavigateButtons(self):

        if len(self.imageList) == 1:
            self.forward_btn.hide()
            self.back_btn.hide()
        elif self.index == 0:
            self.back_btn.hide()
            self.forward_btn.show()
        elif self.index == len(self.imageList) - 1:
            self.forward_btn.hide()
            self.back_btn.show()
        else:
            self.back_btn.show()
            self.forward_btn.show()

    def zoom(self, value):

        self.imageViewLabel.setPixmap(QPixmap(self.imageList[self.index]).scaledToHeight(int(self.HEIGHT * value/100),
                                                                                    Qt.SmoothTransformation))
        self.scroll_area.scroll(100, 100)

    def zoomIn(self):

        if self.zoom_bar.value() < self.zoom_bar.maximum() - 20:
            self.zoom_bar.setValue(self.zoom_bar.value() + 20)
        self.zoom(self.zoom_bar.value())

    def zoomOut(self):

        if self.zoom_bar.value() > self.zoom_bar.minimum() + 20:
            self.zoom_bar.setValue(self.zoom_bar.value() - 20)
        self.zoom(self.zoom_bar.value())