#!/usr/bin/python
# -*- coding: utf-8 -*-
# controller.py
from config import *
from dataListener import *
import copy

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
				_temp["stockType"]       = int(lineList[2])
				_temp["stockName"]       = lineList[3].replace("\n","")
				g_stockDict[lineList[0]] = _temp
			except IndexError:
				break
		#print len(g_stockDict)

	#------------------
	#创建数据连接，分配策略
	#------------------
	def linkServerInit(self):
		self.allSubStockList = []
		#所有的监听器对象池
		self.listenerDict = {}	#key: 股票代码, value 监听对象 一个股票代码一个对象
		#所有策略对象对象池
		self.strategyDict = {}	#key: 股票代码, value{key:策略名, value 监听对象 一个股票代码一个对象}
		#link管理池
		self.linkDict	= {}	#key: mac地址, value 详细对象dict
		
		#global g_linkPool
		self.getNewLinkInit(g_linkPool["d43d7e34f9d0"])

	#当有新的连接连入之后
	def getNewLinkInit(self, linkPool):
		self.creatStrategy(linkPool)
		#self.linkDict[linkPool["macAddress"]] = linkPool

	def creatStrategy(self, linkPool):
		global g_signalStrategyDict
		global g_multipleStrategyDict

		linkPool["singalObjDict"]   = {}
		linkPool["multipleObjDict"] = {}
		linkPool["listenerDict"]    = {}

		#订阅全部股票
		global g_stockDict
		if linkPool["subStock"][0] == "All-1":
			linkPool["subStock"] = []
			for key, value in g_stockDict.items():
				if value["stockType"] == 1:
					linkPool["subStock"].append(key)
			pass

		for _stockName in linkPool["subStock"]:
			if not self.strategyDict.has_key(_stockName):
				self.strategyDict[_stockName] = {}
			#添加单信号策略
			linkPool["singalObjDict"][_stockName] = {}
			for _singalName in linkPool["subSingal"]:
				try:
					_singaleObj = self.strategyDict[_stockName][_singalName]
				except KeyError:
					_singaleObj = copy.copy(g_signalStrategyDict[_singalName])
					self.strategyDict[_stockName][_singalName] = _singaleObj
				_singaleObj.init(_stockName)
				linkPool["singalObjDict"][_stockName][_singalName] = _singaleObj
			#添加多信号策略
			linkPool["multipleObjDict"][_stockName] = {}
			for _multipleName in linkPool["subMultiple"]:
				try:
					_multipleObj = self.strategyDict[_stockName][_multipleName]
				except KeyError:
					_multipleObj = copy.copy(g_multipleStrategyDict[_multipleName])
					self.strategyDict[_stockName][_multipleName] = _multipleObj
				#给多信号策略添加单信号对象
				_multipleObj.init(_stockName,linkPool["singalObjDict"])
				linkPool["multipleObjDict"][_stockName][_multipleName] = _multipleObj
			
			self.creatListener(linkPool, _stockName)

	def creatListener(self, linkPool, stock):
		global g_stockDict
		if not self.listenerDict.has_key(stock):
			newListener = CDataListener(
				stock,
				g_stockDict[stock]["sinApiCode"],
				g_stockDict[stock]["stockType"],
				linkPool["singalObjDict"][stock],
				linkPool["multipleObjDict"][stock])
			newListener.start()
			self.listenerDict[stock] = newListener
			linkPool["listenerDict"][stock] = self.listenerDict[stock]
		else:
			self.listenerDict[stock].getNewStrategyObj(
				linkPool["singalObjDict"][stock],
				linkPool["multipleObjDict"][stock])
			linkPool["listenerDict"][stock] = self.listenerDict[stock]
		self.listenerDict[stock].getRequesHandlerObj(linkPool["requesHandlerObj"])

def main():
	c = Controller()

if __name__ == '__main__':
	main()