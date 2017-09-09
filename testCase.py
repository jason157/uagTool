# coding=utf-8
#import BaseUAGFunction
import tkinter as tk
import configparser
import requests
import json

class HighlightLinesInTextDemo(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.text = tk.Text(self)
		self.text.pack(side="top", fill="both", expand=True)
		self.text.tag_configure("current_line", background="gray")
		self.text.bind("<Motion>", self._highlightline)

	def _highlightline(self, event=None):
		self.text.tag_remove("current_line", 1.0, "end")
		self.text.tag_add("current_line", "current linestart", "current lineend+1c")
def loadConfigFile():
	fileName = "./uagconfig.ini"
	conf = configparser.ConfigParser()
	conf.read(fileName)
	sections = conf.sections() #获取所有的section
	general = conf.items(sections[0]) #获取到section的所有选项，放入字典
	APPInfo = conf.items(sections[1])
	UAGIPList = conf.get('general','UAGIPList') # 获取配置中的具体值
	UAGHTTPPORT =conf.get('general','UAGHTTPPORT')
	UAGHTTPSPORT =conf.get('general','UAGHTTPSPORT')
	return conf

def fenci():
	import jieba
	from wordcloud import WordCloud
	import matplotlib.pyplot as plt

	# 加载自定义分词字典
	jieba.load_userdict("Confdict.txt")

	# 语料
	# corpos = "美媒称，鉴于全球石油市场过度供给的情况，中国原油需求下滑是其首要担忧之一。过量生产拉低了石油价格，但是中国过去一年左右的疲弱需求引发了缓慢的回弹。"
	corpos = open("E:\Py35_workspace\LogAnalisis\InData\Conf.log", 'r').read()
	seg_list = jieba.cut(corpos)
	seg_list2 = jieba.cut(corpos)
	text = " ".join(seg_list)

	# 词频统计
	segStat = {}
	for seg in seg_list2:
		if seg in segStat:
			segStat[seg] += 1
		else:
			segStat[seg] = 1
	# print(segStat)
	with open('segStat.txt', 'w') as f:
		for item in segStat:
			if item.isalpha() and len(item)>1:
				f.write(item)
				f.write("\n")
	f.close()

	# 创建词云
	wordcloud = WordCloud(font_path='C:\\Windows\\Fonts\\FZYTK.TTF',  # 设置字体
	               background_color="black",  # 背景颜色
	               max_words=2000,  # 词云显示的最大词数
	               max_font_size=100,  # 字体最大值
	               random_state=42,
	               )
	wordcloud.generate(text)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

def getToken(url, headers, data):
	errorResult = {
		'errorCode': 404,
		'message':  "connect to server fail"
	}
	try:
		respond = requests.post(url=url, headers=headers, data=data, timeout = 10)
		if respond.status_code == 200:
			respondResult = {
				'token': respond.json()['access_token'],
				'ResultCode':  respond.json()['ResultCode']
			}
		else:
			respondResult = {
				'errorCode': respond.json()['errorCode'],
				'message':  respond.json()['message']
			}
		return respondResult
	except:
		return errorResult

def authToken(url, headers, data):
	respond = requests.post(url=url, headers=headers, data=data, timeout = 10)
	if respond.status_code == 200:
		ResultCode = respond.json()['ResultCode']
		respondResult = {
			'ResultCode': ResultCode
		}
	else:
		respondResult = {
			'errorCode': respond.json()['errorCode'],
			'message':  respond.json()['message']
		}
	return respondResult





config = loadConfigFile()
uagip = config.get('general','UAGIPList')
uaghttpport = config.get('general','UAGHTTPPORT')
getTokenResource = config.get('URLResource','getToken')
authTokenResource = config.get('URLResource','autToken')
appid = config.get('APPInfo','APPID')
apppwd = config.get('APPInfo','APPPWD')
grant_type = config.get('APPInfo','grant_type')

getTokenUrl = "http://" + uagip + ":" + uaghttpport + getTokenResource
authTokenUrl = "http://" + uagip + ":" + uaghttpport + authTokenResource

getTokenData = {
	"app_password": apppwd,
	"grant_type": grant_type,
	"app_id": appid
}
authTokenData = {
	"app_id":appid,
	"access_token":"MjAxNzA5MDExNjIyMjI1OStBY2NUb2tlbitac2tERGVxdEx6OGtLUGtlR3VmRA=="
}

headers = {

}


respond = getToken(url=getTokenUrl,headers=headers,data=json.dumps(getTokenData))
print('Token获取结果：'+ str(respond))
if 'token' in respond:
	token = respond['token']
	authTokenData = {
		"app_id": appid,
		"access_token":token
	}
	authResult = authToken(url=authTokenUrl, headers=headers, data=json.dumps(authTokenData))
	print('Token认证结果：' + str(authResult))