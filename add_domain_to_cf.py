import requests
import json
import time

'''
1.每次手动输入一个域名进行解析,多个的话，会进行循环添加
2.DNS默认添加www和主域名
3.修改SSL模式为flexible
4.只使用了一个账号，介意的话可以每隔一段时间自己更换一下，不过其实无所谓
'''
################个人账号信息##################
account_id = 'fe548f61a4663ba50839112add79eea2'#URL中可以找到
email = 'xxx@gmail.com'#CF账号
api = '99d4fee5a0d0c7437e7ea854166c7f4797929'#API
vps = 'xx.xx.xx.xx'#VPS	
##############################################
while True:
	domain = input('输入你要添加的域名:')

	# 默认添加www和主域名
	names = ['www', domain]
	headers = {'X-Auth-Email' : email,
				'X-Auth-Key' : api,
				'Content-Type' : 'application/json'}
	proxies={'http':'http://127.0.0.1:1080','https':'https://127.0.0.1:1080'}
	data1 = {'name':domain,'account':{'id':account_id,'name':email},'jump_start':False}

	#'''
	#添加域名
	url1 = 'https://api.cloudflare.com/client/v4/zones'
	while True:
		try:		
			r=requests.post(url1, headers=headers, data=json.dumps(data1), proxies=proxies)
			r_result = r.json()
		except Exception as e:
			print(e)
			time.sleep(3)
		else:
			time.sleep(3)
		
			#print(r_result)
			#print(r_result['success'])
			if r_result['success'] != False:
				domain_id = r_result['result']['id']
				#print(domain_id)
			break
	if r_result['success'] == False:
		print(r_result['errors'][0]['message'])
		continue


	#添加DNS
	for name in names:
		data2 = {'type':'A',
			'name':name,
			'content':vps,
			'ttl':1,
			'priority':0,
			'proxied':True}
		url2 = 'https://api.cloudflare.com/client/v4/zones/'+domain_id+'/dns_records'
		while True:
			try:
				r = requests.post(url2,data=json.dumps(data2),headers=headers,proxies=proxies)
			except Exception as e:
				print(e)
				time.sleep(3)
			else:
				time.sleep(3)
				break
		#print(r.json()['result'])
	print('恭喜! %s 添加成功.' % domain)
	#'''
	#domain_id = '529cc89cbfea5f7f98bd4d18d80970d7'

	#修改SSL模式
	url3 = 'https://api.cloudflare.com/client/v4/zones/'+domain_id+'/settings/ssl'
	while True:
		try:
			r = requests.patch(url3,data=json.dumps({'value':'flexible'}),headers=headers,proxies=proxies)
		except:
			time.sleep(3)
		else:
			break
	#print(r.json()['result']['value'])
