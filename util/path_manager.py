import os.path
from PyQt5.QtCore import QTime, QDate

class path_manager:
    FOLDER_ICONS = {
        "N": "img/sys/folder_icons/yellow_folder.png",
        "I": "img/sys/folder_icons/folder (9).png",
        "V": "img/sys/folder_icons/video-folder.png",
        "D": "img/sys/folder_icons/file-storage.png",
        "S": "img/sys/folder_icons/folder (10).png",
        "C": "img/sys/folder_icons/folder (4).png",
        "M": "img/sys/folder_icons/music-folder (1).png",
        "U": "img/sys/folder_icons/folder (6).png",
        "RED": "img/sys/folder_icons/empty-folder (1).png",
        "GREEN": "img/sys/folder_icons/green_folder.png",
        "BLUE": "img/sys/folder_icons/blue_folder.png",
        "ORANGE": "img/sys/folder_icons/orange_folder.png",
        "YELLOW": "img/sys/folder_icons/yellow_folder.png"
    }

    TREE_FOLDER_ICON = "img/sys/tree_view_icons/folder-free-icon-font (1).png"

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

    TREE_FILE_ICONS = {
        ".jpg" : "img/sys/tree_view_icons/picture-free-icon-font.png",
        ".png": "img/sys/tree_view_icons/picture-free-icon-font.png",
        ".jpeg": "img/sys/tree_view_icons/picture-free-icon-font.png",
        ".bmp": "img/sys/tree_view_icons/picture-free-icon-font.png",
        ".ico": "img/sys/tree_view_icons/picture-free-icon-font.png",
        ".pdf": "img/sys/tree_view_icons/acrobat-free-icon-font.png",
        ".mp4": "img/sys/tree_view_icons/play-free-icon-font.png",
        ".mkv": "img/sys/tree_view_icons/play-free-icon-font.png",
        ".vob": "img/sys/tree_view_icons/play-free-icon-font.png",
        ".mpeg": "img/sys/tree_view_icons/play-free-icon-font.png",
        ".mp3": "img/sys/tree_view_icons/music-alt-free-icon-font.png",
        ".wav": "img/sys/tree_view_icons/music-alt-free-icon-font.png"
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
    def get_folder_icon(file_item: list) -> str:
        return path_manager.TREE_FOLDER_ICON

    @staticmethod
    def get_main_folder_icon(folder : str) -> str:
        return path_manager.FOLDER_ICONS.get(folder, "img/sys/folder (3).png")


    @staticmethod
    def get_main_file_icon(file : str) -> str:
        return path_manager.FOLDER_ICON.get(path_manager.get_file_ext(file), "img/sys/tree_view_icons/file-free-icon-font(1).png")

    @staticmethod
    def get_file_icon(file: list) -> str:
        return path_manager.TREE_FILE_ICONS.get(path_manager.get_file_ext(file[0]), "img/sys/tree_view_icons/file-free-icon-font (1).png")

    @staticmethod
    def formatTime(text : str) -> str:

        date, time = text.split(" ")
        time_ , date_ = QTime.fromString(time.split(".")[0], "hh:mm:ss") , QDate.fromString(date, "yyyy-MM-dd")

        formatted_date, formatted_time = date_.toString("yyyy MMM dd"), time_.toString("hh:mm A")

        return f"created on {formatted_date} {formatted_time}"

    @staticmethod
    def get_folder_size(db_manager, folder_path : str) -> str:

        return "{} folders".format(db_manager.folder_count(folder_path))
