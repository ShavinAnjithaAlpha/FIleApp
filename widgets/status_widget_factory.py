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

    icon_dict = {
        ".pdf" : "img/sys/pdf.png",
        ".txt" : "img/sys/text-format.png",
        ".html" : "img/sys/html-5.png",
        ".js" : "img/sys/js.png",
        ".css" : "img/sys/css-3.png",
        ".docx" : "img/sys/doc.png",
        ".zip" : "img/sys/zip (1).png",
        ".rar" : "img/sys/rar.png",
        ".py" : "img/sys/python.png",
        ".java" : "img/sys/java.png"
    }

    @staticmethod
    def FolderStatusWidget(path , kwargs):

        WidgetFactory.format_time(kwargs)

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
        icon_label.setPixmap(QPixmap("img/sys/folder (3).png").scaled(icon_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        form.addRow(title_label)
        form.addRow(icon_label)

        WidgetFactory.addFormLine("Name" , WidgetFactory.getText(str(kwargs["Name"])), form)
        WidgetFactory.addFormLine("Created at" , WidgetFactory.getText(kwargs["Created at"]), form)
        WidgetFactory.addFormLine("Path" , WidgetFactory.getText(WidgetFactory.getStringPath(kwargs["Path"])), form)
        WidgetFactory.addFormLine("Sub Folders",
                                  WidgetFactory.getText(str(WidgetFactory.db_manager.folder_count(kwargs["Path"]))), form)
        WidgetFactory.addFormLine("Files",
                                  WidgetFactory.getText(str(WidgetFactory.db_manager.file_count(kwargs["Path"]))), form)

        fav_label = QLabel()
        if kwargs["favorite"] == 1:
            fav_label.setPixmap(
                QPixmap("img/sys/star.png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.FastTransformation))
        else:
            fav_label.setPixmap(
                QPixmap("img/sys/star (1).png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.FastTransformation))
        form.addRow("Favorite", fav_label)




        widget.setStyleSheet(style_sheet)
        widget.setLayout(form)

        return widget

    @staticmethod
    def addFormLine(key : str, edit : QLineEdit, form : QFormLayout):
        form.addRow(key, None)
        form.addRow(edit)


    @staticmethod
    def getText(text : str) -> QLineEdit:
        edit = QLineEdit()
        edit.setContentsMargins(0, 0, 0, 0)
        edit.setText(text)
        edit.setReadOnly(True)
        edit.setObjectName("field-edit")

        return edit

    @staticmethod
    def ImageStatusWidget(kwargs):

        # get the size
        kwargs["Image Name"] = os.path.split(kwargs["File"])[1]
        kwargs["Size"] = WidgetFactory.format_size(os.stat(kwargs["File"]).st_size)
        kwargs["Image Type"] = os.path.splitext(kwargs["File"])[1].upper()

        # format the time
        WidgetFactory.format_time(kwargs)

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

        # add image details row to form
        WidgetFactory.addFormLine("File Name" , WidgetFactory.getText(os.path.split(kwargs["File"])[1]), form)
        WidgetFactory.addFormLine("Path" , WidgetFactory.getText(WidgetFactory.getStringPath(kwargs["Path"])), form)
        WidgetFactory.addFormLine("Added at" , WidgetFactory.getText(kwargs["Added at"]), form)
        WidgetFactory.addFormLine("Image Type" , WidgetFactory.getText(kwargs["Image Type"]), form)
        WidgetFactory.addFormLine("Size" , WidgetFactory.getText(kwargs["Size"]), form)

        fav_label = QLabel()
        if kwargs["Favorite"] == 1:
            fav_label.setPixmap(
                QPixmap("img/sys/star.png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.FastTransformation))
        else:
            fav_label.setPixmap(
                QPixmap("img/sys/star (1).png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.FastTransformation))
        form.addRow("Favorite", fav_label)

        widget.setStyleSheet(style_sheet)
        widget.setLayout(form)

        return widget

    @staticmethod
    def FileStatusWidget(kwargs):

        # get the size
        kwargs["File Name"] = os.path.split(kwargs["File"])[1]
        kwargs["Size"] = WidgetFactory.format_size(os.stat(kwargs["File"]).st_size)
        kwargs["File Type"] = os.path.splitext(kwargs["File"])[1]

        # format the time
        WidgetFactory.format_time(kwargs)

        widget = QWidget()
        widget.setMaximumWidth(370)
        widget.setObjectName("status-widget")
        # create the form layout
        form = QFormLayout()
        form.setVerticalSpacing(0)
        form.setSpacing(0)
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)

        title_label = QLabel("File")
        title_label.setObjectName("title-label")

        icon_label = QLabel()
        icon_label.setFixedSize(QSize(350, 250))
        icon_label.setPixmap(QPixmap(WidgetFactory.icon_dict.get(kwargs["File Type"], "img/sys/file.png")).scaled(
            icon_label.size(), Qt.KeepAspectRatio, Qt.FastTransformation
        ))

        form.addRow(title_label)
        form.addRow(icon_label)

        WidgetFactory.addFormLine("File" , WidgetFactory.getText(os.path.split(kwargs["File"])[1]), form)
        WidgetFactory.addFormLine("Added at" , WidgetFactory.getText(kwargs["Added at"]), form)
        WidgetFactory.addFormLine("File Type" , WidgetFactory.getText(kwargs["File Type"]), form)
        WidgetFactory.addFormLine("Size" , WidgetFactory.getText(kwargs["Size"]), form)


        fav_label = QLabel()
        if kwargs["Favorite"] == 1:
            fav_label.setPixmap(
                QPixmap("img/sys/star.png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.FastTransformation))
        else:
            fav_label.setPixmap(
                QPixmap("img/sys/star (1).png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.FastTransformation))
        form.addRow("Favorite", fav_label)

        # end of details about the file widgets

        widget.setStyleSheet(style_sheet)
        widget.setLayout(form)

        return widget

    @staticmethod
    def getStringPath(path : str) -> list[str]:

        split_path = path.split(".")[1:]
        path_ = ""
        names = ""

        for item in split_path:
            path_ += ".{}".format(item)
            try:
                names += "/{}".format(WidgetFactory.db_manager.get_folder_name(path_))
            except:
                pass

        return names

    @staticmethod
    def format_size(size : int) -> str:

        if size < 1024:
            return f"{size} Bytes"
        elif size < 1024*1024:
            return "{:.2f} KB".format(size/1024)
        elif size < 1024*1024*1024:
            return "{:.2f} MB".format(size/1024/1024)
        else:
            return "{:.2f} GB".format(size/1024/1024/1024)


    @staticmethod
    def format_time(dict : dict):

        try:
            date, time = dict.get("Added at").split(" ")
        except:
            date, time = dict.get("Created at").split(" ")

        date = QDate.fromString(date, "yyyy-MM-dd")
        time = QTime.fromString(time.split(".")[0], "hh:mm:ss")

        time_text = "{} at {}".format(date.toString("yyyy MMM dd"), time.toString("hh:mm A"))
        if dict.get("Added at", None):
            dict["Added at"] = time_text
        else:
            dict["Created at"] = time_text


