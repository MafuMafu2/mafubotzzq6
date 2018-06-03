# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, re, string, os, ast, pytz, urllib

botStart = time.time()
conf_dir = "./configs/"
cert_dir = "./certs/"

def Linecl(Email, Password):
    cl = LINE(idOrAuthToken=Email, passwd=Password, certificate=cert_dir+Email+".crt")
    return cl

cl = LINE("EtCvLPP27cyHLTt6sfFe.7McWUKbmQViekyv06K3ShG.mpN6ThkgOjL11wZC8syTvRqYvoy/J/Iar5SzdD6juc0=")
cl.log("Auth Token : " + str(cl.authToken))
oepoll = OEPoll(cl)
readOpen = codecs.open(conf_dir+"read.json","r","utf-8")
settingsOpen = codecs.open(conf_dir+"temp.json","r","utf-8")
read = json.load(readOpen)
settings = json.load(settingsOpen)

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

lineSettings = cl.getSettings()

clProfile = cl.getProfile()

clMID = cl.profile.mid

myProfile["displayName"] = clProfile.displayName
myProfile["statusMessage"] = clProfile.statusMessage
myProfile["pictureStatus"] = clProfile.pictureStatus

BG="uf87672295eeef310c67d5ce81bbf189d"
NC="u8adfb790a54a5f81ac2741cc2ede7ce7"
owner=[BG, NC]
admin=[BG, NC, clMID]
admin5=[BG, NC, clMID]
admin4=[BG, NC, clMID]
bots={clMID:cl}
mid=cl.getProfile().mid

msg_dict = {}
bl = [""]

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

def restartBot():
    print ("[Setting]Bot restart")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def backupData():
    try:
        backup = settings
        f = codecs.open(conf_dir+'temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open(conf_dir+'read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def logError(text):
    cl.log("[error] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))

def sendMessageWithMention(to, mid):
    try:
        data = '{"S":"0","E":"9","M":'+json.dumps(mid)+'}'
        text_ = '@MaFuTag '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+data+']}'}, contentType=0)
    except Exception as error:
        logError(error)

def helpmessage():
    helpMessage = """★BGBOT權限機★
——☆MAFU專用☆——
【ad:@】增加權限者☆
【ra:@】刪除權限者☆
【mad:】使用mid增加權限☆
【mra:】使用mid刪除權限☆
——★系統指令★——
【bg:help】查看所有指令
【Update】重啟機器
【Uptime】運行時間
【@bg3sp】測試網速
——★機器設定★——
【Set】查看設定
【About】查看自己的狀態
【Join On/Off】自動入群開關
【Leave On/Off】自動離開副本開關
【Reread On/Off】顯示收回開關
——★一般指令★——
【Me】丟出自己友資
【Mid】查看自己Mid
【Name】查看名字
【Bio】查看個簽
【Picture】查看自己頭貼
【Cover】查看自己封面
【Contact @】查看標注者友資
【Mid @】查看標注者MID
【Name @】查看標注者名稱
【Bio @】查看標注者個簽
【Picture @ 】查看標注者頭貼
【Cover @ 】查看標注者封面
【Time】查看現在時間
【Gcreator】查看群主
【Gurl】丟出群組網址
【urlon】打開網址邀請
【urloff】關閉群組網址
【Glist】查看所有群組
【Gml】查看群組成員
【Ginfo】查看群組訊息
——★群組指令★——
【Ri @】重新邀請
【NT】名字標註成員
【Zt】標註零字
【Zm】零字mid
【Cancel】取消所有成員邀請
【Gn】更改群組名稱
【Gc @】查看個資
【Inv  mid】邀請
【Ban @】黑單
【Unban @】解除黑單
【/cb】清空黑單
【Kill Ban】踢出黑單
【Tagall】標註全體
★Make by Mafu★"""
    return helpMessage

def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(op.param1)
            print ("[ 5 ] 通知添加好友 名字: " + contact.displayName)
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                cl.sendMessage(op.param1, "hello {} Thx for add".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 13:
           if settings["autoJoin"] == True:
                if op.param2 in admin:
                        if op.param3 in mid:
                            cl.acceptGroupInvitation(op.param1)
                            contact1 = cl.getContact(op.param2)
                            group = cl.getGroup(op.param1)
                            welcome = contact1.displayName + "招待使用！"
                            cl.sendMessage(op.param1, welcome)
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            kerror = contact1.displayName + "踢了" + contact2.displayName
            cl.sendMessage(op.param1, kerror)
        if op.type == 15:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            if settings["seeLeave"] == True:
                try:
                    arrData = ""
                    text = "%s "%('成員')
                    arr = []
                    mention = "@x "
                    slen = str(len(text))
                    elen = str(len(text) + len(mention) - 1)
                    arrData = {'S':slen, 'E':elen, 'M':op.param2}
                    arr.append(arrData)
                    text += mention + "離開了群組..."
                    cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                except Exception as error:
                    print(error)
        if op.type == 17:
            if op.param2 in settings['blacklist']:
                cl.sendMessage(op.param1, "進入者於黑名單中")
                cl.kickoutFromGroup(op.param1,[op.param2])
            else:
                contact1 = cl.getContact(op.param2)
                group = cl.getGroup(op.param1)
                if settings["seeJoin"] == True:
                    try:
                        arrData = ""
                        text = "%s "%('歡迎')
                        arr = []
                        mention = "@x "
                        slen = str(len(text))
                        elen = str(len(text) + len(mention) - 1)
                        arrData = {'S':slen, 'E':elen, 'M':op.param2}
                        arr.append(arrData)
                        text += mention + "加入群組！"
                        cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                    except Exception as error:
                        print(error)
        if op.type == 13:
            if op.param3 in settings['blacklist']:
                cl.sendMessage(op.param1, "被邀請者於黑名單中")
                cl.cancelGroupInvitation(op.param1,[op.param3])
        if op.type == 24:
            print ("[ 24 ] 離開副本")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 13:
                if settings["contact"] == True:
                    msg.contentType = 0
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                            cl.sendMessage(msg.to,"[名稱]:\n" + msg.contentMetadata["名稱"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[個簽]:\n" + contact.statusMessage + "\n[頭像]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[名稱]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[個簽]:\n" + contact.statusMessage + "\n[頭像]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面]:\n" + str(cu))
            elif msg.contentType == 7:
                stk_id = msg.contentMetadata['STKID']
                stk_ver = msg.contentMetadata['STKVER']
                pkg_id = msg.contentMetadata['STKPKGID']
                number = str(stk_id) + str(pkg_id)
                if number in settings['sr']:
                    react = settings['sr'][number]
                    cl.sendMessage(to, str(react))
                elif settings["checkSticker"] == True:
                    path = "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png;compress=true".format(stk_id)
                    ret_ = "<<貼圖資料>>"
                    ret_ += "\n[貼圖ID] : {}".format(stk_id)
                    ret_ += "\n[貼圖包ID] : {}".format(pkg_id)
                    ret_ += "\n[貼圖網址] : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n[貼圖圖片網址]：https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png;compress=true".format(stk_id)
                    ret_ += "\n<<完>>"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                    cl.sendMessage(op.param1,ret_)
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    msg.contentType = 0
                    ret_ = "[文章持有者]\n " + msg.contentMetadata["serviceName"]
                    ret_ += "\n[文章預覽]\n " + msg.contentMetadata["text"]
                    ret_ += "\n[文章網址]\n " + msg.contentMetadata["postEndUrl"]
                    cl.sendMessage(msg.to, ret_)
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in admin5:
                if text.lower() == 'bgbye':
                    if msg.toType == 2:
                        ginfo = cl.getGroup(to)
                        cl.leaveGroup(to)
                elif "test" in msg.text:
                    if msg.toType == 2:
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                    cl.sendMessage(midd,"斑鳩生日快樂")
                                except:
                                    pass
    except Exception as error:
        logError(error)

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
