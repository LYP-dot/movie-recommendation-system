from movie_system_api.db_config import get_connection

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id=%s;", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s;", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_user(username, password_hash, nickname=None, age=None, gender=None, favorite_genre_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO user (username, password_hash, nickname, age, gender, favorite_genre_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (username, password_hash, nickname, age, gender, favorite_genre_id))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id

def update_user(user_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    for key, value in kwargs.items():
        if value is not None:
            updates.append(f"{key}=%s")
            params.append(value)
    if not updates:
        cursor.close()
        conn.close()
        return 0
    sql = "UPDATE user SET " + ", ".join(updates) + " WHERE user_id=%s;"
    params.append(user_id)
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE user_id=%s;", (user_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected

def get_users_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM user;")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['count'] if result else 0
