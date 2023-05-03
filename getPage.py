# encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import os
import requests


# html/body/div[1]/table/tbody/tr[2]/td[1]/input
# http://dmfy.emindsoft.com.cn/common/toDoubleexamp.do
def get_as_web(url):
    driverfile_path = r'D:\python\msedgedriver.exe'
    one_driver = webdriver.Edge(executable_path=driverfile_path)
    one_driver.get(url)
    # print(one_driver.title)
    one_driver.implicitly_wait(30)
    asinfo = one_driver.find_element(By.CLASS_NAME, 'asinfotext')
    # if asinfo == None:
    #     print(1)
    #     return ''
    asinfotxt = asinfo.text  # select_element_by_class_name('asinfotext')
    pattern = re.compile(r'Company Website:\n(.*?)\n')
    res = pattern.match(asinfotxt)
    if res is not None:
        # print(res.group().split('\n')[1])
        return res.group().split('\n')[1]
    return 'null'


if __name__ == '__main__':

    driverfile_path = r'D:\python\msedgedriver.exe'
    browser = webdriver.Edge(executable_path=driverfile_path)

    # 要爬取的网页
    contents = []  # 网页内容
    response = []  # 网页数据
    hitUrls = []
    urls = []
    titles = []
    writefile = open("docs.txt", 'w', encoding='UTF-8')
    url = 'https://www.hit.edu.cn/'
    # 第一页
    browser.get(url)
    response.append(browser.page_source)
    # 休息时间
    time.sleep(3)

    hitBaseUrl = r"https://www.hit.edu.cn"
    reg = r'href="/\d+/list.htm"'
    for i in range(len(response)):
        hitUrls = re.findall(reg, response[i])
    print(hitUrls)

    # 打印出来放在一个列表里
    for i in range(len(hitUrls)):
        url1 = hitBaseUrl + hitUrls[i].replace('href="', "").replace('"', "")

        if url1 in urls:
            continue
        browser.get(url1)
        time.sleep(1)
        try:
            content = browser.find_element(By.ID, 'wp_content_w13_0').text
            time.sleep(1)
        except:
            continue
        else:
            contents.append(content)
            b = browser.page_source
            urls.append(url1)
            title = browser.title
            titles.append(title)

    print(titles)
    print(urls)
    for j in range(len(titles)):
        writefile.write(str(j) + '\t\t' + titles[j] + '\t\t' + str(urls[j]) + '\n')
        with open(str(j),'w',encoding='utf-8') as f:
            f.write(contents[j])

    time.sleep(1)
    browser.close()
