import socket
from threading import Thread
import os
import selectors
import uuid
import time

from Scripts import Get

sel = selectors.DefaultSelector()

def get_ip_from_sock(sock):
    sock = str(sock).rsplit("raddr=('", 1)[1]
    sock = str(sock).rsplit("',", 1)[0]
    return sock

def GeneralStarter():
    host = "172.24.10.134"
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8888
    print("\nSYSTEM: General starter initialized")
    connected = False
    while not connected:
        try:
            soc.connect((host, port))
            connected = True
        except:
            pass
    print('SYSTEM: Succesfully connected to general server')
    time.sleep(2)
    send_info(soc)
    print('SYSTEM: Sent system information to server')
    port = ""
    while port == "":
        try:
            data = soc.recv(1024).decode()
            if str(data).__contains__('--PORT--'):
                port = data.split("--PORT--")[1]
                print(port)
                soc.close()
                return port
        except Exception as e:
            print(e)

class Receive(Thread):

    def __init__(self, soc, port):
        Thread.__init__(self)
        self.soc = soc
        self.port = port
        print('SYSTEM: Receiver initialized')       

    def run(self):
        print('SYSTEM: Receiver started')
        while True:
            try:
                data = self.soc.recv(1024).decode()
                if str(data) == "--SENDING_FILE--":
                    get_thread = GetThread(self.port, get_ip_from_sock(self.soc))
                    print('Running get thread')
                    get_thread.start()
                else:
                    print(data)
            except Exception as e:
                print(e)
                time.sleep(1)
                print('Lost connection to server')
                os._exit(1)

class Checker(Thread):

    def __init__(self, dedicated_port):
        Thread.__init__(self)
        print('SYSTEM: Checker initialized')
        host = '172.24.10.134'
        port = dedicated_port

        self.soc = socket.socket()

        self.soc.connect((host, port))
        print('SYSTEM: Sucessfuly connected to checker server')
        checker2 = Checker2(self.soc)
        checker2.start()

    def run(self):
        print('SYSTEM: Checker started')
        while True:
            try:
                time.sleep(1)
                self.soc.sendall("--TEST--".encode("utf-8"))
            except Exception as e:
                print(e)
                print('Lost connection to server1')
                time.sleep(1)
                os._exit(1)


class GetThread(Thread):
    def __init__(self, port, ip):
        Thread.__init__(self)
        self.port = port
        self.ip = ip
    
    def run(self):
        Get.main(self.port, self.ip)


class Checker2(Thread):

    def __init__(self, soc):
        Thread.__init__(self)
        self.soc = soc
        self.soc.settimeout(5.0)

    def run(self):
        while True:
            try:
                time.sleep(1)
                data = self.soc.recv(1024).decode()
                # print(data)
                # self.soc.sendall("--TEST--".encode("utf-8"))
                # print('done')
            except Exception as e:
                print(e)
                print('Lost connection to server2')
                time.sleep(1)
                os._exit(1)

def mac_func():
    mac_address = hex(uuid.getnode())
    mac_address = str(mac_address)
    mac_address = mac_address[2:]
    mac_address = mac_address.upper()
    mac_address = ':'.join(a + b for a, b in zip(mac_address[::2], mac_address[1::2]))
    return mac_address


def get_pc_name():
    with open("Resources\\Computer_name.txt") as f:
        return f.read()


def main():
    main_thread = Main()
    main_thread.start()

    while True:
        try:
            user_input = input(" -> ")
            if user_input == "/restart":
                os._exit(1)
            else:
                main_thread.soc.sendall(str(user_input).encode("utf-8"))
        except:
            pass


def send_info(server_socket):
    hostname = socket.gethostname()
    mac_address = mac_func()
    pc_name = get_pc_name()
    message_to_send = "--PCNAME--||" + hostname + "||" + mac_address + "||" + pc_name
    server_socket.sendall(message_to_send.encode("utf-8"))


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)
        print('SYSTEM: Main thread initialized')
    
    def run(self):
        port = GeneralStarter()
        print("SYSTEM: Dedicated port: {}".format(port))
        host = "172.24.10.134"
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((host, int(port)))
        print('SYSTEM: Successfuly connected to dedicated server')

        # dedicated_starter = dedicated_starter(soc)
        # dedicated_starter.start()

        receiver = Receive(self.soc, port)
        receiver.start()
        checker_port = int(port) + 1
        checker = Checker(checker_port)
        checker.start()



if __name__ == "__main__":
    main()
 