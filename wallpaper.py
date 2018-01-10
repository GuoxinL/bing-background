# -*- coding: utf-8 -*-
import json
import sys
import urllib2
import os

reload(sys)

# 图片保存路径，请设置绝对路径
IMAGE_SAVE_PATH = os.getcwd()

TARGET_DOMAIN = 'http://www.bing.com'
TARGET_URL = '/HPImageArchive.aspx?format=js&idx=0&n=1'


# 获得图片路径
def getImageUrl():
    response = urllib2.urlopen(TARGET_DOMAIN + TARGET_URL)
    jsonObject = json.loads(response.read())
    return TARGET_DOMAIN + jsonObject["images"][0]["url"]


# 创建保存图片路径
def createImageSavePath():
    if not os.path.exists(IMAGE_SAVE_PATH) :
        os.makedirs(IMAGE_SAVE_PATH)



createImageSavePath()

imageUrl = getImageUrl()

# 获得文件名称
fileName = imageUrl.split('/')[-1]
# 下载文件命令
savePath = os.path.join(IMAGE_SAVE_PATH, fileName)

imageFile = urllib2.urlopen(imageUrl)
with open(savePath, 'wb') as output:
    output.write(imageFile.read())

# Ubuntu 设置桌面壁纸命令
gsettings = 'gsettings set org.gnome.desktop.background picture-uri \'file://' + savePath + '\''
print(gsettings)
os.system(gsettings)
