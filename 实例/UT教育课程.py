import requests
from lxml import etree
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://www.utjiaoyu.com/forum.php?mod=forumdisplay&fid=49',
    'Cookie': 'Hm_lvt_61becb4ae594001c2891a8fed5b10e84=1532230811,1533196322,1533469842,1533600795; ecHA_2132_saltkey=CGnO0EZ7; ecHA_2132_lastvisit=1533597817; ecHA_2132_client_created=1533601474; ecHA_2132_client_token=045A4B11B2F47841B1E331D85EED0D5B; ecHA_2132_connect_login=1; ecHA_2132_connect_is_bind=1; ecHA_2132_connect_uin=045A4B11B2F47841B1E331D85EED0D5B; ecHA_2132_visitedfid=49; ecHA_2132_sendmail=1; ecHA_2132_sid=THN8JI; ecHA_2132_ulastactivity=c3adNYofg2dRARe5dna1o%2Bep2VSDuwvom6Oog%2Fo5SPNycjICCMgN; ecHA_2132_auth=253bqIubxj0rT12MI81JGBeBuryy70mqq5cObQ%2BP4eYpXzNsujRY2uZZNTKYZPD%2FE8AmcaztC%2FcYthHLq5qkaHqdgg; ecHA_2132_creditbase=0D0D20D0D88D0D0D0D0; ecHA_2132_lastcheckfeed=28712%7C1533883684; ecHA_2132_checkfollow=1; user_name=lzban8; uid=28712; formhash1=1255307b; ecHA_2132_security_cookiereport=f37eZVj%2BngVVCg5W4lm6nD5FDgUEKqtpEMpPAjOaj7Yz6lJ15pM7; ecHA_2132_checkpm=1; ecHA_2132_nofavfid=1; ecHA_2132_lastact=1533883691%09forum.php%09forumdisplay; ecHA_2132_st_t=28712%7C1533883691%7C33a5b05f0ac7d8b006f73e645f04c209; ecHA_2132_forum_lastvisit=D_49_1533883691'
}

# 解析单个页面中所有的链接标签
def get_pages(page_a_url,page_num):
    resp = requests.get(page_a_url, headers=HEADERS)
    text = resp.text
    html = etree.HTML(text)

    # 加入判断，如果是第一页，则去掉首页的广告位，tbody从第6条开始读取，否则从第2条开始
    if page_num == 1:
        tbody = html.xpath("//table//tbody")[6:]
        # print(tbody)
    else:
        tbody = html.xpath("//table//tbody")[1:]
        # print(tbody)

    for page_url in tbody:
        a_href = page_url.xpath(".//a[@class='s xst']/@href")[0]
        # print(a_href)
        # 调用获取详情页方法
        get_infos(a_href)
3
# 解析详情页
def get_infos(a_href):
    resp = requests.get(a_href, headers=HEADERS)
    text = resp.text
    html = etree.HTML(text)

    # 1.获取标题
    title = html.xpath("//h1/span[@id='thread_subject']/text()")[0]
    print(title)

    # 2.获取链接
    dowload_url = html.xpath("//div[@class='t_fsz']//td//a/@href")[0]
    # dowload_url = html.xpath("//a[@class='gj_safe_a']/@href")[0]
    print('链接：'+dowload_url)

    # 3.获取密码
    # xpath语法
    # password = html.xpath("//div[@class='t_fsz']//td/text()")[3]

    # 正则表达式
    password = re.findall(r'<td class="t_f" .*?>.*?</a>提取码：(.*?)<br />',text,re.DOTALL)[0]
    print('密码：'+password)
    print('='*50)

    # # 定义常用正则表达式
    # r = re.compile(r'<td class="t_f" .*?>.*?密码：(.*?)<br />')
    # # 直接调用r
    # ret = re.findall(r,text)
    # print(ret)
    # print('------------------------------------')

    # 把数据写入txt文件
    fo = open('UT教育内部教程.txt','ab+')
    fo.write((title+'\r\n').encode('UTF-8'))
    fo.write(('链接：'+dowload_url+'\n').encode('UTF-8'))
    fo.write(('密码：'+password+'\n').encode('UTF-8'))
    fo.write(('===================================================='+'\n').encode('utf-8'))

if __name__ == '__main__':
    num = input('请输入想要提取的总页数，如果需要提取前3页，请输入3，并敲击Enter键：')
    # 把用户输入的数据转化为int数字类型
    num = int(num)

    for x in range(1,num+1):
        page_a_url = 'http://www.utjiaoyu.com/forum.php?mod=forumdisplay&fid=49&page=%s' %x
        page_num = int(x)
        print('='*50+'这是第'+str(x)+'页数据'+'='*50)
        get_pages(page_a_url,page_num)