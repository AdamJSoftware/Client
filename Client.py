import socket
from threading import Thread
import os
import selectors
import uuid
import time
import json
import sys
import tkinter as tk
from tkinter import filedialog

from Scripts import Get
from Scripts import File_Sender
from Scripts import BackupSyncEngine
from Scripts import BackupEngine

sel = selectors.DefaultSelector()


def config_read():
    with open('config.json', 'r') as f:
        return json.load(f)


def config_write(data):
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)


def change_ip():
    new_ip = input("Please enter new IP -> ")
    config = config_read()
    config['ip'] = new_ip
    print(config)
    config_write(config)


def error_log(error):
    with open("Resources/ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))


def get_files(server_socket):
    server_ip = get_ip_from_sock(server_socket)
    t = GetFiles(server_ip)
    t.start()


def get_ip():
    config = config_read()
    return(config['ip'])


def get_ip_from_sock(sock):
    sock = str(sock).rsplit("raddr=('", 1)[1]
    sock = str(sock).rsplit("',", 1)[0]
    return sock


def backup_selector():
    config = config_read()
    print(config['backup'])


def backup_exclude():
    config = config_read()
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    config['backup_exclude'].append(file_path)
    config_write(config)


def GeneralStarter():
    host = get_ip()
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
            os._exit(1)
            print(e)


def backup_add():
    config = config_read()
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    config['backup'].append(file_path)
    config_write(config)


class Receive(Thread):

    def __init__(self, soc, port):
        Thread.__init__(self)
        self.soc = soc
        self.port = port
        print('RECEIVER: Initialized')
        print(f'RECEIVER: Running on port: {self.port}')

    def run(self):
        print('RECEIVER: Connected')
        while True:
            try:
                data = self.soc.recv(1024).decode()
                if str(data) == "--SENDING_FILE--":
                    get_thread = GetThread(
                        self.port, get_ip_from_sock(self.soc))
                    print('Running get thread')
                    get_thread.start()
                elif str(data) == "--GETFILES--":
                    print('REQUESTED GET FILES')
                    a = GetFiles(get_ip_from_sock(
                        self.soc), self.soc, int(self.port))
                    a.start()
                else:
                    print(data)
            except Exception as e:
                print(e)
                time.sleep(1)
                print('RECEIVER: Lost connection to server')
                os._exit(1)


class GetFiles(Thread):
    def __init__(self, server_ip, server_socket, server_port):
        Thread.__init__(self)
        self.ip = server_ip
        self.soc = server_socket
        self.port = server_port

    def run(self):
        Get.GETFILES(self.ip, int(self.port))
        print('FINISHED SENDING')
        BackupSyncEngine.main()
        with open("Resources/FTS.txt", "r", encoding="utf-8-sig") as f:
            f = f.readlines()
        print('finished reading FTS')
        for index, file in enumerate(f):
            if file.__contains__("C:/"):
                time.sleep(1)
                message = "--SENDING_BACKUP_FILES--" + \
                    str(socket.gethostname())
                message = message.encode("utf-8")
                self.soc.send(message)
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
                print('SENDING NAME + ' + str(other_file))
                File_Sender.send_backup_files(
                    self.soc, int(self.port)+2, file, other_file)


class Checker(Thread):

    def __init__(self, dedicated_port):
        Thread.__init__(self)
        print('CHECKER: Initialized')
        print(f'CHECKER: Running on port: {dedicated_port}')
        host = get_ip()
        port = dedicated_port

        self.soc = socket.socket()

        self.soc.connect((host, port))
        print('CHECKER: Sucessfully connected to server')
        checker2 = Checker2(self.soc)
        checker2.start()

    def run(self):
        while True:
            try:
                time.sleep(1)
                self.soc.sendall("--TEST--".encode("utf-8"))
            except Exception as e:
                print(e)
                print('SENDING CHECKER: Lost connection to server')
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
                self.soc.recv(1024).decode()
                # print(data)
                # self.soc.sendall("--TEST--".encode("utf-8"))
                # print('done')
            except Exception as e:
                print(e)
                print('RECEIVING CHECKER: Lost connection to server')
                time.sleep(1)
                os._exit(1)


def mac_func():
    mac_address = hex(uuid.getnode())
    mac_address = str(mac_address)
    mac_address = mac_address[2:]
    mac_address = mac_address.upper()
    mac_address = ':'.join(
        a + b for a, b in zip(mac_address[::2], mac_address[1::2]))
    return mac_address


def get_pc_name():
    config = config_read()
    return config['computer_name']


def main():
    main_thread = Main()
    main_thread.start()

    while True:
        try:
            user_input = input(" -> ")
            if user_input == "/restart":
                os._exit(1)
                # time.sleep(2)
            elif user_input == "/change ip":
                change_ip()
            elif user_input == '/backup_selector':
                backup_selector()
            elif user_input == '/backup_add':
                backup_add()
            elif user_input == "/send":
                print(int(main_thread.port))
                File_Sender.main(int(main_thread.port), main_thread.soc)
            elif user_input == "/backup":
                config = config_read()
                BackupEngine.main(config['backup'], config['backup_exclude'])
                print('here')
                File_Sender.backup_send(main_thread.soc, int(
                    main_thread.port), os.path.join('Resources', 'backup_audit.json'))
                print('FINISEHD SENDING BACKUP FILE')
            elif user_input == "/current ip":
                print(get_ip())
            elif user_input == "":
                pass
            elif user_input.__contains__('/'):
                print('Unrecognized command. Please type "/help" for help')
            elif main_thread.connected:
                main_thread.soc.sendall(str(user_input).encode("utf-8"))
        except Exception as e:
            print(e)


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
        try:
            self.connected = False
            self.port = GeneralStarter()
            print("SYSTEM: Dedicated port: {}".format(self.port))
            host = get_ip()
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((host, int(self.port)))
            print('SYSTEM: Successfuly connected to dedicated server')
            self.connected = True

            # dedicated_starter = dedicated_starter(soc)
            # dedicated_starter.start()

            receiver = Receive(self.soc, int(self.port) - 2)
            receiver.start()
            checker_port = int(self.port) - 1
            checker = Checker(checker_port)
            checker.start()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


if __name__ == "__main__":
    main()
