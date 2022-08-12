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

sqlQuery = '''
UPDATE disease set name=REPLACE(name, " ", "_")
'''

cur.execute(sqlQuery)
conn.commit()

cur.close()
conn.close()
