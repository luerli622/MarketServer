#!/usr/bin/python
# -*- coding: utf-8 -*-
# sinaStockDataApi.py
import urllib2
from config import *

class CSinaStockDataApi(object):
	def __init__(self, stockCode, stockType):
		super(CSinaStockDataApi, self).__init__()
		self.stockCode = stockCode			#sinaAPI的请求代码
		self.stockType = stockType			#股票类型 1：A股， 2：商品期货， 3：股指期货
		self.baseURL   = "http://hq.sinajs.cn/list="
		self.tickData  = {
				"stockCode" : stockCode[2:],	#股票代码
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

	def getData(self):
		try:
			html = urllib2.urlopen(self.baseURL + self.stockCode).read()
		except urllib2.HTTPError, exc:
			if exc.code == 404:
				print "Not found !"
				return
			else:          
				print "HTTP request failed with error %d (%s)" % (exc.code, exc.msg)
		except urllib2.URLError, exc:
			print "Failed because:", exc.reason

		self.fomartData(html)

	def fomartData(self, html):
		_data = html.split("\"")
		_data = _data[1]
		if not _data:
			print "subCode Error", self.stockCode
			return 
		_data = _data.split(",")
		#print _data, len(_data)
		#股票格式化
		if self.stockType == 1:
			self.tickData["stockName"]      = _data[0]
			self.tickData["todayOpen"]      = float(_data[1])
			self.tickData["yesterdayClose"] = float(_data[2])
			self.tickData["close"]          = float(_data[3])
			self.tickData["match"]          = float(_data[3])
			self.tickData["dayHigh"]        = float(_data[4])
			self.tickData["dayLow"]         = float(_data[5])
			self.tickData["vol"]            = int(float(_data[8])/100)
			self.tickData["amount"]         = int(float(_data[9])/10000)
			for x in range(5):
				#叫买量
				try:
					self.tickData["bidVol"][x]   = int(_data[10+x*2])/100
				except ValueError:
					pass
				#叫买价
				try:
					self.tickData["bidPrice"][x]   = float(_data[11+x*2])
				except ValueError:
					pass
				#叫卖量
				try:
					self.tickData["askVol"][x]   = int(_data[20+x*2])/100
				except ValueError:
					pass
				#叫卖价
				try:
					self.tickData["askPrice"][x]   = float(_data[21+x*2])
				except ValueError:
					pass
			self.tickData["dateTime"] = datetime.datetime.strptime(_data[30]+" "+_data[31],"%Y-%m-%d %H:%M:%S")
		#商品期货格式化
		if self.stockType == 2:
			self.tickData["stockName"]      = _data[0]
			self.tickData["todayOpen"]      = float(_data[2])
			self.tickData["dayHigh"]        = float(_data[3])
			self.tickData["dayLow"]         = float(_data[4])
			self.tickData["yesterdayClose"] = float(_data[5])
			self.tickData["close"]          = float(_data[8])
			self.tickData["match"]          = float(_data[8])
			self.tickData["vol"]            = int(_data[14])/100
			self.tickData["bidVol"][0]      = int(_data[11])/100
			self.tickData["bidPrice"][0]    = float(_data[6])
			self.tickData["askVol"][0]      = int(_data[12])/100
			self.tickData["askPrice"][0]    = float(_data[7])
			self.tickData["dateTime"]       = datetime.datetime.strptime(_data[17],"%Y-%m-%d")
		#股指期货格式化
		if self.stockType == 3:
			self.tickData["todayOpen"]      = float(_data[0])
			self.tickData["dayHigh"]        = float(_data[1])
			self.tickData["dayLow"]         = float(_data[2])
			self.tickData["close"]          = float(_data[3])
			self.tickData["match"]          = float(_data[3])
			self.tickData["vol"]            = int(_data[4])/100
			self.tickData["yesterdayClose"] = float(_data[13])
			self.tickData["dateTime"]       = datetime.datetime.strptime(_data[36]+" "+_data[37],"%Y-%m-%d %H:%M:%S")
			#print self.tickData

def main():
	if1312 = CSinaStockDataApi("CFF_RE_IF1312", 3)
	if1312.getData()
	pass

if __name__ == '__main__':
	main()