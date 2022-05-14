import os.path

from util.path_manager import path_manager
from util.db_manager import db_manager

from widgets.folder_widget import FolderWidget
from widgets.image_widget import ImageWidget

class FileEngine:
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
            widget = FolderWidget(item[0], item[1], item[2], item[3], self.parent)
            folder_widgets.append(widget)

        for item in files_data:
            if self.getFileType(item[0]) == "img":
                widget = ImageWidget(item[0], item[1], item[2], item[3], self.parent)
                files_widget.append(widget)
            else:
                pass



        self.current_path = path
        if not back:
            # add the path to the stack
            self.path_stack.append(path)

        return (folder_widgets, files_widget)

    def new_folder(self , name : str):

        folder_path = self.db_manager.add_folder(name, self.current_path)
        # create the Folder Widget
        data = self.db_manager.folder(folder_path)

        return FolderWidget(data[0], data[1], data[2], data[3], self.parent)

    def add_files(self, files : list[str]):

        time = self.db_manager.add_files(files, self.current_path)
        # return the files widget lists

        file_widgets = []
        for file in files:
            file_widgets.append(ImageWidget(file, self.current_path, time, False, self.parent))


    def backward(self):

        self.path_stack.pop()
        return len(self.path_stack)

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
