import os

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QComboBox, QFormLayout, QLineEdit)
from PyQt5.QtCore import QSize, Qt, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from util.file_engine import FileEngine
from util.db_manager import db_manager

from style_sheets.status_widget_style_sheet import style_sheet

class WidgetFactory:

    db_manager = db_manager("db/main.db")

    @staticmethod
    def FolderStatusWidget(path , kwargs):

        widget = QWidget()
        widget.setMaximumWidth(370)
        widget.setObjectName("status-widget")
        # create the form layout
        form = QFormLayout()
        form.setVerticalSpacing(0)
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)

        title_label = QLabel("File Folder")
        title_label.setObjectName("title-label")

        icon_label = QLabel()
        icon_label.setFixedSize(QSize(220,170))
        icon_label.setPixmap(QPixmap("img/sys/folder (2).png").scaled(icon_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        form.addRow(title_label)
        form.addRow(icon_label)

        for key in kwargs:
            edit = QLineEdit()
            edit.setText(str(kwargs.get(key)))
            edit.setReadOnly(True)
            edit.setObjectName("field-edit")

            form.addRow(key, edit)

        widget.setStyleSheet(style_sheet)
        widget.setLayout(form)

        return widget

    @staticmethod
    def ImageStatusWidget(kwargs):

        # get the size
        kwargs["Size"] = os.stat(kwargs["File"]).st_size
        kwargs["Image Type"] = os.path.splitext(kwargs["File"])[1]

        widget = QWidget()
        widget.setMaximumWidth(370)
        widget.setObjectName("status-widget")
        # create the form layout
        form = QFormLayout()
        form.setVerticalSpacing(0)
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)

        title_label = QLabel("Image File")
        title_label.setObjectName("title-label")

        icon_label = QLabel()
        icon_label.setFixedSize(QSize(350, 250))
        try:
            icon_label.setPixmap(
                QPixmap(kwargs["File"]).scaled(icon_label.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))
        except:
            icon_label.setPixmap(
                QPixmap("img/sys/photo.png").scaled(icon_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        form.addRow(title_label)
        form.addRow(icon_label)

        for key in kwargs:
            edit = QLineEdit()
            edit.setText(str(kwargs.get(key)))
            edit.setReadOnly(True)
            edit.setObjectName("field-edit")

            form.addRow(key, edit)

        widget.setStyleSheet(style_sheet)
        widget.setLayout(form)

        return widget


