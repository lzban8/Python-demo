import requests
from lxml import etree

# 1.豆瓣热门电影url
douban_url = 'https://movie.douban.com/cinema/nowplaying/wuhan/'

# 2.定义请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    'Referer': "https://movie.douban.com/"
}

# 3.发送get请求
resp = requests.get(douban_url,headers=headers)

# 4.提取resp的text数据
text = resp.text
html = etree.HTML(text)

# 获取第一个ul标签
ul = html.xpath("//ul[@class='lists']")[0]
#print(etree.tostring(ul,encoding='utf-8').decode('utf-8'))

# 获取ul中的所有的li标签
lis = ul.xpath("./li")

movies = []

for li in lis:
    # print(etree.tostring(li,encoding='utf-8').decode('utf-8'))
    title = li.xpath("@data-title")[0]
    score = li.xpath("@data-score")[0]
    duration = li.xpath("@data-duration")[0]
    region = li.xpath("@data-region")[0]
    director = li.xpath("@data-director")[0]
    actors = li.xpath("@data-actors")[0]
    image = li.xpath(".//img/@src")[0]

    print("-----------------------------------")
    print("片名："+title)
    print("评分："+score)
    print("时长："+duration)
    print("上映地区："+region)
    print("导演："+director)
    print("主演："+actors)
    print("电影海报："+image)

    # movie = {
    #     "片名：":title,
    #     "评分：":score,
    #     "时长：":duration,
    #     "上映地区：":region,
    #     "导演：":director,
    #     "主演：":actors,
    #     "电影海报：":image
    # }
    #
    # movies.append(movie)
    #
    # print(movies)