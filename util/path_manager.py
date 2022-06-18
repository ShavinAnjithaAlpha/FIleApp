import os.path
from PyQt5.QtCore import QTime, QDate

class path_manager:
    FOLDER_ICONS = {
        "N": "img/sys/yellow_folder.png",
        "I": "img/sys/image_folder.png",
        "V": "img/sys/video_folder.png",
        "D": "img/sys/doc_folder.png",
        "S": "img/sys/system.png",
        "RED": "img/sys/red_folder.png",
        "GREEN": "img/sys/green_folder.png",
        "BLUE": "img/sys/blue_folder.png",
        "ORANGE": "img/sys/orange_folder.png",
        "YELLOW": "img/sys/yellow_folder.png"
    }

    FILE_ICONS = {
        ".pdf": "img/sys/pdf.png",
        ".txt": "img/sys/text-format.png",
        ".html": "img/sys/html-5.png",
        ".js": "img/sys/js.png",
        ".css": "img/sys/css-3.png",
        ".docx": "img/sys/doc.png",
        ".zip": "img/sys/zip (1).png",
        ".rar": "img/sys/rar.png",
        ".py": "img/sys/python.png",
        ".java": "img/sys/java.png",
        ".mp4": "img/sys/video_folder.png",
        ".mkv": "img/sys/video_folder.png"
    }

    @staticmethod
    def filter_sub_path(parent_path : str , full_path : str):

        sub_path = ""
        for i in range(len(full_path)):
            if not(i < len(parent_path) and parent_path[i] == full_path[i]):
                sub_path += full_path[i]
        if sub_path == "":
            return ""
        return sub_path[1:]

    @staticmethod
    def get_last_index(path : str) -> int:
        if "." in path:
            return int(path.split(".")[-1])
        elif path.isnumeric():
            return int(path)
        else:
            return None

    @staticmethod
    def get_path_for_folder(parent_path  :str, paths) -> str:
        # filter the paths last index
        if paths == []:
            x = 0
        else:
            x = max([path_manager.get_last_index(path_) for path_ in paths]) + 1
        if parent_path.endswith("."):
            return f"{parent_path}{x}"
        else:
            # return the new folder path
            return f"{parent_path}.{x}"

    @staticmethod
    def get_file_ext(file : str) -> str:
        return os.path.splitext(file)[1]

    @staticmethod
    def get_file_name(file : str) -> str:
        return os.path.split(file)[1]

    @staticmethod
    def size(file : str) -> str:

        try:
            size = os.stat(file).st_size

            if size < 1024:
                return f"{size} Bytes"
            elif size < 1024 *1024:
                return "{:.2f} KB".format(size/1024)
            else:
                return "{:.2f} MB".format(size/1024/1024)

        except:
            return "None"

    @staticmethod
    def get_folder_icon(file_item: str) -> str:
        return path_manager.FOLDER_ICONS.get(file_item, "img/sys/folder (3).png")

    @staticmethod
    def get_folder_icon(file_item : list) -> str:
        return path_manager.FOLDER_ICONS.get(file_item[4], "img/sys/folder (3).png")



    @staticmethod
    def get_file_icon(file : str) -> str:
        return path_manager.FILE_ICONS.get(path_manager.get_file_ext(file), "img/sys/file.png")

    @staticmethod
    def get_file_icon(file: list) -> str:
        return path_manager.FILE_ICONS.get(path_manager.get_file_ext(file[0]), "img/sys/file.png")

    @staticmethod
    def formatTime(text : str) -> str:

        date, time = text.split(" ")
        time_ , date_ = QTime.fromString(time.split(".")[0], "hh:mm:ss") , QDate.fromString(date, "yyyy-MM-dd")

        formatted_date, formatted_time = date_.toString("yyyy MMM dd"), time_.toString("hh:mm A")

        return f"created on {formatted_date} {formatted_time}"

    @staticmethod
    def get_folder_size(db_manager, folder_path : str) -> str:

        return "{} folders".format(db_manager.folder_count(folder_path))
