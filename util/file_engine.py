from util.path_manager import path_manager
from util.db_manager import db_manager

from widgets.folder_widget import FolderWidget

class FileEngine:
    def __init__(self, db_manager : db_manager):
        self.current_path = "."
        self.path_stack = [self.current_path ,]
        self.db_manager = db_manager

    def open_folder(self, path : str):

        folder_data = self.db_manager.open_folder(path)
        files_data = self.db_manager.open_files(path)


        folder_widgets = []
        files_widget = []
        for item in folder_data:
            # create the folder widgets and return it
            widget = FolderWidget(item[0], item[1], item[2], item[3])
            folder_widgets.append(widget)

        return folder_widgets

    def new_folder(self , name : str):

        folder_path = self.db_manager.add_folder(name, self.current_path)
        # create the Folder Widget
        data = self.db_manager.folder(folder_path)

        return FolderWidget(data[0], data[1], data[2], data[3])