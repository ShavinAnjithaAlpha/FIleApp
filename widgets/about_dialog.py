from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMenu, QAction, \
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QSize, QTime, QDate, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QIcon, QPixmap

from style_sheets.about_style_sheet import style_sheet


class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()
        self.initializeUI() # initialize the UI
        self.setModal(True)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon("img/sys/FileAppIcon.png"))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.setStyleSheet(style_sheet)
        self.show()

    def initializeUI(self):

        title_label = QLabel("File App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")

        version_label = QLabel("~Beta version 1.0.0")
        version_label.setObjectName("version")

        imageLabel = QLabel()
        imageLabel.setPixmap(
            QPixmap("img/sys/FileAppIcon.png").scaledToHeight(250, Qt.SmoothTransformation)
        )
        imageLabel.adjustSize()

        intro_text = """File App is simple file manager app that can be used for arranged user's files in customized way by through virtual folders. Other basic features are also implemented on this app and you can nicely create and arranged your folder by using color codes and folder types."""
        intro_label = QLabel(intro_text)
        intro_label.setWordWrap(True)
        intro_label.setObjectName("intro")
        intro_label.setAlignment(Qt.AlignCenter)
        # intro_label.adjustSize()



        author_label = QLabel("Developer : Shavin Anjitha Chandrawansha")
        email_link = \
            QLabel("email : <a href='mailto: shavinanjithachandrawansha@gmail.com'>shavinanjithachandawansha@gmail.com</a>")
        email_link.setOpenExternalLinks(True)
        site_link = QLabel("site : <a href='http://shavinanjitha.great-site.net'>shavinanjitha.great-site.net</a>")
        site_link.setOpenExternalLinks(True)

        vbox = QVBoxLayout()
        vbox.addWidget(title_label, alignment=Qt.AlignCenter)
        vbox.addWidget(imageLabel, alignment=Qt.AlignCenter)
        vbox.addWidget(version_label, alignment=Qt.AlignRight|Qt.AlignTop)
        vbox.addWidget(intro_label, alignment=Qt.AlignHCenter)
        vbox.addWidget(author_label, alignment=Qt.AlignHCenter)
        vbox.addWidget(email_link, alignment=Qt.AlignLeft)
        vbox.addWidget(site_link, alignment=Qt.AlignLeft)

        self.setLayout(vbox)

