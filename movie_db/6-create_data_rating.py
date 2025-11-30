import pymysql
import random
from datetime import datetime, timedelta

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "movie_system",
    "charset": "utf8mb4"
}

# 生成评分数据
num_ratings = 100  # 生成 100 条评分记录
users_id = list(range(1, 51))   # 用户ID 1~50
movies_id = list(range(1, 51))  # 电影ID 1~50

ratings = set()  # 用 set 避免重复评分（每人每电影一条）
while len(ratings) < num_ratings:
    user_id = random.choice(users_id)
    movie_id = random.choice(movies_id)
    if (user_id, movie_id) not in ratings:
        ratings.add((user_id, movie_id))

# 转换为列表并生成时间和分数
ratings_data = []
for user_id, movie_id in ratings:
    score = random.randint(1, 5)
    rating_time = datetime.now() - timedelta(days=random.randint(0, 365*3))
    ratings_data.append((user_id, movie_id, score, rating_time))

# 连接数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 创建表
create_table_sql = """
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
cursor.execute(create_table_sql)
print("✅ 用户评分表已创建成功！")

# 插入数据
for r in ratings_data:
    cursor.execute("""
        INSERT INTO rating (user_id, movie_id, score, rating_time)
        VALUES (%s, %s, %s, %s)
    """, r)

conn.commit()
cursor.close()
conn.close()
print("✅ 用户评分数据已插入成功！")
