import os , sys, sqlite3
from util.path_manager import path_manager
import datetime

class db_injector:
    def __init__(self, path = "db/main.db", save_config = True):
        self.path = path
        self.save_config = save_config

    def __enter__(self):
        # create the connection to the database file
        self.con = sqlite3.connect(self.path)
        # ge the connection query slot

        return self.con.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.save_config:
            self.con.commit()
        # close the connection
        self.con.close()
        del self # delete the object


class db_manager:
    def __init__(self, path = "db/main.db"):
        self.path = path
        # initialize the db folder if it does not exist
        if not os.path.exists("db"):
            os.mkdir("db")
            self.initialize_db()


    def initialize_db(self):
        # create the database tables if tables does not exist
        with db_injector(self.path, True) as cursor:
            # create the main folder table
            cursor.execute(
                """CREATE TABLE folders(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL ,
                                        name VARCHAR(150) NOT NULL,
                                        path TEXT NOT NULL UNIQUE ,
                                        time TIMESTAMP NOT NULL ,
                                        fav BOOLEAN NOT NULL)"""
            )

            cursor.execute("""
                    CREATE TABLE files(id INTEGER PRIMARY KEY AUTOINCREMENT  UNIQUE NOT NULL,
                                        file TEXT NOT NULL,
                                        path TEXT NOT NULL,
                                        time TIMESTAMP NOT NULL,
                                        fav BOOLEAN NOT NULL)""")
            print("[INFO] database create successfull.")

    def add_folder(self, name : str , parent_path : str):

        folder_path = path_manager.get_path_for_folder(parent_path, self.get_paths(parent_path))

        now = datetime.datetime.now()
        with db_injector(self.path) as cursor:
            cursor.execute("INSERT INTO folders(name, path, time, fav) VALUES(?, ?, ?, ?)", (name, folder_path,
                                                                                               now, False))
        return folder_path

    def add_file(self, file : str , path : str):

        now = datetime.datetime.now()
        with db_injector(self.path) as cursor:
            cursor.execute("""INSERT INTO files(file , path, time ,fav) VALUES (?, ?, ?, ?)""" ,(file, path, now, False))

    def add_files(self, file_list : list[str], path):

        now = datetime.datetime.now()
        with db_injector(self.path) as cursor:
            for file in file_list:
                cursor.execute(f"""INSERT INTO files(file , path, time ,fav) VALUES (?, ?, ?, ?)""", (file, path, now, False))

        print(now)
        return now


    def get_paths(self, parent_path : str):

        paths = []
        with db_injector(self.path, False) as cursor:
            cursor.execute("SELECT path FROM folders WHERE path LIKE ? ORDER BY path", (f"{parent_path}_%",))
            paths = [x[0] for  x in cursor.fetchall()]

        # filter paths
        paths_ = []
        for item in paths:
            if parent_path == ".":
                if len(item.split(".")) == 2:
                    paths_.append(item)
            else:
                if len(parent_path.split(".")) + 1 == len(item.split(".")):
                    paths_.append(item)

        return paths_

    def open_folder(self, path : str):

        with db_injector(self.path, False) as cursor:
            cursor.execute(f"SELECT name, path, time, fav FROM folders WHERE path LIKE ? ORDER BY time " ,
                           (f"{path}_%", ))
            paths = cursor.fetchall()

            paths_ = []
            for item in paths:
                if path == ".":
                    if len(item[1].split(".")) == 2:
                        paths_.append(item)
                else:
                    if len(path.split(".")) + 1 == len(item[1].split(".")):
                        paths_.append(item)

            return paths_

        return []

    def open_files(self, path  : str):

        with db_injector(self.path, False) as cursor:
            cursor.execute(
                f"SELECT file, path, time, fav FROM files WHERE path = ? ORDER BY time ", (path, ))
            return cursor.fetchall()

        return []

    def get_folder_name(self, path : str):

        with db_injector(self.path, False) as cursor:
            cursor.execute(f"SELECT name FROM folders WHERE path = '{path}' ")
            data = cursor.fetchall()
            if data:
                name = data[0][0]
            else:
                name = None

        return name

    def get_files(self, path : str):

        file_list = []
        with db_injector(self.path, False) as cursor:
            cursor.execute(f"SELECT file FROM files WHERE path = '{path}' ORDER  BY name")
            data = cursor.fetchall()
            if data:
                file_list = [x[0] for x in data]

        return file_list

    def folder(self, path):

        with db_injector(self.path, False) as cursor:
            cursor.execute(
                "SELECT name, path ,time, fav FROM folders WHERE path LIKE ? ", (path ,))
            return cursor.fetchall()[0]

        return []