

class path_manager:

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





