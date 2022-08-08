import os
import re
import pymysql

def normalize(mystring):
    string_list = mystring.split()
    mystring = ""
    for mystr in string_list:
        mystring += mystr.capitalize() + ' '
    mystring = mystring.strip()
    return mystring

conn = pymysql.connect(
    host='localhost',
    port=3306,
    charset='UTF8',
    user='root',
    password='521365zhh',
    db='diseasedb'
)
cur = conn.cursor()

def clean_suffix(text, suffix):
    pos = text.find(suffix)
    if pos > -1:
        text = text[0:pos]
    return text


file_dir = "../textFolder"
files = os.listdir(file_dir)

for file in files:
    fo = open(file_dir + "/" + file, 'r', encoding='utf-8')

    di_id = clean_suffix(str(fo), '.txt')
    myre = r"[^0-9]"
    pattern1 = re.compile(myre)
    di_id = re.sub(myre, '', di_id)

    iter_f = iter(fo)
    file_str = []
    for line in iter_f:
        file_str.append(line)

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
    di_country = normalize(di_country)
    if di_country == "Dr Congo":
        di_country = "Dem. Rep. Congo"
    if di_country == "Congo Dr":
        di_country = "Dem. Rep. Congo"
    if di_country == "Republic Of Congo":
        di_country = "Congo"
    if di_country == "Usa":
        di_country = "United States"
    if di_country == "Uk":
        di_country = "United Kingdom"
    if di_country == "Hong Kong":
        di_country = "China"
    if di_country == "Taiwan":
        di_country = "China"
    if di_country == "Guinea-bissau":
        di_country = "Guinea-Bissau"
    print(di_country)

    sqlQuery = " UPDATE disease set country = %s where id = %s "
    value = (di_country, di_id)

    try:
        cur.execute(sqlQuery, value)
        conn.commit()
        print(di_id + '数据插入成功！')
    except pymysql.Error as e:
        print(di_id + "数据插入失败：" + e)
        conn.rollback()

