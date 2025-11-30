import pymysql

try:
    # 连接数据库
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="movie_system",
        charset="utf8mb4"
    )

    # 创建游标对象
    cursor = conn.cursor()

    # 测试查询：查看数据库中的表
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("数据库连接成功！")
    print("当前数据库中的表：", [table[0] for table in tables])

except pymysql.MySQLError as e:
    print("数据库连接失败！错误信息：", e)

finally:
    # 关闭游标和连接
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
