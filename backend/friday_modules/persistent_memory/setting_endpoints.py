from fastapi import APIRouter, HTTPException, status, Depends
from ...pydantic_models.persistent_memory_module.persistent_memory_models import (
    SettingData,
)
from .db import get_connection

setting_endpoints = APIRouter()


@setting_endpoints.post("/settings", status_code=status.HTTP_201_CREATED)
def set_data(data: SettingData, conn=Depends(get_connection)):
    cur = None
    try:
        cur = conn.cursor()
        query = """INSERT INTO keyval (key, value) VALUES (?, ?)
        ON CONFLICT (KEY)
        DO UPDATE SET value = EXCLUDED.value
        """
        cur.execute(
            query,
            (
                "name",
                data.name,
            ),
        )
        if cur.rowcount > 0:
            conn.commit()
            return {"message": "Data inserted successfully."}
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
