import os

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy, QScrollArea, QScrollBar, QSlider, QStyle, QFileDialog
from PyQt5.QtCore import Qt, QSize, QTime, QDate, QUrl, QState

from PyQt5.QtMultimedia import QMediaContent

from util.Folder import Folder

from style_sheets.video_player_style_sheet import style_sheet

class VideoPlayer(QWidget):
    def __init__(self, video_list : list[str], index : int):
        super(VideoPlayer, self).__init__()
        self.videoList = video_list
        self.index = index
        # initialize the UI
        self.initializeUI()


    def initializeUI(self):

        # create the media player object for this
        self.media_player = QMediaPlayer()

        # create the video widget for render the video
        self.videoWidget = QVideoWidget()
        self.videoWidget.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
        # self.videoWidget.setFixedSize(QSize(1200, 900))

        # create the forward and backward arrow buttons
        self.forward_button = QPushButton()
        self.forward_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))

        self.backward_button = QPushButton()
        self.backward_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))

        # create the grid for packing arrow and video widget
        video_gird = QGridLayout()
        video_gird.setSpacing(0)
        video_gird.setContentsMargins(0, 0, 0, 0)
        video_gird.addWidget(self.backward_button, 0, 0)
        video_gird.addWidget(self.forward_button, 0, 2)
        # video_gird.addWidget(self.videoWidget, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        # create the position slider for video
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        # self.positionSlider.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred))
        # self.positionSlider.hide()

        # create the h box for arrange the control panel items
        hbox = QHBoxLayout()
        hbox.setSpacing(15)
        self.setUpControlPanel(hbox)

        # set up the media player
        self.media_player.setVideoOutput(self.videoWidget)
        self.media_player.stateChanged.connect(self.mediaStateChnaged)
        self.media_player.positionChanged.connect(self.mediaPositionChanged)
        self.media_player.durationChanged.connect(self.mediaDurationChanged)
        self.media_player.error.connect(self.handleError)

        # create the main container
        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(self.videoWidget , 0, 0)
        grid.addWidget(self.positionSlider, 1, 0)
        grid.addLayout(hbox, 2, 0)
        # grid.setRowStretch(1, 1)

        self.setLayout(grid)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(style_sheet)


    def setUpControlPanel(self, hbox : QHBoxLayout):

        # create the play and pause buttons
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.pressed.connect(self.playVideo)


        hbox.addWidget(self.play_button, alignment=Qt.AlignLeft)

    def playVideo(self):

        # check the media player status
        if self.media_player.state() == QMediaPlayer.PlayingState:
            # pause the current media
            self.media_player.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.media_player.state() == QMediaPlayer.StoppedState or self.media_player.state() == QMediaPlayer.PausedState:
            file, _ = QFileDialog.getOpenFileName(self, "", "", "Video Files(*.*)")
            # load the file to the media player
            self.media_player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(file)))
            self.media_player.play() # play the media
            # change the video play button icons
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            # set the position slider
            # self.positionSlider.setRange(0, self.media_player.duration())

            if self.media_player.state() == QMediaPlayer.PlayingState:
                print("playig")
            elif self.media_player.state() == QMediaPlayer.PausedState:
                print("pause")
            elif self.media_player.state() == QMediaPlayer.StalledMedia:
                print("stalled")
            elif self.media_player.state() == QMediaPlayer.StoppedState:
                print("stop")

    def mediaStateChnaged(self, state : QState):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            print("playig")
        elif self.media_player.state() == QMediaPlayer.PausedState:
            print("pause")
        elif self.media_player.state() == QMediaPlayer.StalledMedia:
            print("stalled")
        elif self.media_player.state() == QMediaPlayer.StoppedState:
            print("stop")
            self.media_player.play()


        if state == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def mediaPositionChanged(self, position : int):

        self.positionSlider.setValue(position)

    def mediaDurationChanged(self, duration : int):

        self.positionSlider.setRange(0, duration)

    def handleError(self):

        print(self.media_player.errorString())

if __name__ == "__main__":
    app = QApplication([])
    window = VideoPlayer([], 0)
    window.show()
    app.exec_()