#!/usr/bin/env python
# coding=utf-8

import datetime
import itchat
import time
from itchat.content import *

newInstance = itchat.new_instance()


def write_log(username, text):
    print("%s: %s\n" % (username, text))

chatrooms_dict = {}


def init_chatrooms(wx_chat):
    global chatrooms_dict
    chatrooms_list = wx_chat.get_chatrooms()
    for each in chatrooms_list:
        chatrooms_dict[each['UserName']] = each['NickName']


@newInstance.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def simply_reply(msg):
    try:
        if msg['FromUserName'] == newInstance.storageClass.userName:
            actual_nick_name = u'自己'
            chatroom_user_name = msg['ToUserName']
            chatroom_nick_name = chatrooms_dict[chatroom_user_name] if chatroom_user_name in chatrooms_dict else u"未知群聊"
        else:
            actual_nick_name = msg['ActualNickName'] if 'ActualNickName' in msg else u'未知用户'
            chatroom_user_name = msg['FromUserName']
            chatroom_nick_name = chatrooms_dict[chatroom_user_name] if chatroom_user_name in chatrooms_dict else u"未知群聊"

        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['CreateTime']))
        content = msg['Text']

        log = u'[%s] %s (%s): %s\n' % (chatroom_nick_name, actual_nick_name, create_time, content)
        logfile = 'msg_log/%s' % datetime.date.today().strftime("%Y-%m-%d.txt")
        with open(logfile, 'a') as file_fb:
            file_fb.write(log.encode("utf-8"))
        print log
    except Exception as e:
        print str(e)


newInstance.auto_login(hotReload=True)
init_chatrooms(newInstance)
# print chatrooms_dict
newInstance.run()
newInstance.dump_login_status()
