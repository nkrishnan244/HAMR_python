#! /usr/bin/env python
import serial
import struct

class HamrWriter():
    def __init__(self, port=None, baud_rate=57600):
        if port == None:
            raise AttributeError('please define the port')
        self.ser = serial.Serial(port, baud_rate)

    def convert_float_to_byte_array(value):
        return bytearray(struct.pack('f', value))

    def send_command(cmd_type, value):
        self.ser.close()
        self.ser.open()
        self.ser.write(cmd_type)
        self.ser.write(convert_float_to_byte_array(value))
        self.ser.close()

