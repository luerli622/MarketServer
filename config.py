#!/usr/bin/python
# -*- coding: utf-8 -*-
# config.py
import datetime
import time
import os
import threading
import copy

#多股票策略类:	股票间的信号管理，多股票策略
#import multipleStrategy
#单股票策略类：	单只股票的信号策略
#import signalStrategy

#读取设置参数
execfile(".\config.ini")

#股票代码、股票名称、所属市场对应dic
g_stockDict = {}
#所有融资融券代码
g_smStocks = []

#链接池
g_linkPool		= {}
#"""
#链接池测试
g_linkPool["d43d7e34f9d0"] = {
	"macAddress"		: "d43d7e34f9d0",
	"subStock"			: ["All-sm"],	#All 所有股票代码; All-sm 所有融资融券代码
	"subInstruments"	: [u"if1312"],
	"subSingal"			: ["SQTPointBreakSingal"],
	"subMultiple"		: ["SQTIFandSSEdiffMultiple"],
	#以上由客户端请求
	#----------------
	"requesHandlerObj"	: "testObj-d43d7e34f9d0",	#链接对象
	#----------------
	#以下由controller控制生成
	"listenerDict"		: {},  #数据监听对象dict, key:股票代码, value:监听对象
	"singalObjDict"		: {},  #key: 股票代码, {key: 策略名，value：策略对象}
	"multipleObjDict"	: [],  #key: 股票代码, {key: 策略名，value：策略对象}
	"signalPool"		: []
	}
#"""