#! /usr/bin/env python
"""
A CLI controller for the HAMR.
"""

import hamr_writer

hr = hamr_writer.HamrWriter(port=1)

try:
    while True:
        print 'Would you like to send the HAMR in the x, y, or r direction?'
        direction = raw_input('')
        if direction not in ['x', 'y', 'r']:
            print "That's not a valid direction."
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
                    hr.send_x(val)
                elif direction == 'y':
                    hr.send_y(val)
                elif direction == 'r':
                    hr.send_r(val)
                print 'Sent ' + str(val) + ' to ' + direction
            except ValueError:
                print 'That is not a number'
except KeyboardInterrupt:
    print 'end'
