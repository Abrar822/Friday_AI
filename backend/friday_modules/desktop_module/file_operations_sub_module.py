from pathlib import Path
import pygetwindow as gw
import os
from send2trash import send2trash
import shutil
from ..persistent_memory import locations
from ..persistent_memory.memory_operations import (
    upsert,
    delete,
    rename,
    fetch_locations,
    rename_direct,
    delete_direct,
    upsert_direct
)
from ..persistent_memory.db import get_conn_obj


class FileOperationsSubModule:

    def filter_location_list(self, locations: list, foldername: str):
        return list(
            filter(
                lambda x: x["f_name"].lower() == foldername.lower().strip(), locations
            )
        )

    def search_folder(self, task):
        parent_foldername = task.parameters.parent_foldername
        foldername = task.parameters.foldername

        location_list = self.filter_location_list(
            locations.locations, parent_foldername
        )
        if not location_list:
            return f"Folder '{parent_foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{parent_foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        for p in folder_path.rglob("*"):
            if p.is_dir() and foldername.lower().strip() == p.name.lower().strip():
                os.startfile(p)
                return f"Folder '{foldername}' successfully found."
        return f"Folder '{foldername}' not found inside folder '{parent_foldername}'."

    def search_file(self, task):
        foldername = task.parameters.parent_foldername
        filename = task.parameters.filename

        location_list = self.filter_location_list(locations.locations, foldername)
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        for p in folder_path.rglob("*"):
            if p.is_file() and p.name.lower().strip() == filename.lower().strip():
                os.startfile(p.parent)
                return f"File '{filename}' successfully found."
        return f"File '{filename}' not found inside folder '{foldername}'."

    def move_folder(self, task):
        destination_folder = task.parameters.destination_folder
        source_parent_folder = task.parameters.source_parent_folder
        folder_to_move = task.parameters.folder_to_move

        source_parent_folder_path_res = self.filter_location_list(
            locations.locations, source_parent_folder
        )
        if not source_parent_folder_path_res:
            return (
                f"Folder '{source_parent_folder}' is not registered in Friday memory."
            )
        source_parent_folder_path = source_parent_folder_path_res[0]["location"]

        destination_folder_path_res = self.filter_location_list(
            locations.locations, destination_folder
        )
        if not destination_folder_path_res:
            return f"Folder '{destination_folder}' is not registered in Friday memory."
        destination_folder_path = destination_folder_path_res[0]["location"]

        source_parent_folder_path = Path(source_parent_folder_path)
        if not source_parent_folder_path.is_dir():
            return f"Folder '{source_parent_folder}' is registered, but the physical path '{source_parent_folder_path}' does not exist on this machine."

        destination_folder_path = Path(destination_folder_path)
        if not destination_folder_path.is_dir():
            return f"Folder '{destination_folder}' is registered, but the physical path '{destination_folder_path}' does not exist on this machine."

        actual_folder_path = source_parent_folder_path / folder_to_move
        if not actual_folder_path.is_dir():
            return f"Folder '{folder_to_move}' was not found inside '{source_parent_folder}'."

        new_folder_path = destination_folder_path / folder_to_move
        if new_folder_path.exists():
            return f"Folder '{folder_to_move}' already exists on machine."
        try:
            msg = f"Folder {folder_to_move} moved successfully."
            shutil.move(actual_folder_path, destination_folder_path)
            os.startfile(new_folder_path)

            res = upsert(folder_to_move, str(new_folder_path))
            # Updating the RAM db data and here with auto closes conn
            with get_conn_obj() as conn:
                locations.locations = fetch_locations(conn)

            if res["state"] and res["exist"]:
                msg += " Folder Path updated successfully in Friday memory."
            elif not res["state"]:
                msg += " Folder Path cannot be updated, as some error occurred."
            return msg
        except Exception as err:
            return f"Failed to move folder. Error: {err}"

    def move_file(self, task):
        source_parent_folder = task.parameters.source_parent_folder
        destination_folder = task.parameters.destination_folder
        filename = task.parameters.filename

        location_list = self.filter_location_list(
            locations.locations, source_parent_folder
        )
        if not location_list:
            return (
                f"Folder '{source_parent_folder}' is not registered in Friday memory."
            )

        source_parent_folder_path = Path(location_list[0]["location"])
        if not source_parent_folder_path.is_dir():
            return f"Folder '{source_parent_folder}' is registered, but the physical path '{source_parent_folder_path}' does not exist on this machine."

        location_list = self.filter_location_list(
            locations.locations, destination_folder
        )
        if not location_list:
            return f"Folder '{destination_folder}' is not registered in Friday memory."

        destination_folder_path = Path(location_list[0]["location"])
        if not destination_folder_path.is_dir():
            return f"Folder '{destination_folder}' is registered, but the physical path '{destination_folder_path}' does not exist on this machine."

        old_file_path = source_parent_folder_path / filename
        if not old_file_path.is_file():
            return (
                f"File '{filename}' was not found inside '{source_parent_folder_path}'."
            )

        new_file_path = destination_folder_path / filename
        try:
            shutil.move(old_file_path, new_file_path)
            os.startfile(destination_folder_path)
            return f"File {filename} moved successfully."
        except Exception as err:
            return f"Failed to move file. Error: {err}"

    def create_file(self, task):
        foldername = task.parameters.foldername
        filename = task.parameters.filename
        content = task.parameters.content

        location_list = self.filter_location_list(locations.locations, foldername)
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / filename
        if file_path.is_file():
            return f"File '{filename}' already exists inside '{folder_path}'."

        file_path.write_text(content, encoding="utf-8")
        os.startfile(file_path)
        return f"File '{filename}' created inside folder '{foldername}' successfully."

    def create_folder(self, task):
        destination_folder = task.parameters.destination_foldername
        foldername = task.parameters.folder_to_be_created_name

        location_list = self.filter_location_list(
            locations.locations, destination_folder
        )
        if not location_list:
            return f"Folder '{destination_folder}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.exists():
            return f"Folder '{foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        folder_path = Path(location_list[0]["location"]) / foldername
        if folder_path.exists():
            return f"Folder '{foldername}' already exists on machine."

        folder_path.mkdir(parents=True)
        os.startfile(folder_path)
        return f"Folder '{foldername}' created inside folder '{destination_folder}' successfully."

    def close_file(self, task):
        filename = task.parameters.filename

        for window in gw.getAllWindows():
            if filename.lower() in window.title.lower():
                window.close()
                return
        return f"File '{filename}' is not opened."

    def open_file(self, task):
        filename = task.parameters.filename
        foldername = task.parameters.foldername
        location_list = self.filter_location_list(locations.locations, foldername)
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
            return
        except Exception as err:
            return f"Failed to open file '{filename}'. Error: '{str(err)}'."

    def open_folder(self, task):
        foldername = task.parameters.foldername
        parent_foldername = task.parameters.parent_foldername

        location_list = self.filter_location_list(
            locations.locations, parent_foldername
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
            return
        except Exception as err:
            return f"Failed to open folder '{foldername}'. Error: '{str(err)}'."

    def delete_file(self, task):
        foldername = task.parameters.foldername
        filename = task.parameters.filename

        location_list = self.filter_location_list(locations.locations, foldername)
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

    def delete_folder(self, task):
        parent_foldername = task.parameters.parent_foldername
        folder_to_be_deleted = task.parameters.folder_to_be_deleted_name

        location_list = self.filter_location_list(
            locations.locations, parent_foldername
        )
        if not location_list:
            return f"Folder '{parent_foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{parent_foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        folder_path = folder_path / folder_to_be_deleted
        if not folder_path.is_dir():
            return f"Folder '{folder_to_be_deleted}' was not found inside '{parent_foldername}'."

        msg = f"Folder {folder_to_be_deleted} sent to trash successfully."
        send2trash(folder_path)
        os.startfile(Path(location_list[0]["location"]))

        res = delete(folder_to_be_deleted)

        # updation in db data in RAM
        with get_conn_obj() as conn:
            locations.locations = fetch_locations(conn)

        if res["state"]:
            msg += " Folder Path deleted successfully from Friday memory."
        else:
            msg += " Folder Path cannot be updated, as some error occurred."
        return msg

    def rename_file(self, task):
        foldername = task.parameters.foldername
        filename = task.parameters.filename
        new_filename = task.parameters.new_filename

        location_list = self.filter_location_list(locations.locations, foldername)
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
        os.startfile(file_path)
        return f"File '{filename}' renamed to '{new_filename}' successfully."

    def rename_folder(self, task):
        old_foldername = task.parameters.old_foldername
        new_foldername = task.parameters.new_foldername
        parent_foldername = task.parameters.parent_foldername

        location_list = self.filter_location_list(
            locations.locations, parent_foldername
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

        msg = f"Folder '{old_foldername}' renamed to '{new_foldername}' successfully."

        res = rename(
            old_foldername,
            new_foldername,
            str(new_folder_path),
        )

        # updation in ram data of db
        with get_conn_obj() as conn:
            locations.locations = fetch_locations(conn)

        if res["state"] and res["exist"]:
            msg += " Foldername updated successfully in Friday memory."
        elif not res["state"]:
            msg += " Foldername cannot be updated, as some error occurred."

        return msg

    def rename_folder_direct(self, task):
        old_foldername = task.parameters.old_foldername
        new_foldername = task.parameters.new_foldername

        location_list = self.filter_location_list(locations.locations, old_foldername)
        if not location_list:
            return f"Folder '{old_foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{old_foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        new_folder_path = folder_path.with_name(new_foldername)
        if new_folder_path.is_dir():
            return f"Folder {new_foldername} already exists."

        folder_path.rename(new_folder_path)
        msg = f"Folder '{old_foldername}' renamed to '{new_foldername}' successfully."

        res = rename_direct(old_foldername, new_foldername, str(new_folder_path))
        if res["state"] and res["exist"]:
            msg += " Foldername updated successfully in Friday memory."
        elif not res["state"]:
            msg += " Foldername cannot be updated, as some error occurred."

        with get_conn_obj() as conn:
            locations.locations = fetch_locations(conn)

        return msg

    def delete_folder_direct(self, task):
        foldername = task.parameters.folder_to_be_deleted_name

        location_list = self.filter_location_list(locations.locations, foldername)
        if not location_list:
            return f"Folder '{foldername}' is not registered in Friday memory."

        folder_path = Path(location_list[0]["location"])
        if not folder_path.is_dir():
            return f"Folder '{foldername}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        msg = f"Folder {foldername} sent to trash successfully."
        send2trash(folder_path)

        res = delete_direct(foldername)
        if res["state"]:
            msg += " Folder Path deleted successfully from Friday memory."
        else:
            msg += " Folder Path cannot be updated, as some error occurred."
        with get_conn_obj() as conn:
            locations.locations = fetch_locations(conn)

        return msg

    def move_folder_direct(self, task):
        folder_to_be_moved = task.parameters.folder_to_be_moved
        destination_folder = task.parameters.destination_folder

        location_list = self.filter_location_list(locations.locations, folder_to_be_moved)
        if not location_list:
            return (
                f"Folder '{folder_to_be_moved}' is not registered in Friday memory."
            )
        folder_path = Path(location_list[0]['location'])

        location_list = self.filter_location_list(locations.locations, destination_folder)
        if not location_list:
            return (
                f"Folder '{destination_folder}' is not registered in Friday memory."
            )
        destination_folder_path = Path(location_list[0]['location'])

        if not folder_path.is_dir():
            return f"Folder '{folder_to_be_moved}' is registered, but the physical path '{folder_path}' does not exist on this machine."

        if not destination_folder_path.is_dir():
            return f"Folder '{destination_folder}' is registered, but the physical path '{destination_folder_path}' does not exist on this machine."

        try:
            shutil.move(folder_path, destination_folder_path)
            msg = f"Folder {folder_to_be_moved} moved successfully."
            os.startfile(destination_folder_path)

            new_path = destination_folder_path / folder_to_be_moved
            res = upsert_direct(folder_to_be_moved, str(new_path))
            
            if res["state"] and res["exist"]:
                msg += " Folder Path updated successfully in Friday memory."
            elif not res["state"]:
                msg += " Folder Path cannot be updated, as some error occurred."

            with get_conn_obj() as conn:
                locations.locations = fetch_locations(conn)

            return msg
        except Exception as err:
            return f'Some Error occurred. Error: {err}'