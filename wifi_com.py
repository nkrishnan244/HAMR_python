import socket
import struct

MESSAGE = 'sup'
address = ('192.168.10.13', 2390)

sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP

# arbitrarily set message_type as 100
message_type = 103

def message_generator(message_type, data=[]):
    # test message takes three ints
    msg = chr(message_type)
    msg += struct.pack("<" + 'fff', *data)
    return msg

def send_message(message):
    sock.sendto(message, address)

while True:
    print 'What values?'
    answer = raw_input("")
    data = answer.split(" ")
    converted_data = []
    for i in data:
        print float(i)
        converted_data.append(float(i))

    message = message_generator(message_type, converted_data)
    send_message(message)
