# # 导入模块
# from wxpy import *
#
# # 初始化机器人，扫码登陆
# bot = Bot(cache_path=True)
# # 调用图灵精灵API
# tulingRobot = Tuling(api_key='b3dc2c0e497a4a20a6dac79e58fd171e')
#
# # 给机器人自己发送消息
# bot.self.send('hello,word')
#
# # 给文件传输助手发送消息
# bot.file_helper.send('hello,word')
#
#
import itchat

itchat.auto_login()

itchat.send('Hello, filehelper', toUserName='filehelper')