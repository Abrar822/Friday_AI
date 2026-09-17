from fastapi import APIRouter, Depends, status, HTTPException
from ...pydantic_models.persistent_memory_module.persistent_memory_models import (
    SearchLocation,
    FolderPaths,
    DeleteData,
)
from pathlib import Path
from .db import get_connection

memory_endpoints = APIRouter()


# To search for a location
@memory_endpoints.post("/search", status_code=status.HTTP_200_OK)
def search_location(search_location: SearchLocation, conn=Depends(get_connection)):
    try:
        cursor = conn.cursor()
        query = """SELECT * FROM memory WHERE f_name like ?"""
        cursor.execute(query, (f'%{search_location.f_name.lower()}%',))
        data = cursor.fetchall()
        return data
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


# To upsert the locations
@memory_endpoints.post("/insert", status_code=status.HTTP_201_CREATED)
def insert_data(folder_arr: FolderPaths, conn=Depends(get_connection)):
    folder_paths = folder_arr.folder_locations
    folder_details = []
    for path in folder_paths:
        path = Path(path)
        if path.name == "":
            fname = str(path)[0].lower().strip()
        else:
            fname = path.name.lower()
        if path.is_dir():
            folder_details.append({"f_name": fname, "location": str(path)})

    try:
        query = """
        INSERT INTO memory (f_name, location) VALUES (?, ?) 
        ON CONFLICT (f_name)
        DO UPDATE SET location = excluded.location
        """
        conn.executemany(
            query, [(row["f_name"], row["location"]) for row in folder_details]
        )
        conn.commit()
        return {"message": "Successfully inserted/updated locations"}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


# To display all locations
@memory_endpoints.get("/display", status_code=status.HTTP_200_OK)
def display(conn=Depends(get_connection)):
    try:
        query = """
        SELECT * FROM memory
        """
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


# To delete the particular f_name entry
@memory_endpoints.delete("/delete", status_code=status.HTTP_200_OK)
def delete(delete_f_name: list[DeleteData], conn=Depends(get_connection)):
    try:
        query = """
        DELETE FROM memory where f_name = ?
        """
        conn.executemany(query, [(dic.f_name.lower(),) for dic in delete_f_name])
        conn.commit()
        return {"message": "Deleted locations successfully"}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
