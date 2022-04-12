import random

red_list = [x for x in range(1,34)] #1~33红色球序列
resp = random.sample(red_list,6) #随机选取6个红球
resp.sort() #对选取的6个红球排序
resp.append(random.randint(1,16)) #随机选取1个蓝球

print(resp)