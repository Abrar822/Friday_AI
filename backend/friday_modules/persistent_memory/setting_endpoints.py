from fastapi import APIRouter, HTTPException, status, Depends
from ...pydantic_models.persistent_memory_module.persistent_memory_models import (
    SettingData,
)
from .db import get_connection
from .general_db_operations import fetch_settings_details
from . import storage_declarations

setting_endpoints = APIRouter()


@setting_endpoints.post("/settings", status_code=status.HTTP_201_CREATED)
def set_data(data: SettingData, conn=Depends(get_connection)):
    cur = None
    data = [(key, val) for key, val in data.model_dump().items()]
    try:
        cur = conn.cursor()
        query = """INSERT INTO keyval (key, value) VALUES (?, ?)
        ON CONFLICT (KEY)
        DO UPDATE SET value = EXCLUDED.value
        """
        cur.executemany(
            query, data
        )
        if cur.rowcount > 0:
            conn.commit()
            
            settings_details = fetch_settings_details()
            storage_declarations.settings_details['llm_mode'] = settings_details['llm_mode']
            storage_declarations.settings_details['api_key'] = settings_details['api_key']
            return {"message": "Changes saved successfully."}
    except Exception as err:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Some Error Occurred.",
        )
    finally:
        if cur:
            cur.close()


@setting_endpoints.get("/settings_get", status_code=status.HTTP_200_OK)
def get_data(conn=Depends(get_connection)):
    cur = None
    try:
        cur = conn.cursor()
        query = """SELECT key, value FROM keyval"""
        cur.execute(query)
        data = cur.fetchall()
        return {key:val for key, val in data}
    except Exception as err:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Some Error Occurred.",
        )
    finally:
        if cur:
            cur.close()
