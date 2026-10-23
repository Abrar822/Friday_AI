from fastapi import APIRouter, HTTPException, status, Depends
from ...pydantic_models.persistent_memory_module.persistent_memory_models import (
    SettingData,
)
from .db import get_connection
from .general_db_operations import fetch_settings_details
from . import storage_declarations
from ...core.api_key_handling import get_api_key, set_api_key

setting_endpoints = APIRouter()


@setting_endpoints.post("/settings", status_code=status.HTTP_201_CREATED)
def set_data(data: SettingData, conn=Depends(get_connection)):
    print(data)
    print('start')
    cur = None
    tuples = [(key, val) for key, val in data.model_dump().items() if key != "api_key"]
    try:
        cur = conn.cursor()
        query = """INSERT INTO keyval (key, value) VALUES (?, ?)
        ON CONFLICT (KEY)
        DO UPDATE SET value = EXCLUDED.value
        """
        cur.executemany(query, tuples)
        if cur.rowcount > 0:
            conn.commit()

            settings_details = fetch_settings_details()
            storage_declarations.settings_details["name"] = settings_details["name"]
            storage_declarations.settings_details["llm_mode"] = settings_details[
                "llm_mode"
            ]
            set_api_key(data.api_key)
            storage_declarations.settings_details["api_key"] = get_api_key()
            storage_declarations.settings_details["nickname"] = settings_details[
                "nickname"
            ]
            return {"message": "Changes saved successfully."}
    except Exception as err:
        print(str(err))
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
        data = {key: val for key, val in data}
        data.update({"api_key": get_api_key() or ""})
        return data
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
