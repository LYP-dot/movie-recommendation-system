from movie_system_api.db_config import get_connection
import pymysql

def get_history_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM history;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"获取历史记录数量错误: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_all_history():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT h.*, u.username, u.nickname, m.title as movie_title 
            FROM history h 
            LEFT JOIN user u ON h.user_id = u.user_id 
            LEFT JOIN movie m ON h.movie_id = m.movie_id
            ORDER BY h.watch_time DESC
        """)
        history = cursor.fetchall()

        # 处理日期格式
        for record in history:
            if record.get('watch_time'):
                record['watch_time'] = record['watch_time'].isoformat()

        return history
    except Exception as e:
        print(f"获取历史记录失败: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_history_by_id(history_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT h.*, u.username, u.nickname, m.title as movie_title 
            FROM history h 
            LEFT JOIN user u ON h.user_id = u.user_id 
            LEFT JOIN movie m ON h.movie_id = m.movie_id
            WHERE h.history_id = %s
        """, (history_id,))
        history = cursor.fetchone()

        if history and history.get('watch_time'):
            history['watch_time'] = history['watch_time'].isoformat()

        return history
    except Exception as e:
        print(f"获取历史记录失败: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def add_history(user_id, movie_id, duration_watched=None, completed=False):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO history (user_id, movie_id, duration_watched, completed) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, movie_id, duration_watched, completed))
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        print(f"添加历史记录失败: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def update_history(history_id, duration_watched=None, completed=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        updates = []
        params = []
        if duration_watched is not None:
            updates.append("duration_watched=%s")
            params.append(duration_watched)
        if completed is not None:
            updates.append("completed=%s")
            params.append(completed)
        if not updates:
            return 0
        sql = "UPDATE history SET " + ", ".join(updates) + " WHERE history_id=%s"
        params.append(history_id)
        cursor.execute(sql, params)
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"更新历史记录失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def delete_history(history_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM history WHERE history_id=%s", (history_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"删除历史记录失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def search_history(search_term=None, completed=None, date=None, page=1, limit=10):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
        SELECT h.*, u.username, u.nickname, m.title as movie_title 
        FROM history h 
        LEFT JOIN user u ON h.user_id = u.user_id 
        LEFT JOIN movie m ON h.movie_id = m.movie_id
        WHERE 1=1
        """
        params = []

        if search_term:
            sql += " AND (u.username LIKE %s OR u.nickname LIKE %s OR m.title LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])

        if completed is not None:
            sql += " AND h.completed = %s"
            params.append(completed)

        if date:
            sql += " AND DATE(h.watch_time) = %s"
            params.append(date)

        sql += " ORDER BY h.watch_time DESC"

        # 获取总数
        count_sql = "SELECT COUNT(*) as total FROM (" + sql + ") as count_table"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']

        # 添加分页
        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, (page - 1) * limit])

        cursor.execute(sql, params)
        history = cursor.fetchall()

        # 处理日期格式
        for record in history:
            if record.get('watch_time'):
                record['watch_time'] = record['watch_time'].isoformat()

        return history, total
    except Exception as e:
        print(f"搜索历史记录错误: {e}")
        return [], 0
    finally:
        cursor.close()
        conn.close()


def get_history_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM history;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"获取历史记录数量错误: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()