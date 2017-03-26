#!/usr/bin/python
# coding=utf-8
import numpy
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import DataFrame,Series
from tables import Tables
from baidu import Baidu
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from map import BaiduMap
import sys
import json
import uuid
sys.path.append("..")
from log import Logger

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Grab:
    def __init__(self):
        self._logger = Logger(__file__)
        #profile = FirefoxProfile()
        #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        #self._browser = webdriver.Firefox(profile)
        self._browser = webdriver.Firefox()
        self.baidu = Baidu(self._browser)
        self.map = BaiduMap()
        self.ak = "sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy"
        self.table = Tables();

    def __del__(self):
        self._browser.quit()
        self.record.close()

    def loadData(self):
        with open('allprovinces.json') as json_file:
            data = json.load(json_file)
        return data

    def getData(self):
        data = self.loadData()
        if not data:
            return None
        for pro in data["provincesList"]:
            cities = pro["Citys"]
            proname = pro["Name"]
            if ( len(cities) > 0 ):
                for city in cities:
                    name = city["Name"]
                    self._logger.info("current city: "+name)
                    cityInfo = self.baidu.baike(name)
                    if not cityInfo:
                        continue
                    cityBasic = cityInfo["basic"]
                    summary = cityInfo["summary"]
                    cityImage = self.baidu.niceImage(name+'壁纸',width=1300,height=750)
                    cityGeo = self.map.getGeoAddress(name,self.ak)
                    if cityGeo:
                        if "location" in cityGeo.keys():
                            location = cityGeo["location"]
                            lng = location["lng"]
                            lat = location["lat"]
                    else:
                        lng = "0.0"
                        lat = "0.0"
                    cityID = city["Id"]
                    zoneNum = zipCode = area = climate = ptype = acreage = ""
                    if u"电话区号" in cityBasic:
                        zoneNum = cityBasic[u"电话区号"]
                    if u"邮政区码" in cityBasic:
                        zipCode = cityBasic[u"邮政区码"]
                    if u"地理位置" in cityBasic:
                        area = cityBasic[u"地理位置"]
                    if u"气候条件" in cityBasic:
                        climate = cityBasic[u"气候条件"]
                    if u"行政区类别" in cityBasic:
                        ptype = cityBasic[u"行政区类别"]
                    if u"面    积" in cityBasic:
                        acreage = cityBasic[u"面    积"]
                    cityParams = (cityID,name,proname,ptype,area,zoneNum,acreage,climate,zipCode,lng,lat,summary)
                    self.table.insertTable("city",cityParams)
                    if  cityImage:
                        for pic in cityImage:
                            self.table.insertTable("cityImages",(cityID,str(uuid.uuid1()),pic,"",""))
                    
if __name__ == "__main__":
    grab = Grab()
    grab.getData()

