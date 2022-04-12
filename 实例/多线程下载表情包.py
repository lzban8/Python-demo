import re
import requests
import os
from urllib import request
from lxml import etree
from queue import Queue
import threading

# 生产者
class shengchanzhe(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(shengchanzhe, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        resp = requests.get(url,headers=self.headers)
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
            self.img_queue.put((img_url,file_name))

# 消费者
class xiaofeizhe(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(xiaofeizhe, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,file_name = self.img_queue.get()

            # 判断文件夹是否存在，如果不存在则创建
            if os.path.exists('表情包文件夹'):
                # 下载图片
                request.urlretrieve(img_url, '表情包文件夹/' + file_name)
                print('正在下载：' + file_name)
            else:
                os.makedirs('表情包文件夹')

            # request.urlretrieve(img_url, '表情包文件夹/' + file_name)
            # print('正在下载：' + file_name)


# 主函数
def main():

    page_queue = Queue(100)
    img_queue = Queue(1000)

    # 爬取100页
    for x in range(1,101):
        url = 'http://www.doutula.com/photo/list/?page=%d' %x
        # 把每一页的url添加到队列当中
        page_queue.put(url)

    # 创建5个生产者
    for s in range(5):
        t = shengchanzhe(page_queue,img_queue)
        t.start()
    # 创建5个消费者
    for x in range(5):
        t = xiaofeizhe(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()