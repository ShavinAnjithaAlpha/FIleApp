from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
import datetime

from util.Folder import Folder


class FolderWidget(Folder, QWidget):
    def __init__(self, name, path, time, fav, parent = None):
        super(FolderWidget, self).__init__(name, path, time, fav)
        QWidget.__init__(self, parent)

        # create the folder name label
        nameLabel = QLabel(name)
        hbox = QHBoxLayout()
        hbox.addWidget(nameLabel)

        self.setLayout(hbox)

if __name__ == "__main__":
    app = QApplication([])
    w = FolderWidget("shavin", ".0", "2022.12.12", False)
    w.show()
    print()
    app.exec_()