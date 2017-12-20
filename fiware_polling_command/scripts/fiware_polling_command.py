#!/usr/bin/env python


import time
import requests
import json
import rospy
from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg import PoseStamped

def fiware_polling(): 
	pub = rospy.Publisher('/husky_fiware/move_base_simple/goal', PoseStamped, queue_size=10)
	rospy.init_node('fiware_polling_goal', anonymous=True)
	rate = rospy.Rate(1) #1hz
	while not rospy.is_shutdown():
		
		headers = {
		    'Accept': 'application/json',
		}

		r = requests.get('http://217.172.12.142:1026/v2/entities/Husky_fiware_command', headers=headers)
		print r.text
		j = json.loads(r.text)
		print j['command']['value']
		print j['command']['type']
		if ("PoseStamped" in j['command']['type']):
			try:
				msg = PoseStamped()
				msg.header.frame_id = j['command']['value']['header']['frame_id']
				msg.pose.position.x = j['command']['value']['pose']['position']['x']
				msg.pose.position.y = j['command']['value']['pose']['position']['y']
				msg.pose.position.z = j['command']['value']['pose']['position']['z']
				msg.pose.orientation.x = j['command']['value']['pose']['orientation']['x']
				msg.pose.orientation.y = j['command']['value']['pose']['orientation']['y']
				msg.pose.orientation.z = j['command']['value']['pose']['orientation']['z']
				msg.pose.orientation.w = j['command']['value']['pose']['orientation']['w']
				print msg
				pub.publish(msg)
				rate.sleep()
			except TypeError:
				pass

			time.sleep(1)
	
			headers = {
			    'Content-Type': 'application/json',
			}

			data = '{"command": {"value": "none","type": "String"}}'

			r = requests.patch('http://217.172.12.142:1026/v2/entities/Husky_fiware_command/attrs', headers=headers, data=data)
			print r.text

	


if __name__ == '__main__':
    try:
        fiware_polling()
    except rospy.ROSInterruptException:
        pass
