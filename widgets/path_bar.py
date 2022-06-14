from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
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

        # add home button
        button = QPushButton("Home")
        button.setObjectName("path-button")
        button.pressed.connect(lambda : self.emitPath("Home"))
        # add to the list
        self.button_list.append(button)
        self.hbox.addWidget(button)

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
        hbox2.setContentsMargins(0, 0, 0, 0)
        hbox2.addWidget(base)

        self.setLayout(hbox2)
        self.setStyleSheet(style_sheet)

    def emitPath(self, e):

        if e == "Home":
            self.path_signal.emit(".")
            return

        index = self.paths.index(e)
        # split the path to indexes
        path_split = self.path.split(".")

        new_path = ""
        for i in range(1, index+2):
            new_path += f".{path_split[i]}"

        self.path_signal.emit(new_path)

    def setPath(self, paths : list[str], path : str):

        self.paths = paths
        self.path = path

        #rebuild the widget
        [self.hbox.removeWidget(w) for w in self.button_list]
        self.button_list = []

        # add home button
        button = QPushButton("Home")
        button.setObjectName("path-button")
        button.pressed.connect(lambda: self.emitPath("Home"))
        label = QLabel(">")
        # add to the list
        self.button_list.append(button)
        self.button_list.append(label)
        self.hbox.addWidget(button)
        self.hbox.addWidget(label)

        if self.paths:
            for item in self.paths:
                if item:
                    button = QPushButton(item)
                    button.setObjectName("path-button")
                    button.pressed.connect(lambda e=button.text(): self.emitPath(e))
                    label = QLabel(">")
                    # add to the list
                    self.button_list.append(button)
                    self.button_list.append(label)
                    self.hbox.addWidget(button)
                    self.hbox.addWidget(label)

