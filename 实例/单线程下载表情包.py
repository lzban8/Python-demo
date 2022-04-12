import re
import requests
import os
from urllib import request
from lxml import etree

# 分析页面并下载
def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    resp = requests.get(url,headers=headers)
    text = resp.text
    html = etree.HTML(text)

    # 获取页面所有图片元素
    # imgs = html.xpath("//div[@class ='page-content text-center']//img[@class!='gif']/@data-original")
    imgs = html.xpath("//div[@class ='page-content text-center']//img[@class!='gif']")
    for img in imgs:
        # 用get()方法获取img元素的某个标签值
        img_url = img.get('data-original')
        # 获取图片名字
        img_alt = img.get('alt')
        # 使用正则表达式替换特殊字符为空
        img_alt = re.sub(r'[\?？,，\.。!！\* ]','',img_alt)
        # 用os.path.splitext()分割后缀名
        suffix = os.path.splitext(img_url)[1]
        file_name = img_alt + suffix
        # 判断文件夹是否存在，如果不存在则创建
        if os.path.exists('表情包文件夹'):
            # 下载图片
            request.urlretrieve(img_url, '表情包文件夹/' + file_name)
            print('正在下载：'+file_name)
        else:
            os.makedirs('表情包文件夹')

# 主函数
def main():
    # 爬取100页
    for x in range(1,101):
        url = 'http://www.doutula.com/photo/list/?page=%d' %x
        parse_page(url)

if __name__ == '__main__':
    main()