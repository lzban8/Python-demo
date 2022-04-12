import requests
from lxml import etree
import re

HEADERS = {
    'Cookie': 'bdshare_firstime=1534420009816; __utma=63332592.1002874931.1534420011.1534420011.1539859093.2; __utmz=63332592.1539859093.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ck_RegFromUrl=http%3A//kaijiang.500.com/shtml/ssq/18121.shtml%3F0_ala_baidu; ck_regchanel=baidu; regfrom=0%7Cala%7Cbaidu; sdc_session=1539860681490; seo_key=baidu%7C%7Chttps://www.baidu.com/link?url=OaHIDmaNurjhJzbeh5a3Gxt2jty3YP9nLA7rc7wdJt7aE4ccc_3mQNXbnWsbU2e7Ya_GeGVVWXstaccnCssgp07XY3wDa-8V86rYCWMPw0m&wd=&eqid=988877bf0002234c000000055bc868c3; __utmc=63332592; __utmt=1; ck_RegUrl=kaijiang.500.com; WT_FPC=id=undefined:lv=1539860812385:ss=1539859091735; sdc_userflag=1539859091737::1539860812391::15; __utmb=63332592.15.10.1539859093; CLICKSTRN_ID=59.172.19.12-1534420010.62780::DD38966C2327AA0589D395F185401304; motion_id=1539860860578_0.7816866507534366',
    'Host': 'kaijiang.500.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def parse_number(start_url):
    resp = requests.get(start_url,headers=HEADERS)
    text = resp.content.decode('gbk') #设置编码方式为gbk
    # print(text)
    html = etree.HTML(text)

    lottery_num_url_list = html.xpath("//span//div[@class='iSelectList listOverFlow']/a/@href")
    lottery_num_url_list = html.xpath("//a[@id='change_date']/@href")

    print(lottery_num_url_list)

    for li in lottery_num_url_list:
        print(li)

    return lottery_num_url_list #返回期号url的list

def parse_page(url):
    resp = requests.get(url,headers=HEADERS)
    text = resp.content.decode('gbk') #设置编码方式为gbk
    # print(text)
    html = etree.HTML(text)

    ball = [] #开奖号码
    ball_red = html.xpath("//li[@class='ball_red']/text()") #红球
    for x in ball_red:
        ball.append(x)

    ball_blue = html.xpath("//li[@class='ball_blue']/text()")[0] #蓝球
    ball.append(ball_blue)

    # print(ball)
    print('开奖号码：'+' '.join(ball))

    lottery_num = html.xpath("//font[@class='cfont2']//strong/text()")[0] #开奖期号
    print('开奖期号：'+lottery_num)

    ball_order = re.findall(r'出球顺序：</td>.*?<td>(.*?)</td>',text,re.DOTALL) #出球顺序
    # 去除文本中多余的字符、标签和空格
    for z in ball_order:
        zz = re.sub(r'<.*?>', '', z)
        ball_order = zz.strip() #去除空格

    print('出球顺序：'+ball_order)
    print('--------------------------')

if __name__ == '__main__':
    start_url = "http://kaijiang.500.com/shtml/ssq/03001.shtml"  #从03001期开始

    # 获取所有下拉框期号的url(list)
    lottery_num_url_list = parse_number(start_url)

    # for x in range(18001,500000):
    #     url = "http://kaijiang.500.com/shtml/ssq/%s.shtml" %x
    #     print(x)
    #     parse_page(url)