#! /usr/bin/env python
"""
A higher level interface for sending holonomic movement commands to the HAMR.
"""
import serial
import struct

class HamrWriter():
    def __init__(self, port=None, baud_rate=57600):
        self.val_map = {
            # A dictionary of all the values delineated by the switch function in
            # the embedded arduino code.

            # holonomic inputs
            'SIG_UNINITIALIZED': '!',
            'SIG_HOLO_X': 'x',
            'SIG_HOLO_Y': 'y',
            'SIG_HOLO_R': 'a',
            # differential drive inputs
            'SIG_DD_V': 'd',
            'SIG_DD_R': 'D',
            # Motor Velocities
            'SIG_R_MOTOR': 'r',
            'SIG_L_MOTOR': 'l',
            'SIG_T_MOTOR': 't',
            # right motor PID
            'SIG_R_KP': '1',
            'SIG_R_KI': '2',
            'SIG_R_KD': '3',
            # left motor PID
            'SIG_L_KP': '4',
            'SIG_L_KI': '5',
            'SIG_L_KD': '6',
            # turret motor PID
            'SIG_T_KP': '7',
            'SIG_T_KI': '8',
            'SIG_T_KD': '9',
            # holonomic x PID
            'SIG_HOLO_X_KP': 'Q',
            'SIG_HOLO_X_KI': 'W',
            'SIG_HOLO_X_KD': 'E',
            # holonomic Y PID
            'SIG_HOLO_Y_KP': 'R',
            'SIG_HOLO_Y_KI': 'T',
            'SIG_HOLO_Y_KD': 'Y',
            # holonomic R PID
            'SIG_HOLO_R_KP': 'U',
            'SIG_HOLO_R_KI': 'I',
            'SIG_HOLO_R_KD': 'O'
        }

	if port == None:
            raise AttributeError('please define the port')
        self.ser = serial.Serial(port, baud_rate)

    # Holonomic control commands
    def send_x(self, value=0.0):
        self.send_command('SIG_HOLO_X', value)

    def send_y(self, value=0.0):
        self.send_command('SIG_HOLO_Y', value)

    def send_r(self, value=0.0):
        self.send_command('SIG_HOLO_R', value)

    def kill_motors(self):
        self.send_x()
        self.send_y()
        self.send_r()

    # Helper Methods
    def convert_float_to_byte_array(self, value):
        return bytearray(struct.pack('f', value))

    def send_command(self, cmd_type, value):
        self.ser.close()
        self.ser.open()
        self.ser.write(cmd_type)
        self.ser.write(convert_float_to_byte_array(value))
        self.ser.close()

    def sup(self):
        print 'sup'
