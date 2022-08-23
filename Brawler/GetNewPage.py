import os
import re
import time

import pymysql
from lxml import etree
from selenium import webdriver
from langdetect import detect, LangDetectException

conn = pymysql.connect(
    host='localhost',
    port=3306,
    charset='UTF8',
    user='root',
    password='521365zhh',
    db='diseasedb',
)
cur = conn.cursor()

def cleanstr(text, str):
    pos_end = text.find(str, 1)
    if pos_end > 0:
        text = text[0:pos_end]
    return text

def clean_suffix(text, suffix):
    pos = text.find(suffix)
    if pos > -1:
        text = text[0:pos]
    return text

# initialize the webdriver
driver = webdriver.Chrome()
# read the start number of archive from file
with open('arch_num.txt', 'r') as num_file:
    arch_num = int(num_file.read())
# make a file folder for promedmail texts
if not os.path.exists('./textFolder'):
    os.mkdir('./textFolder')


while True:
    url = 'https://promedmail.org/promed-post/?id=20220704.' + str(arch_num)
    driver.get(url=url)
    # wait for the data loading
    time.sleep(5)
    pageSource = driver.page_source
    promed_text = ''
    tree = etree.HTML(pageSource)
    r = tree.xpath('//div[@class="text1"]//text()')
    # if there is nothing in r, means the archive doesn't exist, break the loop
    if len(r) == 1:
        print(str(arch_num) + " Over")
        break
    for each in r:
        promed_text = promed_text + each + '\n'

    r = tree.xpath('//p[@class="publish_date_html"]//text()')
    di_date = cleanstr(r[1], ' ')
    di_date = di_date.strip()

    promed_text += di_date

    # if the page language is english, save it
    try:
        if detect(promed_text) == 'en':
            text_path = 'textFolder/' + str(arch_num) + '.txt'
            fp = open(text_path, 'w', encoding='utf-8')
            print(str(arch_num) + " Print Successfully")
            fp.write(promed_text)
    except LangDetectException:
        print(str(arch_num) + " Print Error")
        arch_num = arch_num - 1
    arch_num = arch_num + 1
    break

driver.quit()

# write the end archive number into the file
num_fp = open('arch_num.txt', 'w', encoding='utf-8')
num_fp.write(str(arch_num))



file_dir = "./textFolder"
files = os.listdir(file_dir)

for file in files:
    di_list = []
    fo = open(file_dir + "/" + file, 'r', encoding='utf-8')

    # step 1 Get the file id
    di_id = clean_suffix(str(fo), '.txt')
    myre = r"[^0-9]"
    pattern1 = re.compile(myre)
    di_id = re.sub(myre, '', di_id)
    di_list.append(di_id)

    iter_f = iter(fo)
    file_str = []
    for line in iter_f:
        file_str.append(line)
    print(file_str)

    # step 2 Get the disease name
    di_name = file_str[0]
    if di_name.find('Hand, foot & mouth disease') > -1:
        di_name = 'Hand foot & mouth disease'
    # a lot of remove the suffix here
    pos_end = di_name.find(' -')
    if pos_end < 0:
        pos_end = di_name.find(' (')
    di_name = di_name[0:pos_end]
    di_name = clean_suffix(di_name, 'UPDATE')
    di_name = clean_suffix(di_name, ' 20')
    di_name = clean_suffix(di_name, ' :')
    di_name = clean_suffix(di_name, ':')
    di_name = clean_suffix(di_name, ' (')
    di_name = clean_suffix(di_name, '(')
    di_name = clean_suffix(di_name, '- ')
    di_name = clean_suffix(di_name, ',')
    if di_name.endswith(' '):
        di_name = di_name.strip()

    if len(di_name) > 40:
        di_name = di_name[0:40]
    di_list.append(di_name)

    # step 3 Get the class of disease
    di_class = ''
    if di_name.find('INTERNATIONAL JOURNAL') > -1:
        di_class = 'no_use'
    if di_name.find('RESEARCH') > -1:
        di_class = 'no_use'
    if di_name.find('ANNOUNCEMENTS') > -1:
        di_class = 'no_use'
    if di_name.find('ANTIMICROBIAL') > -1:
        di_class = 'no_use'
    if di_name.find('SURVEILLANCE') > -1:
        di_class = 'no_use'
    if di_name.find('WHO') > -1:
        di_class = 'no_use'
    if di_name.find('UNDIAGNOSED') > -1:
        di_class = 'undiagnosed'
    di_list.append(di_class)
    di_country = ''

    # step 4 Get the country of the disease
    magic_number = 0
    for line in file_str:
        pos_country = line.find('ProMED map of ')

        if magic_number == 1:
            if not di_country:
                di_country = line.strip()
            di_country = clean_suffix(di_country, ':')
            while di_country.find(', ') > -1:
                pos_comma = di_country.find(', ')
                pos_comma = pos_comma + 2
                di_country = di_country[pos_comma:]
            break

        if pos_country >= 0:
            pos_country = pos_country + 14
            di_country = line[pos_country:]
            di_country = di_country.strip()
            magic_number = 1
        else:
            pos_country = line.find('ProMED map:')
            if pos_country >= 0:
                pos_country = pos_country + 11
                di_country = line[pos_country:]
                di_country = di_country.strip()
                magic_number = 1

    if not di_country:
        di_country = file_str[0]
        pos_country = di_country.find(' - ')

        if pos_country >= 0:
            pos_country = pos_country + 3
            di_country = di_country[pos_country:]
        else:
            di_country = ''

        di_country = di_country.strip()
        di_country = clean_suffix(di_country, ' (')
        di_country = clean_suffix(di_country, ':')
        di_country = clean_suffix(di_country, ',')
    if len(di_country) > 20:
        di_country = ''
    di_list.append(di_country)

    di_date = file_str[-1]
    print(di_list)
    # Save into the database


    sqlQuery = " INSERT INTO disease (id, name, class, country) VALUE (%s,%s,%s,%s) "
    try:
        cur.execute(sqlQuery, di_list)
        conn.commit()
        print(di_id + 'Data insert successfully')
    except pymysql.Error as e:
        print(di_id + "Data insert failed："+e)
        conn.rollback()
    sqlQuery = " UPDATE disease set date = str_to_date(%s,'%%Y-%%m-%%d') where id = %s "
    value = (di_date, di_id)
    try:
        cur.execute(sqlQuery, value)
        conn.commit()
        print(di_id + 'Date update successfully')
    except pymysql.Error as e:
        print(di_id + "Date update failed："+e)
        conn.rollback()

conn.commit()
print("success")


di_name_list = []
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