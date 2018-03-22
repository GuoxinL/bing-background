#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import urllib2
import os
import platform
import Image
import win32api, win32con, win32gui
import re, os

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
    if not os.path.exists(IMAGE_SAVE_PATH):
        os.makedirs(IMAGE_SAVE_PATH)


def set_wallpaper_from_bmp(bmp_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)


def set_wallpaper(img_path):
    # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
    img_dir = os.path.dirname(img_path)
    bmpImage = Image.open(img_path)
    new_bmp_path = os.path.join(img_dir, 'wallpaper.bmp')
    bmpImage.save(new_bmp_path, "BMP")
    set_wallpaper_from_bmp(new_bmp_path)
createImageSavePath()

imageUrl = getImageUrl()

# 获得文件名称
fileName = imageUrl.split('/')[-1]
# 下载文件命令
savePath = os.path.join(IMAGE_SAVE_PATH, fileName)

imageFile = urllib2.urlopen(imageUrl)
with open(savePath, 'wb') as output:
    output.write(imageFile.read())

# 根据不同的系统，使用不同的api来更换桌面
if (platform.system() == "Windows"):
    # TODO
    print("windows")
    set_wallpaper(savePath)

if (platform.system() == "macosx"):
    # TODO macos 设置桌面
    print("MacOSx")

if (platform.system() == "Linux"):
    # Ubuntu 设置桌面壁纸命令
    gsettings = 'gsettings set org.gnome.desktop.background picture-uri \'file://' + savePath + '\''
    # Ubuntu 设置屏幕保护图片
    gsettings = 'gsettings set org.gnome.desktop.screensaver picture-uri \'file://' + savePath + '\''
    print(gsettings)
    os.system(gsettings)
