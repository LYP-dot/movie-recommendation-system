import pymysql

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "movie_system",
    "charset": "utf8mb4"
}

# 电影类型列表
genres = [
    "Action", "Adventure", "Animation", "Comedy", "Sci-Fi", "Fantasy",
    "Drama", "Thriller", "Horror", "Musical", "Romance", "Mystery", "Historical"
]

# 电影-类型对应关系
# 格式: (电影标题, [类型列表])
movie_genres = [
    ("Inside Out 2", ["Animation", "Adventure", "Drama"]),
    ("Deadpool & Wolverine", ["Action", "Adventure", "Comedy"]),
    ("Moana 2", ["Adventure", "Animation", "Fantasy"]),
    ("Despicable Me 4", ["Animation", "Comedy", "Family"]),
    ("Wicked", ["Musical", "Fantasy", "Drama"]),
    ("Dune: Part Two", ["Sci-Fi", "Adventure", "Drama"]),
    ("Godzilla x Kong: The New Empire", ["Action", "Sci-Fi", "Adventure"]),
    ("Kung Fu Panda 4", ["Animation", "Action", "Adventure"]),
    ("Sonic the Hedgehog 3", ["Action", "Adventure", "Comedy"]),
    ("The Super Mario Bros. Movie 2", ["Animation", "Adventure", "Comedy"]),
    ("Mufasa: The Lion King", ["Drama", "Adventure", "Musical"]),
    ("Venom: The Last Dance", ["Action", "Thriller", "Sci-Fi"]),
    ("Twisters", ["Action", "Thriller", "Drama"]),
    ("Kingdom of the Planet of the Apes", ["Action", "Sci-Fi", "Drama"]),
    ("Bad Boys: Ride or Die", ["Action", "Comedy"]),
    ("Alien: Romulus", ["Sci-Fi", "Horror", "Thriller"]),
    ("Twilight of the Gods", ["Sci-Fi", "Fantasy", "Drama"]),
    ("The Garfield Movie", ["Animation", "Comedy", "Family"]),
    ("The Wild Robot", ["Animation", "Adventure", "Sci-Fi"]),
    ("A Quiet Place: Day One", ["Horror", "Thriller", "Drama"]),
    ("It Ends With Us", ["Drama", "Romance"]),
    ("Snow White: Legacy", ["Fantasy", "Adventure", "Drama"]),
    ("Spider‑Man: Beyond the Spider‑Verse", ["Animation", "Action", "Adventure"]),
    ("Gladiator II", ["Action", "Historical", "Drama"]),
    ("Transformers: One", ["Action", "Adventure", "Sci-Fi"]),
    ("Mad Max: Wasteland", ["Action", "Adventure", "Thriller"]),
    ("Beetlejuice Beetlejuice", ["Comedy", "Horror", "Fantasy"]),
    ("Jurassic World: Extinction", ["Action", "Adventure", "Sci-Fi"]),
    ("Avatar: The Way of Water 2", ["Sci-Fi", "Adventure", "Fantasy"]),
    ("The Flash: Time Paradox", ["Action", "Adventure", "Sci-Fi"]),
    ("Deadpool 3", ["Action", "Comedy", "Adventure"]),
    ("Guardians of the Galaxy Vol. 4", ["Action", "Adventure", "Comedy"]),
    ("Star Wars: Legacy", ["Action", "Adventure", "Sci-Fi"]),
    ("Batman: Shadow of Gotham", ["Action", "Thriller", "Drama"]),
    ("Thor: Ragnarok Reborn", ["Action", "Adventure", "Fantasy"]),
    ("Black Panther: Rising", ["Action", "Adventure", "Drama"]),
    ("Mission Impossible: Dead Reckoning Part 3", ["Action", "Thriller"]),
    ("John Wick: Chapter 4", ["Action", "Thriller"]),
    ("Oppenheimer", ["Drama", "Historical"]),
    ("Barbie", ["Comedy", "Fantasy"]),
    ("Spider-Man: Across the Spider‑Verse", ["Animation", "Action", "Adventure"]),
    ("Guardians of the Galaxy Vol. 3", ["Action", "Adventure", "Comedy"]),
    ("Top Gun: Maverick", ["Action", "Drama"]),
    ("Everything Everywhere All at Once", ["Sci-Fi", "Comedy", "Drama"]),
    ("Knives Out 2", ["Mystery", "Thriller", "Drama"]),
    ("Dune", ["Sci-Fi", "Adventure", "Drama"]),
    ("Blade Runner 2049", ["Sci-Fi", "Drama", "Thriller"]),
    ("Interstellar", ["Sci-Fi", "Drama", "Adventure"]),
    ("The Dark Knight", ["Action", "Drama", "Thriller"]),
    ("Inception", ["Sci-Fi", "Action", "Thriller"]),
]

# 连接数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 1️⃣ 插入 genre 表
for name in genres:
    cursor.execute(
        "INSERT INTO genre (genre_name) VALUES (%s) ON DUPLICATE KEY UPDATE genre_name=genre_name",
        (name,)
    )
conn.commit()

# 获取 genre 映射 {name: genre_id}
cursor.execute("SELECT genre_id, genre_name FROM genre")
genre_map = {name: gid for gid, name in cursor.fetchall()}

# 2️⃣ 插入 movie_genre 表
for movie_title, g_list in movie_genres:
    # 查询 movie_id
    cursor.execute("SELECT movie_id FROM movie WHERE title=%s", (movie_title,))
    movie_res = cursor.fetchone()
    if movie_res:
        movie_id = movie_res[0]
        for gname in g_list:
            # 如果类型存在
            if gname in genre_map:
                genre_id = genre_map[gname]
                cursor.execute(
                    "INSERT IGNORE INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)",
                    (movie_id, genre_id)
                )

conn.commit()
cursor.close()
conn.close()
print("✅ genre 和 movie_genre 表数据插入完成！")
