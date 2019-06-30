import sys
import time
import socket



global can_connect
can_connect = False


def main(IP_TO_SEND):
    global can_connect
    s = socket.socket()

    host = IP_TO_SEND  # Ip address that the TCPServer  is there
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

    while can_connect is False:
        time.sleep(.1)

    try:
        s.connect((host, port))
        print('started reciever')
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


def GETFILES(IP_TO_SEND):
    global can_connect
    s = socket.socket()

    host = IP_TO_SEND  # Ip address that the TCPServer  is there
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

    while can_connect is False:
        time.sleep(.1)


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
    can_connect = False
