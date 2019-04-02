

def main():
    import socket
    from tkinter import filedialog

    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    path = filedialog.askopenfilename()
    name = str(path).rsplit("/", 1)[1]
    name = name.encode("utf-8")
    conn.send(name)
    with open(path, 'rb') as f:
        print('read')
        l = f.read(1024)
        while l:
            conn.send(l)
            l = f.read(1024)
    print('Done sending')
    conn.close()

def backup_send(path):
    import socket
    import time
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    name = str(socket.gethostname())+"||BACKUP.txt"
    name = name.encode("utf-8")
    conn.send(name)
    print('NAME ' + str(name))
    time.sleep(2)
    with open(path, 'rb') as f:
        print('read')
        l = f.read(1024)
        while l:
            conn.send(l)
            l = f.read(1024)
    print('Done sending')
    conn.close()

def send_backup_files(path, name):
    import socket
    import time
    port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    name = name.encode("utf-8")
    try:
        name = name.split("\n")[0]
    except:
        pass
    conn.send(name)
    time.sleep(2)
    print('finished sending name')
    try:
        path = path.split("\n")[0]
    except:
        pass
    print(path)
    with open(path, 'rb') as f:
        print('read')
        l = f.read(1024)
        while l:
            conn.send(l)
            l = f.read(1024)
    print('Done sending')
    conn.close()


if __name__ == '__main__':
    print('got to here')
    main()
