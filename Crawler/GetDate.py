import os
import re
import time
import pymysql
from lxml import etree
from selenium import webdriver

conn = pymysql.connect(
    host='localhost',
    port=3306,
    charset='UTF8',
    user='root',
    password='521365zhh',
    db='diseasedb'
)
cur = conn.cursor()


def cleanstr(text, str):
    pos_end = text.find(str, 1)
    if pos_end > 0:
        text = text[0:pos_end]
    return text


def getDate(url_id):
    url = 'https://promedmail.org/promed-post/?id=20220704.' + url_id
    driver.get(url=url)
    time.sleep(5)
    pageSource = driver.page_source
    tree = etree.HTML(pageSource)
    r = tree.xpath('//p[@class="publish_date_html"]//text()')
    if not r:
        print("Get nothing")
        return ''
    di_date = cleanstr(r[1], ' ')
    di_date = di_date.strip()
    return di_date


driver = webdriver.Chrome()
file_dir = "../textFolder"
files = os.listdir(file_dir)

for file in files:
    fo = open(file_dir + "/" + file, 'r', encoding='utf-8')

    di_id = cleanstr(str(fo), '.txt')
    myre = r"[^0-9]"
    pattern1 = re.compile(myre)
    di_id = re.sub(myre, '', di_id)

    di_date = ''
    while not di_date:
        di_date = getDate(di_id)
    print(di_date)

    sqlQuery = " UPDATE disease set date = str_to_date(%s,'%%Y-%%m-%%d') where id = %s "
    value = (di_date, di_id)

    try:
        cur.execute(sqlQuery, value)
        conn.commit()
        print(di_id + '数据插入成功！')
    except pymysql.Error as e:
        print(di_id + "数据插入失败：" + e)
        conn.rollback()

driver.quit()