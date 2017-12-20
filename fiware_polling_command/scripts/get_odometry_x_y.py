#!/usr/bin/env python


import time
import requests
import json
	
headers = {
	'Accept': 'application/json',
	}

r = requests.get('http://217.172.12.142:1026/v2/entities/husky_fiware', headers=headers)
j = json.loads(r.text)
odom_value = j['odometry/filtered']['value']
odom_value =  odom_value.replace('%27', '"')
odom_value = json.loads(odom_value)
print "x:", odom_value["pose"]["pose"]["position"]["x"]
print "y:", odom_value["pose"]["pose"]["position"]["y"]
