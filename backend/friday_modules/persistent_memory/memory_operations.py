from .db import get_conn_obj
from pathlib import Path
from . import storage_declarations


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
            return {"state": True}
    except Exception as e:
        if conn:
            conn.rollback()
        return {"state": False}
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


def rename_direct(old_foldername: str, new_foldername: str, folder_path: str):
    conn, cur = None, None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """
        UPDATE memory SET f_name = ?, location = ? WHERE f_name = ?
        """
        cur.execute(query, (new_foldername.lower().strip(), folder_path, old_foldername.lower().strip()))
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


def delete_direct(foldername: str):
    conn, cur = None, None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """
        DELETE FROM memory WHERE f_name = ?
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


def upsert_direct(foldername: str, folder_path: str):
    conn, cur = None, None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """
        UPDATE memory SET location = ? WHERE f_name = ?
        """
        cur.execute(query, (folder_path, foldername.lower().strip()))
        if cur.rowcount > 0:
            conn.commit()
        return {"state": True}
    except:
        if cur:
            conn.rollback()
        return {"state": False}
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def remove_stale_paths():
    stale_folders = []
    for obj in storage_declarations.locations:
        f_name = obj["f_name"]
        location = obj["location"]
        if not Path(location).is_dir():
            stale_folders.append((f_name,))

    conn = get_conn_obj()
    cur = conn.cursor()
    query = """
    DELETE FROM memory where f_name = ?
    """
    cur = conn.cursor()
    cur.executemany(query, stale_folders)
    if cur.rowcount:
        conn.commit()
        storage_declarations.locations = fetch_locations(conn)

def handle_renamed_folder_paths(renamedfolder_previous_path: str, old_foldername: str, new_foldername: str):
    updated_folder_details = []
    for obj in storage_declarations.locations:
        f_name = obj['f_name']
        location = obj['location']
        if renamedfolder_previous_path in location:
            new_location = location.replace(old_foldername, new_foldername)
            updated_folder_details.append((new_location, f_name))
            
    conn = get_conn_obj()
    cur = conn.cursor()
    query = """
    UPDATE memory SET location = ? WHERE f_name = ? 
    """
    cur.executemany(query, updated_folder_details)
    if cur.rowcount:
        conn.commit()
        storage_declarations.locations = fetch_locations(conn)
    cur.close()
    conn.close()

def handle_moved_folder_paths(old_folder_path: str, new_folder_path: str):
    updated_folder_details = []
    for obj in storage_declarations.locations:
        location = obj['location']
        f_name = obj['f_name']
        if old_folder_path in location:
            new_location = location.replace(old_folder_path, new_folder_path)
            updated_folder_details.append((new_location, f_name))

    conn = get_conn_obj()
    cur = conn.cursor()
    query = """
    UPDATE memory SET location = ? WHERE f_name = ?
    """
    cur.executemany(query, updated_folder_details)
    if cur.rowcount:
        conn.commit()
        storage_declarations.locations = fetch_locations(conn)
    cur.close()
    conn.close()