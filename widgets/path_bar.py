from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from style_sheets.path_bar_style_sheet import style_sheet

class PathBar(QWidget):

    path_signal = pyqtSignal(str)

    def __init__(self, paths : list[str] = None, path :str = None):
        super(PathBar, self).__init__()
        self.paths = paths
        self.path = path
        self.initilalizeUI()

        self.setMaximumWidth(800)
        self.setFixedHeight(80)

    def initilalizeUI(self):

        self.button_list = []

        # h box for packaging items
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel("Path")
        name_label.setObjectName("lb")
        self.hbox.addWidget(name_label)

        if self.paths:
            # create the widget
            for item in self.paths:
                if item:
                    button = QPushButton(item)
                    button.setObjectName("path-button")
                    button.pressed.connect(lambda e=button.text(): self.emitPath(e))
                    # add to the list
                    self.button_list.append(button)
                    self.hbox.addWidget(button)

        base = QWidget()
        base.setObjectName("base")
        base.setContentsMargins(0, 0, 0, 0)
        base.setLayout(self.hbox)

        hbox2 = QHBoxLayout()
        # hbox2.setContentsMargins(0, 0, 0, 0)
        hbox2.addWidget(base)

        self.setLayout(hbox2)
        self.setStyleSheet(style_sheet)

    def emitPath(self, e):
        print(e)

    def setPath(self, paths : list[str], path : str):

        self.paths = paths
        self.path = path

        #rebuild the widget
        [self.hbox.removeWidget(w) for w in self.button_list]
        self.button_list = []

        for item in self.paths:
            if item:
                button = QPushButton(item)
                button.setObjectName("path-button")
                button.pressed.connect(lambda e=button.text(): self.emitPath(e))
                # add to the list
                self.button_list.append(button)
                self.hbox.addWidget(button)

