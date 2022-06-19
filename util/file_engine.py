import os.path

from util.path_manager import path_manager
from util.db_manager import db_manager

from widgets.folder_widget import FolderWidget
from widgets.image_widget import ImageWidget
from widgets.file_widget import FileWidget

class FileEngine:
    FOLDER_TYPES = {"Normal": "N", "Image Folder": "I", "Video Folder": "V", "Document Folder": "D",
                    "System Folder": "S", "Red": "RED", "Green": "GREEN", "Blue": "BLUE"}

    def __init__(self, db_manager : db_manager, parent = None):
        self.parent = parent
        self.current_path = "."
        self.path_stack = []
        self.db_manager = db_manager

    def open_folder(self, path : str, back = False):

        folder_data = self.db_manager.open_folder(path)
        files_data = self.db_manager.open_files(path)

        folder_widgets = []
        files_widget = []
        for item in folder_data:
            # create the folder widgets and return it
            widget = FolderWidget(item[0], item[1], item[2], item[3], item[4], item[5], self.parent)
            folder_widgets.append(widget)

        for item in files_data:
            if self.getFileType(item[0]) == "img":
                widget = ImageWidget(item[0], item[1], item[2], item[3], self.parent)
                files_widget.append(widget)
            else:
                widget = FileWidget(item[0], item[1], item[2], item[3], self.parent)
                files_widget.append(widget)



        self.current_path = path
        if not back:
            # add the path to the stack
            self.path_stack.append(path)

        return (folder_widgets, files_widget)

    def new_folder(self , name : str, type : str):

        folder_path = self.db_manager.add_folder(name, self.current_path, self.FOLDER_TYPES[type])
        # create the Folder Widget
        data = self.db_manager.folder(folder_path)

        return FolderWidget(data[0], data[1], data[2], data[3], self.FOLDER_TYPES.get(type, "N"), None, self.parent)

    def add_files(self, files : list[str]):

        time = self.db_manager.add_files(files, self.current_path).__str__()
        # return the file widget lists

        file_widgets = []
        for file in files:
            if self.getFileType(file) == "img":
                file_widgets.append(ImageWidget(file, self.current_path, time, False, self.parent))
            else:
                file_widgets.append(FileWidget(file, self.current_path, time, False, self.parent))


        return file_widgets


    def backward(self):

        # self.path_stack.pop()
        return self.path_stack.index(self.current_path) - 1

    def forward(self):

        return self.path_stack.index(self.current_path) + 1

    def path(self, index):
        return self.path_stack[index]

    def count(self):

        return len(self.path_stack)

    def getFileType(self, file : str):

        _, ext = os.path.splitext(file)

        if ext in [".jpg", ".png", ".bmp" ,".svg", ".ico", ".jpeg"]:
            return "img"
        elif ext in [".mp4", ".mkv", ".vob"]:
            return "vid"
        else:
            return "other"

    def getStringPath(self, path : str) -> list[str]:

        split_path = path.split(".")[1:]
        path_ = ""
        names = []

        for item in split_path:
            path_ += ".{}".format(item)
            try:
                names.append(self.db_manager.get_folder_name(path_))
            except:
                pass

        return names

    def open_favorites(self):

        folder_data = self.db_manager.open_favorites_folders()
        files_data = self.db_manager.open_favorites_files()

        folder_widgets = []
        files_widget = []
        for item in folder_data:
            # create the folder widgets and return it
            widget = FolderWidget(item[0], item[1], item[2], item[3], item[4], item[5], self.parent)
            folder_widgets.append(widget)

        for item in files_data:
            if self.getFileType(item[0]) == "img":
                widget = ImageWidget(item[0], item[1], item[2], item[3], self.parent)
                files_widget.append(widget)
            else:
                widget = FileWidget(item[0], item[1], item[2], item[3], self.parent)
                files_widget.append(widget)

        return (folder_widgets, files_widget)