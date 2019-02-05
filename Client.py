import socket
import os
from threading import Thread
import time
import subprocess


global soc
global a
global break_all
global new_IP
global Ip

FNULL = open(os.devnull, 'w')

break_all = False
new_IP = False


class Starter(Thread):
    global soc
    global runnin
    global new_IP
    global break_all
    global Ip
    global connected

    def __init__(self):
        global soc
        global connected
        connected = False
        global break_all
        global Ip
        global new_IP
        host = ""
        Thread.__init__(self)
        print("First thread initialized. Starting connection with server")
        runnin = True
        self.running = True
        self.runnin = runnin

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8888

        j = True
        if new_IP == True:
            while j == True:
                Q = input('Input the IP ADDRESS presented on the server screen until one of them works\n')
                host = Q
                try:
                    soc.connect((host, port))
                    print("Success connecting to server")
                    message = socket.gethostname()
                    print(message)
                    if break_all == True:
                        return
                    else:
                        soc.sendall(message.encode("utf-8"))
                    with open("IP.txt",'w') as f:
                        f.write(host)
                    j = False
                except soc.gettimeout():
                    Q = input("Try the next IP ADDRESS:\n")
                    host = Q

        else:
            host = Ip
            print(host)
            while connected == False:
                try:
                    soc.connect((host, port))
                    print("Success connecting to server")
                    if Network() is True:
                        SSID = Connected_To_Network()
                        print("Adding -> " + SSID + " as server network")
                        with open('Saved_Network.txt', 'w') as f:
                            f.write(SSID)
                    else:
                        pass
                    message = socket.gethostname()
                    print(message)
                    if break_all == True:
                        return
                    else:
                        soc.sendall(message.encode("utf-8"))
                    connected = True
                except:
                    pass

    def run(self):
        global soc
        while self.running:
            if break_all == True:
                return
            print("Enter 'quit' to exit")
            message = ""
            while message != 'quit':
                if break_all == True:
                    return
                message = input(" -> ")
                if message == "/send":
                    message = "--SENDING_FILE--"
                    soc.sendall(message.encode("utf8"))
                    os.system('File_Sender.py')
                if break_all == True:
                    return
                if message != "/send":
                    soc.sendall(message.encode("utf8"))
                elif message == "/rm":
                    rm_message = '--RM--'
                    soc.sendall(rm_message.encode("utf8"))
                    rm()
            print('sending quit')
            message = "--quit--"
            soc.send(message.encode("utf-8"))
            time.sleep(1)
            return message


def rm():
    message = ""
    while message != "/back":
        message = input(" -> ")
        soc.sendall(message.encode("utf8"))

class Receive(Starter):
    global break_all
    global soc

    def __init__(self, Starter):
        global break_all
        global soc
        global runnin
        Thread.__init__(self)
        runnin = Starter.runnin

    def run(self):
        global break_all
        global soc
        while True:
            try:
                data = soc.recv(1024).decode()
                if not str(data).__contains__("--TEST--"):
                    if not str(data).__contains__('testtest'):
                        if data == "":
                            break_all = True
                            return
                        elif str(data) == "--SENDING_FILE--":
                            print('recieving file...')
                            os.system('Get.py')
                        else:
                            print('\n' + "Recieving message from server: " + data)
                            time.sleep(.1)

            except:
                print('server closed')
                break_all = True
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
        print('Starting Internet Check...')
        with open("ping.bat", "w+") as ping:
            ping.write("ping.exe " + Ip + " -n 2 > ping.txt")
        while True:
            while True:
                subprocess.run("ping.bat", stdout=FNULL)
                with open("ping.txt", "r") as file:
                    file = file.read()
                if file.__contains__("Destination host unreachable."):
                    print('Lost connection to server (ping)')
                    break_all = True
                    os.remove("tmp.txt")
                    os._exit(1)
                    return
                else:
                    pass

try:
    with open("IP.txt","r") as IP:
        Ip = IP.readline()
except:
    print("Server IP not found... Creating new log")
    open("IP.txt",'w')
    new_IP = True

def Connected_To_Network():
    subprocess.run("Current_Network.bat", stdout=FNULL)
    with open("Current_Network.txt") as f:
        f = f.read()
        f = f.split(': ')[1]
        f = f.split('\n')[0]
        return f

def Network():
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