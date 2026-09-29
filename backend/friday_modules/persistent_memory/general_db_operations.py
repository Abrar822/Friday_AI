from .db import get_conn_obj

def get_name():
    conn, cur = None, None
    try:
        conn = get_conn_obj()
        cur = conn.cursor()
        query = """SELECT value FROM keyval WHERE key = (?)"""
        cur.execute(query, ('name',))
        return cur.fetchone() 
    except:
        pass
    finally:
        if cur: cur.close()
        if conn: conn.close()