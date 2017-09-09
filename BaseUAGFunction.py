# coding=utf-8
import configparser
import requests

class BaseUAGFunction():
	def __init__(self):
		Configfile = "./uagconfig.ini"
		config = self.loadConfigFile(Configfile)
		self.uagip = config.get('general', 'UAGIPList')
		self.uaghttpport = config.get('general', 'UAGHTTPPORT')
		self.getTokenResource = config.get('URLResource', 'getToken')
		self.authTokenResource = config.get('URLResource', 'autToken')
		self.appid = config.get('APPInfo', 'APPID')
		self.apppwd = config.get('APPInfo', 'APPPWD')
		self.grant_type = config.get('APPInfo', 'grant_type')


	def loadConfigFile(self,Configfile):
		fileName = Configfile
		conf = configparser.ConfigParser()
		conf.read(fileName)
		return conf

	def ConfInvite(self,Head={},body={}):
		ConfID = ''
		return ConfID

	def getToken(url, headers, data):
		errorResult = {
			'errorCode': 404,
			'message': "connect to server fail"
		}
		try:
			respond = requests.post(url=url, headers=headers, data=data, timeout=10)
			if respond.status_code == 200:
				respondResult = {
					'token': respond.json()['access_token'],
					'ResultCode': respond.json()['ResultCode']
				}
			else:
				respondResult = {
					'errorCode': respond.json()['errorCode'],
					'message': respond.json()['message']
				}
			return respondResult
		except:
			return errorResult

	def authToken(url, headers, data):
		respond = requests.post(url=url, headers=headers, data=data, timeout=10)
		if respond.status_code == 200:
			ResultCode = respond.json()['ResultCode']
			respondResult = {
				'ResultCode': ResultCode
			}
		else:
			respondResult = {
				'errorCode': respond.json()['errorCode'],
				'message': respond.json()['message']
			}
		return respondResult