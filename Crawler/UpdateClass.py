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

di_id_list = []
di_name_list = []
di_date_list = []
di_country_list = []
di_cases_list = []
di_class_list = []

sqlQuery = '''
SELECT name
FROM disease
GROUP BY name
ORDER BY count( * ) DESC
LIMIT 93
'''

cur.execute(sqlQuery)
results = cur.fetchall()
for row in results:
    di_name_list.append(row[0])
for di_name in di_name_list:
    di_date_list = []

    sqlQuery = "SELECT * FROM disease WHERE name = %s"

    try:
        cur.execute(sqlQuery, di_name)
        results = cur.fetchall()
        for row in results:
            di_date_list.append(row[2])
    except pymysql.Error as e:
        print("Failed: " + str(e))
    print(di_name)
    print(di_date_list)

    # count the danger level
    posts = len(di_date_list)
    days = (di_date_list[-1] - di_date_list[0]).days
    months = days / 30
    posts_per_month = posts / months
    print(posts_per_month)
    danger_level = ''
    if posts_per_month > 10:
        danger_level = 'Highest'
    elif posts_per_month > 6:
        danger_level = 'High'
    elif posts_per_month > 4:
        danger_level = 'Medium'
    elif posts_per_month > 2:
        danger_level = 'Low'
    else:
        danger_level = 'Lowest'

    # update the class
    sqlQuery = '''
    UPDATE disease set class = %s
    WHERE name = %s
    '''
    cur.execute(sqlQuery, [danger_level, di_name])
conn.commit()


cur.close()
conn.close()
