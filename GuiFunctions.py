# coding=utf-8

import BaseUagLog
import json
import BaseIAMFunction

def openFile(fileName):
	return BaseUagLog.loadLogFile(fileName)
def loadDataToDatabase(filedata):
	return 0
def getConfList(filedata):
	return BaseUagLog.GetAllConfList(filedata)
def getConfInfo(filedata,string):
	Chairman,UAGID = BaseUagLog.getChairmanNuagid(string)
	ConfLog=BaseUagLog.getOneConfLog(filedata, Chairman, UAGID)
	ConfInfo=BaseUagLog.GetConfInfo(ConfLog)
	return ConfInfo
def dictionaryFormat(ConInfo):
	if type(ConInfo)==dict:
		FormatConfInfo=json.dumps(ConInfo,indent=1)
	return FormatConfInfo
def getConfLogbyUAGID():
	return BaseUagLog.getOneConfLog()
def getUAGIDfromConfList(string):
	chaireman,UAGID=BaseUagLog.getChairmanNuagid(string)
	return str(UAGID)
def OpenAccountToOCS(numberlist):
	return BaseIAMFunction.OCSOpenAccount(numberlist)