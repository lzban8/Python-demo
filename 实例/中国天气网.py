import requests
from bs4 import BeautifulSoup

# 定义一个全局变量来存放数据
ALL_DATA = []

# 目标：爬取中国天气网今日全国所有城市的最高气温

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://www.weather.com.cn/textFC/hd.shtml'
}


BASE_DOMAIN = "http://www.weather.com.cn/textFC/"

# 1.获取华北（单页）所有城市最低气温
def parse_page(url):
    resp = requests.get(url,headers=HEADERS)
    text = resp.content.decode('utf-8')
    # html = etree.HTML(text)

    # 这里解析器选择容错性更好的html5lib，而不是lxml
    soup = BeautifulSoup(text,"html5lib")

    conMidtab = soup.find('div',class_='conMidtab')

    tables = conMidtab.find_all('table')
    for table in tables:
        # [2:]的意思是的作用是从2开始取后面的所有数据
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]

            # 加入下标来判断第一个城市,如果是第一个，那么就让tds=[1]
            if index == 0:
                city_td = tds[1]

            city = list(city_td.stripped_strings)[0]
            # [-2]的意思是取倒数第二个td标签：
            temp_td = tds[-2]
            mintemp = list(temp_td.stripped_strings)[0]

            # 把数据存入全局变量!
            ALL_DATA.append("城市："+city+"---"+"最低气温"+mintemp)
            print("城市："+city+"---"+"最低气温"+mintemp)

            ALL_DATA.append({"城市":city,"最低气温":int(mintemp)})
            print({"城市":city,"最低气温":int(mintemp)})

            print('-----------------------两种输出方式，{  }为字典的形式--------------------------')

def main():
    # url1 = 'http://www.weather.com.cn/textFC/hb.shtml'
    # url2 = 'http://www.weather.com.cn/textFC/db.shtml'
    # url3 = 'http://www.weather.com.cn/textFC/hz.shtml'
    # url4 = 'http://www.weather.com.cn/textFC/hn.shtml'
    # url5 = 'http://www.weather.com.cn/textFC/xb.shtml'
    # url6 = 'http://www.weather.com.cn/textFC/xn.shtml'
    # url7 = 'http://www.weather.com.cn/textFC/gat.shtml'

    # 我们发现解析url7港澳台的时候因为网页代码不规范，table没有结束标签，所有在使用lxml解析器的时候会出现错误，所以我们在这里将之前的soup的解析器改为html5lib

    # 我们新建一个列表，来存放所有的url
    urls = {
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    }

    for url in urls:
        parse_page(url)

if __name__ == '__main__':
    main()
