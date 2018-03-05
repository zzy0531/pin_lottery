# coding: utf-8
from random import choice
import argparse

from flask import Flask 
from flask import request,render_template,jsonify
import requests,hashlib,json
  
app = Flask(__name__)  

# 模拟浏览器头
headers = {
	'host': "api.zhihu.com",
	'accept': "*/*",
	'x-app-za': "OS=iOS&Release=10.3.3&Model=iPhone8,2&VersionName=4.1.0&VersionCode=683&Width=1242&Height=2208&DeviceType=Phone&Brand=Apple&OperatorType=46001",
	'x-udid': "AHCAH2SzkApLBWvOUMZ7s9hG-Zh-_NhtVCM=",
	'x-app-versioncode': "683",
	'accept-language': "zh-Hans-CN;q=1, en-CN;q=0.9",
	'accept-encoding': "gzip, deflate",
	'x-api-version': "3.0.64",
	'authorization': "Bearer gt2.0AAAAAAX1feoKkLNkH4BwAAAAAAtNVQJgAgBgPzk1-59vTbuXI60W0XlSl-wNBg==",
	'x-network-type': "WiFi",
	'user-agent': "osee2unifiedRelease/4.1.0 (iPhone; iOS 10.3.3; Scale/3.00)",
	'x-app-build': "release",
	'x-app-version': "4.1.0",
	'x-suger': "SURGVj0wNDA5NjgxMS01NTI5LTRDQUQtQUEzNi1FRkI2M0VDQThDOEE7SURGQT01MDM2NDdEMy01QTlDLTRFMjItODA5NS1FRkUyM0Y5Mzg5QzM=",
	'cookie': "aliyungf_tc=AQAAAH4w9XP89AUAWgqDdYQRcynwI6xp; q_c1=97515fa2381f48a7b6ef8d46de8bc7be|1505561812000|1505561812000; z_c0=gt2.0AAAAAAX1feoKkLNkH4BwAAAAAAtNVQJgAgBgPzk1-59vTbuXI60W0XlSl-wNBg==; _xsrf=a31505e0-0f69-440b-b357-30fffc9838bd; cap_id=\"MzQ2NGE0NThiMmVjNDU3MmE5MzVhYzE0OGYyMTYzYTI=|1505561809|0c36cb283969855952e9e895b77211fd292c0df7\"; l_cap_id=\"ODE3YzMwODM5ZTE0NDdjN2IxY2UyZDdiYjQ1MGYzNDg=|1505561809|6f707b1bf6c0a0ebb6391d0c421ac06e49ceca3b\"; r_cap_id=\"ODZlYTZmNGZhYzU3NDgwOGE4YzUyOWI5OTBmMzA3NjQ=|1505561809|05c714d01ee35a0a6c96b0c330d4f10434fec8bc\"",
	'cache-control': "no-cache",
}


def get(url):
	z = requests.get(url, headers=headers, verify=True)
	return z.json()


def run(url):
	jsdata = get(url)
	info = []
	temp_list = []
	while True:
		for i in jsdata['data']:
			if i['action_type'] == 'repin':
				if i['member']['url_token'] not in temp_list:
					info.append({
						'name': i['member']['name'],
						'url_token': i['member']['url_token'],
					})
					temp_list.append('url_token')
				else:
					pass
		if not jsdata['paging']['is_end']:
			jsdata = get(jsdata['paging']['next'])
		else:
			return info
			break

@app.route('/')
def pin():  
	return render_template('lottery_fill_pin.html')

@app.route('/pin_users',methods=['POST','GET'])
def pins():
	pin_url = request.args.get('pin_url')
	pin_num = request.args.get('pin_num')
	print(pin_url,pin_num)
	pin_id = pin_url.split('/')[-1]
	result = find_lottery(pin_id,pin_num)
	return render_template('lottery_users.html', result=result , pin_id = pin_id , pin_url=pin_url)
 
def find_lottery(pin_id,pin_num):  
	baseurl = 'https://api.zhihu.com/pins/{}/actions?limit=20&offset=0'
	# pin = '892412615123402752'
	info = run(baseurl.format(pin_id))

	d = {}
	for i in range(int(pin_num)):
		t = choice(info)
		d['https://www.zhihu.com/people/'+t['url_token']] = t['name']
	
	return d
  
if __name__ == '__main__':
	app.run(host='0.0.0.0')
	# print(find_lottery(944849427853287424,2))
