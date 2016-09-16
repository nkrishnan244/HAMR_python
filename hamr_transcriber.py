import serial

#!/usr/bin/env python
"""
No more ROS as core communication.
"""

class HamrTranscriber():
    def __init__(self, port=None):
        self.val_map = {'tm': 'timestamp',
            'lv': 'left_motor_velocity',
            'rv': 'right_motor_velocity',
            'tv': 'turret_motor_velocity',
            'dl': 'desired_left_velocity',
            'dr': 'desired_right_velocity',
            'dt': 'desired_turret_velocity'
        }
        # MESSAGE DEFINITIONS:
        # velocity_message: contains the timestamp, velocities and desired
        # velocities of the HAMR. 
        if port == None:
            raise AttributeError('please define the port')
        self.ser = serial.Serial(port, 57600)

    def _read(self):
        """
        Returns the message sent from the HAMR in the form of a dictionary
        Values are raw strings.
        """
        message = {}
        self.ser.close()
        self.ser.open() # do something about this later.
        raw_string = self.ser.readline()
        self.ser.close() # instead of handling it like this
        raw_data_list = raw_string.split(' ')
        for i in raw_data_list:
            line_tuple = self._parse_result(i)
            message[line_tuple[0]] = line_tuple[1]
        return message

    def _parse_result(self, line):
        """
        Returns a tuple of the key and value of a line read from the arduino
        Assumes the invariant of the first two chars representing keys
        """
        return (line[:2], line[2:])

    def jsonify(self):
        print "Not yet implemented"



"""
We'd want to export this in several ways: 

default python hash
json object
ROS message
"""

if __name__ == '__main__':
    ht = HamrTranscriber('/dev/ttyACM0')
    while True:
        print ht._read()