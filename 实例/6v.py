import requests
from lxml import etree

# 6v 2018最新电影
liuv_url = 'http://www.hao6v.com/dy/'

# 定义请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    'Referer': "http://www.hao6v.com/gvod/zx.html"
}

# 发送get请求
resp = requests.get(liuv_url,headers=headers)
# print(resp.content.decode('gbk'))

# 4.提取resp的content数据
text = resp.content.decode('gbk')
html = etree.HTML(text)

# 获取第一个ul标签
ul = html.xpath("//ul")[0]
# print(etree.tostring(ul,encoding='utf-8').decode('utf-8'))

# 获取ul中的所有的li标签
lis = ul.xpath("./li")

for li in lis:
    # print(etree.tostring(li,encoding='utf-8').decode('utf-8'))
    name = li.xpath("./a//text()")[0]
    time = li.xpath("./span/text()")[0]
    href = li.xpath("./a/@href")[0]

    print('-------------------------------------------------------------------------------------------')
    print('片名：'+name)
    print("时间："+time)
    print("地址："+href)
