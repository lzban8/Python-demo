import requests
from lxml import etree

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'https://hr.tencent.com/social.php'
}

BASE_DOMAIN = "https://hr.tencent.com/"

# 获取单页所有的详情url函数
def get_datail_urls(url):

    # 检测获取的url分页路径是否正确
    # print(url)

    resp = requests.get(url, headers=HEADERS)
    text = resp.text
    html = etree.HTML(text)

    #获取html网页中，class值为l square的td标签下面的a标签的href链接
    tr_urls = html.xpath("//td[@class='l square']/a/@href")
    # 检测是否正确获取到a标签中的href值
    # print(tr_urls)

    # map函数，全部自动加上定义的【基本域名头】，然后返回url列表
    tr_urls = map(lambda url:BASE_DOMAIN+url,tr_urls)
    return tr_urls

# 获取详情页面函数
def get_infos(url):
    # 创建一个字典用来存放数据
    datas = {}

    resp = requests.get(url,headers = HEADERS)
    text = resp.text
    html = etree.HTML(text)

    # 定义一个table标签来方便获取详情中的格式
    table = html.xpath("//table[@class='tablelist textl']")[0]

    title = table.xpath(".//tr[@class='h']/td/text()")[0]
    datas['职位名称'] = title

    add = table.xpath(".//tr[@class='c bottomline']/td/text()")[0]
    datas['工作地点'] = add

    tp = table.xpath(".//tr[@class='c bottomline']/td/text()")[1]
    datas['职位类别'] = tp

    num = table.xpath(".//tr[@class='c bottomline']/td/text()")[2]
    datas['招聘人数'] = num

    zhize = table.xpath(".//ul[@class='squareli']/li/text()")
    datas['工作职责'] = zhize

    yaoqi = table.xpath(".//ul[@class='squareli']/li/text()")[1]
    datas['工作要求'] = yaoqi

    return datas

# 爬虫函数
def spider():

    base_url = "https://hr.tencent.com/position.php?lid=&tid=&keywords=python&start={}0#a"

    datas = []

    # 第一个for循环，是用来控制总页数（这里循环10次）
    for x in range(0,10):
        # print('----------------------------------------------------')
        # print(x)
        # print('----------------------------------------------------')
        url = base_url.format(x)

        # 调用函数来获取单页所有的详情url信息
        datail_urls = get_datail_urls(url)

        # 第二个for循环，是用来遍历detail_urls函数中的所有详情的url
        for datail_url in datail_urls:
            # 检测url路径是否带了域名头
            # print(datail_url)

            # 调用get_infos获取单页详情页函数
            data = get_infos(datail_url)

            datas.append(data)

            print(data)



if __name__ == '__main__':
    spider()