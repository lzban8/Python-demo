import requests
from lxml import etree
import os

# 获取桌面路径
import winreg
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 获取单页所有详情页的链接
def get_url(page):
    resp = requests.get(page, headers=headers)
    text = resp.content.decode('gbk')
    # print(text)
    html = etree.HTML(text)
    urls = html.xpath("//ul[@class='wp-list clearfix']/li//h3//a/@href")
    # print(urls)
    for url in urls:
        # 调用获取详情页信息函数
        get_infos(url)
        # break

# 获取详情页信息
def get_infos(url):
    resp = requests.get(url, headers=headers)
    text = resp.content.decode('gbk')
    html = etree.HTML(text)

    foler_name = html.xpath("//div[@class='metaRight']//a//text()")[0]
    # img_url = html.xpath("//div[@id='picture']//p//img//@src")
    # img_names = html.xpath("//div[@id='picture']//p//img//@alt")

    imgs = html.xpath("//div[@id='picture']//p//img")
    for img in imgs:

        i_url = img.xpath(".//@src")[0]
        i_name = img.xpath(".//@alt")[0]

        # print(i_name)
        # print(i_url)
        # print('------------------------------------------------')

        # 调用获取图片函数
        get_img(i_url, i_name, foler_name)

# 获取图片信息
def get_img(url, name, foler_name):
    img_file = requests.get(url, headers=headers)

    # 检测是否存在image文件夹，没有则创建
    if not os.path.exists('image' + '/' + str(foler_name)):
        os.makedirs('image' + '/' + str(foler_name))

    # 拼接图片名
    filename = 'image' + '/' + str(foler_name) + '/' + str(name) + '.jpg'

    fp = open(filename, 'wb')  # 打开文件
    print(filename)
    fp.write(img_file.content)  # 写入文件
    fp.close()


# 运行
if __name__ == '__main__':
    # {}符号用来占坑
    pageX = 'http://www.meizitu.com/a/more_{}.html'
    pageX = 'https://movie.douban.com/celebrity/1275863/photos/?type=C&start={}&sortby=like&size=a&subtype=a'
    xuhao = [0,30,60,90,120,150,180,210,240]

    # 爬取1-9页数据
    for x in xuhao:
        page_url = pageX.format(x)
        # 调用函数获取所有详情页的链接
        get_url(page_url)
