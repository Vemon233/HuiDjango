import os
import re
import pymysql


def clean_suffix(text, suffix):
    pos = text.find(suffix)
    if pos > -1:
        text = text[0:pos]
    return text


conn = pymysql.connect(
    host='localhost',
    port=3306,
    charset='UTF8',
    user='root',
    password='521365zhh',
    db='diseasedb'
)
cur = conn.cursor()

file_dir = "../textFolder"
files = os.listdir(file_dir)

for file in files:
    fo = open(file_dir + "/" + file, 'r', encoding='utf-8')

    # Get the file id
    di_id = clean_suffix(str(fo), '.txt')
    myre = r"[^0-9]"
    pattern1 = re.compile(myre)
    di_id = re.sub(myre, '', di_id)

    # Get the cases
    di_cases = 1

    sqlQuery = " UPDATE disease set cases = %s where id = %s "
    value = (di_cases, di_id)

    try:
        cur.execute(sqlQuery, value)
        conn.commit()
        print(di_id + '数据插入成功！')
    except pymysql.Error as e:
        print(di_id + "数据插入失败：" + e)
        conn.rollback()


conn.commit()

cur.close()
conn.close()
