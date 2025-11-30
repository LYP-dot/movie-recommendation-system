from movie_system_api.db_config import get_connection
import pymysql

def get_ratings_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM rating;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"获取评分数量错误: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_all_ratings():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT r.*, u.username, u.nickname, m.title as movie_title 
            FROM rating r 
            LEFT JOIN user u ON r.user_id = u.user_id 
            LEFT JOIN movie m ON r.movie_id = m.movie_id
            ORDER BY r.rating_time DESC
        """)
        ratings = cursor.fetchall()

        # 处理日期格式
        for rating in ratings:
            if rating.get('rating_time'):
                rating['rating_time'] = rating['rating_time'].isoformat()

        return ratings
    except Exception as e:
        print(f"获取评分数据失败: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_rating_by_id(rating_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT r.*, u.username, u.nickname, m.title as movie_title 
            FROM rating r 
            LEFT JOIN user u ON r.user_id = u.user_id 
            LEFT JOIN movie m ON r.movie_id = m.movie_id
            WHERE r.rating_id = %s
        """, (rating_id,))
        rating = cursor.fetchone()

        if rating and rating.get('rating_time'):
            rating['rating_time'] = rating['rating_time'].isoformat()

        return rating
    except Exception as e:
        print(f"获取评分失败: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def add_rating(user_id, movie_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO rating (user_id, movie_id, score) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, movie_id, score))
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        print(f"添加评分失败: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def update_rating(rating_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "UPDATE rating SET score=%s WHERE rating_id=%s"
        cursor.execute(sql, (score, rating_id))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"更新评分失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def delete_rating(rating_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM rating WHERE rating_id=%s", (rating_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"删除评分失败: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def search_ratings(search_term=None, score=None, date=None, page=1, limit=10):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
        SELECT r.*, u.username, u.nickname, m.title as movie_title 
        FROM rating r 
        LEFT JOIN user u ON r.user_id = u.user_id 
        LEFT JOIN movie m ON r.movie_id = m.movie_id
        WHERE 1=1
        """
        params = []

        if search_term:
            sql += " AND (u.username LIKE %s OR u.nickname LIKE %s OR m.title LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])

        if score:
            sql += " AND r.score = %s"
            params.append(score)

        if date:
            sql += " AND DATE(r.rating_time) = %s"
            params.append(date)

        sql += " ORDER BY r.rating_time DESC"

        # 获取总数
        count_sql = "SELECT COUNT(*) as total FROM (" + sql + ") as count_table"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']

        # 添加分页
        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, (page - 1) * limit])

        cursor.execute(sql, params)
        ratings = cursor.fetchall()

        # 处理日期格式
        for rating in ratings:
            if rating.get('rating_time'):
                rating['rating_time'] = rating['rating_time'].isoformat()

        return ratings, total
    except Exception as e:
        print(f"搜索评分错误: {e}")
        return [], 0
    finally:
        cursor.close()
        conn.close()


def get_ratings_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM rating;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"获取评分数量错误: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()