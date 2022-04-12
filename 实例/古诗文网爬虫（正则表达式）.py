import requests
import re

# https://www.gushiwen.org/default_1.aspx

def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    resp = requests.get(url,headers)
    text = resp.text

    # 利用正则表达式解析text
    # titles = ['aaa','bbb']
    # chaodai = ['清代','明代']
    # zuozhe = ['wang','felix']
    # zhengwen = ['aaaaaaaaaa','bbbbbbbbb']

    titles = re.findall(r'<div class="cont">.*?<b>(.*?)</b>',text,re.DOTALL)
    # .* 代表的是任意的字符
    # ? 代表的是采用非贪婪模式
    # 因为每个标签之间存在换行\n，所以 re.DOTALL 代表的是 . 匹配所有的字符
    # print(titles)

    chaodais = re.findall(r'<p class="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    # print(chaodais)

    zuozhes = re.findall(r'<p class="source">.*?<a.*?>.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    # print(zuozhes)

    zhengwens = re.findall(r'<div class="contson" .*?>(.*?)</div>',text,re.DOTALL)
    chunwenbens = []

    # 通过遍历来清除每个文本信息中多余的标签
    for z in zhengwens:
        # print(z)
        # 替换文本中的<br><p>...等等标签为空白字符
        zz = re.sub(r'<.*?>','',z)
        # print(zz)

        # .strip 可以去掉前后的换行
        # print(zz.strip())

        # 最后把所有处理好的纯文本信息存入chunwenbens列表当中
        chunwenbens.append(zz.strip())

    # 通过zip()函数，可以组合多个列表，生成在一起
    # a = ['1','2']
    # b = ['3','4']
    #
    # c = zip(a,b)
    # c = [
    #     (1,3),
    #     (2,4)
    # ]

    # 定义一个列表，来存储排序好的数据
    contents = []
    for value in zip(titles,chaodais,zuozhes,chunwenbens):
        title,chaodai,zuozhe,chunwenben = value
        content = {
            '标题':title,
            '朝代':chaodai,
            '作者':zuozhe,
            '文本':chunwenben
        }
        contents.append(content)

    for x in contents:
        print(x)
        print('='*40)




if __name__ == '__main__':
    url = 'https://www.gushiwen.org/default_1.aspx'

    # 获取前10页数据
    for x in range(1,11):
        url = 'https://www.gushiwen.org/default_%s.aspx' %x
        parse_page(url)
