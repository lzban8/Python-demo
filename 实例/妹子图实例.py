from bs4 import BeautifulSoup
import requests
import os

# 获取图片链接
def get_img_url(folders, img):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    req = requests.get(img, headers=headers).content  # 请求组图链接
    soup = BeautifulSoup(req, 'html5lib')  # beautsou解析
    soup = soup.find_all(name='div', attrs={'id': 'picture'})  # 查找关键字段
    for m in soup:  # 遍历出图片链接和图片名
        m = m.find_all('img')
        for i in m:
            name = i['alt']
            src = i['src']
            folder = folders
            download_img(src, name, folder)


# 下载图片
def download_img(img_url, img_name, foler):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }

    file = requests.get(img_url, headers=headers)  # 请求图片链接
    if not os.path.exists('imagge' + '/' + str(foler)):  # 检测是否有image目录没有则创建
        os.makedirs('imagge' + '/' + str(foler))
    filename = 'imagge' + '/' + str(foler) + '/' + str(img_name) + '.jpg'  # 拼接图片名
    fp = open(filename, 'wb')  # 打开文件
    print(filename)
    fp.write(file.content)  # 写入文件
    fp.close()


# 访问主页面获取组图链接
def get_url(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    url = 'http://www.meizitu.com/a/more_' + str(page) + '.html'
    reponse = requests.get(url, headers=headers).content
    soup = BeautifulSoup(reponse, 'html5lib')
    soup = soup.find_all(name='div', attrs={"class": "con"})
    for i in soup:
        m = i.find_all('h3')
        for n in m:
            name1 = n.a.string
            html1 = n.a['href']
            get_img_url(name1, html1)

if __name__ == '__main__':
    # 运行
    get_url(1)
