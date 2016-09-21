#! /usr/bin/env python
import serial

ser = serial.Serial('/dev/ttyACM0', 57600)
ser.close()
ser.open()
while True:
    try:
        val = raw_input('go or stop')
        if val == 'go':
            ser.write('y')
            ser.write('0.1')
        else:
            ser.write('y')
            ser.write('0.0')
    except KeyboardInterrupt:
        ser.close()
        print 'serial connection closed'
        break




