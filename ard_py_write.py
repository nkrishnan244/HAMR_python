#! /usr/bin/env python
import serial
import struct

ser = serial.Serial('/dev/ttyACM1', 57600)
ser.close()
ser.open()
while True:
    try:
        val = raw_input('go or stop')
        if val == 'go':
            ser.write('y')
            ba = bytearray(struct.pack('f', 0.2348))
            ser.write(str(ba))
        else:
            ser.write('y')
            ba = bytearray(struct.pack('f', 0.0))
            ser.write(str(ba))
    except KeyboardInterrupt:
        ser.close()
        print 'serial connection closed'
        break




