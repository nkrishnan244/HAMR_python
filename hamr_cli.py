#! /usr/bin/env python
"""
A CLI controller for the HAMR.
"""

import hamr_interpreter as hi
import time

interpreter = hi.HamrInterpreter(port='/dev/ttyACM0', msg_type='hamr_state')



try:
    while True:
        print 'Would you like to send the HAMR in the x, y, or r direction? Or would you like the current state of the HAMR (msg)?'
        direction = raw_input('')
        if direction not in ['x', 'y', 'r', 'msg']:
            interpreter.kill_motors()
            print "That's not a valid command. Killing all motors"
        else:
            if direction == 'msg':
                print 'Reading...'
                print interpreter.read()
                print 'Done'
            else:
                print 'Sending hamr to ' + direction
                print 'What value?'
                try:
                    val = float(raw_input(''))
                    if val > 1.0:
                        print "That's a large value. are you sure you want to send that? y/n"
                        ans = raw_input('')
                        if ans != 'y':
                            print 'assigning value as 0.0'
                            val = 0
                    if direction == 'x':
                        interpreter.send_x(val)
                    elif direction == 'y':
                        interpreter.send_y(val)
                    elif direction == 'r':
                        interpreter.send_r(val)
                    print 'Sent ' + str(val) + ' to ' + direction
                except ValueError:
                    print 'That is not a number'

except KeyboardInterrupt:
    interpreter.kill_motors()
    print 'end'
