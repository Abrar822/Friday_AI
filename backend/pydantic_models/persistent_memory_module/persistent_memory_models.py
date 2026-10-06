from pydantic import BaseModel
from typing import Literal


class SearchLocation(BaseModel):
    f_name: str


class FolderPaths(BaseModel):
    folder_locations: list[str]


class DeleteData(BaseModel):
    f_name: str


class SettingData(BaseModel):
    name: str
    api_key: str
    llm_mode: Literal["groq", "qwen"]
