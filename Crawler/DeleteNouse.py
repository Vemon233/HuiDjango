import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    charset='UTF8',
    user='root',
    password='521365zhh',
    db='diseasedb'
)
cur = conn.cursor()

sqlQuery = "DELETE FROM disease where class=%s"

value = ('no_use')

try:
    cur.execute(sqlQuery, value)
    conn.commit()
    print('Date Deleted Successfully')
except pymysql.Error as e:
    print("数据删除失败：" + str(e))
    # 发生错误时回滚
    conn.rollback()

conn.commit()

cur.close()
conn.close()
