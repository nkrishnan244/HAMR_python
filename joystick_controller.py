import pygame
import pygame.joystick as joystick
import pygame.event as event

# Joystick Constants

"""
ok so thoughts:
    we'll store a state in the class that'll store whether you're in holo or difdrive mode.

    holo mode:
        left joystick: turret
        right joystick: x/y control
    difdrive:
        left joystick: left wheel
        right joystick: right wheel
        triggers: turret.
        Button 1/4 => increase the scalar at which the turret moves.
    Switch between modes:
        press button 9
    Kill it:
        press button 10
"""
class JoystickController:
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
            'TOGGLE_MODE': 9,
            'KILL_MOTORS': 10
        }
        self.holonomic_mode = True
        pygame.init()
        if (joystick.get_count) == 0:
            raise AttributeError('No joystick recognized')
        joystick.init()
        joystick.Joystick(0).init()

    def handle_event(self, event):
        if (event.type == self.event_types['JOY_AXIS_MOTION']):
            # if (self.holonomic_mode):
            #     # handle the joystick event in a holonomic fashion
            # else:
            #     # handle joystick in difdrive mode
            print 'joystick axis'
        elif (event.type == self.event_types['BUTTON_DOWN']):
            if (event.button == self.button_ids['KILL_MOTORS']):
                print 'motors should be killed'
            elif (event.button == self.button_ids['TOGGLE_MODE']):
                self.holonomic_mode = !self.holonomic_mode
                print 'mode toggled'
            elif (!self.holonomic_mode):
                if (event.button == self.button_ids['INCREASE_SCALAR']):
                    print 'increase the rate at which the motor moves'
                elif (event.button == self.button_ids['DECREASE_SCALAR']):
                    print 'decrease the rate at which the motor moves'

                # handle buttondown in holonomic fashion

while True:
    lm = JoystickController()
    event_list = event.get()
    for event_obj in event_list:
        lm.handle_event(event_obj)
        
    # for event_obj in event_list:
    #     if event_obj.type == 7:
    #         joystick_direction = event_obj.axis
    #         movement_magnitude = round(event_obj.value, 2)
    #         if movement_magnitude != 0.0:
    #             if joystick_direction == X_LEFT_JOYSTICK:
    #                 print 'Right Joystick in the x direction scalar: ' + str(movement_magnitude)
    #             elif joystick_direction == Y_LEFT_JOYSTICK:
    #                 print 'right joystick in the y direction scalar: ' + str(movement_magnitude)
    #             elif joystick_direction == X_RIGHT_JOYSTICK:
    #                 print 'moving the hamr in the x direction, scalar: ' + str(movement_magnitude)
    #             elif joystick_direction == Y_RIGHT_JOYSTICK:
    #                 print 'moving the hamr in the y direction, scalar: ' + str(movement_magnitude)
    #     else:
    #         print 'Button pressed: killing motors'
