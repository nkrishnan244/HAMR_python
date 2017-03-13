import pygame
import pygame.joystick as joystick
import pygame.event as event
import hamr_messenger as hm
from time import time as now

class JoystickController:
    """Object that handles joystick events.

    It is important to note that this joystick uses a very particular kind of joystick.
    Usage Instructions:
        The Joystick Controller starts in holonomic mode.
        You can toggle between modes by pressing button 9.
        In holonomic mode:
            Use left joystick to orient the turret
            Use right joystick to move the turret.
        In Dif Drive mode:
            Use left joystick to move left motor.
            Use right joystick to move right motor.
            Use the left/right trigger buttons to move the turret.
            Use buttons 1 and 4 to decrease/increase the speed at which the turret moves, respectively.

        It's important to note that you have total control of the speed of the motors in holonomic mode, but
        have to manually adjust the speed at which the turret moves in dif drive mode.

    Attributes:
        event_types: A dictionary that enumerates events that are handled.
        joystick_axes: A dictionary that translates axes of the joystick to their number representations.
        button_ids: A dictionary that translates button functionality to their number representations.
        holonomic_mode: A boolean that determines whether holonomic drive is being used. If false, dif drive is being used.
        delta_turret: A float that dictates rate at which turret_scalar should be change per button press.
        turret_scalar: A float that dictates the rate at which the turret should move.
        velocity_scalar: A float that is multiplied to the raw readings to lower the values to something more reasonable.
        velocity_vector: An array of floats that stores the values to be sent- either X, Y, R for holonomic or right, left, turret for DD.
    """
    def __init__(self):
        self.event_types = {
            'BUTTON_DOWN': 10,
            'BUTTON_UP': 11,
            'JOY_AXIS_MOTION': 7
        }
        self.joystick_axes = {
            'X_LEFT': 0,
            'Y_LEFT': 1,
            'X_RIGHT': 2,
            'Y_RIGHT': 3
        }
        self.button_ids = {
            'DECREASE_SCALAR': 0,
            'INCREASE_SCALAR': 3,
            'LEFT_TRIGGER': 6,
            'RIGHT_TRIGGER': 7,
            'TOGGLE_MODE': 8,
            'KILL_MOTORS': 9
        }
        self.holonomic_mode = True
        self.delta_turret = 5.0
        self.turret_scalar = 5.0
        self.velocity_scalar = 0.5
        self.messenger = hm.HamrMessenger()
        self.velocity_vector = [0.0, 0.0, 0.0]
	self.last_time      = 0.0
	self.loop_dur 	    = 0.1
        pygame.init()
        if (joystick.get_count) == 0:
            raise AttributeError('No joystick recognized')
        joystick.init()
        joystick.Joystick(0).init()

    def handle_event(self, event):
        if (event.type == self.event_types['JOY_AXIS_MOTION']):
            direction = event_obj.axis
            magnitude = round(event_obj.value, 2)
            if (self.holonomic_mode):
                self.handle_holonomic_joystick_event(direction, magnitude)
            else:
                self.handle_dif_drive_joystick_event(direction, magnitude)
        elif (event.type == self.event_types['BUTTON_DOWN']):
            if (event.button == self.button_ids['KILL_MOTORS']):
                print 'Killing Motors.'
                self.velocity_vector = [0.0, 0.0, 0.0]
                self.messenger.kill_motors()
            elif (event.button == self.button_ids['TOGGLE_MODE']):
                self.holonomic_mode = not self.holonomic_mode
                self.velocity_vector = [0.0, 0.0, 0.0]
                self.messenger.kill_motors()
                if (self.holonomic_mode):
                    print 'Toggling Holonomic Mode.'
                else:
                    print 'Toggling DifDrive Mode.'
            elif (not self.holonomic_mode):
                self.handle_dif_drive_button_event(event)
        elif (event.type == self.event_types['BUTTON_UP']):
            if (event.button == self.button_ids['LEFT_TRIGGER']) or (event.button == self.button_ids['RIGHT_TRIGGER']):
                self.velocity_vector[2] = 0.0
                self._send_dif_drive_message()

    def handle_holonomic_joystick_event(self, axis, value):
        if (axis == self.joystick_axes['X_LEFT']):
            self.velocity_vector[2] = value
        elif (axis == self.joystick_axes['X_RIGHT']):
            self.velocity_vector[0] = value
        elif (axis == self.joystick_axes['Y_RIGHT']):
            self.velocity_vector[1] = -1*value
	print 'Sending: ' + str(self.velocity_vector[0]) +', '+str(self.velocity_vector[1]) +', '+str(self.velocity_vector[2])
        self._send_holo_message()

    def handle_dif_drive_joystick_event(self, axis, value):
        if (axis == self.joystick_axes['Y_LEFT']):
            self.velocity_vector[1] = value
        elif (axis == self.joystick_axes['Y_RIGHT']):
            self.velocity_vector[0] = value
        self._send_dif_drive_message()

    def handle_dif_drive_button_event(self, event):
        if (event.button == self.button_ids['INCREASE_SCALAR']):
            self.turret_scalar += self.delta_turret
            print 'The turret will now move at ' + str(self.turret_scalar) + ' deg/s.'
        elif (event.button == self.button_ids['DECREASE_SCALAR']):
            if (self.turret_scalar > 0):
                self.turret_scalar -= self.delta_turret
                print 'The turret will now move at ' + str(self.turret_scalar) + ' deg/s.'
        elif (event.button == self.button_ids['LEFT_TRIGGER']):
            self.velocity_vector[2] = 1 * self.turret_scalar
            self._send_dif_drive_message()
        elif (event.button == self.button_ids['RIGHT_TRIGGER']):
            self.velocity_vector[2] = -1 * self.turret_scalar
            self._send_dif_drive_message()

    def _send_dif_drive_message(self):
        self.velocity_vector[0] = self.velocity_vector[0] * self.velocity_scalar
        self.velocity_vector[1] = self.velocity_vector[1] * self.velocity_scalar
        self.messenger.send_dif_drive_command(self.velocity_vector[0], self.velocity_vector[1], self.velocity_vector[2])

    def _send_holo_message(self):
        self.messenger.send_holonomic_command(self.velocity_vector[0], self.velocity_vector[1], self.velocity_vector[2])

if __name__ == '__main__':
    jc = JoystickController()
    last_time = 0
    loop_dur  = 0.1
    while True:
	if now()-last_time>loop_dur:
		print (now()-last_time)		
		last_time = now()
		event_list = event.get()
		for event_obj in event_list:
		    jc.handle_event(event_obj)

