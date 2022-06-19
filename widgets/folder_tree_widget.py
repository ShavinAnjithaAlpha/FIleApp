from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QTreeView, QVBoxLayout
from PyQt5.Qt import Qt, QFont, QStandardItem, QStandardItemModel, QHeaderView, QThread, QModelIndex, QSize
from PyQt5.QtGui import QColor, QIcon

from util.db_manager import db_manager
from util.path_manager import path_manager

class TreeBuildThread(QThread):
    def __init__(self, db_manager : db_manager, parent_node : QStandardItem, path : str):
        super(TreeBuildThread, self).__init__()
        self.parent_node = parent_node
        self.path = path
        self.db_manager = db_manager

    def run(self) -> None:

        self.build(self.parent_node, self.path)

    def build(self, parentItem : QStandardItem, path_code : str):

        # get the children of the current parent node
        folders = self.db_manager.open_folder(path_code)
        files = self.db_manager.open_files(path_code)

        folderNodes = []
        if folders:
            for folder in folders:
                folderNode = TreeItem(folder, "Folder")
                folderNodes.append(folderNode)
                parentItem.appendRow(
                    [folderNode,
                     QStandardItem(path_manager.formatTime(folder[2])),
                     QStandardItem(path_manager.get_folder_size(self.db_manager, folder[1]))
                     ]
                )

        if files:
            for file in files:
                fileNode = TreeItem(file, "File")
                parentItem.appendRow(
                    [fileNode,
                     QStandardItem(path_manager.formatTime(file[2])),
                     QStandardItem(path_manager.size(file[0]))
                     ]
                )

        # call to this method for build chidren's children nodes
        for i, node in enumerate(folderNodes):
            self.build(node, folders[i][1])


class TreeItem(QStandardItem):
    def __init__(self, item, type : str):
        super(TreeItem, self).__init__()
        self.item = item
        self.type = type

        if type == "Folder":
            self.setIcon(QIcon("{}".format(path_manager.get_folder_icon(item))))
            self.setText(item[0])
        else:
            self.setIcon(QIcon("{}".format(path_manager.get_file_icon(item))))
            self.setText(path_manager.get_file_name(item[0]))

    def text(self) -> str:

        return self.item[1]

class FolderTreeWidget(QTreeView):
    def __init__(self ,db_mgr : db_manager = None):
        super(FolderTreeWidget, self).__init__()
        if db_mgr is not None:
            self.db_manager = db_mgr
        else:
            self.db_manager = db_manager("../db/main.db")

        # create the header video for tree view
        header_view = QHeaderView(Qt.Horizontal)
        header_view.setContentsMargins(0, 0, 0, 0)
        self.setHeader(header_view)
        self.header().setStretchLastSection(False)

        # create the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["File/Folder", "Date Added", "Size"])
        rootItem = self.model.invisibleRootItem()
        self.setModel(self.model)
        self.setIconSize(QSize(20, 20))
        self.setMinimumSize(QSize(300, 900))
        self.setContentsMargins(0, 0, 0 , 0)

        self.rootPath = "."
        self.buildTreeModel(self.rootPath, rootItem)
        #
        # self.pressed.connect(self.buildSubTree)
        # self.expanded.connect(self.buildSubTree)

    def buildTreeModel(self, path_code : str, parentItem : QStandardItem):

        if parentItem.hasChildren():
            parentItem.removeRow(0)

        # get the children of the current parent node
        folders = self.db_manager.open_folder(path_code)
        files = self.db_manager.open_files(path_code)

        folderNodes = []
        if folders:
            for folder in folders:
                folderNode = TreeItem(folder, "Folder")
                folderNodes.append(folderNode)
                parentItem.appendRow(
                    [folderNode,
                    QStandardItem(path_manager.formatTime(folder[2])),
                     QStandardItem(path_manager.get_folder_size(self.db_manager, folder[1]))
                     ]
                )

        if files:
            for file in files:
                fileNode = TreeItem(file, "File")
                parentItem.appendRow(
                    [fileNode,
                     QStandardItem(path_manager.formatTime(file[2])),
                     QStandardItem(path_manager.size(file[0]))
                     ]
                )

        # call to this method for build chidren's children nodes
        threads = []
        for i ,node in enumerate(folderNodes):
            # self.buildTreeModel(folders[i][1], node)
            thread = TreeBuildThread(self.db_manager, node, folders[i][1])
            threads.append(thread)

        [thread.run() for thread in threads]

    def buildSubTree(self, index : QModelIndex):

        node = self.model.item(index.row(), 0)
        if node.type == "Folder":
            self.buildTreeModel(node.item[1], node)


if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    window.setCentralWidget(FolderTreeWidget())
    window.show()
    app.exec_()

