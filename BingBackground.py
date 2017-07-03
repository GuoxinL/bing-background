# -*- coding: utf-8 -*-
import json
import sys
import urllib2
import os

reload(sys)
sys.setdefaultencoding('utf8')


def getDomain():
    return 'http://www.bing.com'


def getUrl():
    return '/HPImageArchive.aspx?format=js&idx=0&n=1'


# 请求路径
requestUrl = getDomain() + getUrl()
response = urllib2.urlopen(requestUrl)
jsonString = response.read()
jsonObject = json.loads(jsonString)
# 图片路径
imageUrl = getDomain() + jsonObject["images"][0]["url"]
# 获得当前目录
currentFolder = os.getcwd()
# 获得文件名称
fileName = imageUrl.split('/')[-1]
# 下载文件
wget = 'wget -O ' + fileName + ' ' + imageUrl
os.system(wget)
# Ubuntu 设置桌面壁纸命令
gsettings = 'gsettings set org.gnome.desktop.background picture-uri file://' + currentFolder + '/' + fileName
os.system(gsettings)
