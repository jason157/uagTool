# coding=utf-8

import re
import sys
import os
from enum import Enum
DebugFlag =1

'''
Description：
读取文件到内存中
In parameter
	logFileFullPath:文件的全路径 比如d:\\uag.log 等
'''

def loadLogFile(logFileFullPath):
	#uagLog = open('/home/zxin10/log/uag.log')
	if os.path.isfile(logFileFullPath):
		uagLog = open(logFileFullPath, errors='ignore')
		uagLogData = uagLog.readlines()
		uagLog.close()
	else:
		print ("Error: FileName or Path Error")
		return False
	return uagLogData
'''
正在匹配串：
'''# 会议ID SDP
SDPConfIDPattern = re.compile(r'SdpId\[(00JZM.*?)\]')
# 会议ID in UAG
UAGConfIDPattern = re.compile(r'CONF\[(\d.*?)\]')
# 主席正则
ChairmanPatrern =  re.compile(r'Chairman\[(.*?)\]')
ChairmanNumPattern = re.compile(r'\+(\d+)')
# 时间片提取
# 会议ID SDP
SDPIDPattern = re.compile(r'(00JZM\d{22})')
# 会议ID in UAG
UAGIDPattern = re.compile(r'CONF\[(\d.*?)\]')
# 主席正则
ChairmanPatrern = re.compile(r'Chairman\[(.*?)\]')
ChairmanNumPattern = re.compile(r'\+(\d+)')

APPIDPattern = re.compile(r'AppId\[(\d{1,3})\]')
PaticipantsNumPattern = re.compile(r'PaticipantsNum\[(\d{1,2})\]')
ConfTypePattern = re.compile(r'ConfType\[(\d)\]')
EnterpriseIdPattern = re.compile(r'EnterpriseId\[(.*?)\]')
# 参与成员的号码匹配，考虑到固话接入取7-13位号码
ParticipantPattern = ParticipantPattern = re.compile(r'Participant.*?(\d{7,13})')

# 视频会议参数
VideoCapPattern = re.compile(r'VedioCap\[(\d)]')
MaxImageNumPattern = re.compile(r'MaxImageNum\[(\d)\]')
VideoSwitchModePattern = re.compile(r'VedioSwitchMode\[(\d)\]')
RelayModePattern = re.compile(r'RelayMode\[(\d)\]')

# sep ID 正则
SEPIDPattern = re.compile(r'as\sconference\sid\[(.*?)\]')
# 会议持续时间
ConfDurationPattern = re.compile(r'ConfDuration\[(\d+)\]')
# 成员状态 group(0) 号码， group(1) 状态
ParticipantStatePattern = re.compile('AsNotifyParticipantState.*?Status\[(.*?)\]')

'''
Description:
根据主席号码和时间（日期传入 YY-MM-DD 或者 HH:MM:SS)
生成一个匹配到的第一个会议的日志文件: 会议ID.log
In parameter
	logFileFullPath:日志文件的全路径+文件名
	Chairman:主席号码
	ConfTime:时间点
'''
def GetOneConf(logFileFullPath,Chairman,ConfTime):
	if os.path.isfile(logFileFullPath):
		uagLogData=loadLogFile(logFileFullPath)
	else:
		print ("Error: FileName or Path Error")
		return False
	UAGConfID = ""
	for line in uagLogData:
		if ("CreateConference" and str(Chairman) and str(ConfTime)) in line:
			UAGConfID = UAGConfIDPattern.findall(line)
	if len(UAGConfID) == 1:
		ConfLog = open(str(UAGConfID[0]) + '.log','w')
		for line in uagLogData:
			if str(UAGConfID[0]) in line:
				ConfLog.write(line)
		ConfLog.close()
	else:
		print("Get Conf Error ")
		return False
	return True

'''
Description：
传入一个uag.log文件，会检测日志中所有的会议，并分割，单个会议一个文本：A_主席号码_时间.log
生成的文件在脚本的temp目录下
In parameter
	logFileFullPath:日志文件的全路径+文件名
'''
def GetAllConf(logFileFullPath):
	if os.path.isfile(logFileFullPath):
		uagLogData=loadLogFile(logFileFullPath)
	else:
		print ("Error: FileName or Path Error")
		return 0
	UAGConfIDList = []
	ChairmanList = []
	#ChairmanNum = []
	ConfTime = []
	Index  = 0
	#提取出所有的会议信息，包括会议串 主席 时间点
	for line in uagLogData:
		if ("CreateConference" and "Chairman" and "AppId" and "AppPasswd") in line:
			UAGConfIDList.append(UAGConfIDPattern.findall(line)[0])
			ChairmanList.append(ChairmanPatrern.findall(line)[0])
			ConfTime.append(line[0:21])
			Index = Index + 1
	#根据会议串分割日志
	if len(UAGConfIDList) > 0:
		tempPath = "./temp"
		if not os.path.exists(tempPath):
			os.mkdir(tempPath)
		for i in range(len(UAGConfIDList)):
			ConfTime1 = ConfTime[i][9:11] + "-" + ConfTime[i][12:14] + "-" + ConfTime[i][15:17] #规整时间为HH-MM
			ChairmanNumtemp = ChairmanNumPattern.findall(str(ChairmanList[i])) ##从主席中提取出主席的号码串（数字）
			fileName = 'A_'+ str(ChairmanNumtemp[0]) + "_" + ConfTime1 + '.log'# 文件的名称
			FullName = os.path.join(tempPath,fileName) # 文件全路径
			ConfLog = open(FullName,'w',encoding="UTF8") #写入文件，一下几行是写入必要的信息在文件头
			ConfLog.write("会议ID：" + UAGConfIDList[i] + "\n")
			ConfLog.write("会议主席：" + ChairmanList[i] + "\n")
			ConfLog.write("会议时间：" + ConfTime[i] + "\n")
			for line in uagLogData:
				if str(UAGConfIDList[i]) in line: # 判断是否属于同一个会议，同则写入会议
					ConfLog.write(line)
			ConfLog.close()
		else:
			print("Get Conf Error ")
'''
Description:
从单个会议中提取出会议信息:
	会议内部ID
	会议SDP ID
	会议时间
	会议主席
	会议成员列表
	会议类型
	....
'''

def GetConfInfo(uagLogData):
	ConfInfo={ # 会议信息字典
		'UAGID': '',
		'SDPID': '',
		'ConfTime': '',
		'Chairman': '',
		'Members': [],
		'ConfType': '',
		'APPID': '',
	}
	ConfInfoEx = { # 会议信息拓展 视频会议参数
	}
	##会议信息
	ParticipantStat={
	}
	PaticipantsNum = 0
	Members = []
	MemberStatList =[]
	for line in uagLogData:
		if ("CreateConference" and "Chairman" and "AppId" and "AppPasswd") in line:
			ConfInfo['UAGID'] = str(UAGIDPattern.findall(line)[0])
			ConfInfo['Chairman']=str(ChairmanPatrern.findall(line)[0])
			ConfInfo['ConfTime']=str(line[0:21])
			ConfInfo['APPID']=str(APPIDPattern.findall(line)[0])
			ConfType=(ConfTypePattern.findall(line)[0])
			ConfInfo['ConfType']= str(ConfType)
			ConfInfo['EnterpriseId']=EnterpriseIdPattern.findall(line)[0]
			PaticipantsNum = int(PaticipantsNumPattern.findall(line)[0])
		# 提取成员
		if ("Conference,Participant" in line) and (PaticipantsNum > 0):
			Member = ParticipantPattern.findall(line)[0]
			ConfInfo['Members'].append(Member)
			PaticipantsNum -= 1
		#提取提取视频会议参数
		if ("CreateConference" and  "VedioCap" and "MaxImageNum" and "VedioSwitchMode" in line):
			ConfInfoEx['VideoCap']= VideoCapPattern.findall(line)[0]
			ConfInfoEx['MaxImageNum']= MaxImageNumPattern.findall(line)[0]
			ConfInfoEx['VideoSwitchMode'] = VideoSwitchModePattern.findall(line)[0]
			ConfInfoEx['RelayMode'] = RelayModePattern.findall(line)[0]
		# 获取SDPID
		if ("CreateConference" and "Request:SepId" and "SdpId") in line:
			ConfInfo['SDPID']=SDPConfIDPattern.findall(line)[0]
		# 获取会议Ready时间
		if str(ConfInfo['SDPID']) and "confStatus[Ready]" in line:
			ConfInfo['ReadyTime']=str(line[0:21])
		# 获取会议结束时间
		if str(ConfInfo['SDPID']) and "confStatus[end]" in line:
			ConfInfo['EndTime']=str(line[0:21])
			ConfInfo['ConfDuration']=ConfDurationPattern.findall(line)[0]
		# 获取会议asID sepid
		if "Create conference susccess,as conference id" in line:
			ConfInfo['SEPID']=SEPIDPattern.findall(line)[0]
		for member in ConfInfo['Members']:
			if str(member) and "AsNotifyParticipantState:Number" in line:
				#这个stat的形式如下 stat={'num':numstat{'stat-time':'stat'}  } ##这里错了
				TmpStat=str(line[0:21]) + " " + str(member) +" " +  str(ParticipantStatePattern.findall(line)[0])
				MemberStatList.append(TmpStat)

	#如果是视频会议，把拓展字段放入会议信息中
	if ConfInfo['ConfType']=='video':
		ConfInfo['ConfInfoEx'] = ConfInfoEx
	ConfInfo['MemberStat']= MemberStatList
	return ConfInfo

def GetAllConfList(uagLogData):
	ConfList = []
	for line in uagLogData:
		if ("CreateConference" and "Chairman" and "AppId" and "AppPasswd") in line:
			ConfTime = str(line[0:17])
			Chairman = str(ChairmanNumPattern.findall(line)[0])
			UAGID = str(UAGIDPattern.findall(line)[0])
			ConfList.append("Time:" + ConfTime + "--" +"UAGID:" + UAGID + "--" + "Number:" + Chairman)
	return ConfList

def getOneConfLog(filedata,uagid="",Number=""):
	ConfLog=[]
	for line in filedata:
		if uagid and Number in line:
			ConfLog.append(line)
	return ConfLog
def getChairmanNuagid(string):
	numPattern = re.compile(r'Number\:(\d+)')
	uagidPattern = re.compile(r'UAGID\:(\d+)')
	Chairman = str(numPattern.findall(string)[0])
	UAGID = str(uagidPattern.findall(string)[0])
	return Chairman,UAGID










#8-19 实现日志按照会议分类，提取出主席 发起会议时间 会议内部ID
#功能实现需求：
#	1.提取出参与会议的成员
#	2.提取出SDP会议ID
#	3.提取出会议类型
#	4.提取错误请求
#	5.在会议中成员状态的变化
#	6.优化会议过滤










