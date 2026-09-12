from pydantic import BaseModel, Field
from typing import Literal, Annotated


class NoParams(BaseModel):
    pass


class Conversation(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["conversation"]
    parameters: NoParams


class SetVolumeParams(BaseModel):
    level: int


class SetVolume(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["set_volume"]
    parameters: SetVolumeParams


class SetBrightnessParams(BaseModel):
    level: int


class SetBrightness(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["set_brightness"]
    parameters: SetBrightnessParams


class Shutdown(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["perform_shutdown"]
    parameters: NoParams


class Restart(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["perform_restart"]
    parameters: NoParams


class Lock(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["perform_locking"]
    parameters: NoParams


class Sleep(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["perform_sleep"]
    parameters: NoParams


class Hibernate(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["perform_hibernation"]
    parameters: NoParams


class TakeScreenshot(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["take_screenshot"]
    parameters: NoParams


class OpenLocalAppParams(BaseModel):
    display_name: str


class OpenLocalApp(BaseModel):
    id: int
    module: Literal['desktop']
    action: Literal['open_local_app']
    parameters: OpenLocalAppParams


class MoveFolderParams(BaseModel):
    destination_folder: str
    source_parent_folder: str
    folder_to_move: str


class MoveFolder(BaseModel):
    id: int
    module: Literal['desktop']
    action: Literal['move_folder']
    parameters: MoveFolderParams


class MoveFileParams(BaseModel):
    source_parent_folder: str
    destination_folder: str
    filename: str


class MoveFile(BaseModel):
    id: int
    module: Literal['desktop']
    action: Literal['move_file']
    parameters: MoveFileParams


class SearchFileParams(BaseModel):
    parent_foldername: str
    filename: str


class SearchFile(BaseModel):
    id: int
    module: Literal['desktop']
    action: Literal['search_file']
    parameters: SearchFileParams


class SearchFolderParams(BaseModel):
    foldername: str
    parent_foldername: str


class SearchFolder(BaseModel):
    id: int
    module: Literal['desktop']
    action: Literal['search_folder']
    parameters: SearchFolderParams


class CreateFolderParams(BaseModel):
    destination_foldername: str
    folder_to_be_created_name: str


class CreateFolder(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["create_folder"]
    parameters: CreateFolderParams


class CreateFileParams(BaseModel):
    foldername: str
    filename: str
    content: str


class CreateFile(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["create_file"]
    parameters: CreateFileParams


class OpenFileParams(BaseModel):
    filename: str
    foldername: str


class OpenFile(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["open_file"]
    parameters: OpenFileParams


class OpenFolderParams(BaseModel):
    parent_foldername: str
    foldername: str


class OpenFolder(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["open_folder"]
    parameters: OpenFolderParams


class DeleteFileParams(BaseModel):
    filename: str
    foldername: str


class DeleteFile(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["delete_file"]
    parameters: DeleteFileParams


class DeleteFolderParams(BaseModel):
    parent_foldername: str
    folder_to_be_deleted_name: str


class DeleteFolder(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["delete_folder"]
    parameters: DeleteFolderParams


class RenameFileParams(BaseModel):
    foldername: str
    filename: str
    new_filename: str


class RenameFile(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["rename_file"]
    parameters: RenameFileParams


class RenameFolderParams(BaseModel):
    old_foldername: str
    new_foldername: str
    parent_foldername: str


class RenameFolder(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["rename_folder"]
    parameters: RenameFolderParams


class CloseFileParams(BaseModel):
    filename: str


class CloseFile(BaseModel):
    id: int
    module: Literal["desktop"]
    action: Literal["close_file"]
    parameters: CloseFileParams


DeskTopTask = Annotated[
    SetVolume
    | SetBrightness
    | Shutdown
    | Restart
    | Lock
    | Sleep
    | Hibernate
    | TakeScreenshot
    | OpenLocalApp
    | SearchFile
    | SearchFolder
    | MoveFile
    | MoveFolder
    | CreateFolder
    | CreateFile
    | OpenFile
    | OpenFolder
    | DeleteFile
    | DeleteFolder
    | RenameFile
    | RenameFolder
    | CloseFile
    | Conversation,
    Field(discriminator="action"),
]
