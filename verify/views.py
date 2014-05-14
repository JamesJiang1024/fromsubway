#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import XMLRenderer
from rest_framework.parsers import XMLParser
from rest_framework.response import Response
from verify.models import UserPicData
import time
from rest_framework.decorators import api_view
from lxml import etree 
import random

import hashlib

# Create your views here.

def checkSignature(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)
    
    token="jimjiang"

    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s" % tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()

    if tmpstr==signature:
        return HttpResponse(echostr)
    else:
        return None

@api_view(['GET', 'POST'])
def message_judgement(request):
    xml = etree.fromstring(request.read())
    msgType = xml.find("MsgType").text
    fromUser = xml.find("FromUserName").text  
    tousername = xml.find("ToUserName").text
    if msgType == "image":
       picurl = xml.find("PicUrl").text 
       mediaid = xml.find("MediaId").text
       picdata = UserPicData(user_open_id=fromUser, to_username=tousername, media_id=mediaid, pic_url=picurl)   
       picdata.save()
       return Response(textrender(tousername, fromUser, int(time.time()), "text", "succeed"))
    if msgType == "text":
       content = xml.find("Content").text
       if content == "new":
           last = UserPicData.objects.count() - 1
           index = random.Random().sample(range(0,last),1)[0]
           return Response(mediarender(tousername, fromUser, int(time.time()), "image", UserPicData.objects.all()[index].media_id))
       else:
           helptext = "Welcome to from subway, you can use these commad. (new: get random image from our server).Also, you can upload image to our server, when you finished, you will got succeed."
           return Response(textrender(tousername, fromUser, int(time.time()), "text", helptext))
    return Response(msgType)

def textrender(fromuser, touser, createTime, msgtype, content):
    return """
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>
    """ % (touser, fromuser, createTime, msgtype, content)

def mediarender(fromuser, touser, createTime, msgtype, mediaid):
    return """
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Image>
    <MediaId><![CDATA[%s]]></MediaId>
    </Image>
    </xml>
    """ % (touser, fromuser, createTime, msgtype, mediaid)
