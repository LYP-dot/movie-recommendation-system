from movie_system_api.db_config import get_connection
import pymysql


def get_movies_count():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as count FROM movie;")
        result = cursor.fetchone()
        return result['count'] if result else 0
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
                   AVG(r.score) as avg_score
            FROM movie m 
            LEFT JOIN rating r ON m.movie_id = r.movie_id 
            GROUP BY m.movie_id
            ORDER BY m.movie_id DESC
        """)
        movies = cursor.fetchall()

        # 获取每个电影的类型
        for movie in movies:
            # 查询电影类型
            cursor.execute("""
                SELECT g.genre_name 
                FROM movie_genre mg 
                JOIN genre g ON mg.genre_id = g.genre_id 
                WHERE mg.movie_id = %s
            """, (movie['movie_id'],))
            genres = cursor.fetchall()
            movie['genres'] = [genre['genre_name'] for genre in genres]

            # 处理评分
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
                   AVG(r.score) as avg_score
            FROM movie m 
            LEFT JOIN rating r ON m.movie_id = r.movie_id 
            WHERE m.movie_id = %s
            GROUP BY m.movie_id
        """, (movie_id,))
        movie = cursor.fetchone()

        if movie:
            # 查询电影类型
            cursor.execute("""
                SELECT g.genre_id, g.genre_name 
                FROM movie_genre mg 
                JOIN genre g ON mg.genre_id = g.genre_id 
                WHERE mg.movie_id = %s
            """, (movie_id,))
            genres = cursor.fetchall()
            movie['genres'] = [genre['genre_name'] for genre in genres]
            movie['genre_ids'] = [genre['genre_id'] for genre in genres]

            if movie.get('avg_score'):
                movie['avg_score'] = float(movie['avg_score'])

        return movie
    except Exception as e:
        print(f"获取电影错误: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def add_movie(title, release_year=None, language=None, duration=None, director=None, description=None, genre_ids=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 插入电影基本信息
        sql = """
        INSERT INTO movie (title, release_year, language, duration, director, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title, release_year, language, duration, director, description))
        movie_id = cursor.lastrowid

        # 插入电影类型关联
        if genre_ids:
            for genre_id in genre_ids:
                cursor.execute("INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)",
                               (movie_id, genre_id))

        conn.commit()
        return movie_id
    except Exception as e:
        print(f"添加电影错误: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def update_movie(movie_id, title=None, release_year=None, language=None, duration=None, director=None,
                 description=None, genre_ids=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 更新电影基本信息
        updates = []
        params = []
        if title is not None:
            updates.append("title=%s")
            params.append(title)
        if release_year is not None:
            updates.append("release_year=%s")
            params.append(release_year)
        if language is not None:
            updates.append("language=%s")
            params.append(language)
        if duration is not None:
            updates.append("duration=%s")
            params.append(duration)
        if director is not None:
            updates.append("director=%s")
            params.append(director)
        if description is not None:
            updates.append("description=%s")
            params.append(description)

        if updates:
            sql = "UPDATE movie SET " + ", ".join(updates) + " WHERE movie_id=%s;"
            params.append(movie_id)
            cursor.execute(sql, params)

        # 更新电影类型关联
        if genre_ids is not None:
            # 删除旧的类型关联
            cursor.execute("DELETE FROM movie_genre WHERE movie_id=%s", (movie_id,))
            # 插入新的类型关联
            for genre_id in genre_ids:
                cursor.execute("INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)",
                               (movie_id, genre_id))

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


def search_movies(search_term=None, year=None, genre_id=None, page=1, limit=10):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # 基础查询
        sql = """
        SELECT DISTINCT m.*, 
               AVG(r.score) as avg_score
        FROM movie m 
        LEFT JOIN rating r ON m.movie_id = r.movie_id 
        LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
        WHERE 1=1
        """
        params = []

        if search_term:
            sql += " AND (m.title LIKE %s OR m.director LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])

        if year:
            sql += " AND m.release_year = %s"
            params.append(int(year))

        if genre_id:
            sql += " AND mg.genre_id = %s"
            params.append(int(genre_id))

        sql += " GROUP BY m.movie_id ORDER BY m.movie_id DESC"

        # 获取总数
        count_sql = "SELECT COUNT(DISTINCT m.movie_id) as total FROM movie m LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id WHERE 1=1"
        count_params = []

        if search_term:
            count_sql += " AND (m.title LIKE %s OR m.director LIKE %s)"
            count_params.extend([f"%{search_term}%", f"%{search_term}%"])

        if year:
            count_sql += " AND m.release_year = %s"
            count_params.append(int(year))

        if genre_id:
            count_sql += " AND mg.genre_id = %s"
            count_params.append(int(genre_id))

        cursor.execute(count_sql, count_params)
        count_result = cursor.fetchone()
        total = count_result['total'] if count_result else 0

        # 添加分页
        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, (page - 1) * limit])

        cursor.execute(sql, params)
        movies = cursor.fetchall()

        # 为每个电影获取类型信息
        for movie in movies:
            cursor.execute("""
                SELECT g.genre_name 
                FROM movie_genre mg 
                JOIN genre g ON mg.genre_id = g.genre_id 
                WHERE mg.movie_id = %s
            """, (movie['movie_id'],))
            genres = cursor.fetchall()
            movie['genres'] = [genre['genre_name'] for genre in genres]

            if movie.get('avg_score'):
                movie['avg_score'] = float(movie['avg_score'])
            else:
                movie['avg_score'] = 0.0

        return movies, total
    except Exception as e:
        print(f"搜索电影错误: {e}")
        return [], 0
    finally:
        cursor.close()
        conn.close()