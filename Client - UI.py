import os
import socket
import subprocess
import time
import uuid
from Scripts import Get
from Scripts import File_Sender
from Scripts import BackupEngine
from Scripts import BackupSyncEngine
from threading import Thread
global soc

f_null = open(os.devnull, 'w')


class Network(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        subprocess.run("Resources\\Current_Network.bat")


class Starter(Thread):
    global soc

    def __init__(self, new_ip, server_ip):
        global soc
        connected = False
        self.new_ip = new_ip
        self.server_ip = server_ip
        host = ""
        Thread.__init__(self)
        print("First thread initialized. Starting connection with server")
        self.running = True

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8888
        j = True
        if self.new_ip is True:
            first_try = False
            while j is True:
                if first_try is False:
                    user_input = input('Input the IP ADDRESS presented on the server screen until one of them works\n')
                    host = user_input
                else:
                    pass
                try:
                    soc.connect((host, port))
                    os.system('cls')
                    print("Successfully connected to server")
                    message = socket.gethostname()
                    print("Client hostname -> " + message)
                    i = CheckIfNameSent(soc)
                    i.start()
                    with open("Resources\\Temporary_Files\\IP.txt", 'w') as f:
                        f.write(host)
                    j = False
                except Exception as error:
                    error_log(error)
                    os.system('cls')
                    host = input("Try the next IP ADDRESS:\n")
                    first_try = True

        else:
            host = server_ip
            print("Connecting to -> " + host)
            while connected is False:
                try:
                    soc.connect((host, port))
                    print("Successfully connected to server")
                    message = socket.gethostname()
                    print("Client hostname -> " + message)
                    if network_func() is True:
                        ssid = connected_to_network_func()
                        print("Adding -> " + ssid + " as server network")
                        with open('Resources\\Temporary_Files\\Saved_Network.txt', 'w') as f:
                            f.write(ssid)
                    else:
                        pass
                    i = CheckIfNameSent(soc)
                    i.start()
                    connected = True
                except Exception as error:
                    error_log(error)
                    pass

    def run(self):
        global soc
        while self.running:
            while True:
                user_input = input(" -> ")
                if user_input == "/send":
                    message = "--SENDING_FILE--"
                    soc.sendall(message.encode("utf8"))
                    File_Sender.main()
                elif user_input.__contains__('/send to '):
                    message = user_input.split("/send to ")[1]
                    print(message)
                    message = "--SEND_TO--" + message
                    soc.sendall(message.encode("utf-8"))
                elif user_input.__contains__('/wake '):
                    message = user_input.split('/wake ')[1]
                    message = "--WAKE--" + message
                    soc.sendall(message.encode("utf-8"))
                elif user_input == '/backup':
                    message = "--BACKUP--"
                    soc.sendall(message.encode("utf-8"))
                elif user_input == "/cls":
                    os.system('cls')
                else:
                    soc.sendall(user_input.encode("utf8"))


class Receive(Starter):
    global soc

    def __init__(self):
        global soc
        Thread.__init__(self)

    def run(self):
        global soc
        while True:
            try:
                data = soc.recv(1024).decode()
                if not str(data).__contains__("--TEST--"):
                    if data == "":
                        os._exit(1)
                        print('lost connection')
                    elif str(data) == "--SENDING_FILE--":
                        print('recieving file...')
                        s = get_ip_from_sock(soc)
                        print(s)
                        Get.main(s)
                    elif str(data).__contains__("--RM_MESSAGE--"):
                        data = data.split("--RM_MESSAGE--")[1]
                        print("RM: " + data)
                    elif str(data).__contains__("--SENDING_FILE_TO--"):
                        data = data.split("--SENDING_FILE_TO--")[1]
                        s = get_ip_from_sock(data)
                        Get.main(s)
                    elif str(data).__contains__("--CLIENT_ID--"):
                        print('got address')
                        # data = data.split("--CLIENT_ID--")[1]
                        print('starting server')
                        subprocess.call(["python.exe", "Scripts\\File_Sender.py"])
                    elif str(data).__contains__("||BACKUP||"):
                        print("running backup")
                        backup_func()
                    elif str(data).__contains__("--GETFILES--"):
                        print("Getting required files")
                        get_files(soc)
                    else:
                        print('\n' + "Receiving message from server: " + data)
                        time.sleep(.1)
            except Exception as e:
                print('server closed')
                print(str(e))
                if os.path.isfile("Resources\\Temporary_Files\\tmp.txt"):
                    os.remove("Resources\\Temporary_Files\\tmp.txt")
                else:
                    pass
                os._exit(1)
                return


class Checker(Thread):
    def __init__(self):

        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(7)
            with open("Resources\\Temporary_Files\\Current_Network.txt", encoding="(utf-16") as f:
                f = f.read()
                if f != "":
                    pass
                else:
                    if os.path.isfile("Resources\\Temporary_Files\\tmp.txt"):
                        os.remove("Resources\\Temporary_Files\\tmp.txt")
                    else:
                        pass
                    os._exit(1)


class CheckIfNameSent(Thread):
    def __init__(self, server_socket):
        Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        hostname = socket.gethostname()
        mac_address = mac_func()
        message_to_send = "--PCNAME--||" + hostname + "||" + mac_address
        self.server_socket.sendall(message_to_send.encode("utf-8"))


def check_for_ip():
    if os.path.isfile("Resources\\Temporary_Files\\IP.txt"):
        with open("Resources\\Temporary_Files\\IP.txt", "r") as IP:
            server_ip = IP.readline()
            return False, server_ip
    else:
        print("SYSTEM: Creating IP log...")
        with open("Resources\\Temporary_Files\\IP.txt", "w+") as file_to_create:
            file_to_create.write("")
        server_ip = ""
        return True, server_ip


def connected_to_network_func():
    while True:
        try:
            with open("Resources\\Temporary_Files\\Current_Network.txt", encoding="utf-16") as f:
                f = f.read()
            f = f.split('\n')[0]
            return f
        except Exception as error:
            error_print("Couldn't read Current_Network.txt", error)
            pass


def ip_to_send_func(pc_to_connect):
    print(pc_to_connect)
    pc_to_connect = str(pc_to_connect).rsplit("raddr=('", 1)[1]
    pc_to_connect = str(pc_to_connect).rsplit("',", 1)[0]
    print(pc_to_connect)
    return pc_to_connect


def network_func():
    with open("Resources\\Temporary_Files\\Saved_Network.txt") as f:
        f = f.read()
        if f == "Insert SSID":
            return True
        else:
            return False


def mac_func():
    mac_address = hex(uuid.getnode())
    mac_address = str(mac_address)
    mac_address = mac_address[2:]
    mac_address = mac_address.upper()
    mac_address = ':'.join(a + b for a, b in zip(mac_address[::2], mac_address[1::2]))
    return mac_address


def backup_func():
    global soc
    BackupEngine.main()
    File_Sender.backup_send("Resources\\Backup2.txt")


def get_ip_from_sock(sock):
    sock = str(sock).rsplit("raddr=('", 1)[1]
    sock = str(sock).rsplit("',", 1)[0]
    return sock


def get_files(server_socket):
    server_ip = get_ip_from_sock(server_socket)
    Get.GETFILES(server_ip)
    BackupSyncEngine.main()
    with open("Resources\\FTS.txt", "r", encoding="utf-8-sig") as f:
        f = f.readlines()
    print('finished reading FTS')
    for index, file in enumerate(f):
        if file.__contains__("C:\\Users"):
            time.sleep(1)
            message = "--SENDING_BACKUP_FILES--" + str(socket.gethostname())
            message = message.encode("utf-8")
            soc.send(message)
            print('sent message')
            try:
                file = file.split("\n")[0]
            except Exception as error:
                error_print("Error while reading FTS", error)
                error_log(error)
                pass
            other_file = f[index + 1]
            try:
                other_file = other_file.split("\n")[0]
            except Exception as error:
                error_print("Error while reading FTS", error)
                error_log(error)
            print('SENDING BACKUP FILE: ' + str(file))
            print('SENDING NAME + ' + other_file)
            File_Sender.send_backup_files(file, other_file)


def error_log(error):
    with open("Resources\\ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))


def main():
    f = open("Resources\\Temporary_Files\\tmp.txt", "w+")
    f.close()
    new_ip, server_ip = check_for_ip()
    a = Starter(new_ip, server_ip)
    b = Receive()
    e = Checker()
    a.start()
    b.start()
    e.start()


if __name__ == '__main__':
    main()
