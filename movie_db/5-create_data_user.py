import pymysql
import hashlib
import random
from datetime import datetime, timedelta
from faker import Faker

# 初始化 Faker
fake = Faker()

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "movie_system",
    "charset": "utf8mb4"
}

# 假设已有 genre 表，列出 genre_id
favorite_genres = [1,2,3,4,5,6,7,8,9,10,11,12,13]  # 根据你的 genre_id 调整

# 用户数据生成
users = []
for _ in range(50):
    username = fake.user_name()
    password_plain = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    password_hash = hashlib.sha256(password_plain.encode('utf-8')).hexdigest()
    nickname = fake.name()
    age = random.randint(18, 60)
    gender = random.choice(['M','F','O'])
    favorite_genre_id = random.choice(favorite_genres)
    register_date = datetime.now() - timedelta(days=random.randint(0, 365*3))
    users.append((username, password_hash, nickname, age, gender, favorite_genre_id, register_date))

# 连接数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 插入用户数据
for u in users:
    cursor.execute("""
        INSERT INTO user (username, password_hash, nickname, age, gender, favorite_genre_id, register_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, u)

conn.commit()
cursor.close()
conn.close()
print("✅ 用户表 50 条数据已插入成功！")
