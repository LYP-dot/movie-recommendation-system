from movie_system_api.db_config import get_connection

def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie;")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies

def get_movie_by_id(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie WHERE movie_id=%s;", (movie_id,))
    movie = cursor.fetchone()
    cursor.close()
    conn.close()
    return movie

def add_movie(title, release_year=None, language=None, duration=None, director=None, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO movie (title, release_year, language, duration, director, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (title, release_year, language, duration, director, description))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id

def update_movie(movie_id, title=None, release_year=None, language=None, duration=None, director=None, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if title: updates.append("title=%s"); params.append(title)
    if release_year: updates.append("release_year=%s"); params.append(release_year)
    if language: updates.append("language=%s"); params.append(language)
    if duration: updates.append("duration=%s"); params.append(duration)
    if director: updates.append("director=%s"); params.append(director)
    if description: updates.append("description=%s"); params.append(description)
    if not updates:
        cursor.close()
        conn.close()
        return 0
    sql = "UPDATE movie SET " + ", ".join(updates) + " WHERE movie_id=%s;"
    params.append(movie_id)
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected

def delete_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movie WHERE movie_id=%s;", (movie_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected
