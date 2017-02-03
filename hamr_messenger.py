#! /usr/bin/env python
import socket
import struct

class HamrMessenger(object):
    """An interface that allows for motor commands to be sent to the HAMR.

    If the source code on the HAMR was not changed, custom params for initialization should not be
    necessary.

    Attributes:
        server_ip: A string that represents the IP of the access point of the HAMR.
        server_port: An integer that represents the port the HAMR is listening on.
        address: A tuple with server_ip and server_port
        sock: A socket object responsible for sending out messages
        message_types: A dictionary with the name of message associated with a tuple that contains the
                       ID of the message and format of the message.
    """

    def __init__(self, server_ip='192.168.1.1', server_port=2390):
        """Inits the HamrMessenger"""
        self.address=(server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.message_types = {
            'holo_drive': (103, 'fff'),
            'dif_drive': (104, 'fff')
        }

    def send_holonomic_command(self, x=0, y=0, r=0):
        """Sends a command to the HAMR to move in a holonomic fashion.

        Args:
            x: Float that represents the desired velocity in the x direction (m/s).
            y: Float that represents the desired velocity in the y direction (m/s).
            r: Float that represents the desired velocity of the turret (deg/s).
        """
        vector = [float(x), float(y), float(r)]
        msg = self._message_generator('holo_drive', vector)
        self._send_message(msg)

    def send_dif_drive_command(self, right=0, left=0, r=0):
        """Sends a command to the HAMR to move in its dif drive mode.

        Args:
            left: Float that represents the desired velocity of the left motor (m/s).
            right: Float that represents the desired velocity of the right motor (m/s).
            r: Float that represents the desired velocity of the turret motor (deg/s).
        """
        vector = [float(right), float(left), float(r)]
        self._send_message(self._message_generator('dif_drive', vector))

    def kill_motors(self):
        """Method that sets all desired velocities to 0."""
        for i in range(0,5):
            self.send_dif_drive_command()

    def _message_generator(self, message_type, data=[]):
        """Returns a message of the specified type containing the data given."""
        msg_type = self.message_types[message_type][0]
        msg_format = self.message_types[message_type][1]
        msg = chr(msg_type)
        if (len(data) != len(msg_format)):
            raise ValueError('You provided insufficient data for this kind of message')
        msg += struct.pack('<' + msg_format, *data)
        return msg

    def _send_message(self, message):
        for _ in range(0, 2):
            self.sock.sendto(message, self.address)
