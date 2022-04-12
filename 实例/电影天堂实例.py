import requests
from lxml import etree

# 全局变量（请求头）
HEARERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    'Referer': "http://dytt8.net/"
}

# 全局变量（基本域名头）
BASE_DOMAIN = 'http://dytt8.net/'

# 获取单个分页中所有电影的url函数
def get_detail_urls(url):
    # 发送get请求
    resp = requests.get(url, headers=HEARERS)
    # print(resp.content.decode('gbk'))

    # 4.提取resp的text数据。这个函数我们只需要得到a标签中的href值，都是英文或者数字，所以直接使用text就好，不要使用gbk来解码，反而会报错。
    text = resp.text #.encode('gbk').decode('gbk')
    # print(text)
    html = etree.HTML(text)

    # 获取内容中a标签的href链接
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")

    # map函数，全部自动加上定义的【基本域名头】，然后返回url列表
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

# 解析详情页面函数
def parse_detail_page(url):

    #创建一个字典用来存放数据
    movie = {}

    resp = requests.get(url, headers=HEARERS)
    text = resp.content.decode('gbk')
    html = etree.HTML(text)

    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    movie['title'] = title

    # 定义一个zoom标签来方便获取详情中的格式
    zoom = html.xpath("//div[@id='Zoom']")[0]

    # 获取所有图片
    img1 = zoom.xpath(".//img/@src")[0]
    # img2 = zoom.xpath(".//img/@src")[1]

    # 也可以这样
    # imgs = zoom.xpath(".//img/@src")
    # img1 = imgs[0]
    # img2 = imgs[1]
    movie['img1'] = img1
    # movie['img2'] = img2

    # 定义一个函数，来方便我们进行数据的格式化操作
    def parse_info(info,rule):
         # 使用.replace方法替换数据为空白字符串，并清除格式中的空格
        return info.replace(rule,"").strip()

    infos = zoom.xpath(".//text()")

    # 通过使用enumerate来遍历 infos，我们可以得到index下标和info两个数据
    for index,info in enumerate(infos):
        # print(info)
        # print(index)
        # print("-------------------------------------------")

        # 使用.startswith方法判断 如果是以（◎X　　X）开始的，我们就调用上面定义的parse_info()函数来格式化数据
        if info.startswith("◎年　　代"):
            info = parse_info(info,"◎年　　代")
            movie['year'] = info

        elif info.startswith("◎产　　地"):
            info = parse_info(info,"◎产　　地")
            movie['country'] = info

        elif info.startswith("◎类　　别"):
            info = parse_info(info,"◎类　　别")
            movie['category'] = info

        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info,"◎豆瓣评分")
            movie['douban_rating'] = info

        elif info.startswith("◎片　　长"):
            info = parse_info(info,"◎片　　长")
            movie['duration'] = info

        elif info.startswith("◎导　　演"):
            info = parse_info(info,"◎导　　演")
            movie['director'] = info

        elif info.startswith("◎主　　演"):
            # 定义一个主演的列表，来循环存储数据
            actors = []

            # index下标
            info = parse_info(info,"◎主　　演")

            # 先把第一位演员的数据存储进actors
            actors = [info]

            # 使用下标的方式来遍历演员，range()从当前这个下标开始遍历，直到infos长度的值，结束
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()

                # 使用.startswith方法判断 如果出现了◎，我们就结束循环
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie['actors'] = actors

        elif info.startswith("◎简　　介"):
            info = parse_info(info, "◎简　　介")
            for x in range(index+1,len(infos)):
                profile = infos[x].strip()
                if profile.startswith("◎获奖情况"):
                    break
                movie['profile'] = profile

    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie['download_url'] = download_url

    # 信息全部提取完毕，返回字典
    return movie

# spider函数
def spider():
    # {}符号用来占坑
    base_url = 'http://dytt8.net/html/gndy/dyzz/list_23_{}.html'

    # 定义一个电影列表，来存储movie数据
    movies = []

    # 第一个for循环，是用来控制总页数（这里循环10次）
    for x in range(1,11):
        # print('----------------------------------------------------')
        # print(x)
        # print('----------------------------------------------------')
        url = base_url.format(x)

        # 调用get_detail_urls函数来获取单页中所有的电影url列表
        detail_urls = get_detail_urls(url)

        # 第二个for循环，是用来遍历detail_urls函数中的所有电影详情的url
        for detail_url in detail_urls:
            # print(detail_url)

            # 调用parse_detail_page解析详情页面函数
            movie = parse_detail_page(detail_url)

            # 然后将movie添加到movies列表中
            movies.append(movie)

            print(movie)

# main启动
if __name__ == '__main__':
    spider()
