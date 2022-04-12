import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'https://www.qiushibaike.com/'
}

def parse_page(url):
    resp = requests.get(url,headers)
    text = resp.text

    # 作者姓名s
    authors = re.findall(r'<div class="author clearfix">.*?<h2>(.*?)</h2>',text,re.DOTALL)
    # print(authors)

    # 把处理好的作者信息放入zuozhes列表中
    zuozhes = []
    for author in authors:
        author = re.sub(r'<.*?>','',author)
        # print(author.strip())
        zuozhes.append(author.strip())


    # 正文内容s
    contents = re.findall(r'<div class="content">.*?<span>(.*?)</span>',text,re.DOTALL)
    # print(contents)

    # 把处理好的正文内容放入zhengwens列表当中
    zhengwens = []
    for content in contents:
        content = re.sub(r'<.*?>','',content)
        # print(content.strip())
        zhengwens.append(content.strip())

    # 把所有提取到的数据进行排序组合
    wenbens = []
    for value in zip(zuozhes,zhengwens):
        zuozhe,zhengwen = value
        wenben = {
            '作者':zuozhe,
            '内容':zhengwen
        }
        wenbens.append(wenben)

    for x in wenbens:
        print(x)
        print('-'*40)

if __name__ == '__main__':
    url = 'https://www.qiushibaike.com/text/page/1/'
    for x in range(1,11):
        url = 'https://www.qiushibaike.com/text/page/%s/' %x
        parse_page(url)