from movie_system_api.db_config import get_connection

def get_all_ratings():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # 使用 JOIN 查询获取用户名和电影名
        cursor.execute("""
            SELECT r.*, u.username, u.nickname, m.title as movie_title 
            FROM rating r 
            LEFT JOIN user u ON r.user_id = u.user_id 
            LEFT JOIN movie m ON r.movie_id = m.movie_id
            ORDER BY r.rating_time DESC
        """)
        ratings = cursor.fetchall()
        cursor.close()
        conn.close()
        return ratings
    except Exception as e:
        print(f"获取评分数据失败: {e}")
        return []

def add_rating(user_id, movie_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO rating (user_id, movie_id, score) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, movie_id, score))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id

def update_rating(rating_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE rating SET score=%s WHERE rating_id=%s"
    cursor.execute(sql, (score, rating_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected

def delete_rating(rating_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rating WHERE rating_id=%s", (rating_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected
