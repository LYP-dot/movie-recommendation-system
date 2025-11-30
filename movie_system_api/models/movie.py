from movie_system_api.db_config import get_connection
import pymysql


def get_movies_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM movie;")
        result = cursor.fetchone()
        return result['count'] if result else 0  # 修改这里
    except Exception as e:
        print(f"获取电影数量错误: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_all_movies():
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT m.*, 
                   AVG(r.score) as avg_score,
                   GROUP_CONCAT(DISTINCT g.genre_name) as genres
            FROM movie m 
            LEFT JOIN rating r ON m.movie_id = r.movie_id 
            LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
            LEFT JOIN genre g ON mg.genre_id = g.genre_id
            GROUP BY m.movie_id
            ORDER BY m.movie_id DESC
        """)
        movies = cursor.fetchall()

        # 处理 genres 字段格式
        for movie in movies:
            if movie.get('genres'):
                movie['genres'] = movie['genres'].split(',')
            else:
                movie['genres'] = []

            # 确保 avg_score 是浮点数
            if movie['avg_score']:
                movie['avg_score'] = float(movie['avg_score'])
            else:
                movie['avg_score'] = 0.0

        return movies
    except Exception as e:
        print(f"获取电影列表错误: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_movie_by_id(movie_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT m.*, 
                   AVG(r.score) as avg_score,
                   GROUP_CONCAT(DISTINCT g.genre_name) as genres
            FROM movie m 
            LEFT JOIN rating r ON m.movie_id = r.movie_id 
            LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
            LEFT JOIN genre g ON mg.genre_id = g.genre_id
            WHERE m.movie_id = %s
            GROUP BY m.movie_id
        """, (movie_id,))
        movie = cursor.fetchone()

        if movie and movie.get('genres'):
            movie['genres'] = movie['genres'].split(',')
        elif movie:
            movie['genres'] = []

        if movie and movie.get('avg_score'):
            movie['avg_score'] = float(movie['avg_score'])

        return movie
    except Exception as e:
        print(f"获取电影错误: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def add_movie(title, release_year=None, language=None, duration=None, director=None, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO movie (title, release_year, language, duration, director, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title, release_year, language, duration, director, description))
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        print(f"添加电影错误: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def update_movie(movie_id, title=None, release_year=None, language=None, duration=None, director=None,
                 description=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        updates = []
        params = []
        if title: updates.append("title=%s"); params.append(title)
        if release_year: updates.append("release_year=%s"); params.append(release_year)
        if language: updates.append("language=%s"); params.append(language)
        if duration: updates.append("duration=%s"); params.append(duration)
        if director: updates.append("director=%s"); params.append(director)
        if description: updates.append("description=%s"); params.append(description)
        if not updates:
            return 0
        sql = "UPDATE movie SET " + ", ".join(updates) + " WHERE movie_id=%s;"
        params.append(movie_id)
        cursor.execute(sql, params)
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"更新电影错误: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()


def delete_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM movie WHERE movie_id=%s;", (movie_id,))
        conn.commit()
        affected = cursor.rowcount
        return affected
    except Exception as e:
        print(f"删除电影错误: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()