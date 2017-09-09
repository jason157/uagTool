# coding=utf-8
import urllib.request
import socket

def OCSOpenAccount(numberlist):
	xmlTemplatebak='''
	<?xml version="1.0" encoding="UTF-8"?>
	<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:comm3="http://www.chinatelecom.com.cn/schema/ctcc/common/v2_1" xmlns:ns2="http://tempuri.org/ns2.xsd">
	<SOAP-ENV:Header>
	</SOAP-ENV:Header>
	<SOAP-ENV:Body>
	<ns2:QueryBindInfoRequest>
	<AuthValue>
	<UserID>zxin10</UserID>
	<PIN>zxin10</PIN>
	</AuthValue>
	<Sessionid>2017082816354229345</Sessionid>
	<Subscriber_id>86%(number)s@ims.videocall.chinamobile.com</Subscriber_id>
	<AliasAccount>sip:+86%(number)s@ims.videocall.chinamobile.com</AliasAccount>
	</ns2:QueryBindInfoRequest>
	</SOAP-ENV:Body></SOAP-ENV:Envelope>
	'''
	xmlTemplateQueryBindInfoRequest='''<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:comm3="http://www.chinatelecom.com.cn/schema/ctcc/common/v2_1" xmlns:ns2="http://tempuri.org/ns2.xsd"><SOAP-ENV:Header></SOAP-ENV:Header><SOAP-ENV:Body><ns2:QueryBindInfoRequest><AuthValue><UserID>zxin10</UserID><PIN>zxin10</PIN></AuthValue><Sessionid>2017082816354229345</Sessionid><Subscriber_id>86%(number)s@ims.videocall.chinamobile.com</Subscriber_id><AliasAccount>sip:+86%(number)s@ims.videocall.chinamobile.com</AliasAccount></ns2:QueryBindInfoRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>	'''
	#xmlTemplateCreateAccountRequest='''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns2="http://tempuri.org/ns2.xsd"><soapenv:Header/><soapenv:Body><ns2:CreateAccountRequest><AuthValue><UserID>zxin10</UserID><PIN>zxin10</PIN></AuthValue><Sessionid>20170814203820048211</Sessionid><Subscriber_id>86%(number)s@ims.videocall.chinamobile.com</Subscriber_id><AliasAccount>sip:+86%(number)s@ims.videocall.chinamobile.com</AliasAccount><UserType>1</UserType><PackageID>1001</PackageID></ns2:CreateAccountRequest></soapenv:Body></soapenv:Envelope>'''
	xmlTemplateCreateAccountRequest = '''<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:comm3="http://www.chinatelecom.com.cn/schema/ctcc/common/v2_1" xmlns:ns2="http://tempuri.org/ns2.xsd"><SOAP-ENV:Header></SOAP-ENV:Header><SOAP-ENV:Body><ns2:CreateAccountRequest><AuthValue><UserID>zxin10</UserID><PIN>zxin10</PIN></AuthValue><Sessionid>2017082411270302594</Sessionid><Subscriber_id>+86%(number)s@ims.videocall.chinamobile.com</Subscriber_id><AliasAccount>sip:+86%(number)s@ims.videocall.chinamobile.com</AliasAccount><UserType>0</UserType><Limittype>0</Limittype></ns2:CreateAccountRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'''
	#xmlRequest=(xmlTemplate % dict(number="14715008384"))
	ocsurl = "http://192.168.102.220:6000"
	OCSheader = {
		'Content-Type': "text/xml",
		'Cache-Control': "no-cache",
		'Pragma': "no-cache",
		'User-Agent': "Java/1.6.0_43",
		'Accept': "text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2"
	}
	# testurl="http://120.197.90.38:9080"
	timeout=3
	socket.setdefaulttimeout(timeout)
	xmlCreateAccountRequest = (xmlTemplateCreateAccountRequest % dict(number=numberlist))
	#print(xmlRequest)
	request=urllib.request.Request(ocsurl,headers=OCSheader,data=xmlCreateAccountRequest.encode('UTF-8'),method="POST")
	try:
		requestResult=urllib.request.urlopen(request)
		return requestResult.getcode()
		#print(requestResult)
	except urllib.error.URLError as e:
		return 404
		#print ("异常信息：")
		#print (e)

	#print (xmlRequest % dict(number="14715008384"))
