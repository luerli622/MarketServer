#!/usr/bin/python
# -*- coding: utf-8 -*-
# sinaStockDataApi.py
import urllib2
from config import *

class CSinaStockDataApi(object):
	def __init__(self, stocks, sinApiCodes):
		super(CSinaStockDataApi, self).__init__()
		self.stocks = stocks					#股票代码
		self.sinApiCodes = sinApiCodes			#sinaAPI的请求代码
		self.baseURL   = "http://hq.sinajs.cn/list="

	def getData(self):
		try:
			_url = self.baseURL
			for _sinApiCode in self.sinApiCodes:
				_url += _sinApiCode + ","
			_url = _url[:-1]
			html = urllib2.urlopen(_url).read()
			self.decode(html)
		except urllib2.HTTPError, exc:
			if exc.code == 404:
				print "Not found !"
				return
			else:          
				print "HTTP request failed with error %d (%s)" % (exc.code, exc.msg)
		except urllib2.URLError, exc:
			print "Failed because:", exc.reason

	def decode(self, html):
		_strDatas = html.split(";\n")
		for _strData in _strDatas:
			if _strData:
				_data = _strData.split("=")
				_data = _data[0][-6:], self.fomartData(_data[1])
				print _data
		#self.fomartData(html)

	def fomartData(self, _data):
		_data = _data.replace("\"","")
		_data = _data.split(",")
		#股票格式化
		_tickData = self.getDefaultTickData()
		_tickData["stockName"]      = _data[0]
		_tickData["todayOpen"]      = float(_data[1])
		_tickData["yesterdayClose"] = float(_data[2])
		_tickData["close"]          = float(_data[3])
		_tickData["match"]          = float(_data[3])
		_tickData["dayHigh"]        = float(_data[4])
		_tickData["dayLow"]         = float(_data[5])
		_tickData["vol"]            = int(float(_data[8])/100)
		_tickData["amount"]         = int(float(_data[9])/10000)
		for x in range(5):
			#叫买量
			try:
				_tickData["bidVol"][x]   = int(_data[10+x*2])/100
			except ValueError:
				pass
			#叫买价
			try:
				_tickData["bidPrice"][x]   = float(_data[11+x*2])
			except ValueError:
				pass
			#叫卖量
			try:
				_tickData["askVol"][x]   = int(_data[20+x*2])/100
			except ValueError:
				pass
			#叫卖价
			try:
				_tickData["askPrice"][x]   = float(_data[21+x*2])
			except ValueError:
				pass
		_tickData["dateTime"] = datetime.datetime.strptime(_data[30]+" "+_data[31],"%Y-%m-%d %H:%M:%S")
		return _tickData

	def getDefaultTickData(self):
		_tickData  = {
			"stockCode" : "000000",			#股票代码
			"stockName" : "",				#股票名字
			"todayOpen" : 0,				#今日开盘
			"yesterdayClose" : 0,			#昨日收盘
			"close"		: 0,				#最新价
			"match" : 0,					#最新价
			"dayHigh" : 0,					#今日最高
			"dayLow" : 0,				 	#今日最低
			"vol" : 0,						#今日成交量		单位：手
			"amount" : 0,					#今日成交金额	单位：万元
			"askPrice" : [0,0,0,0,0],		#竞卖价
			"askVol" : [0,0,0,0,0],			#竞卖量
			"bidPrice" : [0,0,0,0,0],		#竞买价
			"bidVol" : [0,0,0,0,0],			#竞买量
			"dateTime" : datetime.datetime(1990,1,1,0,0,0) #服务器时间
		}
		return _tickData

def main():
	if1312 = CSinaStockDataApi("CFF_RE_IF1312", 3)
	if1312.getData()
	pass

if __name__ == '__main__':
	main()