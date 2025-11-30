from movie_system_api.db_config import get_connection
import pymysql


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # 使用 LEFT JOIN 获取偏好类型名称
        sql = """
        SELECT u.*, g.genre_name as favorite_genre_name 
        FROM user u 
        LEFT JOIN genre g ON u.favorite_genre_id = g.genre_id
        ORDER BY u.register_date DESC
        """
        cursor.execute(sql)
        users = cursor.fetchall()

        # 处理日期格式
        for user in users:
            if user.get('register_date'):
                user['register_date'] = user['register_date'].isoformat()

        return users
    except Exception as e:
        print(f"获取用户列表错误: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
        SELECT u.*, g.genre_name as favorite_genre_name 
        FROM user u 
        LEFT JOIN genre g ON u.favorite_genre_id = g.genre_id 
        WHERE u.user_id=%s
        """
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()

        if user and user.get('register_date'):
            user['register_date'] = user['register_date'].isoformat()

        return user
    except Exception as e:
        print(f"获取用户错误: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM user WHERE username=%s;", (username,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"通过用户名获取用户错误: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def add_user(username, password_hash, nickname=None, age=None, gender=None, favorite_genre_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO user (username, password_hash, nickname, age, gender, favorite_genre_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (username, password_hash, nickname, age, gender, favorite_genre_id))
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        print(f"添加用户错误: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def update_user(user_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key}=%s")
                params.append(value)

        if not updates:
            return 0

        sql = "UPDATE user SET " + ", ".join(updates) + " WHERE user_id=%s;"
        params.append(user_id)
        cursor.execute(sql, params)
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"更新用户错误: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM user WHERE user_id=%s;", (user_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"删除用户错误: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def get_users_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM user;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"获取用户数量错误: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def search_users(search_term=None, gender=None, favorite_genre=None, page=1, limit=10):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
        SELECT u.*, g.genre_name as favorite_genre_name 
        FROM user u 
        LEFT JOIN genre g ON u.favorite_genre_id = g.genre_id
        WHERE 1=1
        """
        params = []

        if search_term:
            sql += " AND (u.username LIKE %s OR u.nickname LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])

        if gender:
            sql += " AND u.gender = %s"
            params.append(gender)

        if favorite_genre:
            sql += " AND u.favorite_genre_id = %s"
            params.append(favorite_genre)

        sql += " ORDER BY u.register_date DESC"

        # 获取总数
        count_sql = "SELECT COUNT(*) as total FROM (" + sql + ") as count_table"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']

        # 添加分页
        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, (page - 1) * limit])

        cursor.execute(sql, params)
        users = cursor.fetchall()

        # 处理日期格式
        for user in users:
            if user.get('register_date'):
                user['register_date'] = user['register_date'].isoformat()

        return users, total
    except Exception as e:
        print(f"搜索用户错误: {e}")
        return [], 0
    finally:
        cursor.close()
        conn.close()