import sys
import time
import socket


def main(IP_TO_SEND):
    s = socket.socket()

    host = IP_TO_SEND  # Ip address that the TCPServer  is there
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

    try:
        s.connect((host, port))
        print('started reciever')
    except:
        print('Started twice... exiting')
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


def GETFILES(IP_TO_SEND):
    s = socket.socket()

    host = IP_TO_SEND  # Ip address that the TCPServer  is there
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

    s.connect((host, port))
    print('started reciever')

    try:
        pass
    except:
        print('Started twice... exiting')
        sys.exit()
    name = s.recv(1024)
    name = name.decode("utf-8")
    with open("Resources\\" + name, 'wb') as f:
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
