import sys
import time
import socket
import os

global can_connect
can_connect = False


def main(port, host):
    global can_connect
    s = socket.socket()
    port = int(port)+2

    print('GET STARTED')
    print('PORT: {}'.format(port))

    try:
        s.connect((host, port))
        print('started receiver')
    except Exception as e:
        print('Started twice... exiting')
        print(e)
        sys.exit()
    name = s.recv(1024)
    with open(name, 'wb') as f:
        print('receiving data...')
        while True:

            data = s.recv(1024)
            if not data:
                break

            # write data to a file
            f.write(data)

    f.close()
    print('Successfully got the file')
    s.close()
    print('connection closed')
    can_connect = False


def GETFILES(IP_TO_SEND, port):
    global can_connect
    s = socket.socket()

    host = IP_TO_SEND  # Ip address that the TCPServer  is there
    # Reserve a port for your service every new transfer wants a new port or you must wait.
    port = port + 2

    print('CONNECTING TO ' + host + " " + str(port))

    s.connect((host, port))
    print('started reciever')

    try:
        pass
    except:
        print('Started twice... exiting')
        sys.exit()
    name = s.recv(1024)
    name = name.decode("utf-8")
    with open(os.path.join('Resources', name), 'wb') as f:
        print('receiving data...')
        while True:

            data = s.recv(1024)
            if not data:
                break
            f.write(data)

    f.close()
    print('Successfully got the file')
    s.close()
    print('connection closed')
    can_connect = False
