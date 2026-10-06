from .db import get_conn_obj
from fastapi import HTTPException, status

def fetch_settings_details():
    conn, cur = None, None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """SELECT * FROM keyval"""
        cur.execute(query)
        data = cur.fetchall()
        data = {d[1]:d[2] for d in data}
        return data
    except Exception as err:
        print(str(err))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Failed to fetch details,')
    finally:
        if cur: cur.close()
        if conn: conn.close()