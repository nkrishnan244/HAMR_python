import pygame 
import time
import pygame.joystick as joystick
import pygame.event as event 
import hamr_messenger as hm
from time import time as now
import pdb

class nikhil_joystick:
	'HI'

	def __init__(self):
		self.event_types = {
      			'BUTTON_DOWN': 10,
       			'BUTTON_UP': 11,
       			'JOY_AXIS_MOTION': 7
		}

		self.button_names = {
			'ONE': 0,
			'TWO': 1,
			'THREE': 2,
			'FOUR': 3,
			'FIVE': 4,
			'SIX': 5,
			'SEVEN': 6,
			'EIGHT': 7,
			'NINE': 8,
			'TEN': 9,
		}
	
		self.joystick_axes = {
        		'X_LEFT': 0,
        		'Y_LEFT': 1,
        		'X_RIGHT': 2,
        		'Y_RIGHT': 3
		} 
		self.right_value = 0
		self.left_value = 0
		self.velocity_vector = [0.0, 0.0, 0.0]
		self.sensitivity_constant = 0.5
		self.messenger = hm.HamrMessenger()
	
	def handle_event(self, event):
		if (event.type == self.event_types['BUTTON_DOWN']):
			print event.button
		if (event.type == self.event_types['JOY_AXIS_MOTION']):
			if (event.axis == self.joystick_axes['Y_RIGHT']):
				self.right_value = event.value 
				if (abs(self.right_value) < 0.05):
					self.right_value = 0
				if (self.right_value) < 0:
					self.right_value = self.right_value
				if (self.right_value) > 0:
					self.right_value = self.right_value
		if (event.type == self.event_types['JOY_AXIS_MOTION']):
			if (event.axis == self.joystick_axes['Y_LEFT']):
				self.left_value = event.value
				if (abs(self.left_value) < 0.05):
					self.left_value = 0
			self.velocity_vector[0] = self.left_value*-1
			self.velocity_vector[1] = self.right_value*-1			
			self._send_dif_drive_message()
		

    	def _send_dif_drive_message(self):
		self.velocity_vector[0] = self.sensitivity_constant * (self.velocity_vector[0]) ** 3 + (1 - self.sensitivity_constant) * self.velocity_vector[0]
		self.velocity_vector[1] = self.sensitivity_constant * (self.velocity_vector[1]) ** 3 + (1 - self.sensitivity_constant) * self.velocity_vector[1]
        	self.messenger.send_dif_drive_command(self.velocity_vector[0], self.velocity_vector[1], 0)
		#print (self.velocity_vector[0], self.velocity_vector[1], 0)

			
if __name__ == '__main__':  
	pygame.init() 
	joystick.init()
	joystick.Joystick(0).init()
        jc = nikhil_joystick() 
  	while True:
		event_list = event.get()
		for event_obj in event_list: 
			jc.handle_event(event_obj)

   	
