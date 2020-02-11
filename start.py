#bilibili离岸烨 https://space.bilibili.com/8716036
import requests
import threading
import time
import os
import json
import socket
import win32com.client
#######################设置初始化接口
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Speak('服务开始！')
#朗读 需要安装pywin32 https://github.com/mhammond/pywin32/releases
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}#防屏蔽，先设置UA协议头
upstaturl='https://api.bilibili.com/x/space/upstat?mid=8716036'#up主信息获取接口
relstaturl='https://api.bilibili.com/x/relation/stat?vmid=8716036'#用户关系获取接口
videoliurl='http://space.bilibili.com/ajax/member/getSubmitVideos?mid=8716036&pagesize=100&page=1'#up主视频列表获取接口
videoinfourl='http://api.bilibili.com/archive_stat/stat?aid='#视频信息获取接口
#这个接口一次最多获取100条，但是估计大多数人有生之年也发不到100条。所以没写循环读取qvq
lastetcoin=0
lastetfollower=0
lastetlike=0
lastetview=0
coins=0
views=0
changed=False
def ytimer():
    print (time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()))
######################初始化区
    global lastetcoin
    global lastetfollower
    global lastetlike
    global lastetview
    global coins
    coins=0
    global views
    views=0
    global changed
    changed=False
######################upstat区
    res=requests.get(upstaturl,headers=headers)
    html=res.text
    upstat=json.loads(html)
    if lastetlike==0:
        lastetlike=upstat['data']['likes']
    #print ('like:'+str(upstat['data']['likes'])+','+'lastetlike:'+str(lastetlike))
    if upstat['data']['likes']!=lastetlike:
        changed=True
        if upstat['data']['likes']-lastetlike>0:
            print('赞数增加:'+str(upstat['data']['likes']-lastetlike))
            speaker.Speak('赞数增加:'+str(upstat['data']['likes']-lastetlike))
        else:
            print('赞数减少:'+str(lastetlike-upstat['data']['likes']))
            speaker.Speak('赞数减少:'+str(lastetlike-upstat['data']['likes']))
    lastetlike=upstat['data']['likes']
######################relstat区
    res=requests.get(relstaturl,headers=headers)
    html=res.text
    relstat=json.loads(html)
    if lastetfollower==0:
        lastetfollower=relstat['data']['follower']
    #print ('follower:'+str(relstat['data']['follower'])+','+'lastetfollower:'+str(lastetfollower))
    if relstat['data']['follower']!=lastetfollower:
        changed=True
        if relstat['data']['follower']-lastetfollower>0:
            print('关注增加:'+str(relstat['data']['follower']-lastetfollower))
            speaker.Speak('关注增加:'+str(relstat['data']['follower']-lastetfollower))
        else:
            print('关注减少:'+str(lastetfollower-relstat['data']['follower']))
            speaker.Speak('关注减少:'+str(lastetfollower-relstat['data']['follower']))
    lastetfollower=relstat['data']['follower']
    res=requests.get(videoliurl,headers=headers)
    html=res.text
    videoli=json.loads(html)
    countvideo=videoli['data']['count']
    for count in range(countvideo):
        res=requests.get(videoinfourl+str(videoli['data']['vlist'][count]['aid']),headers=headers)
        html=res.text
        videoinfo=json.loads(html)
        coin=videoinfo['data']['coin']
        coins+=coin
    if lastetcoin==0:
        lastetcoin=coins
    #print ('coin:'+str(coins)+','+'lastetcoin:'+str(lastetcoin))
    if coins!=lastetcoin:
        changed=True
        if coins-lastetcoin>0:
            print('硬币增加:'+str(coins-lastetcoin))
            speaker.Speak('硬币增加:'+str(coins-lastetcoin))
        else:
            print('硬币减少:'+str(lastetcoin-coins))
            speaker.Speak('硬币减少:'+str(lastetcoin-coins))
    lastetcoin=coins
    for count in range(countvideo):
        res=requests.get(videoinfourl+str(videoli['data']['vlist'][count]['aid']),headers=headers)
        html=res.text
        videoinfo=json.loads(html)
        view=videoinfo['data']['view']
        views+=view
    if lastetview==0:
        lastetview=views
    #print ('view:'+str(views)+','+'lastetview:'+str(lastetview))
    if views!=lastetview:
        changed=True
        if views-lastetview>0:
            print('浏览量增加:'+str(views-lastetview))
            speaker.Speak('浏览量增加:'+str(views-lastetview))
        else:
            print('浏览量减少:'+str(lastetview-views))
            speaker.Speak('浏览量减少:'+str(lastetview-views))
    lastetview=views
######################更改提示
    if changed==True:
        print('这10秒里发生了很多事，再接再厉嘛')
    else:
        print('这10秒里无事发生')
######################timer循环处理
    global timer
    timer = threading.Timer(10, ytimer)
    timer.start()

timer = threading.Timer(0, ytimer)
timer.start()


