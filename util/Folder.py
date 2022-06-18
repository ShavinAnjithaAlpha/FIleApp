import datetime

class Folder:
    def __init__(self, name, path, time, fav = False, type = "N"):
        self.name = name
        self.path = path
        self.time = time
        self.fav = fav
        self.type = type

    def rename(self, new_name : str):
        pass

    def delete(self):
        pass

    def folder_count(self):

        return 0

    def file_count(self):

        return 0

    def __str__(self):
        return "path: " + self.path