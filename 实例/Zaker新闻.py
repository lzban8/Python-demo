from urllib import request

Zaker_url = 'http://www.myzaker.com/channel/13'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

req = request.Request(Zaker_url,headers=headers)
rest = request.urlopen(req)
print(rest.read().decode('utf-8'))
# request.urlretrieve(url,'科技频道.html')
