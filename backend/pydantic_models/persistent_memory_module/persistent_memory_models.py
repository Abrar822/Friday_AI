from pydantic import BaseModel


class SearchLocation(BaseModel):
    f_name: str


class FolderPaths(BaseModel):
    folder_locations: list[str]


class DeleteData(BaseModel):
    f_name: str

class SettingData(BaseModel):
    name: str