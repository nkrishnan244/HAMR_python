import hamr_writer as hw
import pygame
import pygame.joystick as joystick
import pygame.event as event

# Joystick Constants
X_LEFT_JOYSTICK = 0
Y_LEFT_JOYSTICK = 1
X_RIGHT_JOYSTICK = 2
Y_RIGHT_JOYSTICK = 3
writer = hw.HamrWriter(port='/dev/ttyACM0')


pygame.init()
if joystick.get_count == 0:
    raise AttributeError("No joystick recognized")

joystick.init()
joystick.Joystick(0).init()

while True:
    event_list = event.get()
    for event_obj in event_list:
        if event_obj.type == 7:
            joystick_direction = event_obj.axis
            movement_magnitude = round(event_obj.value, 2)
            if movement_magnitude != 0.0:
                if joystick_direction == X_LEFT_JOYSTICK:
                    writer.send_r(movement_magnitude)
                    print 'rotating turret, scalar: ' + str(movement_magnitude)
                elif joystick_direction == X_RIGHT_JOYSTICK:
                    writer.send_x(movement_magnitude)
                    print 'moving the hamr in the x direction, scalar: ' + str(movement_magnitude)
                elif joystick_direction == Y_RIGHT_JOYSTICK:
                    writer.send_y(movement_magnitude)
                    print 'moving the hamr in the y direction, scalar: ' + str(movement_magnitude)
        else:
            print 'Button pressed: killing motors'
            writer.kill_motors()
