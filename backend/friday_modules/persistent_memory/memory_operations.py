from .db import get_conn_obj


def fetch_locations(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        query = """SELECT f_name, location FROM memory"""
        cursor.execute(query)
        rows = cursor.fetchall()
        file_data = [{"f_name": row[0], "location": row[1]} for row in rows]
        return file_data
    finally:
        if cursor:
            cursor.close()


def upsert(foldername: str, folder_path: str):
    conn = None
    cur = None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """
        UPDATE memory SET location = ?
        WHERE f_name = ?
        """
        cur.execute(query, (folder_path, foldername.lower().strip()))
        if cur.rowcount > 0:
            conn.commit()
            return {"state": True, "exist": True}
        else:
            return {"state": True, "exist": False}
    except Exception as e:
        if conn:
            conn.rollback()
        return {"state": False, "exist": None}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def delete(foldername: str):
    conn = None
    cur = None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """
        DELETE FROM memory where f_name = ?
        """
        cur.execute(query, (foldername.lower().strip(),))
        if cur.rowcount > 0:
            conn.commit()
        return {"state": True}
    except:
        if conn:
            conn.rollback()
        return {"state": False}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def rename(old_foldername: str, new_foldername: str, folder_path: str):
    conn = None
    cur = None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """
        UPDATE memory SET f_name = ?, location = ?
        WHERE f_name = ?
        """
        cur.execute(
            query,
            (
                new_foldername.lower().strip(),
                folder_path,
                old_foldername.lower().strip(),
            ),
        )
        if cur.rowcount > 0:
            conn.commit()
            return {"state": True, "exist": True}
        else:
            return {"state": True, "exist": False}
    except:
        if conn:
            conn.rollback()
        return {"state": False, "exist": None}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
