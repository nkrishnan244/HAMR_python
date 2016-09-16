import serial

#!/usr/bin/env python
"""
No more ROS as core communication.
"""

class HamrTranscriber():
    def __init__(self):
    	self.val_map = {
    		'tm': 'timestamp'
    		'lv': 'left_motor_velocity',
    		'rv': 'right_motor_velocity',
    		'tv': 'turret_motor_velocity',
    		'dl': 'desired_left_velocity',
    		'dr': 'desired_right_velocity',
    		'dt': 'desired_turret_velocity'
    	} 

    def read(self):
    	print "Not yet implemented"

    def jsonify(self):
    	print "Not yet implemented"



"""
We'd want to export this in several ways: 

default python hash
json object
ROS message
"""