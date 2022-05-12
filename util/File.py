import sys, os, datetime

class File:
    def __init__(self, file, path , time ,fav = False):
        self.file = file
        self.path = path
        self.time = time
        self.fav = fav

    def exists(self):

        return os.path.exists(self.file)

    def setFavorite(self, state : bool):

        pass

    def delete(self):
        pass

    def file_size(self):

        if os.path.exists(self.file):
            return os.stat(self.file).st_size

        return 0


