#!/usr/bin/python
# -*- coding: utf-8 -*-
# controller.py
from config import *
from sinaStockDataApi import CSinaStockDataApi as stockApi

class Controller(object):
	def __init__(self):
		super(Controller, self).__init__()
		#基本基础服务初始化
		self.baseServerInit()
		#根据连接请求分配策略及订阅股票
		self.linkServerInit()
	#------------------
	#基本初始服务初始化
	#------------------
	def baseServerInit(self):
		self.loadStockDic()
		self.loadSecuritiesMarginStockCode()
		pass
	#读取股票代码、api请求代码字典
	def loadStockDic(self):
		global g_stockDict
		_fileReader  = open("stockDict.csv","r")
		while 1:
			line     = _fileReader.readline()
			lineList = line.split(",")
			try:
				_temp                    = {}
				_temp["sinApiCode"]      = lineList[1]
				_temp["stockName"]       = lineList[2].replace("\n","")
				g_stockDict[lineList[0]] = _temp
			except IndexError:
				break
		#print len(g_stockDict)
	#读取所有融资融券代码
	def loadSecuritiesMarginStockCode(self):
		global g_smStocks
		_fileReader  = open("smStock.csv","r")
		while 1:
			line     = _fileReader.readline()
			stockCode = line.replace("\n","")
			if not stockCode:
				break
			g_smStocks.append(stockCode)
		#print g_smStocks
	#------------------
	#创建数据连接，分配策略
	#------------------
	def linkServerInit(self):
		self.allSubStockList = []
		#所有的监听器对象池
		self.listenerDict = {}	#key: 股票代码, value 监听对象 一个股票代码一个对象
		#所有策略对象对象池
		self.strategyDict = {}	#key: 股票代码, value{key:策略名, value 监听对象 一个股票代码一个对象}
		#期货服务器列表
		self.futureServerList = []
		#股票服务器列表
		self.stockServerList = []
		
		#global g_linkPool
		self.getNewLinkInit(g_linkPool["d43d7e34f9d0"])

	#当有新的连接连入之后
	def getNewLinkInit(self, linkPool):
		self.getSubStockList(linkPool)
		self.creatStockServer(linkPool)

	def getSubStockList(self, linkPool):
		if linkPool["subStock"] == ['All']:
			linkPool["sinApiCodes"] = []
			for _stockCode, _value in g_stockDict.items():
				linkPool["sinApiCodes"].append(_value["sinApiCode"])
		if linkPool["subStock"] == ['All-sm']:
			linkPool["sinApiCodes"] = []
			for _stockCode, _value in g_stockDict.items():
				if _stockCode in g_smStocks:
					linkPool["sinApiCodes"].append(_value["sinApiCode"])
		else:
			linkPool["sinApiCodes"] = []
			for _stockCode in linkPool["subStock"]:
				linkPool["sinApiCodes"].append(g_stockDict[_stockCode]["sinApiCode"])

	def creatStockServer(self, linkPool):
		stockDataServer = stockApi(linkPool["subStock"],linkPool["sinApiCodes"])
		stockDataServer.getData()
		pass
		#print stockDataServer.sinApiCodes
		#while True:
		#	stockDataServer.getData()
		#	print datetime.datetime.now()
		#	time.sleep(15)
		#	pass


def main():
	c = Controller()


if __name__ == '__main__':
	main()