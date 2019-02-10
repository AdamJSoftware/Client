import os
import socket
import subprocess
import time
from threading import Thread

global soc
global new_IP
global Ip

FNULL = open(os.devnull, 'w')

new_IP = False


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
                    Q = input(
                        'Input the IP ADDRESS presented on the server screen until one of them works\n')
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
                    newmessage = "--PCNAME--||" + message
                    soc.sendall(newmessage.encode("utf-8"))
                    with open("IP.txt", 'w') as f:
                        f.write(host)
                    j = False
                except BaseException:
                    os.system('cls')
                    Q = input("Try the next IP ADDRESS:\n")
                    host = Q
                    first_try = True

        else:
            host = Ip
            print("Connecting to -> " + host)
            while connected == False:
                try:
                    soc.connect((host, port))
                    print("Successfully connected to server")
                    if network_func() is True:
                        SSID = connected_to_network_func()
                        print("Adding -> " + SSID + " as server network")
                        with open('Saved_Network.txt', 'w') as f:
                            f.write(SSID)
                    else:
                        pass
                    message = socket.gethostname()
                    print("Client hostname -> " + message)
                    newmessage = "--PCNAME--||" + message
                    soc.sendall(newmessage.encode("utf-8"))
                    connected = True
                except BaseException:
                    pass

    def run(self):
        global soc
        while self.running:
            message = ""
            while message != 'quit':
                message = input(" -> ")
                if message == "/send":
                    message = "--SENDING_FILE--"
                    soc.sendall(message.encode("utf8"))
                    os.system('File_Sender.py')
                elif message == "/rm":
                    rm_message = '--RM--'
                    soc.sendall(rm_message.encode("utf8"))
                    rm_func()
                else:
                    soc.sendall(message.encode("utf8"))
            print('sending quit')
            message = "--quit--"
            soc.send(message.encode("utf-8"))
            time.sleep(1)
            return message


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
                        print('recieving file...')
                        os.system('Get.py')
                    else:
                        print('\n' + "Recieving message from server: " + data)
                        time.sleep(.1)

            except BaseException:
                print('server closed')
                os.remove("tmp.txt")
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
        with open("ping.bat", "w+") as ping:
            ping.write("ping.exe " + Ip + " -n 1 > ping.txt")
        while True:
            while True:
                subprocess.run("ping.bat", stdout=FNULL)
                with open("ping.txt", "r") as file:
                    file = file.read()
                if file.__contains__("Destination host unreachable.") or file.__contains__(
                        "General failure."):
                    print('Lost connection to server (ping)')
                    os.remove("tmp.txt")
                    os._exit(1)
                    return
                else:
                    pass


try:
    with open("IP.txt", "r") as IP:
        Ip = IP.readline()
except BaseException:
    print("Server IP not found... Creating new log")
    open("IP.txt", 'w')
    new_IP = True


def rm_func():
    print('starting remote')
    message = ""
    while message != "/back":
        message = input(" -> ")
        soc.sendall(message.encode("utf8"))


def connected_to_network_func():
    subprocess.run("Current_Network.bat", stdout=FNULL)
    with open("Current_Network.txt", encoding="utf-16") as f:
        f = f.read()
        f = f.split('\n')[0]
        return f


def network_func():
    with open("Saved_Network.txt") as f:
        f = f.read()
        if f == "Insert SSID":
            return True
        else:
            return False


def main():
    f = open("tmp.txt", "w+")
    f.close()
    c = Checker()
    a = Starter()
    b = Receive(a)
    c.start()
    a.start()
    b.start()


if __name__ == '__main__':
    main()
