import socket
from tkinter import filedialog
import time


def error_log(error):
    with open("Resources\\ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")

def main():
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

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


def backup_send(path):
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

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


def send_backup_files(path, name):
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

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


if __name__ == '__main__':
    main()
