import requests
from lxml import etree
import csv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://www.hao6v.com/',
    'Host': 'www.hao6v.com'
}

# 分析页面
def parse_page(url):
    resp = requests.get(url,HEADERS)
    text = resp.content.decode('gbk')
    # print(text)
    html = etree.HTML(text)
    lis = html.xpath("//ul[@class='list']/li")

    for li in lis:
        a_name = li.xpath(".//a//text()")[0]
        a_time = li.xpath(".//span//text()")[0]
        a_url = li.xpath(".//a//@href")[0]
        print('------------------------------------------------------------------')
        print('片名:'+a_name)
        print('时间：'+a_time)
        print('地址：'+a_url)

        names = ['片名','时间','地址']
        values = [(a_name,a_time,a_url)]
        with open('6v最新电影.csv','w',encoding='utf-8',newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(names)
            writer.writerows(values)

if __name__ == '__main__':
    for x in range(100):
        url = 'http://www.hao6v.com/dy/index_%s.html' %x

        if x == 1:
            parse_page('http://www.hao6v.com/dy/index.html')
            break
        else:
            parse_page(url)