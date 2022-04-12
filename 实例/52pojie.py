from urllib import request

pojie_Url = 'https://www.52pojie.cn/forum-16-1.html'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

req = request.Request(pojie_Url,headers=headers)
resp = request.urlopen(req)
print(resp.read().decode('gbk'))
# request.urlretrieve(url,'52破解精品软件.html')