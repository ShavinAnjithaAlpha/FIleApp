from util.File import File
from util.Folder import Folder
from util.path_manager import path_manager
from util.db_manager import db_manager

class ClipBoard:
    def __init__(self, db_manager : db_manager):
        # declare copied and moved folders and files lists
        self.copied_items =[]
        self.db_manager = db_manager

    def copyItem(self, item : [Folder, File], flag : bool):
        self.copied_items.append(CopiedItem(item, self.db_manager, flag))

    def paste(self, pasteFolder : [Folder, str]):
        [item.setPasteFolder(pasteFolder) for item in self.copied_items]
        # paste the item as database operation
        [item.paste() for item in self.copied_items]





class CopiedItem:
    def __init__(self, copied_item : [Folder, File], db_manager : db_manager, flag : bool = True):
        # set the root copied item as the copied_folder
        self.rootFolder = None
        self.rootFile = None
        self.db_manager = db_manager
        self.pasteRootPath = None
        self.copyFlag = flag

        # set the root items
        if isinstance(copied_item, Folder):
            self.rootFolder = copied_item
        else:
            self.rootFile = copied_item
        # then grab data about that inside in copied folder
        self.children_folders = []
        self.children_files = []

        self.updated_children = []
        self.updated_root = None
        self.updated_file = None
        # build the structure
        self.buildStructure(self.rootFolder)

    def buildStructure(self, rootFolder : Folder):

        if  rootFolder is not None:
            child_folders = self.db_manager.open_folder_as_instance(rootFolder.path)
            if child_folders:
                [self.children_folders.append(x) for x in child_folders]
                # and recall to itself to build the structure recursively
                [self.buildStructure(folder) for folder in child_folders]

            # search for children files in the root folder and append them to list
            [self.children_files.append(x) for x in self.db_manager.open_files_as_instance(rootFolder.path)]

    def setPasteFolder(self, folder : [Folder, str]):
        if isinstance(folder, Folder):
            self.pasteRootPath = folder.path
        else:
            self.pasteRootPath = folder

        if self.rootFolder:
           # update paths
           self.updateFolderPaths()
           self.updateFilesPaths()
        if self.rootFile:
            self.updated_file = File(self.rootFile.file, self.pasteRootPath, self.rootFile.time, self.rootFile.fav)

    def updateFilesPaths(self):

        # update files path to new location
        for file in self.children_files:
            self.updated_children.append(
                File(file.file,
                     ".".join(
                         [self.basePath, path_manager.filter_sub_path(self.rootFolder.path, file.path)]),
                    file.time,
                    file.fav)
            )
        # print("----------update files--------------")
        # print(updated_paths)

    def updateFolderPaths(self):

        # update folders to new location
        self.basePath = path_manager.get_path_for_folder(self.pasteRootPath, self.db_manager.get_paths(self.pasteRootPath))

        # then split all folders to parent path and sub path and updated new paths
        updated_paths = []
        for folder in self.children_folders:
            self.updated_children.append(
                Folder(folder.name,
                       ".".join([self.basePath, path_manager.filter_sub_path(self.rootFolder.path, folder.path)]),
                       folder.time,
                       folder.fav,
                       folder.type)
                )
        self.updated_root = Folder(self.rootFolder.name, self.basePath, self.rootFolder.time, self.rootFolder.fav,
                                   self.rootFolder.type)

    def paste(self):
        if self.rootFolder:
            # save to the database these folders and files
            self.db_manager.add_instance([*self.updated_children, self.updated_root])

            if not self.copyFlag:
                self.remove()

            print("[INFO] successfully pasted all")

        if self.rootFile:
            self.db_manager.add_instance((self.updated_file, ))

    def remove(self):
        if self.rootFolder:
            self.db_manager.delete_from_instance([*self.children_folders, *self.children_files, self.rootFolder])
        if self.rootFile:
            self.db_manager.delete_from_instance((self.rootFile, ))


if __name__ == "__main__":
    pass
    # db_manager = db_manager("../db/main.db")
    # roots = db_manager.open_folder_as_instance(".7")
    # print(roots[0].path)
    # clip = CopiedItem(roots[0], db_manager, False)
    # clip.setPasteFolder(".6")

    # clip.print()
    # [print(i.path) for i in clip.updated_children]
    # clip.paste()

    # print(path_manager.filter_sub_path("5.3.2", "5.3.2.4.8.7"))





