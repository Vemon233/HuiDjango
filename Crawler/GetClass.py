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
SELECT name, count( * ) AS count
FROM disease
WHERE class != 'no_use'
GROUP BY name
ORDER BY count DESC
LIMIT 100
'''

try:
    cur.execute(sqlQuery)
    results = cur.fetchall()
    i = 0
    for row in results:
        print(i)
        print((row[0], row[1]))
        i = i + 1
except pymysql.Error as e:
    print("Failed: "+str(e))

sqlQuery = '''
UPDATE disease set class = 'rare'
WHERE name in (
SELECT A.name FROM(
SELECT DISTINCT name, count( * ) AS count
FROM disease
WHERE class != 'no_use'
AND class != 'undiagnosed'
GROUP BY name
ORDER BY count DESC
LIMIT 10000
) as A
)
'''
cur.execute(sqlQuery)

sqlQuery = '''
UPDATE disease set class = 'less'
WHERE name in (
SELECT A.name FROM(
SELECT DISTINCT name, count( * ) AS count
FROM disease
WHERE class != 'no_use'
AND class != 'undiagnosed'
GROUP BY name
ORDER BY count DESC
LIMIT 92
) as A
)
'''
cur.execute(sqlQuery)

sqlQuery = '''
UPDATE disease set class = 'common'
WHERE name in (
SELECT A.name FROM(
SELECT DISTINCT name, count( * ) AS count
FROM disease
WHERE class != 'no_use'
AND class != 'undiagnosed'
GROUP BY name
ORDER BY count DESC
LIMIT 40
) as A
)
'''
cur.execute(sqlQuery)

sqlQuery = '''
UPDATE disease set class = 'frequent'
WHERE name in (
SELECT A.name FROM(
SELECT DISTINCT name, count( * ) AS count
FROM disease
WHERE class != 'no_use'
AND class != 'undiagnosed'
GROUP BY name
ORDER BY count DESC
LIMIT 15
) as A
)
'''
cur.execute(sqlQuery)

conn.commit()

cur.close()
conn.close()
