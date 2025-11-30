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

# 假设已有用户ID 1~50，电影ID 1~50
users_id = list(range(1, 51))
movies_id = list(range(1, 51))

# 假设电影时长（秒），可根据实际 movie 表替换
movie_durations = {i: random.randint(90, 180) * 60 for i in movies_id}

# 生成观看记录数据
history = []
num_history = 100  # 生成100条记录

for _ in range(num_history):
    user_id = random.choice(users_id)
    movie_id = random.choice(movies_id)
    max_duration = movie_durations[movie_id]
    duration_watched = random.randint(5*60, max_duration)  # 至少观看5分钟
    completed = duration_watched >= max_duration
    watch_time = datetime.now() - timedelta(days=random.randint(0, 365*3))  # 最近三年内
    history.append((user_id, movie_id, watch_time.strftime("%Y-%m-%d %H:%M:%S"), duration_watched, completed))

# 连接数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 插入数据
insert_sql = """
INSERT INTO history (user_id, movie_id, watch_time, duration_watched, completed)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.executemany(insert_sql, history)
conn.commit()

cursor.close()
conn.close()
print("✅ 用户观看记录数据已成功插入 MySQL 表 history！")
