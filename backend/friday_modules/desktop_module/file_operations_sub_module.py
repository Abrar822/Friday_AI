from pathlib import Path
import pygetwindow as gw
import os
from send2trash import send2trash

class FileOperationsSubModule:

    def __init__(self):
        self.actions = {
            "create_file": self.create_file,
            "create_folder": self.create_folder,
            "open_file": self.open_file,
            "open_folder": self.open_folder,
            "delete_file": self.delete_file,
            "delete_folder": self.delete_folder,
            "rename_file": self.rename_file,
            "rename_folder": self.rename_folder,
            "close_file": self.close_file,
            "move_folder": self.move_folder,
            "move_file": self.move_file,
            "search_file": self.search_file,
            "search_folder": self.search_folder,
        }


    def search_folder(self, task, req):
        pass

    def search_file(self, task, req):
        pass

    def move_folder(self, task, req):
        pass

    def move_file(self, task, req):
        pass

    def create_file(self, task, req):
        foldername = task.parameters.foldername
        filename = task.parameters.filename
        content = task.parameters.content

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / filename
        if file_path.exists():
            return f"File '{filename}' already exists inside '{folder_path}'."

        file_path.write_text(content, encoding="utf-8")
        return f"File '{filename}' created inside folder '{foldername}' successfully."

    def create_folder(self, task, req):
        destination_folder = task.parameters.destination_foldername
        foldername = task.parameters.folder_to_be_created_name

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == destination_folder.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{destination_folder}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"]) / foldername
        if folder_path.exists():
            return f"Folder '{foldername}' already exists on machine."

        folder_path.mkdir(parents=True, exist_ok=True)
        return f"Folder '{foldername}' created inside folder '{destination_folder}' successfully."

    def close_file(self, task):
        filename = task.parameters.filename
        for window in gw.getAllWindows():
            if filename.lower() in window.title.lower():
                window.close()
                return f"File '{filename}' closed successfully."
        return f"File '{filename}' is not opened."

    def open_file(self, task, req):
        filename = task.parameters.filename
        foldername = task.parameters.foldername

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.exists():
            return f"Folder '{foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        file_path = folder_path / filename
        if not file_path.is_file():
            return f"File '{filename}' was not found inside '{folder_path}'."

        try:
            os.startfile(file_path)
            return f"File '{filename}' opened successfully."
        except Exception as err:
            return f"Failed to open file '{filename}'. Error: '{str(err)}'."

    def open_folder(self, task, req):
        foldername = task.parameters.foldername
        parent_foldername = task.parameters.parent_foldername

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == parent_foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{parent_foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.exists():
            return f"Folder '{parent_foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        folder_path = folder_path / foldername
        if not folder_path.is_dir():
            return f"Folder '{foldername}' was not found inside '{parent_foldername}'."

        try:
            os.startfile(folder_path)
            return f"Folder '{foldername}' opened successfully."
        except Exception as err:
            return f"Failed to open folder '{foldername}'. Error: '{str(err)}'."

    def delete_file(self, task, req):
        foldername = task.parameters.foldername
        filename = task.parameters.filename

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.exists():
            return f"Folder '{foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        file_path = folder_path / filename
        if not file_path.is_file():
            return f"File '{filename}' was not found inside '{folder_path}'."

        send2trash(file_path)
        return f"File {filename} sent to trash from folder '{foldername}' successfully."

    def delete_folder(self, task, req):
        parent_foldername = task.parameters.parent_foldername
        folder_to_be_deleted = task.parameters.folder_to_be_deleted_name

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == parent_foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{parent_foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{parent_foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        folder_path = folder_path / folder_to_be_deleted
        if not folder_path.is_dir():
            return f"Folder '{folder_to_be_deleted}' was not found inside '{parent_foldername}'."

        send2trash(folder_path)
        return f"Folder {folder_to_be_deleted} sent to trash successfully."

    def rename_file(self, task, req):
        foldername = task.parameters.foldername
        filename = task.parameters.filename
        new_filename = task.parameters.new_filename

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.exists():
            return f"Folder '{foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        file_path = folder_path / filename
        if not file_path.is_file():
            return f"File '{filename}' was not found inside '{folder_path}'."

        if Path(folder_path / new_filename).is_file():
            return f"A file named '{new_filename}' already exists. Please choose a different name."

        new_path = file_path.with_name(new_filename)
        file_path.rename(new_path)
        return f"File '{filename}' renamed to '{new_filename}' successfully."

    def rename_folder(self, task, req):
        old_foldername = task.parameters.old_foldername
        new_foldername = task.parameters.new_foldername
        parent_foldername = task.parameters.parent_foldername

        location_list = list(
            filter(
                lambda x: x["f_name"].lower() == parent_foldername.strip().lower(),
                req.app.state.locations,
            )
        )
        if not location_list:
            return f"Folder '{parent_foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{parent_foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        if not Path(folder_path / old_foldername).is_dir():
            return f"Folder '{old_foldername}' was not found inside '{folder_path}'."

        if Path(folder_path / new_foldername).is_dir():
            return f"A folder named '{new_foldername}' already exists. Please choose a different name."

        folder_path = folder_path / old_foldername
        new_folder_path = folder_path.with_name(new_foldername)
        folder_path.rename(new_folder_path)
        return f"Folder '{old_foldername}' renamed to '{new_foldername}' successfully."

    def execute(self, task):
        action = self.actions.get(task.action)
        if action:
            return action(task)
