#!/usr/bin/env python
"""
The main Python suite for HAMR communcation. Includes read/write capabilities.
"""
import serial
import time
import struct

class HamrInterpreter():
    def __init__(self, port=None, msg_type=None, baud_rate=57600):
        # Dictionary of values that makes the message sent from the Arduino readable.
        self.msg_translation_map = {'tm': 'timestamp',
            'lv': 'left_motor_velocity',
            'rv': 'right_motor_velocity',
            'tv': 'turret_motor_velocity',
            'dl': 'desired_left_velocity',
            'dr': 'desired_right_velocity',
            'dt': 'desired_turret_velocity',
            'cx': 'computed_xdot',
            'cy': 'computed_ydot',
            'ct': 'computed_tdot',
            'hx': 'set_xdot',
            'hy': 'set_ydot',
            'hr': 'set_rdot',
            'sd': 'sensed_drive_angle'
        }

        # A dictionary of all the values delineated by the switch function in
        # the embedded arduino code.
	self.val_map = {
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
            'SIG_HOLO_R_KD': 'O',
            # Requesting Message
            'MSG_REQUEST': 'M'
        }
        # MESSAGE DEFINITIONS:
        self.raw_velocity = set(['tm', 'lv', 'rv', 'tv', 'dl', 'dr', 'dt'])
        self.hamr_state = set(['cx', 'cy', 'ct', 'hx', 'hy', 'hr', 'sd'])

        if msg_type == None:
            raise AttributeError(
                'please define the message type you wish to read')
        self.msg_type = msg_type

        if port == None:
            raise AttributeError('please define the port')
        self.ser = serial.Serial(port, baud_rate)

    #### Reading Methods ####
    def read(self, msg_format='default'):
        """
        Returns the message sent from the HAMR
        default: python dictionary of {string : float} format
        """
        raw_message = self._read_ser()
        if msg_format == 'default':
            return self._default_formatting(raw_message)
            print 'serial read.'
        elif msg_format == 'ros':
            print 'ROS not implemented yet.'

    def stop_com(self):
        """
        Close serial and finish reading from the HAMR
        """
        self.ser.close()


    #### Writing Methods ####
    # Holonomic control commands
    def send_x(self, value=0.0):
        self._send_command('SIG_HOLO_X', value)

    def send_y(self, value=0.0):
        self._send_command('SIG_HOLO_Y', value)

    def send_r(self, value=0.0):
        self._send_command('SIG_HOLO_R', value)

    def kill_motors(self):
        self.send_x()
        self.send_y()
        self.send_r()

    #### Helper Methods ####
    # Reading
    def _read_ser(self):
        """
        Read from serial and return raw string of data
        """
        message = {}
        if not self.ser.isOpen():
            self.ser.open()
        raw_data = self.ser.readline()
        raw_data_list = raw_data.split(' ')
        for i in raw_data_list:
            line_tuple = self._parse_result(i)
            message[line_tuple[0]] = line_tuple[1]
        message_attr = getattr(self, self.msg_type)
        if set(message.keys()) != message_attr:
            print raw_data # print if doesn't match message
            message = self._read_ser()
        return message

    def _parse_result(self, line):
        """
        Returns a tuple of the key and value of a line read from the arduino
        Assumes the invariant of the first two chars representing keys
        """
        return (line[:2], line[2:])

    def _default_formatting(self, raw_dict):
        """
        Returns {string: float} format dictionary
        """
        formatted_msg = {}
        for key, val in raw_dict.iteritems():
            formatted_msg[self.msg_translation_map[key]] = float(str.strip(val))/1000.0
        return formatted_msg

    # Writing
    def _convert_float_to_byte_array(self, value):
        return bytearray(struct.pack('f', value))

    def _send_command(self, cmd_type, value):
        if not self.ser.isOpen():
            self.ser.open()
        print self.val_map[cmd_type]
        self.ser.write(self.val_map[cmd_type])
        val = str(self._convert_float_to_byte_array(value))
        self.ser.write(val)
