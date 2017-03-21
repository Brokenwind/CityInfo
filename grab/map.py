#!/usr/bin/python
# coding: utf-8

__author__ = "Brokenwind"

import numpy
import re
import sys
import os
import urllib2
import json
from IPy import IP
from tables import Tables
from decimal import *
# import Logger
sys.path.append("..")
from log import Logger
# set global charset
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class BaiduMap:
    def __init__(self):
        self._logger = Logger(__file__)
        self.status ={0:"正常",
                      1:"服务器内部错误",
                      2:"请求参数非法",
                      3:"权限校验失败",
                      4:"配额校验失败",
                      5:"ak不存在或者非法",
                      101:"服务禁用",
                      102:"不通过白名单或者安全码不对",
                      200:"无权限",
                      300:"配额错误"}
        self.geoprefix = "http://api.map.baidu.com/geocoder/v2/?address="
        self.revprefix = "http://api.map.baidu.com/geocoder/v2/?location="
        self.suffix = "&output=json&ak="
        self.headers = {}
        self.headers["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"

    def access(self,url):
        """get Json object from specified url
        """
        try:
            req = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(req)
            return json.loads(response.read())
        except Exception,e:
            self._logger.error("error occured when get geo data")
            return None

    def getGeoAddress(self,position,ak):
        """get the longitude and latitude
        # Parameters:
        position: the name of a position
        ak: baidu access key,you need apply for it
        # Return: a dict which contains following attrs:
        location: consists of lng and lat attrs
        precise:
        confidence:
        level:
        """
        url = self.geoprefix + position + self.suffix + ak
        result = None
        try:
            #data = json.loads('{"status":103,"result":{"location":{"lng":123.9872889421725,"lat":47.34769981336638},"precise":0,"confidence":10,"level":"城市"}}')
            data = self.access(url)
            if not data:
                return None
            if "status" in data.keys():
                state = data["status"]
                if not state == 0:
                    if state < 200:
                        if state in self.status.keys():
                            self._logger.warn("did not got address,reason: "+self.status[state])
                        else:
                            self._logger.warn("did not got address,unknow reason")
                    elif state < 300:
                        self._logger.warn("did not got address,reason: "+self.status[200])
                    else:
                        self._logger.warn("did not got address,reason: "+self.status[300])
                    return None
                else:
                    if "result" in data.keys():
                        self._logger.info("successfully got the address")
                        return data["result"]
                    else:
                        self._logger.warn("the data do not have attr result")
                        return None
            else:
                self._logger.warn("the response data do not have attr status")
                return None
        except Exception,e:
            self._logger.error("error occured when when extract information from json object")
            return None
    
if __name__ == "__main__":
    search = BaiduMap()
    #print "%.13f" % search.getGeoAddress("齐齐哈尔铁农园艺","sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")["location"]["lng"]
    #print search.getGeoAddress("齐齐哈尔铁农园艺","sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")
    #print search.reverseGeoAddress("47.34769981336638","123.9872889421725",1,"sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")["formatted_address"]
    #print search.ipLocation("221.12.59.211","sh0wDYRg1LnB5OYTefZcuHu3zwuoFeOy")
    #search.getAllIpAddress()

