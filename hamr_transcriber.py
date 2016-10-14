
#!/usr/bin/env python
"""
No more ROS as core communication.
"""
import serial
import time

class HamrTranscriber():
    def __init__(self, port=None, msg_type=None, baud_rate=57600):
        self.val_map = {'tm': 'timestamp',
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
        # MESSAGE DEFINITIONS:
        self.raw_velocity = set(['tm', 'lv', 'rv', 'tv', 'dl', 'dr', 'dt'])
        self.hamr_state = set(['cx', 'cy', 'ct', 'hx', 'hy', 'hr', 'sd'])
        if port == None:
            raise AttributeError('please define the port')
        self.ser = serial.Serial(port, baud_rate)
        if msg_type == None:
            raise AttributeError(
                'please define the message type you wish to read')
        self.msg_type = msg_type

    def _read_ser(self):
        """
        Read from serial and return raw string of data
        """
        message = {}
        self.ser.close()
        self.ser.open()
        raw_data_list = self.ser.readline().split(' ')
        for i in raw_data_list:
            line_tuple = self._parse_result(i)
            message[line_tuple[0]] = line_tuple[1]
        message_attr = getattr(self, self.msg_type)
        if set(message.keys()) != message_attr:
            message = self._read_ser()
        return message

    def read(self, msg_format='default'):
        """
        Returns the message sent from the HAMR
        default: python dictionary of {string : float} format
        """
        raw_message = self._read_ser()
        if msg_format == 'default':
            return self._default_formatting(raw_message)
        elif msg_format == 'ros':
            print 'do the ros'

    def _default_formatting(self, raw_dict):
        """
        Returns string: float format dictionary
        """
        formatted_msg = {}
        for key, val in raw_dict.iteritems():
            formatted_msg[self.val_map[key]] = float(str.strip(val))/1000.0
        return formatted_msg

    def stop_read(self):
        """
        Close serial and finish reading from the HAMR
        """
        self.ser.close()

    def _parse_result(self, line):
        """
        Returns a tuple of the key and value of a line read from the arduino
        Assumes the invariant of the first two chars representing keys
        """
        return (line[:2], line[2:])


if __name__ == '__main__':
    ht = HamrTranscriber('/dev/ttyACM0', 'hamr_state')
    while True:
        print ht.read()
        time.sleep(0.5)
    ht.stop_read()
