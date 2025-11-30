from movie_system_api.db_config import get_connection

def get_all_history():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # 使用 JOIN 查询获取用户名和电影名
        cursor.execute("""
            SELECT h.*, u.username, u.nickname, m.title as movie_title 
            FROM history h 
            LEFT JOIN user u ON h.user_id = u.user_id 
            LEFT JOIN movie m ON h.movie_id = m.movie_id
            ORDER BY h.watch_time DESC
        """)
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        return history
    except Exception as e:
        print(f"获取历史记录失败: {e}")
        return []

def add_history(user_id, movie_id, duration_watched=None, completed=False):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO history (user_id, movie_id, duration_watched, completed) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (user_id, movie_id, duration_watched, completed))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id

def update_history(history_id, duration_watched=None, completed=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if duration_watched is not None: updates.append("duration_watched=%s"); params.append(duration_watched)
    if completed is not None: updates.append("completed=%s"); params.append(completed)
    if not updates:
        cursor.close()
        conn.close()
        return 0
    sql = "UPDATE history SET " + ", ".join(updates) + " WHERE history_id=%s"
    params.append(history_id)
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected

def delete_history(history_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE history_id=%s", (history_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected
