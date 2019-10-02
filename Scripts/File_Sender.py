import socket
from tkinter import filedialog
import time


def error_log(error):
    with open("Resources/ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


# Reserve a port for your service every new transfer wants a new port or you must wait.
def main(client, port):
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.
    print('PORT: {}'.format(port))
    print('Server listening....')
    client.send('--SENDING_FILE--'.encode('utf-8'))

    conn, address = s.accept()  # Establish connection with client.
    print('Got connection from', address)
    path = filedialog.askopenfilename()
    name = str(path).rsplit("/", 1)[1]
    name = name.encode("utf-8")
    conn.send(name)
    with open(path, 'rb') as f:
        print('read')
        file = f.read(1024)
        while file:
            conn.send(file)
            file = f.read(1024)
    print('Done sending')
    conn.close()


def backup_send(client, port, path):
    # Reserve a port for your service every new transfer wants a new port or you must wait.
    port = port
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')
    print('USING PORT' + str(port))
    client.send('--BACKUP--'.encode('utf-8'))
    conn, address = s.accept()  # Establish connection with client.
    print('Got connection from', address)
    name = str(socket.gethostname())+"||BACKUP.txt"
    name = name.encode("utf-8")
    conn.send(name)
    print('NAME ' + str(name))
    time.sleep(2)
    with open(path, 'rb') as f:
        print('read')
        file = f.read(1024)
        while file:
            conn.send(file)
            file = f.read(1024)
    print('Done sending')
    conn.close()


def send_backup_files(client, port, path, name):
    # Reserve a port for your service every new transfer wants a new port or you must wait.
    port = port
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print(client)
    client.send((('--SENDING_BACKUP_FILES--') +
                 str(socket.gethostname())).encode('utf-8'))

    print('Server listening....')

    conn, address = s.accept()  # Establish connection with client.
    print('Got connection from', address)
    name = name.encode("utf-8")
    # print(name)
    # try:
    #     name = name.split("\n")[0]
    # except Exception as error:
    #     error_log(error)
    #     pass
    conn.send(name)
    time.sleep(2)
    print('finished sending name')
    try:
        path = path.split("\n")[0]
    except Exception as e:
        print(e)
        pass
    print(path)
    with open(path, 'rb') as f:
        print('read')
        file = f.read(1024)
        while file:
            conn.send(file)
            file = f.read(1024)
    print('Done sending')
    conn.close()


def get_ip_from_sock(sock):
    sock = str(sock).rsplit("raddr=('", 1)[1]
    sock = str(sock).rsplit("',", 1)[0]
    return sock
