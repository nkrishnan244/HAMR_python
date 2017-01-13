"""
This is the working python interface for wifi communication for the HAMR (as of 11/14/2016)
If not working- be sure to check the ip address of the HAMR and make sure it matches with
the first value in the address tuple.
Also be sure that the second int for the tuple (the local port) matches up.
Also be sure that the message type is the same.
"""
import socket
import struct

SERVER_IP = '192.168.1.1'
SERVER_PORT = 2390
address = (SERVER_IP, SERVER_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP

# arbitrarily set message_type as 103
messages = {
        'holo_drive': (103, 'fff'),
        'dif_drive': (104, 'fff')
}


def message_generator(message_type, data=[]):
    msg_type = messages[message_type][0]
    msg_format = messages[message_type][1]
    msg = chr(msg_type)
    if (len(data) != len(msg_format)):
        raise ValueError('You have provided insufficient data for a message')
    msg += struct.pack("<" + msg_format, *data)
    return msg

def send_message(message):
    for _ in range(0, 2):
        sock.sendto(message, address)

while True:
    msg_typ = raw_input('What message do you want to send? Holonomic (h) or Dif Drive (d)?\n')
    print 'What values?'
    answer = raw_input("")
    data = answer.split(" ")
    converted_data = []
    for i in data:
        print float(i)
        converted_data.append(float(i))
    if msg_typ == 'h':
        print 'sending holo message'
        send_message(message_generator('holo_drive', converted_data))
    else:
        print 'sending dif drive message'
        send_message(message_generator('dif_drive', converted_data))
