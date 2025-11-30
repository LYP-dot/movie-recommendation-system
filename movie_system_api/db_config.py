import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="movie_system",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 返回字典类型结果
    )
