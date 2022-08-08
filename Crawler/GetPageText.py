import os
import time
from lxml import etree
from selenium import webdriver
from langdetect import detect, LangDetectException

# initialize the webdriver
driver = webdriver.Chrome()
# this is the start number of archive
arch_num = 8698665
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
    for each in r:
        promed_text = promed_text + each + '\n'
    # if the page language is english, save it
    try:
        if detect(promed_text) == 'en':
            text_path = 'textFolder/' + str(arch_num) + '.txt'
            fp = open(text_path, 'w', encoding='utf-8')
            print(str(arch_num) + " Print Successfully")
            fp.write(promed_text)
    except LangDetectException:
        print(str(arch_num) + " Print Error")
        arch_num = arch_num + 1
    arch_num = arch_num - 1
    break

driver.quit()
