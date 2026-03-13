import pymysql

# 数据库连接
try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="movie_system",
        charset="utf8mb4"
    )
    cursor = conn.cursor()
    print("✅ 数据库连接成功！")
except pymysql.MySQLError as e:
    print("❌ 数据库连接失败！错误信息：", e)
    exit(1)

# 定义要创建的表及 SQL（带字段注释）
tables = {}

# 电影表
tables['movie'] = """
CREATE TABLE IF NOT EXISTS movie (
    movie_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '电影唯一标识',
    title VARCHAR(255) NOT NULL COMMENT '电影名称',
    release_year SMALLINT COMMENT '上映年份',
    language VARCHAR(50) COMMENT '语言',
    duration INT COMMENT '时长（分钟）',
    director VARCHAR(200) COMMENT '导演',
    description TEXT COMMENT '简介',
    avg_score DECIMAL(3,2) COMMENT '平均评分（可维护或实时计算）',
    rating_count INT COMMENT '评分人数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影基本信息表';
"""
# 电影类型表
tables['genre'] = """
CREATE TABLE IF NOT EXISTS genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '类型唯一标识',
    genre_name VARCHAR(50) NOT NULL UNIQUE COMMENT '类型名称（Action, Drama 等）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影类型表';
"""

# 电影-类型关联表（多对多）
tables['movie_genre'] = """
CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INT NOT NULL COMMENT '外键关联电影',
    genre_id INT NOT NULL COMMENT '外键关联类型',
    PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_genre FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影-类型关联表（多对多关系）';
"""

# 用户表
tables['user'] = """
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户唯一标识',
    username VARCHAR(100) NOT NULL UNIQUE COMMENT '登录名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    nickname VARCHAR(100) COMMENT '昵称',
    age TINYINT COMMENT '年龄',
    gender ENUM('M','F','O') COMMENT '性别',
    favorite_genre_id INT COMMENT '用户偏好类型',
    register_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    CONSTRAINT fk_favorite_genre FOREIGN KEY (favorite_genre_id)
        REFERENCES genre(genre_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';
"""

# 用户评分表
tables['rating'] = """
CREATE TABLE IF NOT EXISTS rating (
    rating_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评分记录唯一标识',
    user_id INT NOT NULL COMMENT '用户ID',
    movie_id INT NOT NULL COMMENT '电影ID',
    score TINYINT NOT NULL COMMENT '评分（1-5）',
    rating_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '评分时间',
    UNIQUE KEY unique_user_movie (user_id, movie_id),
    CONSTRAINT fk_rating_user FOREIGN KEY (user_id)
        REFERENCES user(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_rating_movie FOREIGN KEY (movie_id)
        REFERENCES movie(movie_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CHECK (score BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户评分表';
"""

# 用户观看记录表
tables['history'] = """
CREATE TABLE IF NOT EXISTS history (
    history_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '观看记录唯一标识',
    user_id INT NOT NULL COMMENT '用户ID',
    movie_id INT NOT NULL COMMENT '电影ID',
    watch_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '观看时间',
    duration_watched INT COMMENT '观看时长（秒）',
    completed BOOLEAN DEFAULT FALSE COMMENT '是否看完',
    CONSTRAINT fk_history_user FOREIGN KEY (user_id)
        REFERENCES user(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_history_movie FOREIGN KEY (movie_id)
        REFERENCES movie(movie_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户观看记录表';
"""

# 循环创建表
for table_name, create_sql in tables.items():
    try:
        cursor.execute(create_sql)
        print(f"✅ 数据表 '{table_name}' 创建成功！")
    except pymysql.MySQLError as e:
        print(f"❌ 数据表 '{table_name}' 创建失败，错误信息：", e)

# 提交事务并关闭连接
conn.commit()
cursor.close()
conn.close()
print("数据库操作完成，连接已关闭。")


