import pygame
import pygame.joystick as joystick
import pygame.event as event

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
                print 'motors should be killed'
            elif (event.button == self.button_ids['TOGGLE_MODE']):
                self.holonomic_mode = not self.holonomic_mode
                if (self.holonomic_mode):
                    print 'Toggling Holonomic Mode.'
                else:
                    print 'Toggling DifDrive Mode.'
            elif (not self.holonomic_mode):
                self.handle_dif_drive_button_event(event)
        elif (event.type == self.event_types['BUTTON_UP']):
            if (event.button == self.button_ids['LEFT_TRIGGER']) or (event.button == self.button_ids['RIGHT_TRIGGER']):
                print 'stopping the turret'


    def handle_holonomic_joystick_event(self, axis, value):
        if (axis == self.joystick_axes['X_LEFT']):
            print 'send turret cmd'
        elif (axis == self.joystick_axes['X_RIGHT']):
            print 'send hamr to x'
        elif (axis == self.joystick_axes['Y_RIGHT']):
            print 'send hamr to y'

    def handle_dif_drive_joystick_event(self, axis, value):
        if (axis == self.joystick_axes['Y_LEFT']):
            print 'move left wheel'
        elif (axis == self.joystick_axes['Y_RIGHT']):
            print 'move right wheel'

    def handle_dif_drive_button_event(self, event):
        if (event.button == self.button_ids['INCREASE_SCALAR']):
            print 'increase the rate at which the motor moves'
        elif (event.button == self.button_ids['DECREASE_SCALAR']):
            print 'decrease the rate at which the motor moves'
        elif (event.button == self.button_ids['LEFT_TRIGGER']):
            print 'move the turret left'
        elif (event.button == self.button_ids['RIGHT_TRIGGER']):
            print 'move the turret right'

if __name__ == '__main__':
    jc = JoystickController()
    while True:
        event_list = event.get()
        for event_obj in event_list:
            jc.handle_event(event_obj)

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
