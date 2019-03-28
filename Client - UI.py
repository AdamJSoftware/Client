import os
import sys
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
global new_IP
global Ip

FNULL = open(os.devnull, 'w')

new_IP = False


class Network(Thread):
    def __init__(self):
        Thread.__init__()

    def run(self):
        subprocess.run("Resources\Current_Network.bat")


class Starter(Thread):
    global soc
    global new_IP
    global Ip
    global connected

    def __init__(self):
        global soc
        global connected
        connected = False
        global Ip
        global new_IP
        host = ""
        Thread.__init__(self)
        print("First thread initialized. Starting connection with server")
        self.running = True

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8888
        j = True
        if new_IP == True:
            first_try = False
            while j == True:
                if first_try is False:
                    Q = input('Input the IP ADDRESS presented on the server screen until one of them works\n')
                    host = Q
                    Ip = Q
                else:
                    pass
                try:
                    soc.connect((host, port))
                    os.system('cls')
                    print("Successfully connected to server")
                    message = socket.gethostname()
                    print("Client hostname -> " + message)
                    macaddress = mac()
                    newmessage = "--PCNAME--||" + message + "||" + macaddress
                    soc.sendall(newmessage.encode("utf-8"))
                    with open("Resources\Temporary_Files\IP.txt", 'w') as f:
                        f.write(host)
                    j = False
                except:
                    os.system('cls')
                    Q = input("Try the next IP ADDRESS:\n")
                    host = Q
                    first_try = True

        else:
            host = Ip
            print("Connecting to -> " + host)
            while connected is False:
                try:
                    soc.connect((host, port))
                    print("Successfully connected to server")
                    if network_func() is True:
                        SSID = connected_to_network_func()
                        print("Adding -> " + SSID + " as server network")
                        with open('Resources\Temporary_Files\Saved_Network.txt', 'w') as f:
                            f.write(SSID)
                    else:
                        pass
                    message = socket.gethostname()
                    macaddress = mac()
                    print("Client hostname -> " + message)
                    newmessage = "--PCNAME--||" + message + "||" + macaddress
                    soc.sendall(newmessage.encode("utf-8"))
                    connected = True
                except:
                    print('an error occured while connecting')

    def run(self):
        global soc
        while self.running:
            while True:
                message = input(" -> ")
                if message == "/send":
                    message = "--SENDING_FILE--"
                    soc.sendall(message.encode("utf8"))
                    File_Sender.main()
                elif message == "/rm":
                    rm_message = '--RM--'
                    soc.sendall(rm_message.encode("utf8"))
                    rm_func()
                elif message.__contains__('/send to '):
                    message = message.split("/send to ")[1]
                    print(message)
                    message = "--SEND_TO--" + message
                    soc.sendall(message.encode("utf-8"))
                elif message.__contains__('/wake '):
                    message = message.split('/wake ')[1]
                    message = "--WAKE--" + message
                    soc.sendall(message.encode("utf-8"))
                else:
                    soc.sendall(message.encode("utf8"))


class Receive(Starter):
    global soc

    def __init__(self, Starter):
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
                        Q = soc
                        ip_to_send_func(Q)
                        print('recieving file...')
                        Get.main()
                    elif str(data).__contains__("--RM_MESSAGE--"):
                        data = data.split("--RM_MESSAGE--")[1]
                        print("RM: " + data)
                    elif str(data).__contains__("--SENDING_FILE_TO--"):
                        data = data.split("--SENDING_FILE_TO--")[1]
                        ip_to_send_func(data)
                        Get.main()
                    elif str(data).__contains__("--CLIENT_ID--"):
                        print('got adress')
                        data = data.split("--CLIENT_ID--")[1]
                        ip_to_send_func(data)
                        print('starting server')
                        File_Sender.main()
                    elif str(data).__contains__("||BACKUP||"):
                        print("running backup")
                        backup_func()
                    elif str(data).__contains__("--GETFILES--"):
                        print("Getting required files")
                        GETFILES(soc)
                        time.sleep(5)
                    else:
                        print('\n' + "Recieving message from server: " + data)
                        time.sleep(.1)
            except:
                print('server closed')
                try:
                    os.remove("Resources\Temporary_Files\\tmp.txt")
                except:
                    pass
                os._exit(1)
                return


class Checker(Thread):
    global soc
    global Ip

    def __init__(self):
        global soc
        global Ip
        Thread.__init__(self)

    def run(self):
        global soc
        global Ip
        with open("Resources\ping.bat", "w+") as ping:
            ping.write("ping.exe " + Ip + " -n 1 > Resources\Temporary_Files\ping.txt")
        while True:
            while True:
                subprocess.run("Resources\ping.bat", stdout=FNULL)
                with open("Resources\Temporary_Files\\ping.txt", "r") as file:
                    file = file.read()
                if file.__contains__("Destination host unreachable.") or file.__contains__("General failure."):
                    print('Lost connection to server (ping)')
                    try:
                        os.remove("Resources\Temporary_Files\\tmp.txt")
                    except:
                        pass
                    os._exit(1)
                    return
                else:
                    pass


class Checker2(Thread):
    def __init__(self):

        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(7)
            with open("Resources\Temporary_Files\Current_Network.txt", encoding="(utf-16") as f:
                f = f.read()
                if f != "":
                    pass
                else:
                    try:
                        os.remove("Resources\Temporary_Files\\tmp.txt")
                    except:
                        pass
                    os._exit(1)


try:
    with open("Resources\Temporary_Files\IP.txt", "r") as IP:
        Ip = IP.readline()
except:
    print("Server IP not found... Creating new log")
    open("Resources\Temporary_Files\IP.txt", 'w')
    new_IP = True


def rm_func():
    print('starting remote')
    message = ""
    while message != "/back":
        message = input(" -> ")
        if message == "/send":
            print('Please select what computer you would like to send a file:')
        elif message.__contains__("/send "):
            soc.send(message.encode("utf-8"))
        soc.sendall(message.encode("utf8"))


def connected_to_network_func():
    while True:
        try:
            with open("Resources\Temporary_Files\Current_Network.txt", encoding="utf-16") as f:
                f = f.read()
            f = f.split('\n')[0]
            return f
        except:
            pass


def ip_to_send_func(Q):
    print(Q)
    Q = str(Q).rsplit("raddr=('", 1)[1]
    Q = str(Q).rsplit("',", 1)[0]
    print(Q)
    with open("Resources\Temporary_Files\IP_TO_SEND.txt", 'w') as f:
        f.write(Q)


def network_func():
    with open("Resources\Temporary_Files\Saved_Network.txt") as f:
        f = f.read()
        if f == "Insert SSID":
            return True
        else:
            return False


def mac():
    mac = hex(uuid.getnode())
    mac = str(mac)
    mac = mac[2:]
    mac = mac.upper()
    mac = ':'.join(a + b for a, b in zip(mac[::2], mac[1::2]))
    return(mac)


def backup_func():
    global soc
    BackupEngine.main()
    File_Sender.backup_send("Resources\\Backup2.txt")

def GETFILES(soc):
    Get.GETFILES()
    BackupSyncEngine.main()
    with open("Resources\\FTS.txt", "r", encoding="utf-8-sig") as f:
        f = f.readlines()
    print('finished reading FTS')
    for index, file in enumerate(f):
        if file.__contains__("C:\\Users"):
            time.sleep(1)
            print('SENDING BACKUP FILE: ' + str(file))
            message = "--SENDING_BACKUP_FILES--" + str(socket.gethostname())
            message = message.encode("utf-8")
            soc.send(message)
            print('sent message')
            File_Sender.send_backup_files(file, f[index + 1])



def main():
    f = open("Resources\Temporary_Files\\tmp.txt", "w+")
    f.close()
    c = Checker()
    a = Starter()
    b = Receive(a)
    e = Checker2()
    # c.start()
    a.start()
    b.start()
    e.start()


if __name__ == '__main__':
    main()
